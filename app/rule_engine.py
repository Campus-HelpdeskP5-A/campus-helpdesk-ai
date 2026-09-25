import re

from app.rules import (
    CATEGORY_RULES,
    IMPACT_RULES,
    URGENCY_RULES,
    PRIORITY_MATRIX,
)


EMERGENCY_KEYWORDS = [
    # Fire / smoke
    "fire", "fires", "burning", "smoke", "smoke smell",
    # Flood / water
    "flood", "flooding", "flooded",
    # Gas / chemical
    "gas leak", "gas leaking", "gas smell",
    "chemical spill", "chemical leak", "toxic fumes",
    # Electrical
    "electric shock", "electrocuted", "electrocution",
    "sparking wires", "exposed wires",
    # Structural
    "collapse", "collapsing", "collapsed", "structural damage",
    # Explosion
    "explosion", "explode", "exploded", "exploding",
    # Medical / injury
    "injured", "injury", "bleeding", "unconscious",
    "trapped", "not breathing",
    # Evacuation
    "evacuate", "evacuation",
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
    label, keyword = _find_matching_rule(text, CATEGORY_RULES)

    if label is None:
        return "OTHER", 0.5, "No keyword matched; defaulted to OTHER."

    return label, 0.9, f"Matched keyword: '{keyword}'."


def suggest_impact(title: str, description: str):
    text = f"{title} {description}"
    label, keyword = _find_matching_rule(text, IMPACT_RULES)

    if label is None:
        return "Medium", 0.5, "No impact keyword matched; defaulted to Medium."

    return label, 0.85, f"Matched impact keyword: '{keyword}'."


def suggest_urgency(title: str, description: str):
    text = f"{title} {description}"
    label, keyword = _find_matching_rule(text, URGENCY_RULES)

    if label is None:
        return "Medium", 0.5, "No urgency keyword matched; defaulted to Medium."

    return label, 0.85, f"Matched urgency keyword: '{keyword}'."


def suggest_priority(title: str, description: str):
    impact, impact_confidence, impact_explanation = suggest_impact(title, description)
    urgency, urgency_confidence, urgency_explanation = suggest_urgency(title, description)

    priority = PRIORITY_MATRIX[impact][urgency]
    confidence = min(impact_confidence, urgency_confidence)
    explanation = (
        f"Impact={impact} ({impact_explanation}) x "
        f"Urgency={urgency} ({urgency_explanation}) -> Priority={priority}."
    )

    return (
        priority,
        confidence,
        explanation,
        impact,
        impact_confidence,
        impact_explanation,
        urgency,
        urgency_confidence,
        urgency_explanation,
    )