"""
Stage 1b — extract the mula (root) text from editions that interleave commentary.

Several GRETIL Upanisad files ship the root verses interleaved with Sankara's
commentary. Including the commentary would mix a much later stratum of Sanskrit into
the Upanisadic bin, so only the root text is kept.

Each verse is delimited by an opening marker (``start <open_prefix> <ref>``) and a
closing marker (``|| <close_prefix><ref> ||``). Everything between the two is root
text; everything else is commentary and is dropped. After extraction the output is
scanned for the commentary marker prefix, and any leaks are reported.

Usage:
    python extract_mula.py \
        --input  ../../data/preprocessing/iast/upanisadic/sa_praznopaniSad-comm.txt \
        --output ../../data/preprocessing/iast/upanisadic/sa_praznopaniSad.txt \
        --open-prefix prup --close-prefix prup_ --comm-prefix prupbh_

Prefixes for the four commented Upanisads in this corpus:
    brhup / brhup_ / brhupbh_      Brhadaranyaka (Kanva recension)
    chup  / chup_  / chupbh_       Chandogya
    aitup / aitup_ / aitupbh_      Aitareya
    prup  / prup_  / prupbh_       Prasna
"""
import argparse
import re
from pathlib import Path


def extract(text: str, open_prefix: str, close_prefix: str) -> list[str]:
    """Return the root verses lying between the opening and closing markers."""
    op, cl = re.escape(open_prefix), re.escape(close_prefix)
    # Opening marker: "start <open_prefix> <ref>";  closing: "|| <close_prefix><ref> ||".
    # Refs are digits with commas, dots, colons or hyphens, depending on the edition.
    pattern = re.compile(
        rf"start\s+{op}\s+[\d,\.\:\-]+\s*\n?([\s\S]*?)\|\|\s*{cl}[\d,\.\:\-]+\s*\|\|",
        re.IGNORECASE,
    )
    return [v.strip() for v in pattern.findall(text) if v.strip()]


def main():
    ap = argparse.ArgumentParser(description="Extract mula verses, dropping commentary.")
    ap.add_argument("--input", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    ap.add_argument("--open-prefix", required=True,
                    help="word following 'start' in opening markers, e.g. prup")
    ap.add_argument("--close-prefix", required=True,
                    help="prefix of closing markers, e.g. prup_")
    ap.add_argument("--comm-prefix", required=True,
                    help="prefix of commentary markers, used for the leak check, e.g. prupbh_")
    args = ap.parse_args()

    verses = extract(args.input.read_text(encoding="utf-8"),
                     args.open_prefix, args.close_prefix)
    if not verses:
        raise SystemExit(f"No mula verses matched in {args.input}. "
                         f"Check --open-prefix / --close-prefix against the file's markers.")

    mula = "\n\n".join(verses)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(mula, encoding="utf-8")

    leaked = [i + 1 for i, line in enumerate(mula.splitlines())
              if re.search(re.escape(args.comm_prefix), line, re.IGNORECASE)]
    print(f"{args.input.name}: extracted {len(verses)} verses, "
          f"{len(mula.split()):,} tokens -> {args.output}")
    if leaked:
        print(f"  WARNING: commentary markers survive on {len(leaked)} line(s): {leaked[:10]}")
    else:
        print("  leak check passed: no commentary markers in output")


if __name__ == "__main__":
    main()
