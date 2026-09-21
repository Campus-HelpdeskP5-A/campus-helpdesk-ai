from fastapi import FastAPI

from app.schemas import TicketRequest, PredictionResponse
from app.decision_engine import DecisionEngine


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


@app.post(
    "/api/v1/predict",
    response_model=PredictionResponse
)
def predict_ticket(ticket: TicketRequest):

    result = decision_engine.predict(
        ticket.title,
        ticket.description
    )

    return result