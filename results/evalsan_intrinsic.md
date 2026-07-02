# EvalSan intrinsic evaluation — per-era models (synchronic sanity check)

Ran the Sandhan et al. (2023) EvalSan intrinsic suite (SLP1 data) on our Epics-era
Word2Vec models. We report it **two ways**:

- **Native (as-published):** EvalSan's own `web.evaluate` functions, unmodified — they
  substitute the **mean vector for OOV words** and score the FULL test set. Only two thin
  shims were needed because the 2023 code predates numpy 2 / sklearn 1.9 (`np.vstack` no
  longer takes a bare generator; `AgglomerativeClustering(affinity=)` → `metric=`). Neither
  shim changes a metric. Code: `code/run_evalsan_native.py`.
- **In-vocab (diagnostic):** same metrics but restricted to words the model actually has,
  with coverage reported. Code: `code/run_evalsan.py`.

## Results

| Task | NATIVE sandhi | NATIVE lemma | in-vocab sandhi (cov) | in-vocab lemma (cov) |
|---|---|---|---|---|
| Synonym MCQ (acc%) | n/a (0 in-vocab rows) | n/a | n/a (0%) | n/a (0%) |
| Categorization-semantic (purity) | **0.27** | **0.42** | 0.40 (46%) | 0.58 (58%) |
| Categorization-syntactic (purity) | 0.10 | ~0.10 | 0.30 (19%) | 0.80 (0.8%) |
| Relatedness (acc% / f) | 33.2 / 0.195 | 34.1 / 0.227 | 44.5 (2.4%) | 44.1 (4.6%) |
| Analogy-semantic (acc%) | ~1 (in-vocab quads) | ~1 | 0.9 (10%) | 1.3 (11%) |
| Analogy-syntactic (acc%) | ~2 | ~0 | 2.2 (5%) | 0.0 (0.3%) |

(MCQ and analogy score only fully-in-vocab items in *both* versions — that's how EvalSan
itself defines them — so they don't differ. The native/in-vocab gap is in categorization and
relatedness, where EvalSan does the OOV→mean substitution.)

## Reading the two versions (important — corrects an intuition)
- **In-vocab is the EASIER, more flattering number, not the harder one.** Restricting to
  known words *raises* semantic-categorization purity (0.58 vs native 0.42 on lemma) because
  EvalSan's OOV→mean substitution collapses ~half the test vocab onto one identical point,
  which adds noise. So the in-vocab variant isolates vector quality from coverage; it does
  not "de-inflate."
- **The native (as-published) number is the legitimate EvalSan benchmark score** and is the
  one to report — it's comparable to the EvalSan paper and immune to any cherry-pick critique.
  It is low mainly because **coverage is low**: a period-specific bin doesn't contain the
  lexicographic/Amarakośa test vocabulary, and ~half the items are OOV.

## What's actually meaningful
- **Semantic categorization is the one real signal.** Native purity 0.42 (lemma) / in-vocab
  0.58, both above the trivial single-cluster baseline (0.11 = largest class / N = 10/90 on the
  in-vocab set). The embeddings encode genuine, if modest, semantic structure.
- **MCQ (0% coverage), relatedness (2–5% in-vocab; native dominated by OOV→mean), and analogy
  (~1%)** are not informative on per-era bins.

## Two structural findings (useful for the paper)
1. **EvalSan largely doesn't transfer to per-era diachronic models** — coverage is the binding
   constraint, not vector quality. Even the synchronic *evaluation tooling* doesn't transfer to
   period bins, which reinforces the transfer/evaluation framing.
2. **A clean preprocessing × task interaction.** Lemmatization helps semantic categorization
   (citation forms → higher coverage & purity) but destroys syntactic categorization (which
   tests inflectional paradigms like kapiḥ/kapī/kapayaḥ — lemmatizing collapses them, 0.8%
   coverage). Sandhi-split is the reverse. "Best preprocessing" is task-dependent — same lesson
   as the diachronic w2v-vs-FastText finding.

## Verdict for the paper
- **Report the native EvalSan numbers** (semantic-categorization purity ≈ 0.42, lemma), state
  the coverage, and add one diagnostic sentence: "conditional on in-vocabulary items purity
  rises to 0.58, so the deficit reflects coverage of period-specific bins, not vector quality."
- That's faithful to the established tool *and* honest about what it measures. One sanity
  paragraph, not a pillar — the diachronic anchor-displacement test remains the real validation.
- **For v2 / a pooled all-era model**, coverage (and thus all EvalSan tasks) will improve.
