"""
case_go_pada.py — focused neighbor tables for the two "instructive miss" case studies,
go and pAda. Same per-era neighbor table as recovery_eval.py (era, n, top neighbors in
IAST (SLP1)), but WITHOUT the drift-score line and WITH each neighbor's cosine score.

Usage:
  python case_go_pada.py --models_dir ../models/w2v-sandhi --out ../results/case_go_pada.md
"""
import argparse
from pathlib import Path

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

from drift import load_wv, PERIODS

ERA_LABEL = {"vedic": "Vedic", "upanisadic": "Upaniṣadic", "epics": "Epic", "sutras": "Sūtra"}


def iast(slp1):
    return transliterate(slp1, sanscript.SLP1, sanscript.IAST)


CASES = [
    dict(iast="go", forms=["go", "gAm", "gAvaH", "gavi", "gavAm", "gObiH"],
         shift="'cow' → metaph. 'earth; rays of light; the senses/eyes; stars; speech'",
         type="widening / metaphor", transition="V→E", pp="72–74, 190–91, 198, 392"),
    dict(iast="pāda", forms=["pAda", "pAdaH", "pAdam", "pAdEH", "pAdayoH"],
         shift="'foot' → 'quarter (¼); a foot/line of verse; foot of a mountain; ray'",
         type="widening / metaphor", transition="V→E", pp="255–259"),
]


def best_form(wv, forms):
    best, bestc = None, 0
    for f in forms:
        if f in wv.key_to_index:
            c = wv.get_vecattr(f, "count")
            if c > bestc:
                best, bestc = f, c
    return best, bestc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models_dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--topk", type=int, default=15)
    args = ap.parse_args()

    wvs = {e: load_wv(args.models_dir, e) for e in PERIODS}
    out = ["# Case studies — go and pāda (neighbors + cosine scores)\n",
           f"Model: `{args.models_dir}` · neighbors: top-{args.topk} (full vocab) · "
           "each entry is IAST (SLP1, cosine).\n", "---\n"]

    for e in CASES:
        out.append(f"## {e['iast']}  (Kamboja pp. {e['pp']})")
        out.append(f"- **Documented shift:** {e['shift']}")
        out.append(f"- **Type:** {e['type']}  ·  **expected transition:** {e['transition']}\n")
        out.append("| Era | n | Top neighbors — IAST (SLP1, cosine) |")
        out.append("|-----|---|--------------------------------------|")
        for era in PERIODS:
            wv = wvs[era]
            form, n = best_form(wv, e["forms"])
            if form is None:
                cell = "_absent / not in vocab_"
            else:
                cell = ", ".join(f"{iast(t)} ({t}, {s:.2f})"
                                 for t, s in wv.most_similar(form, topn=args.topk))
            probe = f" _[{iast(form)}]_" if form else ""
            out.append(f"| {ERA_LABEL[era]}{probe} | {n} | {cell} |")
        out.append("\n---\n")

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote {args.out}")
    print("\n".join(out))


if __name__ == "__main__":
    main()
