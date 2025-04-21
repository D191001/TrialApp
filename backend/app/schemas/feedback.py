from pydantic import BaseModel


class FeedbackBase(BaseModel):
    email: str
    comment: str


class FeedbackCreate(FeedbackBase):
    pass


class Feedback(FeedbackBase):
    id: int

    class Config:
        from_attributes = True
