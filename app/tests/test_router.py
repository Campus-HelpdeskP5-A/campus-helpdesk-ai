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

    assert category == "Maintenance"
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
    result = suggest_priority(
        "Emergency building problem",
        "Fire in the building, everyone is in danger"
    )

    priority = result[0]
    impact = result[3]
    urgency = result[6]

    assert impact == "High"
    assert urgency == "High"
    assert priority == "Critical"


def test_priority_matrix_medium_high():
    result = suggest_priority(
        "Laboratory stopped working",
        "The laboratory class cannot continue"
    )

    priority = result[0]
    impact = result[3]
    urgency = result[6]

    assert impact == "Medium"
    assert urgency == "High"
    assert priority == "High"


def test_priority_matrix_low_low():
    result = suggest_priority(
        "Minor personal issue",
        "This is a minor issue and can wait"
    )

    priority = result[0]
    impact = result[3]
    urgency = result[6]

    assert impact == "Low"
    assert urgency == "Low"
    assert priority == "Low"