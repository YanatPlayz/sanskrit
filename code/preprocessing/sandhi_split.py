"""
Stage 4a — sandhi splitting with ByT5-Sanskrit.

Sandhi fuses adjacent words at their boundaries (iti + uvaca -> ityuvaca), so the
surface text does not expose the word boundaries a distributional model needs. Each
line is passed to the ByT5-Sanskrit multitask model (Nehrdich et al., 2024) in
`unsandhied` mode, and the recovered word forms are written back space-separated.

Lines the model cannot parse fall back to the original whitespace tokenization rather
than being dropped, so no text is lost; the count of such lines is reported at the end.

Neural segmentation is used in preference to a rule-based segmenter because it handles
out-of-vocabulary forms and residual editorial noise more gracefully.

Runs the model over the whole corpus, so this is the slow stage of the pipeline.

Usage:
    python sandhi_split.py --input  ../../data/final/final_iast_chunked/epics_corpus.txt \
                           --output ../../data/final/final_unsandhied/epics_corpus.txt
"""
import argparse
from pathlib import Path

from dharmamitra_sanskrit_grammar import DharmamitraSanskritProcessor
from tqdm import tqdm


def split_line(processor, line: str) -> list[str]:
    """Return the sandhi-split tokens of `line`, or its plain tokens if parsing fails."""
    results = processor.process_batch([line], mode="unsandhied", human_readable_tags=False)
    tokens = [entry.get("unsandhied", "").strip()
              for entry in results[0]["grammatical_analysis"]
              if entry.get("unsandhied", "").strip()]
    return tokens or line.split()


def main():
    ap = argparse.ArgumentParser(description="Sandhi-split a corpus with ByT5-Sanskrit.")
    ap.add_argument("--input", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    processor = DharmamitraSanskritProcessor()
    n_failed = 0

    with open(args.input, encoding="utf-8") as fin, \
         open(args.output, "w", encoding="utf-8") as fout:
        for line in tqdm(fin, desc="Sandhi splitting"):
            line = line.strip()
            if not line:
                fout.write("\n")
                continue
            try:
                fout.write(" ".join(split_line(processor, line)) + "\n")
            except Exception:
                n_failed += 1
                fout.write(line + "\n")  # keep the text, unsplit
            fout.flush()

    print(f"-> {args.output}")
    if n_failed:
        print(f"   {n_failed:,} line(s) failed to parse and were kept unsplit")


if __name__ == "__main__":
    main()
