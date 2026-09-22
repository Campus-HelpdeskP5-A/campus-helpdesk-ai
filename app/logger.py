import logging
import json
from datetime import datetime, timezone


logger = logging.getLogger("campus_helpdesk_ai")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def log_prediction(ticket_id: str, prediction: dict, agent_id: str = None, overridden: bool = False):
    """
    Beysagel kol prediction event beshakl 3aam, sale7 le ay
    prediction_type (CATEGORY / PRIORITY / SLA_RISK / DUPLICATE),
    3ashan kol el endpoints el arba3a beysta5demo nafs el logger.

    MESH beysagel ay sensitive payload (passwords, tokens, PII) - bas
    el prediction fields el mottafa2 3aleeha.
    """
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": "ai_prediction",
        "ticket_id": ticket_id,
        "agent_id": agent_id,
        "overridden": overridden,
        "prediction_type": prediction.get("prediction_type"),
        "value": prediction.get("value"),
        "confidence": prediction.get("confidence"),
        "model_version": prediction.get("model_version"),
    }

    logger.info(json.dumps(log_entry, ensure_ascii=False))


def log_override(ticket_id: str, agent_id: str, field: str, original_value: str, new_value: str):
    """
    Beysagel lama el agent yeghayar prediction el AI (override).
    Da el data el momken nesta5demo ba3dein le-hisab "Override rate"
    el matloob fel spec ("Override rate: nisbet ma el agent yghayar el suggestion").
    """
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": "ai_suggestion_override",
        "ticket_id": ticket_id,
        "agent_id": agent_id,
        "field": field,
        "original_value": original_value,
        "new_value": new_value,
    }

    logger.info(json.dumps(log_entry, ensure_ascii=False))