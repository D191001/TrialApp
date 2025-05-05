from unittest.mock import AsyncMock, patch

import pytest
from app.schemas.user import UserCreate, UserLogin
from fastapi.testclient import TestClient


def test_register(client: TestClient):
    user_data = {
        "email": "test@example.com",
        "name": "Test User",
        "password": "testpassword123",
    }
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_register_duplicate_email(client: TestClient):
    user_data = {
        "email": "duplicate@example.com",
        "name": "Test User",
        "password": "testpassword123",
    }
    # Первая регистрация
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 200

    # Повторная регистрация с тем же email
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 400
    assert "уже существует" in response.json()["detail"]


def test_login_success(client: TestClient):
    # Сначала регистрируем пользователя
    user_data = {
        "email": "login@example.com",
        "name": "Login Test",
        "password": "testpassword123",
    }
    client.post("/api/v1/auth/register", json=user_data)

    # Пробуем залогиниться
    login_data = {"email": "login@example.com", "password": "testpassword123"}
    response = client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client: TestClient):
    # Сначала регистрируем пользователя
    user_data = {
        "email": "wrong@example.com",
        "name": "Wrong Password Test",
        "password": "testpassword123",
    }
    client.post("/api/v1/auth/register", json=user_data)

    # Пробуем залогиниться с неверным паролем
    login_data = {"email": "wrong@example.com", "password": "wrongpassword"}
    response = client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 401
    assert "Неверный email или пароль" in response.json()["detail"]


@pytest.fixture
def mock_yandex_user_info():
    return {
        "id": "12345",
        "default_email": "yandex@example.com",
        "display_name": "Yandex User",
        "real_name": "Real Name",
        "default_avatar_id": "avatar123",
    }


@pytest.fixture
def mock_yandex_token():
    return {"access_token": "test_token"}


@patch("httpx.AsyncClient.post")
@patch("httpx.AsyncClient.get")
async def test_yandex_callback(
    mock_get,
    mock_post,
    client: TestClient,
    mock_yandex_token,
    mock_yandex_user_info,
):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json = lambda: mock_yandex_token

    mock_get.return_value.status_code = 200
    mock_get.return_value.json = lambda: mock_yandex_user_info

    response = client.get("/api/v1/auth/yandex/callback?code=test_code")
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "user" in data
    assert data["user"]["email"] == mock_yandex_user_info["default_email"]
