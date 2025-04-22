from datetime import datetime
from typing import List, Optional

from app.api.deps import get_current_user
from app.db import models
from app.db.database import get_db
from app.schemas import feedback as feedback_schemas
from fastapi import APIRouter, Depends, HTTPException, Query, status
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


class CommentBase(BaseModel):
    text: str
    parent_id: Optional[int] = None


class CommentCreate(CommentBase):
    pass


class CommentUpdate(CommentBase):
    pass


class CommentResponse(CommentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    author_email: str

    class Config:
        orm_mode = True


@router.post("/comments", response_model=CommentResponse)
async def create_comment(
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if comment.parent_id:
        parent = (
            db.query(models.Comment)
            .filter(models.Comment.id == comment.parent_id)
            .first()
        )
        if not parent:
            raise HTTPException(
                status_code=404, detail="Parent comment not found"
            )

    db_comment = models.Comment(
        text=comment.text, user_id=current_user.id, parent_id=comment.parent_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


@router.get("/comments", response_model=List[CommentResponse])
async def get_comments(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    comments = (
        db.query(models.Comment)
        .filter(models.Comment.is_deleted == False)
        .order_by(models.Comment.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return comments


@router.put("/comments/{comment_id}", response_model=CommentResponse)
async def update_comment(
    comment_id: int,
    comment: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_comment = (
        db.query(models.Comment)
        .filter(models.Comment.id == comment_id)
        .first()
    )
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if db_comment.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this comment"
        )

    db_comment.text = comment.text
    db_comment.updated_at = datetime.utcnow()
    db.commit()
    return db_comment


@router.delete("/comments/{comment_id}")
async def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_comment = (
        db.query(models.Comment)
        .filter(models.Comment.id == comment_id)
        .first()
    )
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if db_comment.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this comment"
        )

    db_comment.is_deleted = True
    db.commit()
    return {"status": "success"}
