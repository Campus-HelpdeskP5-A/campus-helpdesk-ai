from fastapi import FastAPI

from app.schemas import (
    TicketTextRequest,
    SLARiskRequest,
    DuplicateRequest,
    PredictionResponse,
)
from app.decision_engine import DecisionEngine
from app.logger import log_prediction


app = FastAPI(
    title="Campus Helpdesk AI",
    version="0.1.0"
)


decision_engine = DecisionEngine()


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "campus-helpdesk-ai"
    }


@app.post("/predict/category", response_model=PredictionResponse)
def predict_category(ticket: TicketTextRequest):
    result = decision_engine.predict_category(ticket.title, ticket.description)
    # ticket_id="pending" mo2akkat - hayet3addel lama el Backend yeb3at el UUID el 7a2i2i
    log_prediction(ticket_id="pending", prediction=result)
    return result


@app.post("/predict/priority", response_model=PredictionResponse)
def predict_priority(ticket: TicketTextRequest):
    result = decision_engine.predict_priority(ticket.title, ticket.description)
    log_prediction(ticket_id="pending", prediction=result)
    return result


@app.post("/predict/sla-risk", response_model=PredictionResponse)
def predict_sla_risk(request: SLARiskRequest):
    result = decision_engine.predict_sla_risk(
        request.workload,
        request.priority,
        request.ticket_age_hours,
    )
    log_prediction(ticket_id="pending", prediction=result)
    return result


@app.post("/predict/duplicate", response_model=PredictionResponse)
def predict_duplicate(request: DuplicateRequest):
    existing_tickets = [
        {"id": t.id, "text": t.text}
        for t in request.existing_tickets
    ]
    result = decision_engine.predict_duplicate(
        request.title,
        request.description,
        existing_tickets,
    )
    log_prediction(ticket_id="pending", prediction=result)
    return result