import re

from app.rules import (
    CATEGORY_RULES,
    IMPACT_RULES,
    URGENCY_RULES,
    PRIORITY_MATRIX,
)


EMERGENCY_KEYWORDS = [
    "fire",
    "flood",
    "gas leak",
    "electric shock",
    "explosion",
    "collapse",
]


def _find_matching_rule(text: str, rules: dict):
    text = text.lower()

    for label, keywords in rules.items():
        for keyword in keywords:
            # \b = word boundary, biyman3 en "ac" tetla3 sa7 gowa "back"
            pattern = r"\b" + re.escape(keyword) + r"\b"
            if re.search(pattern, text):
                return label, keyword

    return None, None


def is_emergency(title: str, description: str):
    """
    System-level rule trigger, mesh training label.
    Lazem yet7arek 2abl ay ML/priority logic, w yeb2a separate
    3an el urgency el 3adeya.
    """
    text = f"{title} {description}".lower()

    for keyword in EMERGENCY_KEYWORDS:
        pattern = r"\b" + re.escape(keyword) + r"\b"
        if re.search(pattern, text):
            return True, keyword

    return False, None


def suggest_category(title: str, description: str):
    text = f"{title} {description}"

    category, keyword = _find_matching_rule(
        text,
        CATEGORY_RULES
    )

    if category:
        return (
            category,
            0.9,
            f"Category suggested by rule based on keyword: {keyword}"
        )

    return (
        "OTHER",
        0.5,
        "No specific category keyword was detected."
    )


def suggest_impact(title: str, description: str):
    text = f"{title} {description}"

    impact, keyword = _find_matching_rule(
        text,
        IMPACT_RULES
    )

    if impact:
        return (
            impact,
            0.85,
            f"Impact estimated from keyword: {keyword}"
        )

    return (
        "Low",
        0.5,
        "No specific impact keyword was detected."
    )


def suggest_urgency(title: str, description: str):
    text = f"{title} {description}".lower()

    low_urgency_phrases = [
        "not urgent",
        "can wait",
        "when possible",
        "minor",
    ]

    for phrase in low_urgency_phrases:
        if phrase in text:
            return (
                "Low",
                0.85,
                f"Urgency estimated from low-urgency phrase: {phrase}"
            )

    urgency, keyword = _find_matching_rule(
        text,
        URGENCY_RULES
    )

    if urgency:
        return (
            urgency,
            0.85,
            f"Urgency estimated from keyword: {keyword}"
        )

    return (
        "Low",
        0.5,
        "No specific urgency keyword was detected."
    )


def suggest_priority(title: str, description: str):
    (
        impact,
        impact_confidence,
        impact_explanation
    ) = suggest_impact(
        title,
        description
    )

    (
        urgency,
        urgency_confidence,
        urgency_explanation
    ) = suggest_urgency(
        title,
        description
    )

    priority = PRIORITY_MATRIX[impact][urgency]

    priority_confidence = round(
        min(
            impact_confidence,
            urgency_confidence
        ),
        2
    )

    priority_explanation = (
        "Priority calculated using the impact × urgency matrix. "
        f"Impact={impact}, Urgency={urgency}."
    )

    return (
        priority,
        priority_confidence,
        priority_explanation,
        impact,
        impact_confidence,
        impact_explanation,
        urgency,
        urgency_confidence,
        urgency_explanation,
    )