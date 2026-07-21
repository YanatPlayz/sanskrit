"""
recovery_eval.py — assemble RECOVERY EVIDENCE for the validation set.

For each documented shift (paper/validation_set.md) this emits, per era:
  - token frequency (n)
  - the top-K full-vocabulary nearest neighbors, in IAST (SLP1)
and the precomputed drift scores (second-order + Procrustes, per era-pair and
full span) from analysis/<model>/drift_scores.csv.

It does NOT decide recovered/partial/failed. The verdict is a *subjective*
philological judgment: read the neighbor trajectory against the documented shift,
check each neighbor's sense in a dictionary (WisdomLib / Monier-Williams), and
write the verdict in the blank field. The script only lays out the evidence.

Usage:
    python recovery_eval.py \
        --models_dir ../models/w2v-sandhi \
        --scores ../analysis/w2v-sandhi/drift_scores.csv \
        --out ../results/recovery_evidence.md
"""
import argparse
import csv
from pathlib import Path

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

from drift import load_wv, PERIODS  # PERIODS = vedic, upanisadic, epics, sutras

ERA_LABEL = {"vedic": "Vedic", "upanisadic": "Upaniṣadic", "epics": "Epic", "sutras": "Sūtra"}


def iast(slp1):
    return transliterate(slp1, sanscript.SLP1, sanscript.IAST)


