import enum

from app.db.base_class import Base
from sqlalchemy import Column, DateTime, Enum, Integer, String, Text, func


class Gender(str, enum.Enum):
    male = "male"
    female = "female"


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    email = Column(String, unique=True)
    username = Column(String)  # используем username вместо name
    hashed_password = Column(
        String, nullable=True
    )  # Добавляем поле для хэша пароля
    age = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    photo_url = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
