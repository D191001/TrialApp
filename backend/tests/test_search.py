import pytest
from fastapi.testclient import TestClient


def test_search_users(client: TestClient, auth_headers):
    params = {
        "gender": "female",
        "min_age": 20,
        "max_age": 30,
        "distance": 10,
        "interests": "music,travel",
    }
    response = client.get(
        "/api/v1/search", params=params, headers=auth_headers
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    if len(response.json()) > 0:
        user = response.json()[0]
        assert "id" in user
        assert "name" in user
        assert "age" in user
        assert "gender" in user
        assert "distance" in user
        assert "interests" in user
