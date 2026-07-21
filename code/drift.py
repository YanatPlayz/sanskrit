"""
drift.py — Diachronic semantic-drift analysis for per-era FastText models.

Computes three complementary drift metrics for every word shared across all eras:
  1. Nearest-neighbor Jaccard distance      (alignment-free, interpretable)
  2. Local-neighborhood / second-order sim   (alignment-free, robust; Hamilton et al. 2016)  -> HEADLINE
  3. Orthogonal Procrustes + cosine          (alignment-based; confirmatory)

Point --models_dir at any directory laid out as
    <models_dir>/<era>/<arch>_<era>.model
(the layout train.py writes), so the same analysis runs unchanged over every cell of
the grid. FastText and Word2Vec models are detected automatically.

Writes drift_scores.csv (every metric for every trackable word), top_movers.csv,
most_stable.csv, and case_studies.txt (per-era neighbor lists for the case words).

Usage:
    python drift.py --models_dir ../models/w2v-sandhi --out_dir ../analysis/w2v-sandhi \
                    --stoplist sanskrit_stoplist_slp1.txt
"""

import argparse
import csv
from pathlib import Path

import numpy as np
from gensim.models import FastText, Word2Vec
from scipy.linalg import orthogonal_procrustes
from scipy.stats import spearmanr

# Chronological order matters: this is the time axis.
PERIODS = ["vedic", "upanisadic", "epics", "sutras"]

# Case-study terms (SLP1). Philosophically/loaded vocabulary with known trajectories.
CASE_WORDS = ["Darma", "karma", "Atman", "fta", "yajYa", "deva",
              "brahman", "asura", "agni", "rAjan", "rAjA", "nfpa"]

TOPK = 25            # neighborhood size for Jaccard / second-order
N_ANCHORS = 1000     # anchor count for Procrustes
ANCHOR_MIN_COUNT = 10
DISPLAY_K = 12       # neighbors shown in case studies


# ----------------------------------------------------------------------------- loading
def load_wv(models_dir, era):
    """Load a KeyedVectors for `era`, auto-detecting FastText vs Word2Vec by filename.
    Works on the old fasttext_<era>.model and on train.py's word2vec_<era>.model."""
    d = Path(models_dir) / era
    ft, w2 = d / f"fasttext_{era}.model", d / f"word2vec_{era}.model"
    if ft.exists():
        return FastText.load(str(ft)).wv
    if w2.exists():
        return Word2Vec.load(str(w2)).wv
    cand = list(d.glob("*.model"))
    if not cand:
        raise FileNotFoundError(d)
    try:
        return FastText.load(str(cand[0])).wv
    except Exception:
        return Word2Vec.load(str(cand[0])).wv


def era_vocab(wv, min_count=1):
    return {w for w in wv.key_to_index
            if wv.get_vecattr(w, "count") >= min_count}


def l2norm(mat):
    n = np.linalg.norm(mat, axis=1, keepdims=True)
    n[n == 0] = 1.0
    return mat / n


# ----------------------------------------------------------------------------- neighbor machinery
class EraSpace:
    """Holds normalized vectors restricted to a shared candidate vocabulary,
    so neighbor sets across eras are drawn from the SAME pool (comparable)."""
    def __init__(self, wv, shared_words):
        self.wv = wv
        self.words = [w for w in shared_words if w in wv.key_to_index]
        self.idx = {w: i for i, w in enumerate(self.words)}
        self.mat = l2norm(np.vstack([wv[w] for w in self.words]).astype(np.float64))

    def neighbors(self, word, topk):
        """Top-k neighbors of `word` within the shared pool (cosine)."""
        if word not in self.idx:
            return []
        v = self.mat[self.idx[word]]
        sims = self.mat @ v
        sims[self.idx[word]] = -np.inf  # exclude self
        order = np.argpartition(-sims, topk)[:topk]
        order = order[np.argsort(-sims[order])]
        return [self.words[i] for i in order]

    def cos_to(self, word, others):
        """Cosine of `word` to each word in `others` (all in shared pool)."""
        v = self.mat[self.idx[word]]
        return np.array([float(self.mat[self.idx[o]] @ v) for o in others])


# ----------------------------------------------------------------------------- metrics
def jaccard_distance(a, b):
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return np.nan
    return 1.0 - len(sa & sb) / len(sa | sb)


