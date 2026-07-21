"""
Stage 6 — transliterate IAST to SLP1.

Everything upstream works in IAST, which is what GRETIL ships and what ByT5-Sanskrit
expects. The embedding models instead consume SLP1, a reversible ASCII encoding in
which every Sanskrit phoneme is exactly one character. That one-character-per-phoneme
property matters for FastText, whose character n-grams would otherwise be computed over
multi-byte diacritics rather than over phonemes.

Unicode is normalized to NFC on both sides of the conversion, so precomposed and
combining-diacritic spellings of the same IAST character map to the same SLP1 output.

Run once per corpus variant that will be trained on:
    final_iast              -> final_slp1/corpus     (raw)
    final_unsandhied_refined -> unsandhied           (sandhi-split; the released corpus)
    final_lemma             -> lemma                 (lemmatized)

Usage:
    python transliterate.py --input-dir  ../../data/final/final_unsandhied_refined \
                            --output-dir ../../data/final/unsandhied
"""
import argparse
import unicodedata
from pathlib import Path

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate


def iast_to_slp1(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    text = transliterate(text, sanscript.IAST, sanscript.SLP1)
    return unicodedata.normalize("NFC", text)


def main():
    ap = argparse.ArgumentParser(description="Transliterate a folder of IAST texts to SLP1.")
    ap.add_argument("--input-dir", required=True, type=Path)
    ap.add_argument("--output-dir", required=True, type=Path)
    args = ap.parse_args()

    files = sorted(args.input_dir.glob("*.txt"))
    if not files:
        raise SystemExit(f"No .txt files in {args.input_dir}")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for path in files:
        out = args.output_dir / path.name
        out.write_text(iast_to_slp1(path.read_text(encoding="utf-8")), encoding="utf-8")
        print(f"{path.name} -> {out}")

    print(f"\n{len(files)} file(s) transliterated IAST -> SLP1")


if __name__ == "__main__":
    main()
