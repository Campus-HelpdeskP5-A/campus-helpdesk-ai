import csv
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from sklearn.metrics import f1_score, classification_report
from app.rule_engine import suggest_category


DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "classification" / "classification_dataset.csv"


def load_dataset(path):
    rows = []
    with open(path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=",")
        for row in reader:
            if not row.get("title") or not row.get("category"):
                continue
            rows.append(row)
    return rows


def evaluate():
    rows = load_dataset(DATA_PATH)

    print(f"Total samples: {len(rows)}")

    if len(rows) == 0:
        print("No rows loaded. Check delimiter/encoding/column names.")
        with open(DATA_PATH, encoding="utf-8-sig") as f:
            reader = csv.DictReader(f, delimiter=",")
            print("Column names found:", reader.fieldnames)
        return

    y_true = []
    y_pred = []

    for row in rows:
        title = row["title"]
        description = row["description"]
        true_category = row["category"]

        predicted_category, confidence, explanation = suggest_category(
            title, description
        )

        y_true.append(true_category)
        y_pred.append(predicted_category)

    macro_f1 = f1_score(y_true, y_pred, average="macro", zero_division=0)

    print(f"Rule-based baseline Macro F1: {macro_f1:.4f}")
    print()
    print(classification_report(y_true, y_pred, zero_division=0))

    print("\n--- Sample misclassifications ---")
    errors_shown = 0
    for row, pred in zip(rows, y_pred):
        if row["category"] != pred and errors_shown < 15:
            print(f"TRUE={row['category']:25s} PRED={pred:25s} | {row['title']}")
            errors_shown += 1


if __name__ == "__main__":
    evaluate()