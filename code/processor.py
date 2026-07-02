from dharmamitra_sanskrit_grammar import DharmamitraSanskritProcessor
from pathlib import Path
from tqdm import tqdm

# Paths
input_file = Path("../data/final/final_iast_chunked/epics_corpus.txt")
output_file = Path("../data/final/final_unsandhiedtest/epics_test.txt")

# Initialize the processor
processor = DharmamitraSanskritProcessor()

# Process the file
with open(input_file, "r", encoding="utf-8") as fin, \
     open(output_file, "w", encoding="utf-8") as fout:

    for line in tqdm(fin, desc="Sandhi splitting"):
        line = line.strip()

        # Skip empty lines
        if not line:
            fout.write("\n")
            continue

        try:
            results = processor.process_batch(
                [line],
                mode="unsandhied",
                human_readable_tags=False
            )

            tokens = []
            for entry in results[0]["grammatical_analysis"]:
                token = entry.get("unsandhied", "").strip()
                if token:
                    tokens.append(token)

            # Fallback if nothing parsed
            if not tokens:
                tokens = line.split()

            fout.write(" ".join(tokens) + "\n")
            fout.flush()

        except Exception as e:
            # Robust fallback: keep original line
            fout.write(line + "\n") 
            fout.flush()