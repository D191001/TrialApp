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
    allow_methods=["*"],
    allow_headers=["*"],
)

# Роуты
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(feedback.router, prefix="/feedback", tags=["feedback"])


@app.get("/health-check")
async def health_check():
    return {"status": "healthy"}


@app.get("/")
async def root():
    return {"message": "API is running"}
