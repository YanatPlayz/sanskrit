from pathlib import Path

base_dir = Path("../data/final")
out_dir = Path("../data/corpus")
out_dir.mkdir(parents=True, exist_ok=True)
periods = ["sutras"]

for period in periods:
    out_file = out_dir / f"{period}_corpus.txt"
    with open(out_file, "w", encoding="utf-8") as fout:
        for txt_file in (base_dir / period).glob("*.txt"):
            with open(txt_file, "r", encoding="utf-8") as fin:
                for line in fin:
                    line = line.strip()
                    if line:
                        fout.write(line + "\n")