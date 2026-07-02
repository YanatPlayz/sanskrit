from dharmamitra_sanskrit_grammar import DharmamitraSanskritProcessor
from pathlib import Path
from tqdm import tqdm

INPUT_FILE = Path("../data/final/final_unsandhied/upanisadic_corpus.txt")
OUTPUT_FILE = Path("../data/final/final_unsandhied_refined/upanisadic_corpus.txt")
LENGTH_THRESHOLD = 15

processor = DharmamitraSanskritProcessor()

def split_long_token(token: str) -> list[str]:
    """
    Attempt to unsandhi-split a single long token.
    Return a list of tokens if improved, else [token].
    """
    try:
        result = processor.process_batch(
            [token],
            mode="unsandhied",
            human_readable_tags=False
        )

        splits = [
            x.get("unsandhied", "").strip()
            for x in result[0]["grammatical_analysis"]
            if x.get("unsandhied", "").strip()
        ]

        # Accept only meaningful improvements
        if len(splits) > 1 and " ".join(splits) != token:
            return splits

    except Exception:
        pass

    return [token]


with open(INPUT_FILE, "r", encoding="utf-8") as fin, \
     open(OUTPUT_FILE, "w", encoding="utf-8") as fout:

    for line in tqdm(fin, desc="Refining long compounds"):
        line = line.strip()

        if not line:
            fout.write("\n")
            continue

        tokens = line.split()
        new_tokens = []

        for tok in tokens:
            if len(tok) >= LENGTH_THRESHOLD:
                print("long word: ", tok)
                new_tokens.extend(split_long_token(tok))
            else:
                new_tokens.append(tok)

        fout.write(" ".join(new_tokens) + "\n")