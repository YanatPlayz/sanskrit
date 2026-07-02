"""
recovery_anchor_test.py — Hamilton et al. (2016) Table 2/3-style DIRECTIONAL test.

For each documented shift we specify, A PRIORI from Kamboja's glosses, anchor words that
denote the OLD sense and the NEW sense. We then measure whether the target word moved
TOWARD the new-sense anchors and AWAY from the old-sense anchors across the era-transition
where the change is documented to occur.

This converts the subjective neighbor read into a falsifiable, pre-registered prediction:
  - two-anchor shift:  delta = (cos_new - cos_old)|end  -  (cos_new - cos_old)|start
  - new-only shift:    delta =  cos_new|end             -   cos_new|start
A shift is "in the attested direction" iff delta > 0.

With only 4 eras a per-word significance test is underpowered, so significance comes from the
POPULATION: a binomial sign test over all testable documented shifts (H0: direction is a
coin flip). Anchors are sense-denoting words chosen from the documented glosses, NOT from the
model's neighbor lists, so the test is not circular.

Usage:
  python recovery_anchor_test.py --models_dir ../models/w2v-sandhi --out ../results/anchor_test.md
"""
import argparse
from pathlib import Path

import numpy as np
from scipy.stats import binomtest

from drift import load_wv, PERIODS  # vedic, upanisadic, epics, sutras

TRANS = {  # documented transition -> (start_era, end_era)
    "V→U": ("vedic", "upanisadic"), "V→E": ("vedic", "epics"),
    "V→S": ("vedic", "sutras"), "U→E": ("upanisadic", "epics"),
    "U→S": ("upanisadic", "sutras"), "V→E/S": ("vedic", "epics"),
}

# target forms to probe (reuse the best-present form per era)
TARGET = {
    "asura": ["asura", "asurAH", "asurAn", "asurasya"],
    "ātman": ["AtmA", "Atman", "AtmAnam", "AtmanaH", "Atmani"],
    "brahman": ["brahma", "brahman", "brahmaRaH"],
    "varuṇa": ["varuRa", "varuRaH", "varuRam"],
    "go": ["go", "gAm", "gAvaH", "gavi"],
    "hari": ["hari", "hariH", "harim", "hareH"],
    "yoga": ["yoga", "yogaH", "yogam", "yogena"],
    "guṇa": ["guRa", "guRaH", "guRam", "guRAH"],
    "soma": ["soma", "somaH", "somam"],
    "prajāpati": ["prajApati", "prajApatiH", "prajApatim"],
    "kṣatra": ["kzatra", "kzatram", "kzatrasya"],
    "śūdra": ["SUdra", "SUdraH", "SUdram"],
    "ari": ["ari", "ariH", "arim", "areH"],
    "uttama": ["uttama", "uttamaH", "uttamam"],
    "pāda": ["pAda", "pAdaH", "pAdam"],
    "tejas": ["tejas", "tejaH", "tejasA"],
    "setu": ["setu", "setuH", "setum"],
    "bhṛtya": ["Bftya", "BftyaH", "Bftyam", "BftyAH"],
    "arka": ["arka", "arkaH", "arkam"],
    "aṃśu": ["aMSu", "aMSuH", "aMSavaH"],
    "preta": ["preta", "pretaH", "pretam"],
    "vrata": ["vrata", "vratam", "vratasya"],
    "rājan": ["rAjA", "rAja", "rAjan", "rAjAnam"],
    "deva": ["deva", "devAH", "devaH"],     # control
    "veda": ["veda", "vedaH", "vedam"],     # control
}