def second_order_drift(space_a, space_b, word, topk):
    """1 - cosine between the two similarity-profiles of `word` over the union
    of its neighbors in A and B. Alignment-free (Hamilton et al. 2016)."""
    na = space_a.neighbors(word, topk)
    nb = space_b.neighbors(word, topk)
    union = list(dict.fromkeys(na + nb))  # order-preserving unique; all in shared pool
    if len(union) < 2:
        return np.nan
    sa = space_a.cos_to(word, union)
    sb = space_b.cos_to(word, union)
    denom = np.linalg.norm(sa) * np.linalg.norm(sb)
    if denom == 0:
        return np.nan
    return 1.0 - float((sa @ sb) / denom)


def procrustes_map(base_wv, other_wv, anchors):
    """Rotation R s.t. normalized other-space ≈ base-space, fit on anchor words."""
    B = l2norm(np.vstack([base_wv[w] for w in anchors]).astype(np.float64))
    O = l2norm(np.vstack([other_wv[w] for w in anchors]).astype(np.float64))
    R, _ = orthogonal_procrustes(O, B)
    return R


def procrustes_drift(base_wv, other_wv, R, word):
    vb = base_wv[word].astype(np.float64)
    vo = other_wv[word].astype(np.float64)
    vb /= (np.linalg.norm(vb) or 1.0)
    vo = vo @ R
    vo /= (np.linalg.norm(vo) or 1.0)
    return 1.0 - float(vb @ vo)


