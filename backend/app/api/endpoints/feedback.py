from typing import List

from app.api.deps import get_current_user
from app.db import models
from app.db.database import get_db
from app.schemas import feedback as feedback_schemas
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/", response_model=List[feedback_schemas.Feedback])
def get_feedbacks(
    db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    return db.query(models.Feedback).all()


@router.post("/", response_model=feedback_schemas.Feedback)
def create_feedback(
    feedback: feedback_schemas.FeedbackCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        db_feedback = models.Feedback(
            **feedback.dict(),
            user_id=current_user.id,
            user_name=current_user.email
        )
        db.add(db_feedback)
        db.commit()
        db.refresh(db_feedback)
        return db_feedback
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
