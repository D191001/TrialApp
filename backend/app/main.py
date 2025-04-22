from app.api.endpoints import auth, feedback, users
from app.core.config import settings
from app.db import models
from app.db.database import engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Инициализация базы данных
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TrialApp API",
    description="Backend API с OAuth2 авторизацией через Яндекс и системой комментариев",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://trialapp.ru",
        "http://localhost:8000",
        "https://oauth.yandex.ru",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Подключение роутеров с префиксами
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(feedback.router, prefix="/api/feedback", tags=["feedback"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
