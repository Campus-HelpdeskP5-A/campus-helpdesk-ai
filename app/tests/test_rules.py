from app.rule_engine import (
    suggest_category,
    suggest_impact,
    suggest_urgency,
    suggest_priority,
)


def test_maintenance_category():
    category, confidence, explanation = suggest_category(
        "Air conditioner is not working",
        "The AC in room 205 stopped working"
    )

    assert category == "HVAC_AC"
    assert confidence > 0
    assert explanation


def test_impact_medium():
    impact, confidence, explanation = suggest_impact(
        "AC problem in laboratory",
        "The laboratory is affected"
    )

    assert impact == "Medium"
    assert confidence > 0
    assert explanation


def test_urgency_high():
    urgency, confidence, explanation = suggest_urgency(
        "Emergency",
        "The system stopped working and classes cannot continue"
    )

    assert urgency == "High"
    assert confidence > 0
    assert explanation


def test_priority_matrix_high_high():
    (
        priority,
        confidence,
        explanation,
        impact,
        impact_confidence,
        impact_explanation,
        urgency,
        urgency_confidence,
        urgency_explanation,
    ) = suggest_priority(
        "Emergency building problem",
        "Fire in the building, everyone is in danger"
    )

    assert impact == "High"
    assert urgency == "High"
    assert priority == "Critical"
    assert confidence > 0
    assert explanation


def test_priority_matrix_medium_high():
    (
        priority,
        confidence,
        explanation,
        impact,
        impact_confidence,
        impact_explanation,
        urgency,
        urgency_confidence,
        urgency_explanation,
    ) = suggest_priority(
        "Laboratory stopped working",
        "The laboratory class cannot continue"
    )

    assert impact == "Medium"
    assert urgency == "High"
    assert priority == "High"


def test_priority_matrix_low_low():
    (
        priority,
        confidence,
        explanation,
        impact,
        impact_confidence,
        impact_explanation,
        urgency,
        urgency_confidence,
        urgency_explanation,
    ) = suggest_priority(
        "Minor personal issue",
        "This is a minor issue and can wait"
    )

    assert impact == "Low"
    assert urgency == "Low"
    assert priority == "Low"