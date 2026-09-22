import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.sla_risk import SLARiskModel

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "sla_risk" / "sla_risk_dataset (1).csv"


def bucket_workload(value, low_thresh, high_thresh):
    if value <= low_thresh:
        return "Low"
    elif value <= high_thresh:
        return "Medium"
    return "High"


def load_rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def evaluate():
    rows = load_rows(DATA_PATH)
    print(f"Total samples: {len(rows)}")

    workloads = sorted(int(r["team_workload"]) for r in rows)
    n = len(workloads)
    low_thresh = workloads[n // 3]
    high_thresh = workloads[(2 * n) // 3]
    print(f"Workload thresholds -> Low<={low_thresh}, Medium<={high_thresh}, High>{high_thresh}")

    model = SLARiskModel()
    tp = fp = tn = fn = 0

    for row in rows:
        workload_label = bucket_workload(int(row["team_workload"]), low_thresh, high_thresh)
        priority = row["priority"].strip().title()
        age_hours = float(row["ticket_age_minutes"]) / 60.0

        features = {
            "workload": workload_label,
            "priority": priority,
            "ticket_age_hours": age_hours,
        }

        result = model.predict(features)
        predicted = result["sla_risk"]
        actual = row["sla_breach"].strip() == "1"

        if predicted and actual:
            tp += 1
        elif predicted and not actual:
            fp += 1
        elif not predicted and not actual:
            tn += 1
        else:
            fn += 1

    total = tp + fp + tn + fn
    accuracy = (tp + tn) / total if total else 0.0
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0

    print(f"TP={tp}  FP={fp}  TN={tn}  FN={fn}")
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1 Score:  {f1:.4f}")


if __name__ == "__main__":
    evaluate()