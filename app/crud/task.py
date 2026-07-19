import uuid
from typing import Optional

from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate


def create_task(db: Session, project_id: uuid.UUID, task_in: TaskCreate) -> Task:
    task = Task(project_id=project_id, **task_in.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_task(db: Session, task_id: uuid.UUID) -> Optional[Task]:
    return db.query(Task).filter(Task.id == task_id).first()


def list_tasks_for_project(
    db: Session,
    project_id: uuid.UUID,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
):
    query = db.query(Task).filter(Task.project_id == project_id)
    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    return query.order_by(Task.created_at.desc()).offset(skip).limit(limit).all()


def update_task(db: Session, task: Task, data: dict) -> Task:
    for field, value in data.items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: Task) -> None:
    db.delete(task)
    db.commit()