import json
from collections import defaultdict

def analyze_mapping(json_path):
    # Load JSON
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Total entries (surface → lemma pairs)
    total_entries = len(data)

    # Unique lemmas
    lemmas = set(data.values())
    total_unique_lemmas = len(lemmas)

    # Count forms per lemma
    lemma_to_forms = defaultdict(list)
    for form, lemma in data.items():
        lemma_to_forms[lemma].append(form)

    # Find lemma with most forms
    most_forms_lemma = max(lemma_to_forms.items(), key=lambda x: len(x[1]))
    most_forms_count = len(most_forms_lemma[1])

    # Print stats
    print(f"Total entries: {total_entries}")
    print(f"Unique lemmas: {total_unique_lemmas}")
    print(f"Lemma with most forms: '{most_forms_lemma[0]}'")
    print(f"Number of forms for that lemma: {most_forms_count}")
    print(f"Forms: {most_forms_lemma[1]}")

    return {
        "total_entries": total_entries,
        "unique_lemmas": total_unique_lemmas,
        "lemma_with_most_forms": most_forms_lemma[0],
        "num_forms_for_that_lemma": most_forms_count,
        "forms": most_forms_lemma[1],
    }


if __name__ == "__main__":
    analyze_mapping("../../sanskrit_lemmas_copy.json")  # change to your file name
