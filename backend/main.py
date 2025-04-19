from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.endpoints import auth, feedback, users
from backend.app.db import models
from backend.app.db.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Добавляем CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
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
