from dharmamitra_sanskrit_grammar import DharmamitraSanskritProcessor
from pathlib import Path
from tqdm import tqdm

# Paths
input_file = Path("../data/final/final_unsandhied_refined/epics_corpus2.txt")
output_file = Path("../data/final/final_lemma_test/epics_test2.txt")

# Initialize the processor
processor = DharmamitraSanskritProcessor()

# Process the file
with open(input_file, "r", encoding="utf-8") as fin, \
     open(output_file, "w", encoding="utf-8") as fout:

    for line in tqdm(fin, desc="Lemmatizing"):
        line = line.strip()

        # Skip empty lines
        if not line:
            fout.write("\n")
            continue

        try:
            print(f"Processing line: {line}")
            results = processor.process_batch(
                [line],
                mode="unsandhied-lemma-morphosyntax",
                human_readable_tags=False
            )

            lemmas = []
            for entry in results[0]["grammatical_analysis"]:
                lemma = entry.get("lemma", "").strip()
                lemma = lemma.replace("-", "")
                if lemma:
                    lemmas.append(lemma)

            # Fallback if nothing parsed
            if not lemmas:
                lemmas = line.split()

            fout.write(" ".join(lemmas) + "\n")
            fout.flush()

        except Exception as e:
            # Robust fallback: keep original line
            fout.write(line + "\n") 
            fout.flush()