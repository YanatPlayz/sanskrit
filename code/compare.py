"""
compare.py — grid comparison across preprocessing variants and architectures.

Reproduces the model-comparison table in the paper. For each cell of the grid it reports:

  orthog%     share of a word's top-10 nearest neighbors that are merely orthographic
              look-alikes (shared >=4-character affix, or edit distance <=2) rather than
              semantic associates, averaged over the case words x periods. This is the
              diagnostic that separates FastText from word2vec: short character n-grams
              retrieve inflected echoes of the stem instead of synonyms. Lower is better.
  so~proc     Spearman correlation between the second-order and Procrustes change scores,
              used as a reliability estimate — two measures with different failure modes
              agreeing is evidence the ranking reflects signal rather than noise.
  freq~drift  Spearman correlation between log total frequency and the change score,
              a check on whether apparent change is a frequency artifact.
  sharedV     vocabulary trackable across all four periods.

Requires train.py to have produced models/<name>/ and drift.py to have produced
analysis/<name>/drift_scores.csv for every model listed in MODELS.

Usage:
    python compare.py
"""
import csv
from pathlib import Path
import numpy as np
from scipy.stats import spearmanr
from drift import load_wv, PERIODS, CASE_WORDS

REPO = Path(__file__).resolve().parent.parent
STOPLIST = Path(__file__).resolve().parent / "sanskrit_stoplist_slp1.txt"
MODELS = {  # label -> directory name, shared by models/<name> and analysis/<name>
    "ft-raw-3-6":    "ft-raw-3-6",
    "w2v-raw":       "w2v-raw",
    "ft-sandhi-3-6": "ft-sandhi-3-6",
    "ft-sandhi-6-12": "ft-sandhi-6-12",
    "w2v-sandhi":    "w2v-sandhi",
    "w2v-lemma":     "w2v-lemma",
}
STOP = set(STOPLIST.read_text(encoding="utf-8").replace("#", " # ").split())


def lev(a, b):
    if abs(len(a) - len(b)) > 2:
        return 3
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[-1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def orthographic(w, n):
    if w == n:
        return True
    k = 4
    if w[:k] == n[:k] and len(w) >= k and len(n) >= k:
        return True
    if w[-k:] == n[-k:] and len(w) >= k and len(n) >= k:
        return True
    return lev(w, n) <= 2


def pollution(models_dir):
    """Mean fraction of top-10 full-vocab neighbors that are orthographic, over case words x eras."""
    fracs = []
    for era in PERIODS:
        try:
            wv = load_wv(models_dir, era)
        except Exception:
            continue
        for w in CASE_WORDS:
            if w not in wv.key_to_index:
                continue
            nbrs = [t for t, _ in wv.most_similar(w, topn=10)]
            fracs.append(np.mean([orthographic(w, n) for n in nbrs]))
    return float(np.mean(fracs)) if fracs else float("nan")


def diagnostics(analysis_dir):
    rows = list(csv.DictReader(open(REPO / "analysis" / analysis_dir / "drift_scores.csv")))
    rob = [r for r in rows
           if min(int(r[f"freq_{e}"]) for e in PERIODS) >= 10 and r["word"] not in STOP
           and r["so_ved_sut"] not in ("", "nan") and r["proc_ved_sut"] not in ("", "nan")]
    so = np.array([float(r["so_ved_sut"]) for r in rob])
    proc = np.array([float(r["proc_ved_sut"]) for r in rob])
    tot = np.array([sum(int(r[f"freq_{e}"]) for e in PERIODS) for r in rob])
    return len(rows), spearmanr(so, proc).correlation, spearmanr(np.log(tot), so).correlation


print(f"{'model':<15}{'orthog%':>9}{'so~proc':>9}{'freq~drift':>12}{'sharedV':>9}")
print("-" * 54)
for label, d in MODELS.items():
    pol = pollution(str(REPO / "models" / d))
    nrows, soproc, freq = diagnostics(d)
    print(f"{label:<15}{pol*100:>8.0f}%{soproc:>9.2f}{freq:>12.2f}{nrows:>9}")

print("\n--- rAjan/rAjA + Darma neighbors by model (top-8, full vocab) ---")
for label, d in MODELS.items():
    print(f"\n[{label}]")
    for w in ["rAjA", "rAjan", "Darma"]:
        for era in ["vedic", "epics", "sutras"]:
            wv = load_wv(str(REPO / "models" / d), era)
            if w in wv.key_to_index:
                ns = ", ".join(t for t, _ in wv.most_similar(w, topn=8))
                print(f"   {w:<6}[{era:6}] {ns}")
                break
