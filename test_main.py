from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_read_items():
    with TestClient(app) as client:
        response = client.get("/cars")
        data = response.json()
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        assert len(response.json()) == 25
        assert data[0]["price"] == 1300
