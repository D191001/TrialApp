from app.db.database import get_db
from app.schemas import users as user_schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/register/yandex", response_model=user_schemas.User)
async def register_user_with_yandex(token: str, db: Session = Depends(get_db)):
    try:
        # Тут будет логика регистрации через Яндекс
        user = user_schemas.User(
            id=1,
            email="test@example.com",
            full_name="Test User",
            is_active=True,
        )
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
