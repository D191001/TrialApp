import pytest
from fastapi.testclient import TestClient


def test_create_room(client: TestClient, auth_headers):
    room_data = {
        "name": "Test Room",
        "description": "Test Description",
        "is_private": False,
    }
    response = client.post(
        "/api/v1/rooms", json=room_data, headers=auth_headers
    )
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data["id"], int)
    assert data["name"] == room_data["name"]


def test_get_room(client: TestClient, auth_headers):
    response = client.get("/api/v1/rooms/1", headers=auth_headers)
    assert response.status_code == 200
    assert "id" in response.json()
    assert "participants" in response.json()


def test_invite_to_room(client: TestClient, auth_headers):
    invite_data = {"user_id": 2}
    response = client.post(
        "/api/v1/rooms/1/invite", json=invite_data, headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Пользователь приглашен"
