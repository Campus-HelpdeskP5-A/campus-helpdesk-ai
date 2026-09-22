import csv
import sys
from pathlib import Path
from collections import defaultdict

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.duplicate import DuplicateDetector


DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "duplicates" / "duplicate_dataset.csv"


def load_dataset(path):
    rows = []
    with open(path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=",")
        for row in reader:
            if not row.get("title"):
                continue
            rows.append(row)
    return rows


def build_ticket_pool(rows):
    """
    Kol row (ma3ada ORIGINAL) beyeb2a ticket 'active' fel pool.
    Kol ticket leih id fareed 3ashan neb2a ne3raf nrag3o sa7.
    """
    pool = []
    for i, row in enumerate(rows):
        if row["role"] == "ORIGINAL":
            continue
        pool.append({
            "id": f"row_{i}",
            "text": f"{row['title']} {row['description']}",
            "cluster_id": row["cluster_id"],
            "role": row["role"],
        })
    return pool


def precision_at_k(queries, pool, k_values=(1, 3, 5)):
    detector = DuplicateDetector()
    detector.fit(pool)

    results = {k: [] for k in k_values}

    for query in queries:
        candidates = detector.find_duplicates(
            query["title"],
            query["description"],
            top_k=max(k_values),
            threshold=0.0,  # neshoof kol el candidates, mesh nefelter mo3akaran
        )

        # nrag3 el role bta3 kol candidate 3ashan ne3raf howa DUPLICATE walla laa
        candidate_roles = []
        for c in candidates:
            matched = next((p for p in pool if p["id"] == c["ticket_id"]), None)
            if matched:
                candidate_roles.append(matched["role"])

        for k in k_values:
            top_k_roles = candidate_roles[:k]
            true_duplicates_in_topk = sum(
                1 for r in top_k_roles
                if r == "DUPLICATE" and query["cluster_id"] in [
                    p["cluster_id"] for p in pool
                    if p["id"] in [c["ticket_id"] for c in candidates[:k]]
                ]
            )
            # Precision@K = (sawab duplicates fel top K) / K
            correct = sum(
                1 for c, role in zip(candidates[:k], top_k_roles)
                if role == "DUPLICATE"
            )
            results[k].append(correct / k)

    return {k: sum(v) / len(v) for k, v in results.items()}


def evaluate():
    rows = load_dataset(DATA_PATH)
    print(f"Total rows: {len(rows)}")

    originals = [r for r in rows if r["role"] == "ORIGINAL"]
    print(f"Total ORIGINAL queries: {len(originals)}")

    queries = [
        {
            "title": r["title"],
            "description": r["description"],
            "cluster_id": r["cluster_id"],
        }
        for r in originals
    ]

    pool = build_ticket_pool(rows)
    print(f"Ticket pool size: {len(pool)}")

    scores = precision_at_k(queries, pool)

    print("\n--- Precision@K (TF-IDF + Cosine Similarity baseline) ---")
    for k, score in scores.items():
        print(f"Precision@{k}: {score:.4f}")


if __name__ == "__main__":
    evaluate()