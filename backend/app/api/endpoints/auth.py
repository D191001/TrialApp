import os
from datetime import datetime, timedelta
from typing import Optional

import jwt
import requests
from app.api.deps import get_current_user
from app.core.config import settings
from app.db.database import get_db
from app.db.models import User
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

router = APIRouter()


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str


@router.get("/login/yandex")
def yandex_login():
    """
    Эндпоинт для начала OAuth авторизации через Яндекс
    """
    return {
        "auth_url": f"https://oauth.yandex.ru/authorize?response_type=code&client_id={settings.YANDEX_CLIENT_ID}&redirect_uri={settings.YANDEX_REDIRECT_URI}"
    }


@router.get("/callback/yandex")
async def yandex_callback(
    code: str = None,
    error: str = None,
    error_description: str = None,
    db: Session = Depends(get_db),
):
    """
    Обработчик callback от Яндекса
    """
    if error:
        raise HTTPException(
            status_code=400,
            detail=f"Authorization failed: {error}. {error_description}",
        )

    try:
        # Запрос токена
        token_response = requests.post(
            "https://oauth.yandex.ru/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": settings.YANDEX_CLIENT_ID,
                "client_secret": settings.YANDEX_CLIENT_SECRET,
                "redirect_uri": settings.YANDEX_REDIRECT_URI,
            },
        )

        if token_response.status_code != 200:
            raise HTTPException(
                status_code=400,
                detail=f"Token exchange failed: {token_response.text}",
            )

        token_data = TokenResponse(**token_response.json())
        expires_at = datetime.utcnow() + timedelta(
            seconds=token_data.expires_in
        )

        # Получаем информацию о пользователе с правильным параметром
        user_response = requests.get(
            "https://login.yandex.ru/info",
            params={"oauth_token": token_data.access_token},
        )

        if user_response.status_code != 200:
            raise HTTPException(
                status_code=400, detail="Failed to get user info"
            )

        user_info = user_response.json()

        # Обновляем или создаем пользователя
        user = (
            db.query(User)
            .filter(User.yandex_id == str(user_info["id"]))
            .first()
        )
        if not user:
            user = User(
                email=user_info["default_email"],
                yandex_id=str(user_info["id"]),
                access_token=token_data.access_token,
                refresh_token=token_data.refresh_token,
                token_expires=expires_at,
                full_name=user_info.get("real_name", ""),
                is_active=True,
            )
            db.add(user)
        else:
            user.access_token = token_data.access_token
            user.refresh_token = token_data.refresh_token
            user.token_expires = expires_at
            user.last_login = datetime.utcnow()

        db.commit()

        return {
            "status": "success",
            "email": user.email,
            "expires_in": token_data.expires_in,
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


async def refresh_yandex_token(refresh_token: str, db: Session) -> User:
    """
    Обновление токена доступа
    """
    try:
        token_response = requests.post(
            "https://oauth.yandex.ru/token",
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": settings.YANDEX_CLIENT_ID,
                "client_secret": settings.YANDEX_CLIENT_SECRET,
            },
        )

        if token_response.status_code != 200:
            raise HTTPException(
                status_code=401, detail="Failed to refresh token"
            )

        token_data = TokenResponse(**token_response.json())

        # Обновляем токены в базе
        user = (
            db.query(User).filter(User.refresh_token == refresh_token).first()
        )

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.access_token = token_data.access_token
        user.refresh_token = token_data.refresh_token
        user.token_expires = datetime.utcnow() + timedelta(
            seconds=token_data.expires_in
        )

        db.commit()
        return user

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


async def get_user_with_valid_token(user: User, db: Session) -> User:
    """
    Проверка и обновление токена если нужно
    """
    if user.token_expires and user.token_expires <= datetime.utcnow():
        try:
            user = await refresh_yandex_token(user.refresh_token, db)
        except HTTPException:
            raise HTTPException(status_code=401, detail="Token expired")
    return user


@router.get("/me")
async def get_current_user(token: str, db: Session = Depends(get_db)):
    """
    Проверка текущего пользователя
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user = db.query(User).filter(User.id == payload["user_id"]).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Проверяем валидность токена
        user = await get_user_with_valid_token(user, db)

        return {
            "email": user.email,
            "full_name": user.full_name,
            "avatar_url": user.avatar_url,
        }
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
