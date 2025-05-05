from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Получаем абсолютный путь к корневой директории проекта
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Settings(BaseSettings):
    PROJECT_NAME: str = "TrialApp"
    YANDEX_CLIENT_ID: str
    YANDEX_CLIENT_SECRET: str
    JWT_SECRET: str
    DATABASE_URL: str
    ALLOWED_HOSTS: str
    YANDEX_REDIRECT_URI: str
    DEBUG: bool = False
    DB_HOST: str
    DB_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    model_config = SettingsConfigDict(
        env_file=str(ROOT_DIR / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


settings = Settings()
