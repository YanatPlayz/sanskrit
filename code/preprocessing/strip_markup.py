"""
Stage 1d — strip editorial markup, verse references, and digital detritus.

After the header is gone the text still carries apparatus that is not Sanskrit: verse
and chapter references, bracketed editorial insertions, and punctuation used as
structural markup. All of it is replaced with whitespace (not deleted) so that words
on either side are never accidentally fused into one token.

Reference formats vary by GRETIL edition. Bracketed references are always removed;
the other styles below occur in some editions only and are opted into with
``--extra-patterns``, since applying them indiscriminately deletes real text:

    [A-Za-z]+\\d[\\d\\.,]*[a-z]*\\.          kaj001.1.04a.
    [A-Za-z\\-]+_\\d[\\d\\.,]*[A-Za-z]?[:]*  apgs-anA_1.6
    \\d+[\\d\\.,]*(?:[*]\\d+)?[_\\d]*[a-z]?  01,000.000*0017_02
    \\.\\.\\s*[A-Za-z]+_\\d[\\d\\.,]*        .. manu_1.10

The output of this stage is what the corpus was built from; inspect a sample before
and after when adding a new text, since an over-broad pattern silently deletes verses.

Usage:
    python strip_markup.py --input-dir  ../../data/preprocessing/clean/sutras \
                           --output-dir ../../data/preprocessing/clean/sutras-stripped
"""
import argparse
import re
from pathlib import Path

# Bracketed references and editorial insertions: <1.1.1>, (…), […], {…}
BRACKET_PATTERN = r"\(.*?\)|\<.*?\>|\[.*?\]|\{.*?\}"

# Characters used purely as markup in GRETIL editions.
METADATA_CHARS = ["*", "@", "=", "'", '"', "-"]


def clean(text: str, extra_patterns: list[str]) -> str:
    reference_regex = re.compile("|".join([BRACKET_PATTERN, *extra_patterns]))
    text = reference_regex.sub(" ", text)
    for char in METADATA_CHARS:
        text = text.replace(char, " ")
    text = text.replace(".", " ")  # danda and verse-number dots
    return "\n".join(line.strip() for line in text.splitlines() if line.strip())


def main():
    ap = argparse.ArgumentParser(description="Strip editorial markup and verse references.")
    ap.add_argument("--input-dir", required=True, type=Path)
    ap.add_argument("--output-dir", required=True, type=Path)
    ap.add_argument("--extra-patterns", nargs="*", default=[],
                    help="additional reference regexes for this edition (see module docstring)")
    args = ap.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    files = sorted(args.input_dir.glob("*.txt"))
    if not files:
        raise SystemExit(f"No .txt files in {args.input_dir}")

    for path in files:
        before = path.read_text(encoding="utf-8")
        after = clean(before, args.extra_patterns)
        (args.output_dir / path.name).write_text(after, encoding="utf-8")
        print(f"{path.name}: {len(before.split()):,} -> {len(after.split()):,} tokens")

    print(f"\n{len(files)} file(s) -> {args.output_dir}")


if __name__ == "__main__":
    main()
