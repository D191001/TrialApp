import os

import httpx
from app.db.database import get_db
from app.services import yandex_oauth
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/login/yandex")
async def yandex_login():
    client_id = os.getenv("YANDEX_CLIENT_ID")
    redirect_uri = "https://trialapp.ru/callback"

    if not client_id:
        raise HTTPException(
            status_code=500, detail="YANDEX_CLIENT_ID not configured"
        )

    auth_url = f"https://oauth.yandex.ru/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}"
    return {"auth_url": auth_url}


@router.get("/callback/yandex")
async def yandex_callback(code: str, db: Session = Depends(get_db)):
    try:
        client_id = os.getenv("YANDEX_CLIENT_ID")
        client_secret = os.getenv("YANDEX_CLIENT_SECRET")

        # В будущем здесь будет обмен кода на токен
        return {"access_token": "temporary_token", "token_type": "bearer"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
