from pydantic import BaseModel


class TicketRequest(BaseModel):
    title: str
    description: str


class PredictionResponse(BaseModel):
    category: str
    category_confidence: float
    category_explanation: str

    impact: str
    impact_confidence: float
    impact_explanation: str

    urgency: str
    urgency_confidence: float
    urgency_explanation: str

    priority: str
    priority_confidence: float
    priority_explanation: str

    category_method: str
    priority_method: str