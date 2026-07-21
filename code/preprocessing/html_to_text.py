"""
Stage 1a — HTML to plain text.

Most GRETIL texts are downloaded as "Plain Transformation" .txt files and skip this
stage. The Mahabharata is distributed as HTML, so it is flattened to text here before
entering the rest of the pipeline.

Usage:
    python html_to_text.py --input ../../data/raw/epics/MBH1-18U.HTM \
                           --output ../../data/preprocessing/iast/epics/mahabharata.txt
"""
import argparse
import re
from pathlib import Path

from bs4 import BeautifulSoup


def html_to_text(html: str) -> str:
    text = BeautifulSoup(html, "html.parser").get_text(separator="\n")
    return re.sub(r"[\r\n]+", "\n", text).strip()


def main():
    ap = argparse.ArgumentParser(description="Flatten a GRETIL HTML edition to plain text.")
    ap.add_argument("--input", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    text = html_to_text(args.input.read_text(encoding="utf-8"))
    args.output.write_text(text, encoding="utf-8")
    print(f"{args.input.name} -> {args.output}  ({len(text.split()):,} tokens)")


if __name__ == "__main__":
    main()
