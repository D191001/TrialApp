import uuid

import httpx
from app.core.config import settings
from app.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
    verify_token,
)
from app.db.base import get_db
from app.models.user import User
from app.schemas.user import Token, UserCreate, UserLogin
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/register", response_model=Token)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Проверяем, не существует ли уже пользователь с таким email
    db_user = db.query(User).filter(User.email == user_data.email).first()
    if db_user:
        raise HTTPException(
            status_code=400, detail="Пользователь с таким email уже существует"
        )

    # Создаем нового пользователя
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        id=str(uuid.uuid4()),
        email=user_data.email,
        username=user_data.name,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Создаем токен доступа
    access_token = create_access_token(
        data={"sub": user_data.email, "user_id": db_user.id}
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
async def login(form_data: UserLogin, db: Session = Depends(get_db)):
    # Ищем пользователя по email
    user = db.query(User).filter(User.email == form_data.email).first()
    if not user or not user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
        )

    # Проверяем пароль
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
        )

    # Генерируем токен
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id}
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/yandex")
async def login_yandex():
    params = {
        "response_type": "code",
        "client_id": settings.YANDEX_CLIENT_ID,
        "redirect_uri": settings.YANDEX_REDIRECT_URI,
        "scope": "login:email",
    }
    url = "https://oauth.yandex.ru/authorize?" + "&".join(
        f"{k}={v}" for k, v in params.items()
    )
    return {"auth_url": url}


@router.get("/yandex/callback")
async def yandex_callback(code: str, db: Session = Depends(get_db)):
    # Обмен code на OAuth-токен через запрос к Яндексу
    async with httpx.AsyncClient() as client:
        token_resp = await client.post(
            "https://oauth.yandex.ru/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": settings.YANDEX_CLIENT_ID,
                "client_secret": settings.YANDEX_CLIENT_SECRET,
                "redirect_uri": settings.YANDEX_REDIRECT_URI,
            },
        )
        # Явная обработка ошибки "code has expired"
        if token_resp.status_code != 200:
            try:
                error_data = token_resp.json()
                if error_data.get(
                    "error"
                ) == "invalid_grant" and "expired" in error_data.get(
                    "error_description", ""
                ):
                    raise HTTPException(
                        status_code=400,
                        detail="Код авторизации Яндекса истёк или уже был использован. Пожалуйста, начните авторизацию заново и получите новый code.",
                    )
            except Exception:
                pass
            raise HTTPException(
                status_code=400,
                detail="Ошибка обмена кода на токен. Проверьте корректность кода авторизации или повторите процесс входа через Яндекс.",
            )
        token_data = token_resp.json()
        # 2. Получаем профиль пользователя из Яндекс ID
        user_resp = await client.get(
            "https://login.yandex.ru/info",
            headers={"Authorization": f"OAuth {token_data['access_token']}"},
        )
        if user_resp.status_code != 200:
            raise HTTPException(
                status_code=400, detail="User info fetch failed"
            )
        user_info = user_resp.json()

        # 3. Создаём или ищем пользователя в базе
        user_id = user_info.get("id")
        email = user_info.get("default_email")
        name = user_info.get("real_name") or user_info.get("display_name")
        avatar = user_info.get("default_avatar_id")

        # Поиск пользователя в базе
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            user = User(
                id=user_id, email=email, username=name, photo_url=avatar
            )  # изменено: name -> username
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            # Обновляем данные пользователя, если что-то изменилось
            user.email = email
            user.username = name  # изменено: name -> username
            user.photo_url = avatar
            db.commit()
            db.refresh(user)

        # 4. Генерируем JWT-токен для сессии
        jwt_token = create_access_token(subject=user_id)

        # 5. Возвращаем JWT-токен клиенту в cookie и в теле ответа
        response = JSONResponse(
            content={
                "access_token": jwt_token,
                "token_type": "bearer",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "name": user.username,  # оставляем как есть, т.к. уже исправлено
                    "avatar": user.photo_url,
                },
            }
        )
        response.set_cookie(
            key="access_token",
            value=jwt_token,
            httponly=True,
            secure=True,
            samesite="lax",
        )
        return response


async def get_current_user_from_jwt(request: Request):
    token = request.cookies.get("access_token")
    # Также ищем токен в query-параметре ?token=...
    if not token:
        token = request.query_params.get("token")
    if not token or not await verify_token(token):
        raise HTTPException(
            status_code=401, detail="Invalid or missing JWT token"
        )
    # Здесь можно декодировать токен и получить user_id, затем найти пользователя в БД
    # user_id = decode_jwt(token)
    # user = get_user_by_id(user_id)
    # return user
    return {"user_id": "from_jwt"}  # Заглушка


# Теперь вы можете использовать Depends(get_current_user_from_jwt) для защиты маршрутов FastAPI.


@router.get("/user/{user_id}")
async def get_user_by_id(user_id: str):
    # Здесь должна быть реальная логика поиска пользователя в БД по user_id
    # user = get_user_by_id_from_db(user_id)
    # if not user:
    #     raise HTTPException(status_code=404, detail="Пользователь не найден")
    # return user
    return {
        "id": user_id,
        "email": "user@example.com",
        "name": "Demo User",
        "avatar": None,
    }
