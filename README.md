# A Computational Approach to Measuring Semantic Change in Sanskrit Literature

Tanay Agrawal (tanayagrawal31@gmail.com). This repository contains the code, data, and other resources accompanying the paper titled above.

Diachronic word embeddings are the standard tool for tracking semantic change, but they have been validated almost entirely on modern, high-resource, and well-segmented languages. This project tests whether the paradigm transfers to Sanskrit, whose phonological fusion (*sandhi*), compounding, heavy inflection, and polysemy all work against the distributional approach.

A 2.7M-token corpus spanning four canonical periods is segmented with a neural byte-level sandhi splitter, embeddings are trained per period, and recovery is evaluated against a validation set of shifts documented in Indological scholarship. Of 21 testable shifts, 19 move in the philologically attested direction (one-sided sign test, *p* ≈ 1.1 × 10⁻⁴).

## Repository contents

| Folder | Description |
|---|---|
| `corpus/` | The four-period sandhi-split corpus, in SLP1. This is the input to the primary model. |
| `code/preprocessing/` | The pipeline that turns GRETIL source texts into that corpus. |
| `code/` | Training, change metrics, the recovery evaluation, and the EvalSan benchmarks. |

The validation set of documented shifts, with source and target senses, change type, transition, and citation for each entry, can be found in the paper's appendix.

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

The corpus is imbalanced: the Epic bin is roughly 7.8× the Upaniṣadic bin. Because bin size affects the geometry of an embedding space independently of meaning, the change metrics below favor comparisons of structure *within* periods over raw geometry
comparisons *across* them.

Text is encoded in SLP1, a reversible ASCII scheme in which one character is one phoneme. Convert back to IAST or Devanagari with `indic-transliteration`.

All source texts come from [GRETIL](https://gretil.sub.uni-goettingen.de/) (Göttingen Register of Electronic Texts in Indian Languages).

## Preprocessing pipeline

Each script takes explicit `--input`/`--output`
paths to run per-period.

| Stage | Script | Function |
|---|---|---|
| 1a | `html_to_text.py` | Flattens HTML editions (the Mahābhārata) to text. |
| 1b | `extract_mula.py` | Drops commentary for certain interleaved editions. |
| 1c | `strip_header.py` | Removes the GRETIL header block. |
| 1d | `strip_markup.py` | Removes verse references, editorial brackets, and structural punctuation. |
| 2 | `build_corpus.py` | Concatenates one period's texts into `<period>_corpus.txt`. |
| 3 | `chunk.py` | Splits long lines at whitespace to fit the analyzer's context window. |
| 4a | `sandhi_split.py` | Recovers word boundaries with ByT5-Sanskrit. |
| 4b | `split_long_compounds.py` | Second pass re-segmenting residual long compounds individually. |
| 5 | `lemmatize.py` | Builds the `lemma` variant via a cached form→lemma lookup table. |
| 6 | `transliterate.py` | Converts IAST to SLP1. Run once per variant that will be trained on. |

## Training

Note that gensim's multi-worker training is not bit-for-bit reproducible even with a fixed seed. Δ values may differ in the third decimal place; the direction of each shift and the sign test are stable.

## Analysis

`train.py` trains one cell of the grid (preprocessing variant × architecture ×
period) with fixed hyperparameters.

```bash
python train.py --variant sandhi --arch word2vec --out_dir ../models/w2v-sandhi
python train.py --variant sandhi --arch fasttext --min_n 6 --max_n 12 --out_dir ../models/ft-sandhi-6-12
```

`drift.py` computes the change metrics for every word trackable across all four periods, and writes per-period neighbor lists for the case-study words.

```bash
python drift.py --models_dir ../models/w2v-sandhi --out_dir ../analysis/w2v-sandhi
```

`recovery_anchor_test.py` has, for each documented shift, anchor words denoting the old and new senses that are specified *a priori* from the literature. A word counts as moving in its attested direction if

```
Δ = [cos(w, new) − cos(w, old)]_end − [cos(w, new) − cos(w, old)]_start  >  0
```

Two-sided contrast is important as absolute cosine similarities fall as embedding spaces
grow more dispersed, so measuring against both senses isolates semantic change from
changes in the geometry of the space. 

`recovery_eval.py` assembles per-period neighbor lists in both SLP1 and IAST, alongside the drift scores.

`run_evalsan.py` and `run_evalsan_native.py` evaluate a single period's embeddings on the
[EvalSan](https://github.com/Jivnesh/SanEval) intrinsic tasks. The two scripts differ in how they handle OOV items. `run_evalsan_native.py` calls the published EvalSan code, which substitutes the mean vector for OOV words and scores the full test set. `run_evalsan.py` instead restricts every task to its in-vocabulary items and reports coverage next to each score.