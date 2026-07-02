import json
import sys
import time
import random
import os
from dharmamitra_sanskrit_grammar import DharmamitraSanskritProcessor

# Paths
UNSANDHIED_IN = "../data/final/final_unsandhied_refined/epics_corpus.txt"
SIMULATED_OUT = "../data/final/final_lemma/epics_corpus.txt"
DICTIONARY_JSON = "../data/sanskrit_lemmas.json"
CHUNK_SIZE = 10 

HOTFIXES = {
    "na": "na",
    "mā": "mā",
    "ca": "ca",
    "iva": "iva"
}

if os.path.exists(DICTIONARY_JSON):
    with open(DICTIONARY_JSON, "r", encoding="utf-8") as f:
        lookup_table = json.load(f)
    print(f"Loaded {len(lookup_table)} existing lemmas from {DICTIONARY_JSON}")
else:
    lookup_table = {}
    print("No existing dictionary found. Starting fresh.")

# 1. Load and Shuffle
with open(UNSANDHIED_IN, "r", encoding="utf-8") as f:
    unsandhied_lines = [line.strip() for line in f if line.strip()]

# Only process tokens that we don't have in the dictionary
all_tokens = set(" ".join(unsandhied_lines).split())
unique_tokens = [t for t in all_tokens if t not in lookup_table]

random.shuffle(unique_tokens)
print(f"New Tokens to Process: {len(unique_tokens)} | Press 'ESC' to stop.")

processor = DharmamitraSanskritProcessor()

def build_dictionary():
    if not unique_tokens:
        print("All tokens already known. Skipping API calls.")
        return

    for i in range(0, len(unique_tokens), CHUNK_SIZE):
        chunk = unique_tokens[i : i + CHUNK_SIZE]
        test_string = " iti ".join(chunk)
        
        print(f"\nBatch {i//CHUNK_SIZE + 1} | Sample: {chunk[0]}...")
        
        try:
            results = processor.process_batch([test_string], mode="lemma", human_readable_tags=False)
            
            if results and "grammatical_analysis" in results[0]:
                analysis = results[0]["grammatical_analysis"]
                api_lemmas = [item.get("lemma", "").strip().replace("-", "") for item in analysis]
                
                grouped = []
                current = []
                for l in api_lemmas:
                    if l == "iti":
                        if current: 
                            grouped.append(current[0])
                            current = []
                    else:
                        if l: current.append(l)
                if current: grouped.append(current[0])

                if len(grouped) == len(chunk):
                    for word, lemma in zip(chunk, grouped):
                        # Apply HOTFIX check here
                        lookup_table[word] = HOTFIXES.get(word, lemma)
                        print(f"  {word:<18} -> {lookup_table[word]:<18} ✅")
                else:
                    # Fallback
                    for word in chunk:
                        res = processor.process_batch([word], mode="lemma")
                        if res and res[0]["grammatical_analysis"]:
                            l = res[0]["grammatical_analysis"][0].get("lemma", word).strip().replace("-", "")
                        else:
                            l = word
                        lookup_table[word] = HOTFIXES.get(word, l)
                        print(f"    [FB] {word:<15} -> {lookup_table[word]:<15}")
            
        except Exception as e:
            print(f"  🟥 API Error: {e}")
            time.sleep(1)

# Execute API Fetching
build_dictionary()

# 3. Save the Dictionary to JSON for future use
print(f"\nSaving updated dictionary to {DICTIONARY_JSON}...")
with open(DICTIONARY_JSON, "w", encoding="utf-8") as f:
    json.dump(lookup_table, f, ensure_ascii=False, indent=4)

# 4. Final Replacement
print(f"Applying lookup to full corpus...")
with open(SIMULATED_OUT, "w", encoding="utf-8") as fout:
    for line in unsandhied_lines:
        words = line.split()
        fout.write(" ".join([lookup_table.get(w, w) for w in words]) + "\n")

print("Success.")