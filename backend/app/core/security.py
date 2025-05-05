from datetime import UTC, datetime, timedelta
from typing import Dict

import httpx
from app.core.config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

# Инициализация компонентов безопасности
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# Обновляем create_access_token для использования email
def create_access_token(*, data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = {"email": email}
        return token_data
    except JWTError:
        raise credentials_exception


# Оставляем существующие функции для Яндекс OAuth
async def get_yandex_user_info(token: str) -> Dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://login.yandex.ru/info",
            headers={"Authorization": f"OAuth {token}"},
        )
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid Yandex token")
        return response.json()


async def verify_token(token: str) -> bool:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[ALGORITHM]
        )
        return bool(payload.get("sub"))
    except JWTError:
        return False
