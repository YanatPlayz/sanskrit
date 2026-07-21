# Measuring Semantic Change in Sanskrit

Code and corpus for *A Computational Approach to Measuring Semantic Change in Sanskrit
Literature*.

Diachronic word embeddings are the standard tool for tracking semantic change, but they
have been validated almost entirely on modern, high-resource, well-segmented languages.
This project tests whether the paradigm transfers to Sanskrit, whose phonological fusion
(*sandhi*), compounding, heavy inflection, and polysemy all work against the assumption
that text arrives as a clean sequence of word tokens.

A 2.7M-token corpus spanning four canonical periods is segmented with a neural
byte-level sandhi splitter, embeddings are trained per period, and recovery is evaluated
against a validation set of shifts documented in Indological scholarship. Of 21 testable
shifts, 19 move in the philologically attested direction (one-sided sign test,
*p* ≈ 1.1 × 10⁻⁴).

## What is here

| | |
|---|---|
| `corpus/` | The four-period sandhi-split corpus, in SLP1. This is the input to the primary model. |
| `code/preprocessing/` | The pipeline that turns GRETIL source texts into that corpus. |
| `code/` | Training, change metrics, the recovery evaluation, and the EvalSan benchmarks. |

The validation set of documented shifts, with source and target senses, change type, transition, and citation for each entry, is in the paper's appendix.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Sandhi splitting and lemmatization call the ByT5-Sanskrit model through the
`dharmamitra-sanskrit-grammar` package, which requires network access.

## Corpus

Sandhi-split for four bins, following standard periodization by literary stratum rather than by century, since individual works cannot be dated precisely.

| Period | Date | Tokens | Vocab (freq ≥ 5) |
|---|---|---|---|
| Vedic | 1500 – 600 BCE | 417K | 10,783 |
| Upaniṣadic | 700 – 200 BCE | 228K | 5,493 |
| Epic | 400 BCE – 400 CE | 1.78M | 30,103 |
| Sūtra/Śāstra | 200 BCE – 500 CE | 290K | 8,591 |

The corpus is imbalanced — the Epic bin is roughly 7.8× the Upaniṣadic bin. Because bin size affects the geometry of an embedding space independently of meaning, the change metrics below favor comparisons of structure *within* periods over raw geometry
comparisons *across* them.

Text is encoded in SLP1, a reversible ASCII scheme in which one character is one phoneme. Convert back to IAST or Devanagari with `indic-transliteration`.

