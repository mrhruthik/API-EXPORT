from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "success"


def test_leads_endpoint():
    response = client.get("/leads")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_outreach_summary():
    response = client.get("/outreach/summary")

    assert response.status_code == 200

    data = response.json()

    assert "total_leads" in data
    assert "sent" in data


def test_docs_available():
    response = client.get("/docs")

    assert response.status_code == 200