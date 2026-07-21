"""
Stage 5 — lemmatization via a cached surface-form to lemma lookup table.

Sanskrit inflection scatters one lexeme across dozens of surface forms, each of which
gets its own embedding and its own (much reduced) frequency. Lemmatizing collapses them
back together. This produces the `lemma` corpus variant; the paper reports that it did
not improve on the sandhi-split variant, since the lookup can conflate forms that carry
distinct senses.

Running the model over every token occurrence would be prohibitively slow, so lemmas
are resolved once per *distinct* surface form and cached in a JSON lookup table. Reruns
load the table and only query forms not already in it, which makes adding a new text
cheap. Tokens absent from the table pass through unchanged.

Distinct forms are batched into one request joined by the separator `iti`, which the
model reliably treats as a token boundary; the response is regrouped on that separator.
If a batch comes back misaligned (the group count does not match the batch size) the
whole batch is re-queried one form at a time rather than trusting a shifted alignment.

Usage:
    python lemmatize.py --input   ../../data/final/final_unsandhied_refined/epics_corpus.txt \
                        --output  ../../data/final/final_lemma/epics_corpus.txt \
                        --lookup  ../../data/sanskrit_lemmas.json
"""
import argparse
import json
from pathlib import Path

from dharmamitra_sanskrit_grammar import DharmamitraSanskritProcessor

SEPARATOR = "iti"
BATCH_SIZE = 10

# Very high-frequency indeclinables the lemmatizer sometimes resolves to an inflected
# verb or a homograph. They are invariant, so they are pinned to themselves.
PINNED = {"na": "na", "mā": "mā", "ca": "ca", "iva": "iva"}


def lemma_of(processor, form: str) -> str:
    """Resolve one surface form on its own; fall back to the form itself."""
    res = processor.process_batch([form], mode="lemma", human_readable_tags=False)
    if res and res[0].get("grammatical_analysis"):
        return res[0]["grammatical_analysis"][0].get("lemma", form).strip().replace("-", "")
    return form


def resolve_batch(processor, batch: list[str]) -> list[str] | None:
    """Resolve a batch in one request; return None if the response does not align."""
    joined = f" {SEPARATOR} ".join(batch)
    res = processor.process_batch([joined], mode="lemma", human_readable_tags=False)
    if not res or "grammatical_analysis" not in res[0]:
        return None

    grouped, current = [], []
    for item in res[0]["grammatical_analysis"]:
        lemma = item.get("lemma", "").strip().replace("-", "")
        if lemma == SEPARATOR:
            if current:
                grouped.append(current[0])
                current = []
        elif lemma:
            current.append(lemma)
    if current:
        grouped.append(current[0])

    return grouped if len(grouped) == len(batch) else None


def build_lookup(processor, forms: list[str], lookup: dict, batch_size: int) -> None:
    """Populate `lookup` in place for every form not already present."""
    n_batches = -(-len(forms) // batch_size)
    for i in range(0, len(forms), batch_size):
        batch = forms[i:i + batch_size]
        print(f"  batch {i // batch_size + 1}/{n_batches} ({batch[0]} ...)")
        try:
            grouped = resolve_batch(processor, batch)
            if grouped is None:  # misaligned response — resolve individually
                grouped = [lemma_of(processor, form) for form in batch]
            for form, lemma in zip(batch, grouped):
                lookup[form] = PINNED.get(form, lemma)
        except Exception as exc:
            print(f"  request failed ({exc}); leaving {len(batch)} form(s) unresolved")


def main():
    ap = argparse.ArgumentParser(description="Lemmatize a corpus via a cached lookup table.")
    ap.add_argument("--input", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    ap.add_argument("--lookup", required=True, type=Path,
                    help="JSON lookup table; created if absent, extended in place otherwise")
    ap.add_argument("--batch-size", type=int, default=BATCH_SIZE)
    args = ap.parse_args()

    lookup = {}
    if args.lookup.exists():
        lookup = json.loads(args.lookup.read_text(encoding="utf-8"))
        print(f"Loaded {len(lookup):,} known lemmas from {args.lookup}")

    lines = [ln.strip() for ln in args.input.read_text(encoding="utf-8").splitlines() if ln.strip()]
    forms = sorted({tok for line in lines for tok in line.split()})
    missing = [f for f in forms if f not in lookup]
    print(f"{len(forms):,} distinct forms in {args.input.name}; {len(missing):,} not yet resolved")

    if missing:
        build_lookup(DharmamitraSanskritProcessor(), missing, lookup, args.batch_size)
        args.lookup.parent.mkdir(parents=True, exist_ok=True)
        args.lookup.write_text(json.dumps(lookup, ensure_ascii=False, indent=4), encoding="utf-8")
        print(f"Lookup table now holds {len(lookup):,} entries -> {args.lookup}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as fout:
        for line in lines:
            fout.write(" ".join(lookup.get(tok, tok) for tok in line.split()) + "\n")

    unresolved = sum(1 for f in forms if f not in lookup)
    print(f"-> {args.output}")
    if unresolved:
        print(f"   {unresolved:,} form(s) had no lemma and were left as-is")


if __name__ == "__main__":
    main()
