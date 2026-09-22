from app.sla_risk import SLARiskModel


def test_high_workload_high_priority_old_ticket_is_risky():
    model = SLARiskModel()

    result = model.predict({
        "workload": "High",
        "priority": "Critical",
        "ticket_age_hours": 20,
    })

    assert result["sla_risk"] is True
    assert result["method"] == "rule-based"


def test_low_everything_is_not_risky():
    model = SLARiskModel()

    result = model.predict({
        "workload": "Low",
        "priority": "Low",
        "ticket_age_hours": 1,
    })

    assert result["sla_risk"] is False


def test_single_factor_is_enough_recall_centric():
    # Wahed factor bas (high priority) lazem yekaffi 3ashan yeb2a risky,
    # 3ashan el rule recall-centric (single_df >= 1 mesh >= 2)
    model = SLARiskModel()

    result = model.predict({
        "workload": "Low",
        "priority": "Critical",
        "ticket_age_hours": 1,
    })

    assert result["sla_risk"] is True


def test_missing_features_default_safely():
    model = SLARiskModel()

    result = model.predict({})

    assert result["sla_risk"] is False
    assert "explanation" in result