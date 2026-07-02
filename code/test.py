import json
import random
import os

# Paths
UNSANDHIED_IN = "../data/final/final_unsandhied_refined/sutras_corpus.txt"
DICTIONARY_JSON = "../data/sanskrit_lemmas.json"
CHUNK_SIZE = 10

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
all_tokens = list(" ".join(unsandhied_lines).split())
unique_tokens = [t for t in all_tokens if t not in lookup_table]

random.shuffle(unique_tokens)
print(f"All tokens: {len(all_tokens)} | New Tokens to Process: {len(unique_tokens)} | Press 'ESC' to stop.")