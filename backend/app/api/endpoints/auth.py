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
    client_id = os.getenv("YANDEX_CLIENT_ID")
    redirect_uri = os.getenv(
        "YANDEX_REDIRECT_URI", "https://trialapp.ru/callback"
    )

    auth_url = f"https://oauth.yandex.ru/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}"
    return {"auth_url": auth_url}


@router.get("/callback/yandex")
async def yandex_callback(code: str, db: Session = Depends(get_db)):
    client_id = os.getenv("YANDEX_CLIENT_ID")
    client_secret = os.getenv("YANDEX_CLIENT_SECRET")

    # TODO: Обменять код на токен
    return {"message": "Authentication successful"}
