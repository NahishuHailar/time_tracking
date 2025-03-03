from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_project():
    response = client.get("/api/v1/projects/1")
    assert response.status_code == 200