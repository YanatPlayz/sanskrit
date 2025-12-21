from sanskrit_parser.parser.sandhi_analyzer import LexicalSandhiAnalyzer
from sanskrit_parser.base.sanskrit_base import SanskritObject
from pathlib import Path

analyzer = LexicalSandhiAnalyzer()

def normalize_token(token_slp1: str):
    """
    Given a Sanskrit token (SLP1), perform Sandhi splitting into valid words

    Returns best split
    """
    # Wrap input as SanskritObject
    obj = SanskritObject(token_slp1)

    # --- 1. SANDHI SPLITTING ---
    g = analyzer.getSandhiSplits(obj)
    if (g == None):
        return [token_slp1]
    paths = g.find_all_paths(1)   # top split

    if not paths:
        return [token_slp1]
    
    return paths[0]


# Setup paths
input_base = Path("../data/final/sutras")
output_base = Path("../data/lexical/sutras")
output_base.mkdir(parents=True, exist_ok=True)

def process_file(input_file):
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()
    
    tokens = text.split()
    processed_tokens = []
    
    # Process all tokens
    for i in range(0, len(tokens), 5):
        t = " ".join(tokens[i:i+5])
        splits = normalize_token(t)
        # splits is a list of objects. Convert to string.
        split_strings = [str(s) for s in splits]
        processed_tokens.extend(split_strings)
        print(split_strings)
        
    final_text = " ".join(processed_tokens)
    
    
    output_file = output_base / input_file.name
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_text)
    print(f"Processed {input_file.name}")

# Iterate files
if __name__ == "__main__":
    for input_file in input_base.glob("*.txt"):
        process_file(input_file)
