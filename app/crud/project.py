import uuid
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.task import Task, TaskStatusEnum
from app.schemas.project import ProjectCreate


def create_project(db: Session, project_in: ProjectCreate) -> Project:
    project = Project(**project_in.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def get_project(db: Session, project_id: uuid.UUID) -> Optional[Project]:
    return db.query(Project).filter(Project.id == project_id).first()


def list_projects(db: Session, skip: int = 0, limit: int = 50):
    return db.query(Project).order_by(Project.created_at.desc()).offset(skip).limit(limit).all()


def update_project(db: Session, project: Project, data: dict) -> Project:
    for field, value in data.items():
        setattr(project, field, value)
    db.commit()
    db.refresh(project)
    return project


def delete_project(db: Session, project: Project) -> None:
    db.delete(project)
    db.commit()


def get_project_task_stats(db: Session, project_id: uuid.UUID) -> dict:
    total = db.query(func.count(Task.id)).filter(Task.project_id == project_id).scalar()
    done = (
        db.query(func.count(Task.id))
        .filter(Task.project_id == project_id, Task.status == TaskStatusEnum.DONE)
        .scalar()
    )
    return {"total_tasks": total or 0, "done_tasks": done or 0}