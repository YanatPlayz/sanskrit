"""
run_evalsan.py — run the EvalSan (Sandhan et al. 2023) intrinsic tasks on one of OUR
per-era Word2Vec models, faithfully but HONESTLY: every task is restricted to its
in-vocabulary items (no mean-vector substitution for OOV, which would inflate scores),
and coverage is reported next to every score so a low number is never mistaken for a
real result.

Tasks (SLP1 data shipped with EvalSan):
  - Synonym MCQ        accuracy  (pick the candidate closest to the target; gold = col 'a')
  - Categorization     purity    (KMeans into #classes; Sandhan's calculate_purity)
  - Relatedness        acc + macroF (cosine thresholded at 0.25/0.50 -> {0,1,2})
  - Analogy            accuracy  (3CosAdd: b - a + c ~ d)

Usage:
  python run_evalsan.py --model ../models/w2v-sandhi/epics/word2vec_epics.model --label sandhi-epics
"""
import argparse
import csv
from pathlib import Path

import numpy as np
import pandas as pd
from gensim.models import Word2Vec
from sklearn.cluster import KMeans

DATA = Path(__file__).resolve().parent / "EvalSan/evaluations/Intrinsic/Data"


def calculate_purity(y_true, y_pred):
    """Sandhan et al.'s purity (web/evaluate.py)."""
    y_true, y_pred = np.asarray(y_true), np.asarray(y_pred)
    tc = np.zeros((len(set(y_true)), len(y_true)))
    pc = np.zeros((len(set(y_pred)), len(y_true)))
    for i, cl in enumerate(set(y_true)):
        tc[i] = (y_true == cl).astype(int)
    for i, cl in enumerate(set(y_pred)):
        pc[i] = (y_pred == cl).astype(int)
    return float(np.sum(np.max(pc.dot(tc.T), axis=1)) / len(y_true))


def cos(a, b):
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))


def task_mcq(wv):
    df = pd.read_csv(DATA / "final_synonym_MCQs_AK.csv")
    n_tot = len(df)
    correct = scored = 0
    for i in range(n_tot):
        q, a, b, c, d = (str(df.iloc[i, j]) for j in range(5))
        if not all(w in wv.key_to_index for w in (q, a, b, c, d)):
            continue
        scored += 1
        sims = {w: cos(wv[w], wv[q]) for w in (a, b, c, d)}
        if max(sims, key=sims.get) == a:
            correct += 1
    acc = 100 * correct / scored if scored else float("nan")
    return dict(name="Synonym MCQ (acc%)", score=acc, cov=f"{scored}/{n_tot}",
                covpct=100 * scored / n_tot)


def _categorization(wv, rows, label):
    # rows: list of [class, member, member, ...]
    X, y = [], []
    for r in rows:
        cls = r[0]
        for w in r[1:]:
            if w and w in wv.key_to_index:
                X.append(w); y.append(cls)
    n_total = sum(max(len(r) - 1, 0) for r in rows)
    if len(set(y)) < 2 or len(X) < len(set(y)):
        return dict(name=label, score=float("nan"), cov=f"{len(X)}/{n_total}",
                    covpct=100 * len(X) / max(n_total, 1))
    M = np.vstack([wv[w] for w in X])
    k = len(set(y))
    best = 0.0
    for seed in (0, 1, 2):
        pred = KMeans(n_clusters=k, n_init=10, random_state=seed).fit_predict(M)
        best = max(best, calculate_purity(y, pred))
    return dict(name=label, score=best, cov=f"{len(X)}/{n_total}",
                covpct=100 * len(X) / max(n_total, 1))


def task_categorization(wv):
    sem = [ln.strip().split(",") for ln in open(DATA / "final_semantic_categorization.csv")]
    syn = [ln.strip().split(",") for ln in open(DATA / "final_syntactic_categorization.csv")]
    # syntactic file has no leading class label; the row index IS the class
    syn = [[str(i)] + r for i, r in enumerate(syn)]
    return [_categorization(wv, sem, "Categorization-semantic (purity)"),
            _categorization(wv, syn, "Categorization-syntactic (purity)")]


def task_relatedness(wv, lo=0.25, hi=0.50):
    rows = [ln.strip().split(",") for ln in open(DATA / "automated_relatedness_AK_test.csv")]
    yt, yp = [], []
    n_tot = len(rows)
    for w1, w2, g in rows:
        if w1 in wv.key_to_index and w2 in wv.key_to_index:
            s = cos(wv[w1], wv[w2])
            yp.append(2 if s >= hi else 1 if s >= lo else 0)
            yt.append(int(g))
    if not yt:
        return dict(name="Relatedness (acc%)", score=float("nan"), cov=f"0/{n_tot}", covpct=0.0)
    yt, yp = np.array(yt), np.array(yp)
    acc = 100 * np.mean(yt == yp)
    return dict(name="Relatedness (acc%)", score=acc, cov=f"{len(yt)}/{n_tot}",
                covpct=100 * len(yt) / n_tot)


def task_analogy(wv, path, label):
    df = pd.read_csv(path)
    n_tot = len(df)
    correct = scored = 0
    vocab = wv.key_to_index
    for _, row in df.iterrows():
        a, b, c, d = (str(row[k]) for k in ("a", "b", "c", "d"))
        if not all(w in vocab for w in (a, b, c, d)):
            continue
        scored += 1
        # faithful 3CosAdd over the FULL vocabulary: b - a + c ~ d; most_similar
        # auto-excludes the three input words. Correct iff top-1 == d.
        top = wv.most_similar(positive=[b, c], negative=[a], topn=1)
        if top and top[0][0] == d:
            correct += 1
    acc = 100 * correct / scored if scored else float("nan")
    return dict(name=label, score=acc, cov=f"{scored}/{n_tot}", covpct=100 * scored / n_tot)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--label", default="model")
    args = ap.parse_args()
    wv = Word2Vec.load(args.model).wv

    results = [task_mcq(wv)]
    results += task_categorization(wv)
    results.append(task_relatedness(wv))
    results.append(task_analogy(wv, DATA / "Final_semantic_analogies.csv", "Analogy-semantic (acc%)"))
    results.append(task_analogy(wv, DATA / "final_syntactic_analogies.csv", "Analogy-syntactic (acc%)"))

    print(f"\n=== EvalSan intrinsic — {args.label}  (vocab={len(wv.key_to_index):,}) ===")
    print(f"{'task':<36}{'score':>9}{'coverage':>14}{'cov%':>8}")
    print("-" * 67)
    for r in results:
        sc = f"{r['score']:.2f}" if r["score"] == r["score"] else "n/a"
        print(f"{r['name']:<36}{sc:>9}{r['cov']:>14}{r['covpct']:>7.1f}%")
    print("\nNote: every task restricted to IN-VOCAB items; coverage shown. Low coverage "
          "=> score not meaningful (reported for transparency, not as a result).")


if __name__ == "__main__":
    main()
