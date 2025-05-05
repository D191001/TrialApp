import pytest
from app.core.security import get_current_user
from app.main import app
from app.schemas.user import UserInDB, UserUpdate
from fastapi.testclient import TestClient


@pytest.fixture
def mock_user():
    return UserInDB(
        id=1,
        email="test@example.com",
        name="Test User",
        photo_url=None,
        age=None,
        gender=None,
        bio=None,
    )


@pytest.fixture
def auth_headers():
    return {"Authorization": "Bearer test-token"}


@pytest.fixture
def client(mock_user):
    async def override_get_current_user():
        return mock_user

    app.dependency_overrides[get_current_user] = override_get_current_user
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides = {}
