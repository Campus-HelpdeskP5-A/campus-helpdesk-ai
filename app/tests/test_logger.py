import json
import logging

from app.logger import log_prediction, log_override


def test_log_prediction_outputs_valid_json(caplog):
    prediction = {
        "prediction_type": "CATEGORY",
        "value": {"category": "HVAC_AC", "is_emergency": False, "emergency_keyword": None},
        "confidence": 0.9,
        "model_version": "category-rules-v1",
        "explanation": "Category suggested by rule.",
    }

    with caplog.at_level(logging.INFO, logger="campus_helpdesk_ai"):
        log_prediction(ticket_id="pending", prediction=prediction, agent_id="agent_1")

    assert len(caplog.records) == 1

    logged_data = json.loads(caplog.records[0].message)

    assert logged_data["event"] == "ai_prediction"
    assert logged_data["ticket_id"] == "pending"
    assert logged_data["agent_id"] == "agent_1"
    assert logged_data["prediction_type"] == "CATEGORY"
    assert logged_data["value"]["category"] == "HVAC_AC"
    assert "timestamp" in logged_data


def test_log_prediction_does_not_leak_sensitive_fields(caplog):
    prediction = {
        "prediction_type": "CATEGORY",
        "value": {"category": "IT_NETWORK_ACCOUNTS"},
        "confidence": 0.8,
        "model_version": "category-ml-v1",
        "explanation": "predicted",
        "password": "should_never_appear",  # lw etb3atet be2l-8alat
    }

    with caplog.at_level(logging.INFO, logger="campus_helpdesk_ai"):
        log_prediction(ticket_id="pending", prediction=prediction)

    logged_data = json.loads(caplog.records[0].message)

    assert "password" not in logged_data
    assert "should_never_appear" not in caplog.records[0].message


def test_log_override_outputs_valid_json(caplog):
    with caplog.at_level(logging.INFO, logger="campus_helpdesk_ai"):
        log_override(
            ticket_id="550e8400-e29b-41d4-a716-446655440000",
            agent_id="agent_2",
            field="category",
            original_value="HVAC_AC",
            new_value="ELECTRICAL",
        )

    assert len(caplog.records) == 1

    logged_data = json.loads(caplog.records[0].message)

    assert logged_data["event"] == "ai_suggestion_override"
    assert logged_data["ticket_id"] == "550e8400-e29b-41d4-a716-446655440000"
    assert logged_data["field"] == "category"
    assert logged_data["original_value"] == "HVAC_AC"
    assert logged_data["new_value"] == "ELECTRICAL"