import csv
import sys
from pathlib import Path
from collections import defaultdict

import joblib
from sklearn.metrics import f1_score

sys.path.append(str(Path(__file__).resolve().parent.parent))


DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "classification" / "classification_dataset.csv"
MODEL_DIR = Path(__file__).resolve().parent.parent / "models" / "category"


# El 5 keyword traps el mazkoreen 7arfeyan fel spec document.
# Da mesh mawgood (aw momken yeb2a mawgood be sofa mokhtalefa) fel training data,
# w howa el real test lel model: hal howa bytraf el context wala bas el keyword.
SPEC_KEYWORD_TRAPS = [
    ("AC leaking water on floor", "", "HVAC_AC"),
    ("Laptop needs new AC adapter", "", "IT_HARDWARE_PRINTING"),
    ("Projector won't power on", "", "AV_CLASSROOM_EQUIPMENT"),
    ("Lab PC can't reach Wi-Fi", "", "IT_NETWORK_ACCOUNTS"),
    ("Broken door on network cabinet", "", "BUILDING_STRUCTURE"),
]


def load_dataset(path):
    rows = []
    with open(path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=",")
        for row in reader:
            if not row.get("title") or not row.get("category"):
                continue
            rows.append(row)
    return rows


def check_performance_by_difficulty(model, vectorizer, rows):
    by_difficulty = defaultdict(lambda: {"true": [], "pred": []})

    for row in rows:
        text = f"{row['title']} {row['description']}"
        vector = vectorizer.transform([text])
        prediction = model.predict(vector)[0]

        difficulty = row.get("difficulty", "UNKNOWN")
        by_difficulty[difficulty]["true"].append(row["category"])
        by_difficulty[difficulty]["pred"].append(prediction)

    print("--- Macro F1 by difficulty level ---")
    for difficulty, data in sorted(by_difficulty.items()):
        f1 = f1_score(data["true"], data["pred"], average="macro", zero_division=0)
        print(f"{difficulty:10s} (n={len(data['true']):4d}): Macro F1 = {f1:.4f}")


def check_spec_keyword_traps(model, vectorizer):
    print("\n--- Spec keyword-trap sentences (unseen phrasing) ---")
    correct = 0

    for title, description, expected in SPEC_KEYWORD_TRAPS:
        text = f"{title} {description}"
        vector = vectorizer.transform([text])
        prediction = model.predict(vector)[0]
        confidence = max(model.predict_proba(vector)[0])

        status = "OK" if prediction == expected else "WRONG"
        if prediction == expected:
            correct += 1

        print(f"[{status}] '{title}' -> predicted={prediction} (expected={expected}, confidence={confidence:.2f})")

    print(f"\nSpec keyword-trap accuracy: {correct}/{len(SPEC_KEYWORD_TRAPS)}")


def main():
    model_path = MODEL_DIR / "category_model.joblib"
    vectorizer_path = MODEL_DIR / "category_vectorizer.joblib"

    if not model_path.exists() or not vectorizer_path.exists():
        print("Model not found. Run train_category_model.py first.")
        return

    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)

    rows = load_dataset(DATA_PATH)

    check_performance_by_difficulty(model, vectorizer, rows)
    check_spec_keyword_traps(model, vectorizer)


if __name__ == "__main__":
    main()