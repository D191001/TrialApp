import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse

router = APIRouter()


@router.get("/auth/login/yandex")
async def login_yandex():
    """
    Эндпоинт для начала OAuth авторизации через Яндекс
    """
    client_id = os.getenv("YANDEX_CLIENT_ID")
    redirect_uri = os.getenv("YANDEX_REDIRECT_URI")

    if not client_id:
        raise HTTPException(
            status_code=500, detail="YANDEX_CLIENT_ID not configured"
        )

    auth_url = (
        f"https://oauth.yandex.ru/authorize?"
        f"response_type=code&"
        f"client_id={client_id}&"
        f"redirect_uri={redirect_uri}"
    )

    return {"auth_url": auth_url}


@router.get("/auth/callback/yandex")
async def yandex_callback(code: str):
    """
    Обработчик callback от Яндекса
    """
    return {"status": "success", "auth_code": code}
