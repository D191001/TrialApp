import os

import httpx
from app.db.database import get_db
from app.services import yandex_oauth
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/login/yandex")
async def login_yandex():
    return {
        "auth_url": f"{yandex_oauth.YANDEX_AUTH_URL}?response_type=code&client_id={os.getenv('YANDEX_CLIENT_ID')}"
    }


@router.get("/callback/yandex")
async def yandex_callback(code: str, db: Session = Depends(get_db)):
    async with httpx.AsyncClient() as client:
        # Получаем токен
        token_response = await client.post(
            yandex_oauth.YANDEX_TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": os.getenv("YANDEX_CLIENT_ID"),
                "client_secret": os.getenv("YANDEX_CLIENT_SECRET"),
            },
        )
        token_data = token_response.json()

        # Получаем информацию о пользователе
        user_info = await yandex_oauth.get_yandex_user_info(
            token_data["access_token"]
        )

        # Создаем JWT токен
        access_token = yandex_oauth.create_access_token(
            {"sub": user_info["email"]}
        )

        return {"access_token": access_token, "token_type": "bearer"}
