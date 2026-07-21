"""
Stage 3 — split long lines into chunks that fit the neural analyzer's context window.

ByT5-Sanskrit operates on byte sequences with a bounded context, so lines longer than
the limit must be broken up before segmentation. Splits are made at whitespace, never
mid-word, so no token is cut in half; a line with no whitespace before the limit (a
single very long compound) is cut at the limit as a last resort.

Usage:
    python chunk.py --input  ../../data/final/final_iast/sutras_corpus.txt \
                    --output ../../data/final/final_iast_chunked/sutras_corpus.txt
"""
import argparse
from pathlib import Path

MAX_CHARS = 350


def chunk_text(text: str, max_chars: int = MAX_CHARS) -> list[str]:
    """Break `text` into <= max_chars pieces, splitting at whitespace where possible."""
    chunks = []
    text = text.strip()
    while len(text) > max_chars:
        split_at = text.rfind(" ", 0, max_chars)
        if split_at == -1:
            split_at = max_chars  # unbroken run longer than the limit
        chunks.append(text[:split_at].strip())
        text = text[split_at:].strip()
    if text:
        chunks.append(text)
    return chunks


def main():
    ap = argparse.ArgumentParser(description="Chunk a corpus to fit the analyzer context window.")
    ap.add_argument("--input", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    ap.add_argument("--max-chars", type=int, default=MAX_CHARS)
    args = ap.parse_args()

    with open(args.input, encoding="utf-8") as f:
        all_chunks = [c for line in f for c in chunk_text(line, args.max_chars)]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(all_chunks) + "\n", encoding="utf-8")
    print(f"{args.input.name}: {len(all_chunks):,} chunks (max {args.max_chars} chars) "
          f"-> {args.output}")


if __name__ == "__main__":
    main()
