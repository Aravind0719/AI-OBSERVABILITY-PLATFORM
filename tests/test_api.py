from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_get_existing_trace():
    response = client.get("/traces/abc123")
    assert response.status_code == 200
    assert response.json() == {
    "trace_id": "abc123",
    "status": "completed",
    "service": "ai-observability-platform",
}

def test_trace_not_found():
    response = client.get("/traces/unknown123")
    assert response.status_code == 404
    assert response.json() == {
    "detail": "Trace not found"
}

def test_invalid_trace_id():
    response = client.get("/traces/a")
    assert response.status_code == 422

