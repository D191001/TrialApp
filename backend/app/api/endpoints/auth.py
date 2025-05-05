import httpx
from app.core import security
from app.core.config import settings
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


@router.post("/yandex")
async def login_yandex():
    return {
        "url": f"https://oauth.yandex.ru/authorize?response_type=code&client_id={settings.YANDEX_CLIENT_ID}"
    }


@router.get("/yandex/callback")
async def yandex_callback(code: str):
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://oauth.yandex.ru/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": settings.YANDEX_CLIENT_ID,
                "client_secret": settings.YANDEX_CLIENT_SECRET,
            },
        )

        if token_response.status_code != 200:
            raise HTTPException(
                status_code=400, detail="Could not validate credentials"
            )

        access_token = security.create_access_token(
            token_response.json().get("access_token")
        )
        return {"access_token": access_token, "token_type": "bearer"}