# --- the validation set (documented shifts grounded in Kamboja; see paper/validation_set.md) ---
# forms: probe these surface forms per era, use the highest-count present one for neighbors.
VALIDATION = [
    # ---------- Tier A ----------
    dict(iast="asura", forms=["asura", "asurAH", "asurAn", "asurasya", "asurANAm"],
         shift="'lord, mighty / life-giving god' (epithet even of Indra, Varuṇa, Agni) → 'demon'",
         type="pejoration (religious)", transition="V→E", pp="55–56, 78", tier="A"),
    dict(iast="ātman", forms=["AtmA", "Atman", "AtmAnam", "AtmanaH", "Atmani", "Atmane"],
         shift="'breath' → 'life, vital essence; body' → 'the Self, Absolute Soul'",
         type="abstraction / widening", transition="V→U", pp="57–59", tier="A"),
    dict(iast="brahman", forms=["brahma", "brahman", "brahmaRaH", "brahmaRA", "brahmaRi"],
         shift="'prayer, sacred utterance' → 'sacred knowledge / Veda / priest' → 'the Absolute'",
         type="abstraction / widening", transition="V→U", pp="58–60", tier="A"),
    dict(iast="varuṇa", forms=["varuRa", "varuRaH", "varuRam", "varuRasya"],
         shift="'supreme all-encompassing sovereign, moral governor' → 'god of waters / ocean'",
         type="narrowing / demotion", transition="V→E", pp="56–57, 78", tier="A"),
    dict(iast="go", forms=["go", "gAm", "gAvaH", "gavi", "gavAm", "gObiH"],
         shift="'cow' → metaph. 'earth; rays of light; the senses/eyes; stars; speech'",
         type="widening / metaphor", transition="V→E", pp="72–74, 190–91, 198, 392", tier="A"),
    dict(iast="hari", forms=["hari", "hariH", "harim", "hareH", "harayaH"],
         shift="'tawny / yellow-green (color)' → soma, rays, fire; → 'horse, lion'; → name of Viṣṇu",
         type="specialization (color → divine name)", transition="V→E", pp="100, 219–229", tier="A"),
    dict(iast="yoga", forms=["yoga", "yogaH", "yogam", "yogasya", "yogena"],
         shift="'act of yoking/harnessing' → 'union; means' → 'spiritual discipline; superhuman power'",
         type="abstraction → technical term", transition="V→E/S", pp="309–311", tier="A"),
    dict(iast="guṇa", forms=["guRa", "guRaH", "guRam", "guRAH", "guREH", "guRAn"],
         shift="'strand, cord; bowstring' → 'quality, attribute' → 'virtue' → (Sāṅkhya) the three guṇas",
         type="abstraction / widening", transition="U→E", pp="95, 164, 296–97", tier="A"),
    # ---------- Tier B ----------
    dict(iast="soma", forms=["soma", "somaH", "somam", "somasya", "somena"],
         shift="'the soma plant / its ritual juice' → substitute plants; identified with the moon",
         type="widening / referential", transition="V→E", pp="71, 100", tier="B"),
    dict(iast="prajāpati", forms=["prajApati", "prajApatiH", "prajApatim", "prajApateH"],
         shift="'lord of creatures' → 'the creator, supreme god' (rises in the Brāhmaṇas)",
         type="elevation / amelioration", transition="V→U", pp="56, 124", tier="B"),
    dict(iast="kṣatra", forms=["kzatra", "kzatram", "kzatrasya", "kzatriya", "kzatriyaH"],
         shift="'might, dominion, rule' → 'the warrior/ruling class (kṣatriya)'",
         type="shift (→ social class)", transition="V→E", pp="60–61, 124", tier="B"),
    dict(iast="śūdra", forms=["SUdra", "SUdraH", "SUdram", "SUdrasya", "SUdrAH"],
         shift="'(a non-Aryan tribe / aboriginal section)' → 'the servile/labour class, 4th varṇa'",
         type="widening", transition="V→E", pp="60", tier="B"),
    dict(iast="ari", forms=["ari", "ariH", "arim", "areH", "arayaH", "arIn"],
         shift="'non-giver, miser' → 'enemy' AND 'master, lord, pious man'",
         type="divergence (polysemy split)", transition="V→E", pp="60–62, 149", tier="B"),
    dict(iast="uttara", forms=["uttara", "uttaram", "uttarA", "uttaraH"],
         shift="'upper, higher' → 'later, subsequent; northern; superior'",
         type="widening (spatial → temporal/qual.)", transition="V→S", pp="272–276", tier="B"),
    dict(iast="uttama", forms=["uttama", "uttamaH", "uttamam", "uttamA"],
         shift="'uppermost, highest' → 'best, most excellent; last'",
         type="abstraction (spatial → evaluative)", transition="V→E", pp="269–271", tier="B"),
    dict(iast="pāda", forms=["pAda", "pAdaH", "pAdam", "pAdEH", "pAdayoH"],
         shift="'foot' → 'quarter (¼); foot/line of verse; foot of mountain; ray'",
         type="widening / metaphor", transition="V→E", pp="255–259", tier="B"),
    dict(iast="tejas", forms=["tejas", "tejaH", "tejasA", "tejasaH"],
         shift="'sharpness, edge; fire, brilliance' → 'splendour; vital energy, spiritual power, majesty'",
         type="abstraction", transition="U→E", pp="183", tier="B"),
    dict(iast="setu", forms=["setu", "setuH", "setum", "setoH", "setavaH"],
         shift="'bond, fetter (that binds)' → 'causeway, dam, bridge'; fig. 'boundary; protection'",
         type="concretization / shift", transition="U→S", pp="239–243", tier="B"),
    dict(iast="bhṛtya", forms=["Bftya", "BftyaH", "Bftyam", "BftyAH", "BftyAnAm"],
         shift="'one to be supported, a dependent' → 'servant, slave'",
         type="shift / pejoration", transition="U→E", pp="365–368", tier="B"),
    dict(iast="arka", forms=["arka", "arkaH", "arkam", "arkasya"],
         shift="'ray, flash; hymn of praise' → 'the sun'; also 'the arka plant'",
         type="shift", transition="V→E", pp="386", tier="B"),
    dict(iast="aṃśu", forms=["aMSu", "aMSuH", "aMSum", "aMSavaH"],
         shift="'soma filament/stalk; soma juice' → 'ray of light, sunbeam'",
         type="metaphor / shift", transition="V→E", pp="101, 223", tier="B"),
    dict(iast="preta", forms=["preta", "pretaH", "pretam", "pretasya", "pretAH"],
         shift="'departed, deceased one' → 'ghost, spirit of the dead'",
         type="specialization / pejoration", transition="V→E", pp="81", tier="B"),
    dict(iast="vrata", forms=["vrata", "vratam", "vratasya", "vratAni", "vrate"],
         shift="'divine ordinance, command of the gods; sacred rite' → '(self-imposed) vow, observance, fast'",
         type="shift", transition="V→E", pp="(general)", tier="B"),
    dict(iast="rājan", forms=["rAjA", "rAja", "rAjan", "rAjAnam", "rAjYaH"],
         shift="sacral kingship → heroic/epic sovereign → administrative statecraft register",
         type="shift (register drift)", transition="V→E/S", pp="208 (verify)", tier="B"),
    # ---------- Controls ----------
    dict(iast="deva", forms=["deva", "devAH", "devAn", "devasya", "devAnAm", "devaH"],
         shift="'celestial god' — STABLE in Sanskrit (pejoration only on Iranian side, Av. daēva)",
         type="stable (control)", transition="—", pp="55", tier="C"),
    dict(iast="veda", forms=["veda", "vedaH", "vedam", "vedasya", "vedAH"],
         shift="'knowledge' → specialized 'the Veda (corpus)'; relatively stable",
         type="near-stable (control)", transition="—", pp="160", tier="C"),
]