All source texts come from [GRETIL](https://gretil.sub.uni-goettingen.de/) (Göttingen Register of Electronic Texts in Indian Languages), downloaded as Plain Transformation `.txt` files. The processing steps (cleaning, segmentation, transliteration) are released with this repository; the
underlying texts remain subject to GRETIL's own terms and the terms of the editions they
derive from.

## Preprocessing pipeline

Only needed to rebuild the corpus from GRETIL sources, or to build the `raw` and `lemma`
variants (which are not distributed). Every script takes explicit `--input`/`--output`
paths; run them per period.

| Stage | Script | What it does |
|---|---|---|
| 1a | `html_to_text.py` | Flattens HTML editions (the Mahābhārata) to text. |
| 1b | `extract_mula.py` | Drops Śaṅkara's commentary from the interleaved Upaniṣad editions, keeping only root text. |
| 1c | `strip_header.py` | Removes the GRETIL header block. |
| 1d | `strip_markup.py` | Removes verse references, editorial brackets, and structural punctuation. |
| 2 | `build_corpus.py` | Concatenates one period's texts into `<period>_corpus.txt`. |
| 3 | `chunk.py` | Splits long lines at whitespace to fit the analyzer's context window. |
| 4a | `sandhi_split.py` | Recovers word boundaries with ByT5-Sanskrit. **Slow — this is the expensive stage.** |
| 4b | `split_long_compounds.py` | Second pass re-segmenting residual long compounds individually. |
| 5 | `lemmatize.py` | Builds the `lemma` variant via a cached form→lemma lookup table. |
| 6 | `transliterate.py` | Converts IAST to SLP1. Run once per variant that will be trained on. |

Stage 1b is worth calling out: several GRETIL Upaniṣad files interleave the root verses
with a commentary written centuries later. Left in, that commentary would contaminate the
Upaniṣadic bin with a much later stratum of the language.

## Training

Note that gensim's multi-worker training is not bit-for-bit reproducible even with a
fixed seed. Δ values may differ in the third decimal place; the direction of each shift
and the sign test are stable.

## Analysis

**`train.py`** — trains one cell of the grid (preprocessing variant × architecture ×
period). Every cell shares one frozen hyperparameter configuration, so any difference in
the results traces to the factor under study rather than to tuning.

```bash
python train.py --variant sandhi --arch word2vec --out_dir ../models/w2v-sandhi
python train.py --variant sandhi --arch fasttext --min_n 6 --max_n 12 --out_dir ../models/ft-sandhi-6-12
```

**`drift.py`** — computes the change metrics for every word trackable across all four
periods, and writes per-period neighbor lists for the case-study words.

```bash
python drift.py --models_dir ../models/w2v-sandhi --out_dir ../analysis/w2v-sandhi
```

Two metrics, chosen to have different failure modes:

- *Second-order similarity* — compares a word not by its raw vector but by what it is
  similar to. Independently trained spaces have unrelated coordinate frames, so the word
  is described within each period by its vector of cosine similarities to a reference
  set, and the two profiles are compared. Needs no cross-period alignment.
- *Procrustes-aligned cosine distance* — rotates each period's space onto the Vedic space
  using orthogonal Procrustes fit on stable high-frequency words, then compares vectors
  directly. No rotation can perfectly reconcile independently trained spaces, so this
  carries alignment noise; it is a cross-check, and its agreement with the second-order
  measure is the reliability estimate reported in the paper.

**`recovery_anchor_test.py`** — the headline evaluation. For each documented shift,
anchor words denoting the old and new senses are specified *a priori* from the
scholarship, never read off the model's neighbor lists. A word counts as moving in its
attested direction if

```
Δ = [cos(w, new) − cos(w, old)]_end − [cos(w, new) − cos(w, old)]_start  >  0
```

The two-sided contrast matters: absolute cosine similarities fall as embedding spaces
grow more dispersed, so measuring against both senses isolates semantic change from
changes in the geometry of the space. Significance comes from a one-sided binomial sign
test over the whole set, since with four periods a per-word test would be underpowered.

**`recovery_eval.py`** — assembles the qualitative evidence: per-period neighbor lists
in both SLP1 and IAST, alongside the drift scores. It deliberately does not issue a
verdict. Deciding whether a trajectory matches a documented shift is a philological
judgment made by reading the neighbors against the sources and checking each neighbor's
sense in a dictionary; the script only lays out the evidence for that reading.

**`case_go_pada.py`** — neighbor tables with cosine scores for the two instructive
misses, *go* and *pāda*.

**`compare.py`** — the grid comparison table: orthographic pollution, cross-metric
reliability, frequency correlation, and trackable vocabulary per model. Requires
`train.py` and `drift.py` to have been run for every model it lists.

### EvalSan benchmarks

`run_evalsan.py` and `run_evalsan_native.py` evaluate a single period's embeddings on the
[EvalSan](https://github.com/Jivnesh/SanEval) intrinsic tasks (Sandhan et al., 2023).
Clone it into `code/EvalSan` first — it is not vendored here.

The two scripts differ in how they handle out-of-vocabulary test items, and the gap
between them is the point. `run_evalsan_native.py` calls the published EvalSan code
unmodified, which substitutes the mean vector for OOV words and scores the full test set.
`run_evalsan.py` instead restricts every task to its in-vocabulary items and reports
coverage next to each score, so a number computed from a handful of items is never
mistaken for a real result. Coverage is the binding constraint here: EvalSan itself
reports that roughly 55% of relatedness test words are OOV, and a single diachronic
period has a much smaller vocabulary than the pooled corpus those benchmarks assume.