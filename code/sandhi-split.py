from sanskrit_parser import Parser
import logging

logging.getLogger("sanskrit_parser").setLevel(logging.WARNING)

# path to your cleaned SLP1 file
file_path = "../data/final/epics/sa_rAmAyaNa.txt"

# read the text
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# simple whitespace tokenization
tokens = text.split()
chunk = tokens[:4]  # take first 5 tokens"
chunk_text = " ".join(chunk)


print("ORIGINAL CHUNK:")
print(chunk_text)
print()

parser = Parser(input_encoding="slp1", output_encoding="slp1", replace_ending_visarga='s', lexical_lookup="combined", score=True)

for token in chunk: # test first 20 tokens
    splits = parser.split(token, limit=5)
    if splits:
        print(f"Token: {token}")
        for split in splits:
            print("Lexical Split:", split)
    else:
        print(f"No splits found for: {token}")
    print("-------")