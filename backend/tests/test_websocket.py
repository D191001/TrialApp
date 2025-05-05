import json

import pytest
from app.schemas.user import UserInDB
from fastapi.testclient import TestClient


def test_websocket_connection(client: TestClient):
    with client.websocket_connect("/api/v1/ws/1") as websocket:
        data = {"text": "Test message"}
        websocket.send_json(data)
        response = websocket.receive_json()
        assert "id" in response
        assert "text" in response
        assert response["text"] == data["text"]


def test_websocket_multiple_clients(client: TestClient):
    with client.websocket_connect("/api/v1/ws/1") as websocket1:
        with client.websocket_connect("/api/v1/ws/1") as websocket2:
            data = {"text": "Test message"}
            websocket1.send_json(data)
            response1 = websocket1.receive_json()
            response2 = websocket2.receive_json()
            assert response1 == response2
