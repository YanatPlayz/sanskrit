import re

configs = [
    #{
    #    "input":          "../data/preprocessing/iast/upanisadic/sa_bRhadAraNyakopaniSadkANva-recension-comm.txt",
    #    "output":         "../data/preprocessing/iast/upanisadic/sa_bRhadAraNyakopaniSadkANva.txt",
    #    "open_prefix":    "brhup",    # word after "start" in opening markers
    #    "close_prefix":   "brhup_",   # prefix of closing markers
    #    "comm_prefix":    "brhupbh_", # prefix of commentary markers (for leak check)
    #},
    #{
    #    "input":          "../data/preprocessing/iast/upanisadic/sa_chAndogyopaniSad-comm.txt",
    #    "output":         "../data/preprocessing/iast/upanisadic/sa_chAndogyopaniSad.txt",
    #    "open_prefix":    "chup",
    #    "close_prefix":   "chup_",
    #    "comm_prefix":    "chupbh_",
    #},
    #{
    #    "input":          "../data/preprocessing/iast/upanisadic/sa_aitareyopaniSad-comm.txt",
    #    "output":         "../data/preprocessing/iast/upanisadic/sa_aitareyopaniSad.txt",
    #    "open_prefix":    "aitup",
    #    "close_prefix":   "aitup_",
    #    "comm_prefix":    "aitupbh_",
    #},
    {
        "input":          "../data/preprocessing/iast/upanisadic/sa_praznopaniSad-comm.txt",
        "output":         "../data/preprocessing/iast/upanisadic/sa_praznopaniSad.txt",
        "open_prefix":    "prup",
        "close_prefix":   "prup_",
        "comm_prefix":    "prupbh_",
    }
]

# =============================================================================
# EXTRACTION — no need to edit below this line
# =============================================================================

def extract_mula(cfg: dict):
    input_path  = cfg["input"]
    output_path = cfg["output"]
    op          = re.escape(cfg["open_prefix"])
    cl          = re.escape(cfg["close_prefix"])
    comm        = re.escape(cfg["comm_prefix"])

    print(f"\n{'='*60}")
    print(f"Processing: {input_path}")

    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Opening marker:  "start <open_prefix> <ref>"
    # Closing marker:  "|| <close_prefix><ref> ||"
    # Ref format:      digits, commas, dots, colons, hyphens (all variants)
    pattern = re.compile(
        rf'start\s+{op}\s+[\d,\.\:\-]+\s*\n?([\s\S]*?)\|\|\s*{cl}[\d,\.\:\-]+\s*\|\|',
        re.IGNORECASE
    )

    matches = pattern.findall(text)

    if not matches:
        print("WARNING: No mula verses found. Check open_prefix / close_prefix in config.")
        return

    verses = [v.strip() for v in matches if v.strip()]
    mula_text = "\n\n".join(verses)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(mula_text)

    print(f"Extracted {len(verses)} mula verses.")
    print(f"Output:    {output_path}")

    # Leak check
    leaked = [(i+1, line) for i, line in enumerate(mula_text.splitlines())
              if re.search(comm, line, re.IGNORECASE)]
    if leaked:
        print(f"WARNING: {len(leaked)} line(s) contain commentary markers:")
        for lineno, line in leaked[:10]:
            print(f"  Line {lineno}: {line[:120]}")
    else:
        print("Check passed: no commentary markers in output.")

    print(f"--- FIRST VERSE ---\n{verses[0][:200]}")
    print(f"--- LAST VERSE  ---\n{verses[-1][:200]}")
    print(f"Estimated tokens:   {len(mula_text.split()):,}")


if __name__ == "__main__":
    for cfg in configs:
        extract_mula(cfg)