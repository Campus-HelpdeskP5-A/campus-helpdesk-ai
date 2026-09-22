from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class DuplicateDetector:
    """
    TF-IDF + Cosine Similarity baseline (AI-03).
    Betrank el ticket el gdeed dedd active tickets mawgoda,
    w bterga3 candidates + similarity score.

    MOHEM: el input bas title (+ description lw mawgoda).
    MESH momken tetla3 hagat zay minutes_after_original hena,
    dah evaluation feature bas, mesh similarity feature.
    """

    def __init__(self):
        self.vectorizer = None
        self.fitted = False

    def fit(self, existing_tickets: list[dict]):
        """
        existing_tickets: list of dicts, kol dict fih:
            - "id": ticket id
            - "text": title (+ description) el ticket el active
        """
        if not existing_tickets:
            self.fitted = False
            return

        texts = [t["text"] for t in existing_tickets]

        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            min_df=1,
        )

        self._tickets = existing_tickets
        self._matrix = self.vectorizer.fit_transform(texts)
        self.fitted = True

    def find_duplicates(self, title: str, description: str, top_k: int = 5, threshold: float = 0.3):
        """
        Betraga3 top_k candidates ele a2rab similarity, maa score.
        Lw msh fitted (yaani mfeesh active tickets aslan), betraga3 [].
        """
        if not self.fitted:
            return []

        query_text = f"{title} {description}"
        query_vector = self.vectorizer.transform([query_text])

        similarities = cosine_similarity(query_vector, self._matrix)[0]

        ranked = sorted(
            zip(self._tickets, similarities),
            key=lambda pair: pair[1],
            reverse=True,
        )

        candidates = []
        for ticket, score in ranked[:top_k]:
            if score < threshold:
                continue

            candidates.append({
                "ticket_id": ticket["id"],
                "similarity_score": round(float(score), 3),
                "explanation": (
                    f"Text similarity of {round(float(score), 3)} "
                    f"with existing ticket {ticket['id']}."
                ),
            })

        return candidates


def suggest_duplicates(title: str, description: str, existing_tickets: list[dict], top_k: int = 5, threshold: float = 0.3):
    """
    Rule-baseline-safe wrapper function, zay ba2y el suggest_* functions
    fi rule_engine.py. Btsawy try/except gowaha 3ashan law feeh crash
    (zay tickets list fadya aw corrupted data), terga3 [] mesh tewalla3
    kol el decision_engine.
    """
    try:
        detector = DuplicateDetector()
        detector.fit(existing_tickets)
        return detector.find_duplicates(title, description, top_k=top_k, threshold=threshold)
    except Exception:
        return []