from pathlib import Path
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
import unicodedata

input_folder = Path("../data/iast/epics") #run once for each folder
output_folder = Path("../data/slp1/epics")
output_folder.mkdir(exist_ok=True)

for input_file in input_folder.glob("*.txt"):
    output_file = output_folder / input_file.name #same file name

    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()

    slp1_text = unicodedata.normalize("NFC", text)
    slp1_text = transliterate(slp1_text, sanscript.IAST, sanscript.SLP1) #transliterate iast to slp1
    slp1_text = unicodedata.normalize("NFC", slp1_text)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(slp1_text)