from app.rules.router import suggest_category, suggest_priority


def test_maintenance_category():
    category, confidence, explanation = suggest_category(
        "Air conditioner is not working",
        "The AC in room 205 stopped working"
    )

    assert category == "Maintenance"
    assert confidence > 0


def test_high_priority():
    priority, confidence, explanation = suggest_priority(
        "Emergency",
        "There is a fire in the building"
    )

    assert priority == "High"
    assert confidence > 0