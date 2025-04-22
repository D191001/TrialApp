from datetime import datetime

from pydantic import BaseModel


class FeedbackBase(BaseModel):
    message: str


class FeedbackCreate(FeedbackBase):
    pass


class Feedback(FeedbackBase):
    id: int
    user_id: int
    user_name: str
    created_at: datetime

    class Config:
        from_attributes = True
