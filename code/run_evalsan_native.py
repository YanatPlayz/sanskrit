"""
run_evalsan_native.py — run EvalSan's OWN evaluation functions, unmodified.

Unlike run_evalsan.py (which restricts to in-vocab items), this calls the EvalSan code
exactly as published: their evaluate_categorization / evaluate_relatedness_classification
substitute the MEAN VECTOR for OOV words and score the FULL test set; their MCQ and analogy
score only fully-in-vocab rows. The only changes are two compatibility shims required because
the 2023 code predates numpy 2 / sklearn 1.9 (np.vstack no longer accepts a bare generator;
AgglomerativeClustering's `affinity` kwarg was renamed `metric`). Neither shim changes any
metric — they just let the original code execute.

Usage:
  python run_evalsan_native.py --model ../models/w2v-sandhi/epics/word2vec_epics.model --tag sandhi-epics
"""
import argparse
import os
import sys
import numpy as np
import pandas as pd
from gensim.models import Word2Vec

INTRINSIC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "EvalSan/evaluations/Intrinsic")


def install_shims():
    # shim 1: numpy>=2 rejects np.vstack(<generator>); materialize generators to lists.
    _orig_vstack = np.vstack
    def _vstack(tup, *a, **k):
        if hasattr(tup, "__iter__") and not hasattr(tup, "__len__"):
            tup = list(tup)
        return _orig_vstack(tup, *a, **k)
    np.vstack = _vstack
    # shim 2: sklearn>=1.4 renamed AgglomerativeClustering(affinity=) -> metric=.
    import web.evaluate as wev
    from sklearn.cluster import AgglomerativeClustering as _AC
    def _AC_compat(*a, **k):
        if "affinity" in k:
            k["metric"] = k.pop("affinity")
        return _AC(*a, **k)
    wev.AgglomerativeClustering = _AC_compat


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--tag", default="ours")
    args = ap.parse_args()
    model_path = os.path.abspath(args.model)

    os.chdir(INTRINSIC)
    sys.path.insert(0, INTRINSIC)
    sys.path.insert(0, os.path.join(INTRINSIC, "word_embeddings_benchmarks"))

    from web.vocabulary import Vocabulary
    from web.embedding import Embedding
    from web.evaluate import evaluate_categorization, evaluate_relatedness_classification
    install_shims()
    from Similarities import evaluate_similarity_MCQs
    from Analogies import analogy_evaluator

    # Build the Embedding exactly as their .vec-file branch does: whole-word -> vector.
    wv = Word2Vec.load(model_path).wv
    words = list(wv.key_to_index)
    emb = Embedding(Vocabulary(words=words), [wv[w] for w in words])
    print(f"\n############## EvalSan NATIVE — {args.tag} (vocab={len(words):,}) ##############")

    # ---- Relatedness (their thresholds 0.25/0.50; mean-vector OOV substitution) ----
    rows = [l.strip().split(",") for l in open("Data/automated_relatedness_AK_test.csv")]
    X = np.asarray([[r[0], r[1]] for r in rows]); Y = np.asarray([int(r[2]) for r in rows])
    acc, f = evaluate_relatedness_classification(emb, args.tag, X, Y, 0.25, 0.5)
    print(f"Relatedness:: accuracy {acc:.2f}  f-score {f:.4f}   (full {len(Y)} pairs, OOV->mean)")

    # ---- Synonym MCQ (their code; scores only fully-in-vocab rows) ----
    try:
        evaluate_similarity_MCQs(emb, args.tag)
    except ZeroDivisionError:
        print("Similarity (Accuracy): n/a  (0 fully-in-vocab MCQ rows)")

    # ---- Categorization (method='all'; mean-vector OOV substitution) ----
    X, Y = [], []
    DF = pd.read_csv("Data/final_syntactic_categorization.csv", header=None, sep=",")
    for i in range(len(DF)):
        for w in DF.iloc[i, :]:
            X.append(w); Y.append(i)
    print(f"Categorization (Syntactic): {evaluate_categorization(emb, np.asarray(X), np.asarray(Y)):.4f}"
          f"   (full {len(X)} words, OOV->mean)")

    X, Y = [], []
    for line in open("Data/final_semantic_categorization.csv"):
        p = line.strip().split(",");
        for w in p[1:]:
            X.append(w); Y.append(p[0])
    print(f"Categorization (Semantic):  {evaluate_categorization(emb, np.asarray(X), np.asarray(Y)):.4f}"
          f"   (full {len(X)} words, OOV->mean)")

    # ---- Analogy (their full-vocab 3CosAdd; scores only in-vocab quads) ----
    analogy_evaluator("Data/Final_semantic_analogies.csv", emb, args.tag, "sem.csv", savefile=True)
    analogy_evaluator("Data/final_syntactic_analogies.csv", emb, args.tag, "syn.csv", savefile=True)


if __name__ == "__main__":
    main()
