"""
train.py — frozen-config trainer for the diachronic embedding grid.

The "grid" = (preprocessing variant) x (architecture) x (era), trained with ONE
identical hyperparameter config so the only thing that varies is what you study.

Variants -> corpus (all SLP1):
    raw     data/final/final_slp1/corpus/<era>_corpus.txt   (surface forms; not released)
    sandhi  corpus/<era>_corpus.txt                         (ByT5 sandhi-split; released)
    lemma   data/final/lemma/<era>_corpus.txt               (ByT5 lemmatized; not released)

Architectures: fasttext (subword) | word2vec (no subword -> semantic neighbors)

Examples:
    # primary model: word2vec on the sandhi corpus, all 4 eras
    #   -> models/w2v-sandhi/<era>/word2vec_<era>.model
    python train.py --variant sandhi --arch word2vec --out_dir ../models/w2v-sandhi
    # matched fasttext control, same frozen config
    python train.py --variant sandhi --arch fasttext --out_dir ../models/ft-sandhi-3-6
    # the [6,12] n-gram range reported in the paper
    python train.py --variant sandhi --arch fasttext --min_n 6 --max_n 12 \
        --out_dir ../models/ft-sandhi-6-12

Output layout is exactly what drift.py expects:
    <out_dir>/<era>/<arch>_<era>.model   (+ params.json, stats.csv)
"""

import argparse
import csv
import json
from pathlib import Path

from gensim.models import FastText, Word2Vec
from gensim.models.word2vec import LineSentence

REPO = Path(__file__).resolve().parent.parent
PERIODS = ["vedic", "upanisadic", "epics", "sutras"]

CORPORA = {
    # The sandhi-split corpus is the one released with this repository. The raw and
    # lemmatized variants are intermediate products of the preprocessing pipeline and
    # are not distributed; rebuild them with code/preprocessing/ to reproduce those rows
    # of the grid, or override the location with --corpus_dir.
    "raw":    "data/final/final_slp1/corpus/{era}_corpus.txt",
    "sandhi": "corpus/{era}_corpus.txt",
    "lemma":  "data/final/lemma/{era}_corpus.txt",
}

# ---- FROZEN CONFIG: identical for every cell of the grid; reported in the paper. ----
# NB: gensim training with workers>1 is not bit-for-bit reproducible even with seed;
#     for exact reproducibility set workers=1 (much slower). We match the existing
#     models' settings (workers=4) and fix seed for near-reproducibility.
FROZEN = dict(
    vector_size=300,
    window=5,
    min_count=5,
    sg=1,            # skip-gram
    negative=10,
    sample=1e-4,
    epochs=10,
    seed=42,
    workers=4,
)


def train_one(corpus_path, arch, min_n, max_n):
    sentences = LineSentence(str(corpus_path))
    if arch == "fasttext":
        model = FastText(min_n=min_n, max_n=max_n, **FROZEN)
    else:
        model = Word2Vec(**FROZEN)
    model.build_vocab(corpus_iterable=sentences)
    model.train(corpus_iterable=sentences,
                total_examples=model.corpus_count, epochs=FROZEN["epochs"])
    return model


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", required=True, choices=list(CORPORA))
    ap.add_argument("--arch", required=True, choices=["fasttext", "word2vec"])
    ap.add_argument("--out_dir", required=True)
    ap.add_argument("--corpus_dir", default=None,
                    help="directory holding <era>_corpus.txt, overriding the variant's default path")
    ap.add_argument("--eras", nargs="+", default=PERIODS)
    ap.add_argument("--min_n", type=int, default=3)   # fasttext only
    ap.add_argument("--max_n", type=int, default=6)   # fasttext only
    ap.add_argument("--epochs", type=int, default=FROZEN["epochs"])  # override frozen epochs
    args = ap.parse_args()
    FROZEN["epochs"] = args.epochs

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    # Persist the exact recipe (replaces the old ad-hoc params.rtf).
    params = {"variant": args.variant, "arch": args.arch,
              "corpus_template": CORPORA[args.variant], **FROZEN}
    if args.arch == "fasttext":
        params["min_n"], params["max_n"] = args.min_n, args.max_n
    (out / "params.json").write_text(json.dumps(params, indent=2), encoding="utf-8")

    stats = []
    for era in args.eras:
        corpus = (Path(args.corpus_dir) / f"{era}_corpus.txt" if args.corpus_dir
                  else REPO / CORPORA[args.variant].format(era=era))
        if not corpus.exists():
            print(f"  !! missing corpus for {era}: {corpus}")
            continue
        print(f"[{args.arch}/{args.variant}] training {era} from {corpus.name} ...")
        model = train_one(corpus, args.arch, args.min_n, args.max_n)

        era_dir = out / era
        era_dir.mkdir(parents=True, exist_ok=True)
        model.save(str(era_dir / f"{args.arch}_{era}.model"))

        n_tokens = int(sum(model.wv.get_vecattr(w, "count") for w in model.wv.key_to_index))
        stats.append({"era": era, "vocab": len(model.wv.key_to_index),
                      "train_tokens": n_tokens, "sentences": model.corpus_count})
        print(f"    vocab={stats[-1]['vocab']:,}  tokens(>=min_count)={n_tokens:,}")

    with open(out / "stats.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=["era", "vocab", "train_tokens", "sentences"])
        wr.writeheader()
        wr.writerows(stats)
    print(f"\nDone. Models + params.json + stats.csv in {out}")


if __name__ == "__main__":
    main()
