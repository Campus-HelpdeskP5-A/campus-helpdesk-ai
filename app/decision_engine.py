from app.rule_engine import (
    suggest_category,
    suggest_priority,
)
from app.category_classifier import CategoryClassifier


class DecisionEngine:

    def __init__(self):
        self.category_classifier = CategoryClassifier()

    def predict(self, title: str, description: str):

        text = f"{title} {description}"

        # Try ML category prediction first
        category_result = self.category_classifier.predict(text)

        if category_result is not None:
            category, confidence = category_result

            category_method = "ml"
            category_explanation = (
                "Category predicted by the trained ML model."
            )

        else:
            # Fallback to rule-based baseline
            (
                category,
                confidence,
                category_explanation
            ) = suggest_category(
                title,
                description
            )

            category_method = "rule-based"

        # Priority = Impact × Urgency matrix
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
        }