from pathlib import Path
# Paths
input_file = Path("../data/final/final_iast/sutras_corpus.txt")
output_file = Path("../data/final/final_iast_chunked/sutras_corpus.txt")

def chunk_text(text, max_chars=350):
    chunks = []
    text = text.strip()

    while len(text) > max_chars:
        # find last whitespace before limit
        split_at = text.rfind(" ", 0, max_chars)
        if split_at == -1:
            split_at = max_chars  # emergency fallback

        chunks.append(text[:split_at].strip())
        text = text[split_at:].strip()

    if text:
        chunks.append(text)

    return chunks

all_chunks = []
for line in open(input_file, "r", encoding="utf-8"):
    all_chunks.extend(chunk_text(line))

with open(output_file, "w", encoding="utf-8") as fout:
    fout.write("\n".join(all_chunks) + "\n")