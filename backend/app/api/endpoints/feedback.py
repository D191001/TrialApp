from datetime import datetime
from typing import List

from app.api.deps import get_current_user
from app.db import models
from app.db.database import get_db
from app.schemas import feedback as feedback_schemas
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
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


class CommentCreate(BaseModel):
    text: str


class CommentResponse(BaseModel):
    id: int
    text: str
    created_at: datetime
    author_name: str
    author_email: str


@router.post("/comments", response_model=CommentResponse)
async def create_comment(
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    new_comment = models.Comment(
        text=comment.text,
        user_id=current_user.id,
        created_at=datetime.utcnow(),
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return {
        "id": new_comment.id,
        "text": new_comment.text,
        "created_at": new_comment.created_at,
        "author_name": current_user.full_name,
        "author_email": current_user.email,
    }


@router.get("/comments", response_model=List[CommentResponse])
async def get_comments(db: Session = Depends(get_db)):
    comments = (
        db.query(models.Comment)
        .order_by(models.Comment.created_at.desc())
        .all()
    )
    return [
        {
            "id": comment.id,
            "text": comment.text,
            "created_at": comment.created_at,
            "author_name": comment.author.full_name,
            "author_email": comment.author.email,
        }
        for comment in comments
    ]
