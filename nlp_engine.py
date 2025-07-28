import spacy
import json

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")


def load_data(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


def extract_entities(texts):
    all_entities = []

    for text in texts:
        doc = nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        all_entities.append({
            "text": text,
            "entities": entities
        })

    return all_entities


if __name__ == "__main__":
    # Load scraped ISRO updates
    data = load_data("data/isro_updates.json")

    # Extract entities from each headline
    results = extract_entities(data)

    # Print results
    for item in results:
        print(f"\n🔹 {item['text']}")
        for entity, label in item["entities"]:
            print(f"   → {entity} ({label})")
