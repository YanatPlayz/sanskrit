"""
Stage 2 — concatenate the cleaned texts of one period into a single corpus file.

Each period's individual works are merged into ``<period>_corpus.txt``, one non-empty
line per line of source text. This is the unit everything downstream operates on: the
four period corpora are the four bins of the diachronic study.

Periods: vedic, upanisadic, epics, sutras.

Usage:
    python build_corpus.py --input-dir ../../data/preprocessing/clean/sutras \
                           --output    ../../data/final/final_iast/sutras_corpus.txt
"""
import argparse
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description="Merge one period's texts into a corpus file.")
    ap.add_argument("--input-dir", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()

    files = sorted(args.input_dir.glob("*.txt"))
    if not files:
        raise SystemExit(f"No .txt files in {args.input_dir}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    n_lines = 0
    with open(args.output, "w", encoding="utf-8") as fout:
        for path in files:
            with open(path, encoding="utf-8") as fin:
                for line in fin:
                    line = line.strip()
                    if line:
                        fout.write(line + "\n")
                        n_lines += 1
            print(f"  + {path.name}")

    tokens = len(args.output.read_text(encoding="utf-8").split())
    print(f"\n{len(files)} file(s), {n_lines:,} lines, {tokens:,} tokens -> {args.output}")


if __name__ == "__main__":
    main()
