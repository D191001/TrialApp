from contextlib import asynccontextmanager

from app.api.api_v1.api import api_router
from app.core.config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup...")
    yield
    print("Application shutdown...")


app = FastAPI(
    title="TrialApp API",
    description="Backend API для приложения знакомств",
    version="1.0.0",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)

# CORS middleware с обновленными настройками
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Для разработки
        "http://localhost:8000",  # Для локального API
        "https://trialapp.ru",  # Для продакшена
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Роуты API
app.include_router(api_router, prefix="/api/v1")
