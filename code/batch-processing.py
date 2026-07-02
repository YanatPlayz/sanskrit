from dharmamitra_sanskrit_grammar import DharmamitraSanskritProcessor
from pathlib import Path
from tqdm import tqdm

# Paths
input_file = Path("../data/final/final_iast_chunked/epics_corpus.txt")
output_file = Path("../data/final/final_lemma_test/epics_test2.txt")
output_file.parent.mkdir(parents=True, exist_ok=True)

processor = DharmamitraSanskritProcessor()

BATCH_SIZE = 3
lines_buffer = []

def process_buffer(buffer, file_out):
    if not buffer:
        return
        
    # Process the entire buffer as a batch
    results = processor.process_batch(
        buffer,
        mode="unsandhied-lemma-morphosyntax",
        human_readable_tags=False
    )

    for r, original in zip(results, buffer):
        # Check if the line was originally empty
        if not original.strip():
            file_out.write("\n")
            continue
            
        tokens = [
            e.get("lemma", "").strip().replace("-", "")
            for e in r.get("grammatical_analysis", [])
            if e.get("lemma")
        ]
        
        # Fallback to original if no lemmas found
        file_out.write(" ".join(tokens) if tokens else original.strip())
        file_out.write("\n")

with open(input_file, "r", encoding="utf-8") as fin, \
     open(output_file, "w", encoding="utf-8") as fout:

    for line in tqdm(fin, desc="Lemmatizing"):
        # We keep the line even if it's empty to keep the batch synced
        lines_buffer.append(line.strip())

        if len(lines_buffer) == BATCH_SIZE:
            process_buffer(lines_buffer, fout)
            lines_buffer.clear()

    # Final leftovers
    if lines_buffer:
        process_buffer(lines_buffer, fout)