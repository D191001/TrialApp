from app.api.endpoints import auth, feedback, users
from app.db import models
from app.db.database import engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Добавляем CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://localhost:8000",
        "https://trialapp.ru",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Set-Cookie", "Authorization"],
    expose_headers=["Set-Cookie"],
)

# Роуты с префиксом api для соответствия конфигурации фронтенда
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(feedback.router, prefix="/api/feedback", tags=["feedback"])


@app.get("/health-check")
async def health_check():
    """
    Простой эндпоинт для проверки работоспособности
    """
    return {"status": "healthy"}


@app.get("/")
async def root():
    return {"message": "API is running"}
