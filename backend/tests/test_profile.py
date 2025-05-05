import pytest
from fastapi.testclient import TestClient


def test_get_profile(client: TestClient, auth_headers, mock_user):
    response = client.get("/api/v1/profile", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == mock_user.id
    assert data["email"] == mock_user.email


def test_update_profile(client: TestClient, auth_headers):
    update_data = {"bio": "New bio", "age": 26, "gender": "female"}
    response = client.put(
        "/api/v1/profile", json=update_data, headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Профиль успешно обновлен"


def test_upload_photo(client: TestClient, auth_headers):
    files = {"photo": ("test.jpg", b"test content", "image/jpeg")}
    response = client.post(
        "/api/v1/profile/photos", files=files, headers=auth_headers
    )
    assert response.status_code == 200
    assert "photo_url" in response.json()
