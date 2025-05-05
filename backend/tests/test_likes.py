import pytest
from fastapi.testclient import TestClient


def test_add_like(client: TestClient, auth_headers):
    response = client.post("/api/v1/likes/2", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Лайк добавлен"


def test_remove_like(client: TestClient, auth_headers):
    response = client.delete("/api/v1/likes/2", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Лайк удален"


def test_get_matches(client: TestClient, auth_headers):
    response = client.get("/api/v1/likes/matches", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
