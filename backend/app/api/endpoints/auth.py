import os
from datetime import datetime, timedelta

import jwt
import requests
from app.api.deps import get_current_user
from app.core.config import settings
from app.db.database import get_db
from app.db.models import User
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/login/yandex")
def yandex_login():
    """
    Эндпоинт для начала OAuth авторизации через Яндекс
    """
    return {
        "auth_url": f"https://oauth.yandex.ru/authorize?response_type=code&client_id={settings.YANDEX_CLIENT_ID}&redirect_uri={settings.YANDEX_REDIRECT_URI}"
    }


@router.get("/callback/yandex")
async def yandex_callback(code: str, db: Session = Depends(get_db)):
    """
    Обработчик callback от Яндекса
    """
    try:
        # Получаем токены
        token_data = requests.post(
            "https://oauth.yandex.ru/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": settings.YANDEX_CLIENT_ID,
                "client_secret": settings.YANDEX_CLIENT_SECRET,
            },
        ).json()

        # Получаем информацию о пользователе
        user_info = requests.get(
            "https://login.yandex.ru/info",
            headers={"Authorization": f"OAuth {token_data['access_token']}"},
        ).json()

        # Создаем или обновляем пользователя
        user = (
            db.query(User)
            .filter(User.yandex_id == str(user_info["id"]))
            .first()
        )
        if not user:
            user = User(
                email=user_info["default_email"],
                full_name=user_info.get("real_name", ""),
                yandex_id=str(user_info["id"]),
                access_token=token_data["access_token"],
                refresh_token=token_data.get("refresh_token"),
                token_expires=datetime.utcnow()
                + timedelta(seconds=token_data["expires_in"]),
                avatar_url=user_info.get("default_avatar_id"),
            )
            db.add(user)
        else:
            user.last_login = datetime.utcnow()
            user.access_token = token_data["access_token"]
            user.refresh_token = token_data.get("refresh_token")
            user.token_expires = datetime.utcnow() + timedelta(
                seconds=token_data["expires_in"]
            )

        db.commit()

        # Создаем JWT токен для клиента
        token = jwt.encode(
            {"user_id": user.id, "exp": datetime.utcnow() + timedelta(days=1)},
            settings.SECRET_KEY,
            algorithm="HS256",
        )

        return {
            "status": "registered",
            "email": user.email,
            "token": token,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/me")
async def get_current_user(token: str, db: Session = Depends(get_db)):
    """
    Проверка текущего пользователя
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user = db.query(User).filter(User.id == payload["user_id"]).first()
        return {
            "email": user.email,
            "full_name": user.full_name,
            "avatar_url": user.avatar_url,
        }
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
