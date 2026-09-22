from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_predict_category_shape():
    response = client.post("/predict/category", json={
        "title": "AC is not cooling",
        "description": "The AC in the lab is not cooling properly",
    })

    assert response.status_code == 200
    data = response.json()

    assert data["prediction_type"] == "CATEGORY"
    assert "category" in data["value"]
    assert 0 <= data["confidence"] <= 1
    assert data["model_version"].startswith("category-")
    assert data["explanation"]


def test_predict_priority_shape():
    response = client.post("/predict/priority", json={
        "title": "Fire in the building",
        "description": "Everyone is in danger",
    })

    assert response.status_code == 200
    data = response.json()

    assert data["prediction_type"] == "PRIORITY"
    assert data["value"]["priority"] == "Critical"
    assert data["value"]["impact"] == "High"
    assert data["value"]["urgency"] == "High"
    assert data["model_version"] == "priority-rules-v1"


def test_predict_sla_risk_shape():
    response = client.post("/predict/sla-risk", json={
        "workload": "High",
        "priority": "Critical",
        "ticket_age_hours": 20,
    })

    assert response.status_code == 200
    data = response.json()

    assert data["prediction_type"] == "SLA_RISK"
    assert data["value"]["sla_risk"] is True
    assert data["model_version"] == "sla-rules-v1"


def test_predict_duplicate_shape():
    response = client.post("/predict/duplicate", json={
        "title": "AC not working in room 101",
        "description": "",
        "existing_tickets": [
            {"id": "t1", "text": "AC not working in room 101"},
            {"id": "t2", "text": "Wifi is down in the library"},
        ],
    })

    assert response.status_code == 200
    data = response.json()

    assert data["prediction_type"] == "DUPLICATE"
    assert "candidates" in data["value"]
    assert data["model_version"] == "duplicate-tfidf-v1"


def test_predict_duplicate_empty_pool():
    response = client.post("/predict/duplicate", json={
        "title": "AC issue",
        "description": "room 101",
        "existing_tickets": [],
    })

    assert response.status_code == 200
    data = response.json()

    assert data["value"]["candidates"] == []
    assert data["confidence"] == 0.0