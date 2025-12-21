from pathlib import Path

input_folder = Path("../data/slp1/sutras")
output_folder = Path("../data/clean/sutras")
output_folder.mkdir(exist_ok=True)

for input_file in input_folder.glob("*.txt"):
    output_file = output_folder / input_file.name #same file name

    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    start_i = 0
    for i, line in enumerate(lines):
        if line.strip().startswith("# text"):
            start_i = i + 1
            break
    
    cleaned_lines = lines[start_i:]

    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(cleaned_lines)