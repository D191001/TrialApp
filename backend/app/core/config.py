import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    YANDEX_CLIENT_ID: str = "your-client-id"
    YANDEX_CLIENT_SECRET: str = "your-client-secret"
    YANDEX_REDIRECT_URI: str = "http://localhost:8000/api/auth/callback/yandex"
    SECRET_KEY: str = "your-secret-key"

    class Config:
        env_file = ".env"


settings = Settings()

DATABASE_URL = os.getenv("DATABASE_URL")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
