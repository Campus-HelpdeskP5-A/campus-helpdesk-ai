import csv
import sys
from pathlib import Path

import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.metrics import f1_score, classification_report

sys.path.append(str(Path(__file__).resolve().parent.parent))


DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "classification" / "classification_dataset.csv"
MODEL_DIR = Path(__file__).resolve().parent.parent / "models" / "category"
BASELINE_MACRO_F1 = 0.7711


def load_dataset(path):
    texts = []
    labels = []
    groups = []

    with open(path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=",")
        for row in reader:
            if not row.get("title") or not row.get("category"):
                continue

            text = f"{row['title']} {row['description']}"
            texts.append(text)
            labels.append(row["category"])
            groups.append(row["cluster_id"])

    return texts, labels, groups


def train_and_evaluate():
    texts, labels, groups = load_dataset(DATA_PATH)
    texts = np.array(texts)
    labels = np.array(labels)
    groups = np.array(groups)

    print(f"Total samples: {len(texts)}")
    print(f"Unique clusters: {len(set(groups))}")

    # GroupKFold: kol cluster_id yeb2a fully gowa train aw fully gowa test,
    # mesh momken yensa2 (leakage prevention, required by spec).
    gkf = GroupKFold(n_splits=5)

    fold_scores = []

    for fold_index, (train_idx, test_idx) in enumerate(gkf.split(texts, labels, groups)):
        X_train_text, X_test_text = texts[train_idx], texts[test_idx]
        y_train, y_test = labels[train_idx], labels[test_idx]

        vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            min_df=2,
        )
        X_train = vectorizer.fit_transform(X_train_text)
        X_test = vectorizer.transform(X_test_text)

        model = LogisticRegression(
            class_weight="balanced",
            max_iter=1000,
        )
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        fold_f1 = f1_score(y_test, y_pred, average="macro", zero_division=0)
        fold_scores.append(fold_f1)

        print(f"Fold {fold_index + 1}: Macro F1 = {fold_f1:.4f}")

    mean_f1 = np.mean(fold_scores)
    std_f1 = np.std(fold_scores)

    print()
    print(f"Cross-validated Macro F1: {mean_f1:.4f} (+/- {std_f1:.4f})")
    print(f"Rule-based baseline Macro F1: {BASELINE_MACRO_F1:.4f}")

    if mean_f1 > BASELINE_MACRO_F1:
        print("Result: ML model BEATS the rule-based baseline.")
    else:
        print("Result: ML model does NOT beat the rule-based baseline. "
              "This is a valid, reportable result.")

    # Final model: yet-train 3ala KOL el data (msh fold wa7da),
    # 3ashan yeb2a el production model. Da mesh el evaluation number,
    # el evaluation number howa el cross-validated score fo2.
    print("\nTraining final model on full dataset for persistence...")

    final_vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        min_df=2,
    )
    X_full = final_vectorizer.fit_transform(texts)

    final_model = LogisticRegression(
        class_weight="balanced",
        max_iter=1000,
    )
    final_model.fit(X_full, labels)

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    model_path = MODEL_DIR / "category_model.joblib"
    vectorizer_path = MODEL_DIR / "category_vectorizer.joblib"

    joblib.dump(final_model, model_path)
    joblib.dump(final_vectorizer, vectorizer_path)

    print(f"Saved model to: {model_path}")
    print(f"Saved vectorizer to: {vectorizer_path}")

    # Full classification report on the last fold, lel error analysis
    print("\n--- Classification report (last fold) ---")
    print(classification_report(y_test, y_pred, zero_division=0))


if __name__ == "__main__":
    train_and_evaluate()