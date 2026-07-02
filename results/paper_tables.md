# Paper-ready results tables (v1, w2v-sandhi primary)

All numbers below are final for the v1 corpus. Each table has a **caption** (drop into the
paper), **how to read**, and **where it goes / how to integrate**. Primary model =
`w2v-sandhi` (word2vec on neural sandhi-split SLP1 text).

---

## Table 1 — Corpus statistics (per period)

| Period | ~Date | Tokens (raw) | Model vocab | Train tokens (≥min-count) | Lines/sents |
|---|---|---:|---:|---:|---:|
| Vedic | ~1500–800 BCE | 416,913 | 10,783 | 348,815 | 59,036 |
| Upaniṣadic | ~800–300 BCE | 227,782 | 5,493 | 193,577 | 8,410 |
| Epic | ~400 BCE–400 CE | 1,784,671 | 30,103 | 1,654,124 | 262,656 |
| Sūtra/Śāstra | ~600 BCE–500 CE | 290,043 | 8,591 | 227,296 | 23,430 |
| **Total** | | **2,719,409** | | | |

**How to read:** four diachronic bins; "model vocab" = types after min-count=5;
"train tokens" = tokens surviving min-count. The corpus is **imbalanced**: Epic ≈ 4.3×
Vedic and ≈ 7.8× Upaniṣadic tokens.
**Integrate:** §Corpus. State the imbalance as a *design property* you control for (size
isn't matched; the alignment-free second-order metric and the within-era neighbor/anchor
tests are robust to it). Add the honest v1 caveat that transmitted Upaniṣadic interleaves
later commentary (v2 fix is future work).

---

## Table 2 — Model grid: what supports recovery (RQ2)

| Model (preproc × arch) | Orthographic-neighbor % ↓ | Metric agreement (so~proc) ↑ | freq~drift | Trackable vocab ↑ |
|---|---:|---:|---:|---:|
| FastText / raw (3-6) | 68% | 0.67 | −0.04 | 801 |
| word2vec / raw | 7% | 0.70 | +0.14 | 801 |
| FastText / sandhi (3-6) | 67% | 0.74 | +0.12 | 1,345 |
| FastText / sandhi (6-12) | 19% | 0.65 | +0.26 | 1,345 |
| **word2vec / sandhi** | **4%** | **0.70** | +0.30 | **1,345** |
| word2vec / lemma | 7% | 0.58 | +0.21 | 1,246 |

**FastText n-gram tuning (the key control):** raising the char-n-gram range from 3-6 to 6-12
cuts orthographic pollution **67% → 19%** — confirming the pollution is a *short*-n-gram
artifact (short shared prefixes like the 4-char *rāj-* drive spurious neighbors; 6+ char grams
are closer to morphemes). But even tuned FastText stays **~5× more polluted than word2vec
(19% vs 4%)** and is the **least reliable** variant (so~proc 0.65, lowest of all). So word2vec
remains the recommendation — and demonstrably *not for lack of tuning FastText*.

**How to read each column:**
- **Orthographic-neighbor %** = fraction of a word's top-10 neighbors that are merely
  *spelling*-similar (shared ≥4-char prefix/suffix or Levenshtein ≤2), averaged over the
  case words × eras. **Lower = more semantic.** FastText ≈ 67–68% (subword n-grams pull in
  spelling-mates, e.g. *rāja→rātri* "night"); word2vec ≈ 4–7%. **This is the headline for
  "word2vec > FastText for change recovery."**
- **so~proc** = Spearman agreement between the two drift metrics (second-order vs Procrustes)
  = reliability. Higher = the metrics corroborate each other. word2vec-sandhi 0.70; lemma
  lowest (0.58).
- **freq~drift** = Spearman(log-frequency, drift). Hamilton's "law of conformity" predicts
  **negative** (frequent words change slower); we get **positive** everywhere → a *reversed/
  spurious* relation, almost certainly a small-corpus + imbalance artifact. **Report as a
  limitation, NOT a law.**
- **Trackable vocab** = words present in all 4 eras (what you can study end-to-end).
  Sandhi-splitting lifts it 801→1,345 (**+68%**).

**The two orthogonal effects (state this explicitly):** *architecture* governs neighbor
quality (4% vs 67% pollution); *preprocessing* governs coverage (801→1,345). word2vec-sandhi
is the joint optimum: lowest pollution + highest coverage + good reliability.
**Integrate:** §Results RQ2 + §Discussion. This is contribution C3.

**Epoch robustness (justifies the frozen 10-epoch config — methods footnote / appendix):**
more epochs *overtrain the small period bins* and reduce cross-metric reliability. Same
corpus, only epochs varied:

| Model | so~proc @10ep | so~proc @30ep |
|---|---:|---:|
| word2vec / sandhi (primary) | **0.70** | 0.25 |
| FastText / sandhi 6-12 | 0.65 | 0.42 |

At 30 epochs the flagship *asura* recovery also degrades — Epic neighbors drift toward
*sura* "god" / *deva* / *namaskṛta* "revered" and the demonic cluster (dānava, daitya,
piśāca) drops out of the top-10. 30 epochs yields prettier *within*-era neighbor lists but a
noisier *between*-era drift signal — the same overtraining from two sides. **We use 10 epochs.**

