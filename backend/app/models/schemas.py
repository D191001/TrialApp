from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    full_name: str | None = None

    class Config:
        from_attributes = True


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


class FeedbackBase(BaseModel):
    email: str
    comment: str

    class Config:
        from_attributes = True
