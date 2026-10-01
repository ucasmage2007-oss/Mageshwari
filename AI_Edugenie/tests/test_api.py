import os

# Prevent accidental real API calls during tests.
os.environ["GEMINI_API_KEY"] = ""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "EduGenie" in response.text


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_validation_rejects_empty_text():
    response = client.post("/qa", json={"text": ""})
    assert response.status_code == 422


def test_quiz_validation():
    response = client.post("/quiz", json={"text": "Solar energy comes from the Sun.", "count": 0})
    assert response.status_code == 422
