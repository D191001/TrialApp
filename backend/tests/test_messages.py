import pytest
from fastapi.testclient import TestClient


def test_send_message(client: TestClient, auth_headers):
    message_data = {"text": "Test message"}
    response = client.post(
        "/api/v1/rooms/1/messages", json=message_data, headers=auth_headers
    )
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data["id"], int)
    assert data["text"] == message_data["text"]


def test_get_messages(client: TestClient, auth_headers):
    response = client.get("/api/v1/rooms/1/messages", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
