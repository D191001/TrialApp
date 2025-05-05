from app.core.security import get_current_user
from app.schemas.user import UserInDB
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/{user_id}")
async def add_like(
    user_id: int, current_user: UserInDB = Depends(get_current_user)
):
    return {"message": "Лайк добавлен"}


@router.delete("/{user_id}")
async def remove_like(
    user_id: int, current_user: UserInDB = Depends(get_current_user)
):
    return {"message": "Лайк удален"}


@router.get("/matches")
async def get_matches(current_user: UserInDB = Depends(get_current_user)):
    return [
        {
            "id": 3,
            "name": "Пользователь из матча",
            "age": 27,
            "gender": "male",
            "email": "match@example.com",
        }
    ]
