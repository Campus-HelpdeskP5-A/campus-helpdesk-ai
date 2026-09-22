from pydantic import BaseModel
from typing import Optional, List, Dict, Any


# ---------- Request shapes ----------

class TicketTextRequest(BaseModel):
    title: str
    description: str


class SLARiskRequest(BaseModel):
    workload: str          # "Low" | "Medium" | "High"
    priority: str          # "Low" | "Medium" | "High" | "Critical"
    ticket_age_hours: float


class ExistingTicket(BaseModel):
    id: str
    text: str


class DuplicateRequest(BaseModel):
    title: str
    description: str
    existing_tickets: List[ExistingTicket]


# ---------- Unified response shape (matches predictions table) ----------

class PredictionResponse(BaseModel):
    prediction_type: str          # "CATEGORY" | "PRIORITY" | "SLA_RISK" | "DUPLICATE"
    value: Dict[str, Any]
    confidence: float
    model_version: str
    explanation: str