# OLD-sense / NEW-sense anchors (SLP1), a priori from documented glosses. [] => not used.
ANCHORS = {
    "asura":   (["indra", "indraH", "mitra", "mitraH", "varuRa", "varuRaH", "savitar"],
                ["rakzas", "rAkzasa", "dAnava", "dAnavaH", "dEtya", "dEtyaH", "piSAca", "yakza", "yakzaH"]),
    "ātman":   (["prARa", "prARaH", "apAna", "apAnaH", "vAyu", "vAyuH", "SarIram"],
                ["brahman", "brahma", "purusza", "puruzaH", "jIva", "jIvaH"]),
    "brahman": (["mantra", "stoma", "stomaH", "uktha", "ukTam", "yajuH", "sAma"],
                ["Atman", "AtmA", "purusza", "puruzaH", "ananta", "anantam", "akzaram"]),
    "varuṇa":  (["indra", "indraH", "mitra", "mitraH", "aryamA", "Baga"],
                ["jala", "jalam", "ap", "apaH", "samudra", "samudraH", "sindhu", "sindhuH", "udaka"]),
    "go":      (["Denu", "DenuH", "vatsa", "vatsaH", "kzIra"],
                ["pfTivI", "pfTivIm", "raSmi", "raSmiH", "BUmi"]),
    "hari":    (["harita", "haritaH", "babhru", "piSaNga"],
                ["vizRu", "vizRuH", "vAnara", "vAnaraH", "kapi", "kapiH"]),
    "yoga":    (["yuj", "yojana", "yojanam", "raSmi"],
                ["DyAna", "DyAnam", "samADi", "samADiH", "yogin", "yogI", "sAMKya"]),
    "guṇa":    (["tantu", "sUtra", "rajju", "pASa", "jyA"],
                ["svaBAva", "svaBAvaH", "prakfti", "prakftiH", "doza", "dozaH", "lakzaRa"]),
    "soma":    (["ozaDi", "latA", "vIruD"],
                ["candra", "candraH", "candramas", "indu", "induH"]),
    "prajāpati": ([],
                ["svayaMBU", "svayaMBUH", "brahmA", "sraszwA", "pitAmaha", "pitAmahaH"]),
    "kṣatra":  (["bala", "balam", "ojas", "ojaH", "vIrya", "vIryam"],
                ["kzatriya", "kzatriyaH", "brAhmaRa", "vESya", "varRa"]),
    "śūdra":   (["dasyu", "dAsa", "dAsaH", "anArya"],
                ["vESya", "vESyaH", "brAhmaRa", "kzatriya", "varRa", "caRqAla"]),
    "ari":     (["mitra", "mitraH", "suhfd", "sakhA"],
                ["Satru", "SatruH", "ripu", "ripuH", "amitra", "amitraH", "dvizat"]),
    "uttama":  (["praTama", "madhyama", "madhyamam", "antya"],
                ["SreszWa", "agrya", "agryam", "mukhya", "muKyam", "parama", "paramam"]),
    "pāda":    (["caraRa", "caraRam", "aNGri", "jaNGA", "hasta"],
                ["caturTa", "caturTam", "turIya", "kalA"]),
    "tejas":   (["agni", "agniH", "jvAlA", "Sucis"],
                ["yaSas", "yaSaH", "SrI", "SriyA", "praBAva", "vIrya"]),
    "setu":    (["banDana", "pASa"],
                ["tIra", "tIram", "anUpa", "nadI", "banDa"]),
    "bhṛtya":  ([],
                ["dAsa", "dAsaH", "sevaka", "paricara", "preszya"]),
    "arka":    (["stoma", "uktha", "arcana"],
                ["sUrya", "sUryaH", "ravi", "raviH", "BAskara", "divAkara"]),
    "aṃśu":    (["soma", "somaH"],
                ["raSmi", "raSmiH", "kiraRa", "kiraRaH"]),
    "preta":   (["mfta", "mftaH"],
                ["pizAca", "piSAca", "BUta", "BUtam", "rakzas"]),
    "vrata":   (["ftam", "ftasya", "Darman", "vidhi"],
                ["upavAsa", "tapas", "tapaH", "niyama", "niyamaH"]),
    "rājan":   (["deva", "devaH", "soma", "somaH", "agni", "agniH"],
                ["rAjya", "rAjyam", "Satru", "SatruH", "daRqa", "amAtya"]),
    # controls — expect NO directional movement toward the "new"(demon/corpus) anchors
    "deva":    (["indra", "indraH", "viSve"],
                ["rakzas", "piSAca", "dAnava"]),
    "veda":    (["jYAna", "vidyA"],
                ["vedANga", "vedAnta", "itihAsa", "purARa"]),
}

TRANSITION = {  # per word (matches validation_set.md)
    "asura": "V→E", "ātman": "V→U", "brahman": "V→U", "varuṇa": "V→E", "go": "V→E",
    "hari": "V→E", "yoga": "V→E", "guṇa": "U→E", "soma": "V→E", "prajāpati": "V→U",
    "kṣatra": "V→E", "śūdra": "V→E", "ari": "V→E", "uttama": "V→E", "pāda": "V→E",
    "tejas": "U→E", "setu": "U→S", "bhṛtya": "U→E", "arka": "V→E", "aṃśu": "V→E",
    "preta": "V→E", "vrata": "V→E", "rājan": "V→E", "deva": "V→S", "veda": "V→S",
}
CONTROLS = {"deva", "veda"}


