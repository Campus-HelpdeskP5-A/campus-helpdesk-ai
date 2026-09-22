from app.rule_engine import (
    suggest_category,
    suggest_priority,
    is_emergency,
)
from app.category_classifier import CategoryClassifier
from app.model_registry import ModelRegistry
from app.sla_risk import SLARiskModel
from app.duplicate import DuplicateDetector


class DecisionEngine:

    def __init__(self):
        self.category_classifier = CategoryClassifier()

        registry = ModelRegistry()
        model, vectorizer = registry.load_category_model()

        if model is not None and vectorizer is not None:
            self.category_classifier.load_model(model, vectorizer)

        self.sla_model = SLARiskModel()

    def predict_category(self, title: str, description: str):
        text = f"{title} {description}"

        # Emergency check dayman awel 7aga, mesh gowa el ML flow
        emergency, emergency_keyword = is_emergency(title, description)

        category_result = None
        try:
            category_result = self.category_classifier.predict(text)
        except Exception:
            category_result = None

        if category_result is not None:
            category, confidence = category_result
            model_version = "category-ml-v1"
            explanation = "Category predicted by the trained ML model."
        else:
            category, confidence, explanation = suggest_category(title, description)
            model_version = "category-rules-v1"

        return {
            "prediction_type": "CATEGORY",
            "value": {
                "category": category,
                "is_emergency": emergency,
                "emergency_keyword": emergency_keyword,
            },
            "confidence": confidence,
            "model_version": model_version,
            "explanation": explanation,
        }

    def predict_priority(self, title: str, description: str):
        (
            priority,
            priority_confidence,
            priority_explanation,
            impact,
            impact_confidence,
            impact_explanation,
            urgency,
            urgency_confidence,
            urgency_explanation,
        ) = suggest_priority(title, description)

        return {
            "prediction_type": "PRIORITY",
            "value": {
                "priority": priority,
                "impact": impact,
                "urgency": urgency,
            },
            "confidence": priority_confidence,
            "model_version": "priority-rules-v1",
            "explanation": priority_explanation,
        }

    def predict_sla_risk(self, workload: str, priority: str, ticket_age_hours: float):
        result = self.sla_model.predict({
            "workload": workload,
            "priority": priority,
            "ticket_age_hours": ticket_age_hours,
        })

        return {
            "prediction_type": "SLA_RISK",
            "value": {
                "sla_risk": result["sla_risk"],
            },
            "confidence": result["confidence"],
            "model_version": "sla-rules-v1",
            "explanation": result["explanation"],
        }

    def predict_duplicate(self, title: str, description: str, existing_tickets: list):
        try:
            detector = DuplicateDetector()
            detector.fit(existing_tickets)
            candidates = detector.find_duplicates(title, description)
        except Exception:
            candidates = []

        top_confidence = candidates[0]["similarity_score"] if candidates else 0.0

        return {
            "prediction_type": "DUPLICATE",
            "value": {
                "candidates": candidates,
            },
            "confidence": top_confidence,
            "model_version": "duplicate-tfidf-v1",
            "explanation": (
                f"Found {len(candidates)} candidate(s) via TF-IDF cosine similarity."
                if candidates else
                "No similar tickets found in the active pool."
            ),
        }