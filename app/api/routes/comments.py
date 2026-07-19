import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import comment as comment_crud
from app.crud import task as task_crud
from app.db.session import get_db
from app.schemas.comment import ActivityLogOut, CommentCreate, CommentOut
from app.services.activity import log_activity

router = APIRouter(tags=["Comments & Activity"])


@router.post("/tasks/{task_id}/comments", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
def add_comment(task_id: uuid.UUID, comment_in: CommentCreate, db: Session = Depends(get_db)):
    task = task_crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    comment = comment_crud.create_comment(db, task_id, comment_in)
    log_activity(db, task_id, action="COMMENT_ADDED", detail=f"{comment_in.author_name} commented")
    return comment


@router.get("/tasks/{task_id}/comments", response_model=list[CommentOut])
def list_comments(task_id: uuid.UUID, db: Session = Depends(get_db)):
    task = task_crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    return comment_crud.list_comments_for_task(db, task_id)


@router.get("/tasks/{task_id}/activity", response_model=list[ActivityLogOut])
def get_task_activity(task_id: uuid.UUID, db: Session = Depends(get_db)):
    task = task_crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    return comment_crud.list_activity_for_task(db, task_id)