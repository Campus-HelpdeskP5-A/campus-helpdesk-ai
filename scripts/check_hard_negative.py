import csv
import sys
from pathlib import Path

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


def build_pool(rows):
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


def check_hard_negatives(rows, pool, threshold=0.3, top_k=1):
    """
    Lekol ORIGINAL, nshoof: el HARD_NEGATIVE beta3 nafs el cluster,
    hal el detector barafdo (sa7), wala byeddeeh score 3ale w
    ye5aleeh yetla3 top-1 (False Positive khateer).
    """
    detector = DuplicateDetector()
    detector.fit(pool)

    originals = [r for r in rows if r["role"] == "ORIGINAL"]

    total_with_hard_negative = 0
    false_positive_count = 0

    for original in originals:
        cluster_id = original["cluster_id"]

        hard_negative = next(
            (r for i, r in enumerate(rows)
             if r["cluster_id"] == cluster_id and r["role"] == "HARD_NEGATIVE"),
            None
        )

        if hard_negative is None:
            continue

        total_with_hard_negative += 1

        candidates = detector.find_duplicates(
            original["title"],
            original["description"],
            top_k=top_k,
            threshold=threshold,
        )

        hard_negative_id = None
        for i, r in enumerate(rows):
            if r is hard_negative:
                hard_negative_id = f"row_{i}"
                break

        flagged_ids = [c["ticket_id"] for c in candidates]

        if hard_negative_id in flagged_ids:
            false_positive_count += 1
            score = next(c["similarity_score"] for c in candidates if c["ticket_id"] == hard_negative_id)
            print(f"[FALSE POSITIVE] cluster={cluster_id} | score={score} | "
                  f"'{original['title']}' vs HARD_NEGATIVE '{hard_negative['title']}'")

    print(f"\nTotal clusters with HARD_NEGATIVE: {total_with_hard_negative}")
    print(f"False positives (HARD_NEGATIVE flagged as duplicate in top-{top_k}): {false_positive_count}")

    if total_with_hard_negative > 0:
        fp_rate = false_positive_count / total_with_hard_negative
        print(f"False Positive Rate on HARD_NEGATIVE: {fp_rate:.4f}")


def main():
    rows = load_dataset(DATA_PATH)
    pool = build_pool(rows)
    check_hard_negatives(rows, pool)


if __name__ == "__main__":
    main()