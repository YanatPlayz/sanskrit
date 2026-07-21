"""
Stage 1c — drop the GRETIL header block.

Every GRETIL plain-text file opens with a header (source URL, editorial credits,
encoding notes) terminated by a line beginning ``# text``. Everything up to and
including that line is metadata, not Sanskrit, and is removed here.

Files without a ``# text`` marker are passed through unchanged and reported, so a
missing marker is visible rather than silently dropping the whole file.

Usage:
    python strip_header.py --input-dir  ../../data/preprocessing/iast/sutras \
                           --output-dir ../../data/preprocessing/clean/sutras
"""
import argparse
from pathlib import Path

HEADER_END = "# text"


def strip_header(lines: list[str]) -> tuple[list[str], bool]:
    """Return (body, found_marker). Body is everything after the ``# text`` line."""
    for i, line in enumerate(lines):
        if line.strip().startswith(HEADER_END):
            return lines[i + 1:], True
    return lines, False


def main():
    ap = argparse.ArgumentParser(description="Strip GRETIL headers from a folder of texts.")
    ap.add_argument("--input-dir", required=True, type=Path)
    ap.add_argument("--output-dir", required=True, type=Path)
    args = ap.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    files = sorted(args.input_dir.glob("*.txt"))
    if not files:
        raise SystemExit(f"No .txt files in {args.input_dir}")

    for path in files:
        with open(path, encoding="utf-8") as f:
            body, found = strip_header(f.readlines())
        (args.output_dir / path.name).write_text("".join(body), encoding="utf-8")
        note = "" if found else "   [no '# text' marker — passed through unchanged]"
        print(f"{path.name}: {len(body)} lines{note}")

    print(f"\n{len(files)} file(s) -> {args.output_dir}")


if __name__ == "__main__":
    main()
