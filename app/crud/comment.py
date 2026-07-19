import uuid

from sqlalchemy.orm import Session

from app.models.activity_log import ActivityLog
from app.models.comment import Comment
from app.schemas.comment import CommentCreate


def create_comment(db: Session, task_id: uuid.UUID, comment_in: CommentCreate) -> Comment:
    comment = Comment(task_id=task_id, **comment_in.model_dump())
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def list_comments_for_task(db: Session, task_id: uuid.UUID, skip: int = 0, limit: int = 100):
    return (
        db.query(Comment)
        .filter(Comment.task_id == task_id)
        .order_by(Comment.created_at.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def list_activity_for_task(db: Session, task_id: uuid.UUID, skip: int = 0, limit: int = 100):
    return (
        db.query(ActivityLog)
        .filter(ActivityLog.task_id == task_id)
        .order_by(ActivityLog.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )