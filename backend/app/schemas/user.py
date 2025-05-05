from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class Gender(str, Enum):
    male = "male"
    female = "female"


class UserBase(BaseModel):
    email: EmailStr
    name: str
    age: Optional[int] = None
    gender: Optional[Gender] = None
    bio: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: str | None = None
    user_id: str | None = None


class UserInDB(UserBase):
    id: int
    photo_url: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    bio: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[Gender] = None
    model_config = ConfigDict(from_attributes=True)