TIER_TITLE = {"A": "Tier A — flagship shifts", "B": "Tier B — well-documented",
              "C": "Controls — expected stable"}



def best_form(wv, forms):
    """Highest-count present form, with its count."""
    best, bestc = None, -1
    for f in forms:
        if f in wv.key_to_index:
            c = wv.get_vecattr(f, "count")
            if c > bestc:
                best, bestc = f, c
    return best, (bestc if bestc >= 0 else 0)


def neighbors(wv, form, k):
    if form is None or form not in wv.key_to_index:
        return []
    return [(t, s) for t, s in wv.most_similar(form, topn=k)]


def load_scores(path):
    rows = {}
    if Path(path).exists():
        for r in csv.DictReader(open(path)):
            rows[r["word"]] = r
    return rows


def score_line(entry, scores):
    """Return a one-line drift summary pulled from drift_scores.csv, or '—'."""
    # use whichever probe form is present in the scores table
    row = None
    for f in entry["forms"]:
        if f in scores:
            row = scores[f]
            key = f
            break
    if row is None:
        return "_drift scores: — (word not in shared 4-era vocab; rely on neighbor trajectory)_"

    def g(k):
        try:
            return f"{float(row[k]):.3f}"
        except (KeyError, ValueError):
            return "—"
    return (f"_drift ({key}):_ "
            f"**second-order** V→U {g('so_ved_upa')} · U→E {g('so_upa_epi')} · "
            f"E→S {g('so_epi_sut')} · **full V→S {g('so_ved_sut')}**  ||  "
            f"**Procrustes** V→U {g('proc_ved_upa')} · U→E {g('proc_upa_epi')} · "
            f"E→S {g('proc_epi_sut')} · full {g('proc_ved_sut')}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models_dir", required=True)
    ap.add_argument("--scores", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--topk", type=int, default=15)
    args = ap.parse_args()

    wvs = {e: load_wv(args.models_dir, e) for e in PERIODS}
    scores = load_scores(args.scores)

    out = []
    out.append("# Recovery Evidence — w2v-sandhi\n")
    out.append("Per documented shift: full-vocabulary nearest neighbors by era (IAST, SLP1 in "
               "parentheses) + precomputed drift scores. **The verdict is yours to fill in** — "
               "read each trajectory against the documented shift, verify neighbor senses in "
               "WisdomLib/Monier-Williams, then write recovered / partial / failed with a reason.\n")
    out.append(f"Model: `{args.models_dir}` · neighbors: top-{args.topk} (full vocab) · "
               f"periods: Vedic → Upaniṣadic → Epic → Sūtra.\n")

    docs = [e for e in VALIDATION if e["tier"] != "C"]
    out.append(f"{len(docs)} documented shifts and "
               f"{len(VALIDATION) - len(docs)} controls follow, each with its per-period "
               f"neighbor trajectory and drift scores. Fill in a verdict per entry.\n")
    out.append("---\n")

    current_tier = None
    for e in VALIDATION:
        if e["tier"] != current_tier:
            current_tier = e["tier"]
            out.append(f"\n# {TIER_TITLE[current_tier]}\n")

        out.append(f"## {e['iast']}  (Kamboja pp. {e['pp']})")
        out.append(f"- **Documented shift:** {e['shift']}")
        out.append(f"- **Type:** {e['type']}  ·  **expected transition:** {e['transition']}")
        out.append(f"- {score_line(e, scores)}\n")
        out.append("| Era | n | Top neighbors — IAST (SLP1) |")
        out.append("|-----|---|------------------------------|")
        for era in PERIODS:
            wv = wvs[era]
            form, n = best_form(wv, e["forms"])
            nbrs = neighbors(wv, form, args.topk)
            if not nbrs:
                cell = "_absent / not in vocab_"
            else:
                cell = ", ".join(f"{iast(t)} ({t})" for t, _ in nbrs)
            probe = f" _[{iast(form)}]_" if form else ""
            out.append(f"| {ERA_LABEL[era]}{probe} | {n} | {cell} |")
        out.append("")
        out.append("**Verdict (subjective):** ______  ·  **Notes:** ______\n")
        out.append("---\n")

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote {args.out}  ({len(VALIDATION)} validation words)")


if __name__ == "__main__":
    main()