def best_form(wv, forms):
    best, bestc = None, -1
    for f in forms:
        if f in wv.key_to_index and wv.get_vecattr(f, "count") > bestc:
            best, bestc = f, wv.get_vecattr(f, "count")
    return best


def mean_anchor_vec(wv, anchors):
    vecs = [wv[a] for a in anchors if a in wv.key_to_index]
    return (np.mean(vecs, axis=0) if vecs else None), len(vecs)


def cos(a, b):
    if a is None or b is None:
        return None
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))


def era_present(wv, forms):
    return best_form(wv, forms) is not None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models_dir", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    wvs = {e: load_wv(args.models_dir, e) for e in PERIODS}

    rows, testable_dirs = [], []
    for word, (start_i, end_i) in ((w, TRANS[TRANSITION[w]]) for w in TARGET):
        old_anc, new_anc = ANCHORS[word]
        # choose start/end eras: documented transition, falling back to first/last era present
        present = [e for e in PERIODS if era_present(wvs[e], TARGET[word])]
        if not present:
            rows.append((word, "—", None, None, None, "target OOV all eras")); continue
        start = start_i if era_present(wvs[start_i], TARGET[word]) else present[0]
        end = end_i if era_present(wvs[end_i], TARGET[word]) else present[-1]
        if start == end:
            rows.append((word, f"{start}→{end}", None, None, None, "single era only")); continue

        def co(era):
            wv = wvs[era]
            t = wv[best_form(wv, TARGET[word])]
            ov, no = mean_anchor_vec(wv, old_anc)
            nv, nn = mean_anchor_vec(wv, new_anc)
            return cos(t, ov), cos(t, nv), no, nn

        co_s, cn_s, no_s, nn_s = co(start)
        co_e, cn_e, no_e, nn_e = co(end)
        two = bool(old_anc)
        if cn_s is None or cn_e is None:
            rows.append((word, f"{start[:3]}→{end[:3]}", None, None, None,
                         f"new-anchors OOV (n={nn_s},{nn_e})")); continue
        if two and (co_s is not None and co_e is not None):
            delta = (cn_e - co_e) - (cn_s - co_s)
            detail = f"old {co_s:+.2f}→{co_e:+.2f} | new {cn_s:+.2f}→{cn_e:+.2f}"
        else:
            delta = cn_e - cn_s
            detail = f"new {cn_s:+.2f}→{cn_e:+.2f} (new-only)"
        direction = "✓ toward new" if delta > 0 else "✗ away"
        rows.append((word, f"{start[:3]}→{end[:3]}", round(delta, 3), direction, detail,
                     f"anc old={len(old_anc)} new={len(new_anc)}"))
        if word not in CONTROLS:
            testable_dirs.append(delta > 0)

    k = sum(testable_dirs); n = len(testable_dirs)
    p = binomtest(k, n, 0.5, alternative="greater").pvalue if n else float("nan")

    out = ["# Directional anchor-displacement test (Hamilton 2016, Table 2/3 style)\n",
           "For each documented shift we measure whether the target moves TOWARD new-sense "
           "anchors / AWAY from old-sense anchors across the documented era-transition. "
           "Anchors are sense words from the glosses, chosen a priori (not from neighbor lists).\n",
           f"**Headline: {k} of {n} documented shifts move in the attested direction "
           f"(binomial sign test, H0=0.5, one-sided p = {p:.5f}).**\n",
           "| word | transition | Δ | direction | detail |",
           "|---|---|---|---|---|"]
    for word, tr, delta, direction, detail, note in rows:
        d = f"{delta:+.3f}" if isinstance(delta, float) else "—"
        flag = " *(control)*" if word in CONTROLS else ""
        out.append(f"| {word}{flag} | {tr} | {d} | {direction or note} | {detail or note} |")
    out.append("\n*Controls (deva, veda) are excluded from the sign test; they should NOT move "
               "toward the demon/late-corpus anchors.*")
    Path(args.out).write_text("\n".join(out), encoding="utf-8")
    print(f"Headline: {k}/{n} in attested direction, sign-test p={p:.5f}")
    print(f"Wrote {args.out}")
    # also echo the table to stdout
    for word, tr, delta, direction, detail, note in rows:
        d = f"{delta:+.3f}" if isinstance(delta, float) else "  — "
        print(f"  {word:11} {tr:8} {d:>7}  {(direction or note):14} {detail or ''}")


if __name__ == "__main__":
    main()
