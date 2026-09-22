from app.rule_engine import (
    suggest_category,
    suggest_priority,
    is_emergency,
)
from app.category_classifier import CategoryClassifier
from app.model_registry import ModelRegistry


MODEL_VERSION = "rule-baseline-v1"


class DecisionEngine:

    def __init__(self):
        self.category_classifier = CategoryClassifier()

        registry = ModelRegistry()
        model, vectorizer = registry.load_category_model()

        if model is not None and vectorizer is not None:
            self.category_classifier.load_model(model, vectorizer)

    def predict(self, title: str, description: str):

        text = f"{title} {description}"

        # Emergency check dayman awel 7aga, mesh gowa el ML flow
        emergency, emergency_keyword = is_emergency(title, description)

        # Try ML category prediction first, with safe fallback
        category_result = None
        try:
            category_result = self.category_classifier.predict(text)
        except Exception:
            category_result = None

        if category_result is not None:
            category, confidence = category_result
            category_method = "ml"
            category_explanation = (
                "Category predicted by the trained ML model."
            )
        else:
            (
                category,
                confidence,
                category_explanation
            ) = suggest_category(
                title,
                description
            )
            category_method = "rule-based"

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
        ) = suggest_priority(
            title,
            description
        )

        return {
            "category": category,
            "category_confidence": confidence,
            "category_explanation": category_explanation,
            "category_method": category_method,

            "impact": impact,
            "impact_confidence": impact_confidence,
            "impact_explanation": impact_explanation,

            "urgency": urgency,
            "urgency_confidence": urgency_confidence,
            "urgency_explanation": urgency_explanation,

            "priority": priority,
            "priority_confidence": priority_confidence,
            "priority_explanation": priority_explanation,
            "priority_method": "rule-based-matrix",

            "is_emergency": emergency,
            "emergency_keyword": emergency_keyword,

            "model_version": MODEL_VERSION,
        }