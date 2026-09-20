from fastapi import FastAPI
from pydantic import BaseModel

from app.rules.router import suggest_category, suggest_priority


app = FastAPI(
    title="Campus Helpdesk AI",
    version="0.1.0"
)


class TicketRequest(BaseModel):
    title: str
    description: str


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "campus-helpdesk-ai"
    }


@app.post("/api/v1/predict")
def predict_ticket(ticket: TicketRequest):
    category, category_confidence, category_explanation = suggest_category(
        ticket.title,
        ticket.description
    )

    priority, priority_confidence, priority_explanation = suggest_priority(
        ticket.title,
        ticket.description
    )

    return {
        "category": category,
        "category_confidence": category_confidence,
        "category_explanation": category_explanation,
        "priority": priority,
        "priority_confidence": priority_confidence,
        "priority_explanation": priority_explanation,
        "method": "rule-based"
    }