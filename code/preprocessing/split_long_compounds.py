"""
Stage 4b — second segmentation pass over residual long compounds.

The first pass (sandhi_split.py) works line by line and leaves some long compounds
intact. Because compounding can merge many words into a single very long token, these
residuals are rare surface forms that carry almost no distributional signal. This pass
re-submits every token at or above a length threshold to the segmenter on its own,
where the model has an easier target.

A split is accepted only if it actually breaks the token into more than one piece;
otherwise the original token is kept unchanged. Tokens that fail to parse are also
kept as-is, so this pass can only ever add boundaries, never lose text.

Usage:
    python split_long_compounds.py \
        --input  ../../data/final/final_unsandhied/upanisadic_corpus.txt \
        --output ../../data/final/final_unsandhied_refined/upanisadic_corpus.txt
"""
import argparse
from pathlib import Path

from dharmamitra_sanskrit_grammar import DharmamitraSanskritProcessor
from tqdm import tqdm

LENGTH_THRESHOLD = 15


def split_long_token(processor, token: str) -> list[str]:
    """Segment a single long token; return [token] unchanged if that fails or gains nothing."""
    try:
        result = processor.process_batch([token], mode="unsandhied", human_readable_tags=False)
        splits = [x.get("unsandhied", "").strip()
                  for x in result[0]["grammatical_analysis"]
                  if x.get("unsandhied", "").strip()]
        if len(splits) > 1 and " ".join(splits) != token:
            return splits
    except Exception:
        pass
    return [token]


def main():
    ap = argparse.ArgumentParser(description="Second segmentation pass over long compounds.")
    ap.add_argument("--input", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    ap.add_argument("--threshold", type=int, default=LENGTH_THRESHOLD,
                    help=f"minimum token length to re-segment (default {LENGTH_THRESHOLD})")
    args = ap.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    processor = DharmamitraSanskritProcessor()
    n_seen = n_split = 0

    with open(args.input, encoding="utf-8") as fin, \
         open(args.output, "w", encoding="utf-8") as fout:
        for line in tqdm(fin, desc="Refining long compounds"):
            line = line.strip()
            if not line:
                fout.write("\n")
                continue
            new_tokens = []
            for tok in line.split():
                if len(tok) >= args.threshold:
                    n_seen += 1
                    pieces = split_long_token(processor, tok)
                    n_split += len(pieces) > 1
                    new_tokens.extend(pieces)
                else:
                    new_tokens.append(tok)
            fout.write(" ".join(new_tokens) + "\n")

    print(f"-> {args.output}")
    print(f"   {n_split:,} of {n_seen:,} long tokens (>= {args.threshold} chars) were split")


if __name__ == "__main__":
    main()