### Table 2b — the money example (neighbors of *rājan/rājā*, Vedic, top-8)

| Model | Vedic neighbors of *rājā* |
|---|---|
| FastText / sandhi (3-6) | rāj, rāja, rāje, rājñī, rājānau, rājasu, rājan, vaiśvāmitraḥ — *all spelling-variants of √rāj (orthographic)* |
| FastText / sandhi (6-12) | aruṇa, **pati, deva**, bhuvanasya, **śuci**, netā, dhāruṇa, **jāta** — *semantic (the n-gram fix)* |
| **word2vec / sandhi** | **deva, priya, pati, jāta, vrata, śuci, soma, jana — *the sacral-kingship divine company*** |

**How to read / integrate:** a three-way side-by-side that shows *why* FastText fails for
recovery **and** that it's an n-gram-length effect. ft-3-6 returns morphological echoes of the
same string; ft-6-12 recovers the meaning field (pati "lord", deva, śuci, jāta) — nearly
word2vec; word2vec is cleanest. Put in §Results RQ2. This is the figure-free demonstration that
the FastText problem is short-n-gram-driven, not inherent to subwords.

---

## Table 3 — Validation set (documented shifts)

Full table is `paper/validation_set.md` — **24 documented shifts + 2 controls**, each with
from→to, change type, expected transition, Kamboja page(s), and per-era frequency. Tiered:
8 Tier-A flagship, 16 Tier-B, 2 controls (deva, veda).
**How to read / integrate:** §Validation set (its own short section). This is the instrument
that makes the study a *recovery/evaluation*. Cite Kamboja per row; note **blind curation**
(built from Kamboja's index, filtered only by trackability, before seeing any results) — the
core anti-cherry-pick defense.

---

## Table 4 — Recovery: directional anchor-displacement test (HEADLINE)

> **19 of 21 testable documented shifts move in the attested direction; binomial sign test,
> H0 = 0.5, one-sided p = 0.00011. The deva control does NOT move toward the demonic anchors.**

Full per-word table: `results/anchor_test.md`. Method: for each shift, anchors denoting the
old and new sense (chosen a priori from Kamboja's glosses, **not** from neighbor lists);
Δ = (cos→new − cos→old)|end − (cos→new − cos→old)|start over the documented transition;
Δ>0 = attested direction. **Two misses** are honest and interpretable:
- **go** (Δ=−0.13): the metaphorical senses (earth/rays) are *Vedic poetic-register* and
  *recede* over time — not a monotonic widening. Method correctly flags a non-directional
  shift.
- **pāda** (Δ=−0.10): the "quarter" anchors are sparse.
**Three not testable by anchors** (yoga, bhṛtya, veda): their new-sense vocabulary postdates
the old era, so no fixed cross-era reference exists → recovered qualitatively via neighbors
instead (yoga is the clean example of anchor-undefined / neighbor-recovered).

**How to read / integrate:** §Results 6.1 — your quantitative recovery result. Pair with
Table 5 (EvalSan) and §6.2 case studies. State the deflation diagnosis (why the *toward-minus-
away* contrast is needed) as a methods point — it's the reason the two-sided design matters.

---

## Table 5 — EvalSan synchronic sanity (secondary)

| | Native (as-published, OOV→mean) | In-vocab (diagnostic) |
|---|---|---|
| Semantic categorization purity (lemma) | **0.42** | 0.58 (58% cov) |
| Semantic categorization purity (sandhi) | 0.27 | 0.40 (46% cov) |
| (trivial single-cluster baseline) | 0.11 | 0.11 |

Full detail: `results/evalsan_intrinsic.md`. MCQ/relatedness/analogy are coverage-dead on
per-era bins (report as such).
**How to read / integrate:** §Results 6.4, **one paragraph**. "Semantic-categorization purity
(native 0.42 / in-vocab 0.58) is well above the 0.11 trivial baseline → the vectors encode
real semantic structure; the remaining EvalSan tasks lack coverage on period-specific bins —
itself evidence that lexicographic intrinsic benchmarks don't transfer to diachronic per-era
Sanskrit." Note the lemma-helps-semantic / kills-syntactic interaction as a one-liner (C3).

---

## Case-study neighbor tables (qualitative centerpiece)

Source: `results/recovery_evidence.md` (per-era top-15 neighbors, IAST+SLP1, + my draft
verdicts you've now verified). Feature these **7**: **asura, ātman, brahman, varuṇa, guṇa**
(clean recoveries) + **go, yoga** (instructive limits, explained above).
**How to read / integrate:** §Results 6.2. For each: 1–2 sentences of neighbor trajectory →
the documented shift (Kamboja) → WisdomLib gloss of the key neighbors → one honest hedge.
This is where your manual validation becomes prose.

---

## Integration checklist (order of assembly)
1. §Corpus → Table 1.  2. §Methods → frozen config + metrics + **the anchor test**.
3. §Validation set → Table 3 (+ blind-curation note).  4. §Results 6.1 → **Table 4 (headline)**.
5. §Results 6.2 → 7 case studies.  6. §Results 6.3 (RQ2) → Tables 2 + 2b.
7. §Results 6.4 → Table 5 (one ¶).  8. §Discussion → freq~drift artifact, go/pāda, imbalance,
   polysemy ceiling → contextual future work.
