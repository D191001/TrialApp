from app.db import models
from app.db.database import get_db
from app.schemas import feedback as feedback_schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/feedback", response_model=feedback_schemas.Feedback)
def create_feedback(
    feedback: feedback_schemas.FeedbackCreate, db: Session = Depends(get_db)
):
    db_feedback = models.Feedback(**feedback.dict())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback
