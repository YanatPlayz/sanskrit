from pathlib import Path
import re

input_folder = Path("../data/pramana")
output_folder = Path("../data/pramanas")
output_folder.mkdir(exist_ok=True)

REFERENCE_PATTERNS = [
    r"\(.*?\)|\<.*?\>|\[.*?\]|\{.*?\}",                      # <1.1.1>
    #r"[A-Za-z]+\d[\d\.,]*[a-z]*\.",                          # kaj001.1.04a.
    #r"[A-Za-z\-]+_\d[\d\.,]*[A-Za-z]?[:]*",                  # apgs-anA_1.6
    #r"\d+[\d\.,]*(?:[*]\d+)?[_\d]*[a-z]?\s?",               # 01,000.000*0017_02
    #r"\d+[\d\.,:]*[\d\.,]*[:]*",                             # 1.1.1:
    #r"\.\.\s*[A-Za-z]+_\d[\d\.,]*",                         # .. manu_1.10
    #r"^\s*start\s+[A-Za-z]+\s+[\d\.,]+\s*",
]

REFERENCE_REGEX = re.compile("|".join(REFERENCE_PATTERNS))
DOT_REGEX = re.compile(r'\.')
METADATA_CHARS = ['*', '@', '=', '\'','\"', '-']

for input_file in input_folder.glob("*.txt"):
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()
    
    text = REFERENCE_REGEX.sub(" ", text)

    for char in METADATA_CHARS:
        text = text.replace(char, ' ')

    text = DOT_REGEX.sub(" ", text)

    lines = text.splitlines()
    cleaned_lines = [line.strip() for line in lines if line.strip()]
    final_text = "\n".join(cleaned_lines)

    output_file = output_folder / input_file.name #same file name
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_text)