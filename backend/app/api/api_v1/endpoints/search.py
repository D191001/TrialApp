from typing import List

from app.core.security import get_current_user
from app.schemas.search import SearchParams, UserSearchResult
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("", response_model=List[UserSearchResult])
async def search_users(
    gender: str = None,
    min_age: int = None,
    max_age: int = None,
    distance: float = None,
    interests: str = None,
    current_user=Depends(get_current_user),
):
    # Здесь будет логика поиска
    return [
        {
            "id": 2,
            "name": "Другой пользователь",
            "age": 28,
            "gender": "female",
            "distance": 5.3,
            "interests": ["music", "travel"],
        }
    ]
