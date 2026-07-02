from dharmamitra_sanskrit_grammar import DharmamitraSanskritProcessor

# Initialize the processor
processor = DharmamitraSanskritProcessor()

# Process a batch of sentences
sentences = [
    "mādrī sutau kathayatām na bhavanti rogāḥ"
]

# Using different modes
results = processor.process_batch(
    sentences,
    mode="unsandhied-lemma-morphosyntax",  # or 'lemma' or 'unsandhied-lemma-morphosyntax'
    human_readable_tags=True
)

print(results[0]["grammatical_analysis"])

tokens = []
for entry in results[0]["grammatical_analysis"]:
    token = entry.get("lemma", "")
    if token:
        tokens.append(token)
print(*tokens)