# ----------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models_dir", required=True)
    ap.add_argument("--out_dir", required=True)
    ap.add_argument("--topk", type=int, default=TOPK)
    ap.add_argument("--stoplist", default=str(Path(__file__).resolve().parent / "sanskrit_stoplist_slp1.txt"),
                    help="SLP1 function-word list; excluded from rankings/stats "
                         "(not from drift_scores.csv). Pass '' to disable.")
    args = ap.parse_args()

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    STOP = set()
    if args.stoplist:
        for ln in Path(args.stoplist).read_text(encoding="utf-8").splitlines():
            STOP.update(ln.split("#")[0].split())
        print(f"Loaded stoplist: {len(STOP)} function words (excluded from rankings)")

    print(f"Loading models from {args.models_dir} ...")
    wvs = {e: load_wv(args.models_dir, e) for e in PERIODS}

    # Shared vocabulary across ALL eras (the words we can track end-to-end).
    shared = set(era_vocab(wvs[PERIODS[0]]))
    for e in PERIODS[1:]:
        shared &= era_vocab(wvs[e])
    shared = sorted(shared)
    print(f"Shared vocab across all {len(PERIODS)} eras: {len(shared):,} words")

    # Per-era restricted spaces (common candidate pool -> comparable neighbors).
    spaces = {e: EraSpace(wvs[e], shared) for e in PERIODS}

    # Frequencies per era (for control + reporting).
    freq = {e: {w: int(wvs[e].get_vecattr(w, "count")) for w in shared} for e in PERIODS}

    # Anchors for Procrustes: shared words frequent in every era.
    anchor_pool = [w for w in shared
                   if all(freq[e][w] >= ANCHOR_MIN_COUNT for e in PERIODS)]
    anchor_pool.sort(key=lambda w: min(freq[e][w] for e in PERIODS), reverse=True)
    anchors = anchor_pool[:N_ANCHORS]
    print(f"Procrustes anchors: {len(anchors)} (min-count>={ANCHOR_MIN_COUNT})")

    # Pre-fit Procrustes rotations: align every era onto Vedic (the base).
    base = PERIODS[0]
    R = {base: np.eye(wvs[base].vector_size)}
    for e in PERIODS[1:]:
        R[e] = procrustes_map(wvs[base], wvs[e], anchors)

    # Era transitions to score: each adjacent step + the full span.
    spans = [(PERIODS[i], PERIODS[i + 1]) for i in range(len(PERIODS) - 1)]
    spans.append((PERIODS[0], PERIODS[-1]))  # full trajectory (headline)

    # ---- compute all metrics for every shared word ----
    rows = []
    for w in shared:
        row = {"word": w}
        for e in PERIODS:
            row[f"freq_{e}"] = freq[e][w]
        for a, b in spans:
            tag = f"{a[:3]}_{b[:3]}"
            row[f"jac_{tag}"] = jaccard_distance(
                spaces[a].neighbors(w, args.topk), spaces[b].neighbors(w, args.topk))
            row[f"so_{tag}"] = second_order_drift(spaces[a], spaces[b], w, args.topk)
            # Procrustes in the common base frame: distance between aligned a and b.
            vb = wvs[a][w].astype(np.float64); vb @= R[a]; vb /= (np.linalg.norm(vb) or 1.0)
            vo = wvs[b][w].astype(np.float64); vo @= R[b]; vo /= (np.linalg.norm(vo) or 1.0)
            row[f"proc_{tag}"] = 1.0 - float(vb @ vo)
        rows.append(row)

    # ---- write full table ----
    fieldnames = list(rows[0].keys())
    with open(out / "drift_scores.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=fieldnames)
        wr.writeheader()
        wr.writerows(rows)
    print(f"Wrote {out/'drift_scores.csv'} ({len(rows)} words)")

    # ---- rankings on the headline metric (second-order, full span) ----
    span_tag = f"{PERIODS[0][:3]}_{PERIODS[-1][:3]}"
    key = f"so_{span_tag}"
    ranked = [r for r in rows if not np.isnan(r[key])]
    ranked.sort(key=lambda r: r[key], reverse=True)

    def total_freq(r):
        return sum(r[f"freq_{e}"] for e in PERIODS)

    # Min-frequency filter (rank real signal) + exclude function words from rankings.
    robust = [r for r in ranked
              if min(r[f"freq_{e}"] for e in PERIODS) >= 10 and r["word"] not in STOP]

    with open(out / "top_movers.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=["word", key, f"jac_{span_tag}",
                                           f"proc_{span_tag}", "min_freq", "tot_freq"])
        wr.writeheader()
        for r in robust[:60]:
            wr.writerow({"word": r["word"], key: round(r[key], 4),
                         f"jac_{span_tag}": round(r[f"jac_{span_tag}"], 4),
                         f"proc_{span_tag}": round(r[f"proc_{span_tag}"], 4),
                         "min_freq": min(r[f"freq_{e}"] for e in PERIODS),
                         "tot_freq": total_freq(r)})
    with open(out / "most_stable.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=["word", key, "min_freq", "tot_freq"])
        wr.writeheader()
        for r in sorted(robust, key=lambda r: r[key])[:60]:
            wr.writerow({"word": r["word"], key: round(r[key], 4),
                         "min_freq": min(r[f"freq_{e}"] for e in PERIODS),
                         "tot_freq": total_freq(r)})

    # ---- frequency-control check ("law of conformity": frequent words drift less) ----
    logf = np.array([np.log(total_freq(r)) for r in robust])
    drift = np.array([r[key] for r in robust])
    rho, p = spearmanr(logf, drift)
    print(f"\nFrequency control (robust set, n={len(robust)}): "
          f"Spearman(log total_freq, drift) = {rho:.3f} (p={p:.2e})")

    # ---- cross-metric agreement (triangulation) ----
    so = np.array([r[key] for r in robust])
    jac = np.array([r[f"jac_{span_tag}"] for r in robust])
    proc = np.array([r[f"proc_{span_tag}"] for r in robust])
    print("Cross-metric Spearman (full span, robust set):")
    print(f"  second-order vs jaccard : {spearmanr(so, jac).correlation:.3f}")
    print(f"  second-order vs procrustes: {spearmanr(so, proc).correlation:.3f}")
    print(f"  jaccard vs procrustes     : {spearmanr(jac, proc).correlation:.3f}")

    print("\nTop 20 movers (second-order, full span, min_freq>=10):")
    for r in robust[:20]:
        print(f"  {r['word']:<14} so={r[key]:.3f}  jac={r[f'jac_{span_tag}']:.3f}  "
              f"proc={r[f'proc_{span_tag}']:.3f}  minf={min(r[f'freq_{e}'] for e in PERIODS)}")

    # ---- case studies: neighbor lists per era (full vocab) + drift across span ----
    lines = []
    for w in CASE_WORDS:
        lines.append("=" * 70)
        present = [e for e in PERIODS if w in wvs[e].key_to_index]
        lines.append(f"{w}    (in-vocab: {', '.join(present) or 'NONE'})")
        if w in dict((r['word'], r) for r in rows):
            r = next(r for r in rows if r['word'] == w)
            lines.append(f"  full-span drift: second-order={r.get(f'so_{span_tag}', float('nan')):.3f}  "
                         f"jaccard={r.get(f'jac_{span_tag}', float('nan')):.3f}  "
                         f"procrustes={r.get(f'proc_{span_tag}', float('nan')):.3f}")
        for e in PERIODS:
            if w not in wvs[e].key_to_index:
                lines.append(f"  [{e}] —")
                continue
            nbrs = [t for t, _ in wvs[e].most_similar(w, topn=DISPLAY_K)]
            cnt = int(wvs[e].get_vecattr(w, "count"))
            lines.append(f"  [{e}] (n={cnt})  " + ", ".join(nbrs))
    (out / "case_studies.txt").write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {out/'case_studies.txt'}, {out/'top_movers.csv'}, {out/'most_stable.csv'}")


if __name__ == "__main__":
    main()
