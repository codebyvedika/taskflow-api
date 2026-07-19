import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import project as project_crud
from app.crud import task as task_crud
from app.db.session import get_db
from app.schemas.task import TaskCreate, TaskOut, TaskStatusUpdate, TaskUpdate
from app.services.activity import log_activity

router = APIRouter(tags=["Tasks"])


@router.post("/projects/{project_id}/tasks", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(project_id: uuid.UUID, task_in: TaskCreate, db: Session = Depends(get_db)):
    project = project_crud.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    task = task_crud.create_task(db, project_id, task_in)
    log_activity(db, task.id, action="TASK_CREATED", detail=f"Task '{task.title}' created")
    return task


@router.get("/projects/{project_id}/tasks", response_model=list[TaskOut])
def list_tasks(
    project_id: uuid.UUID,
    status_filter: Optional[str] = None,
    priority_filter: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    project = project_crud.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    return task_crud.list_tasks_for_project(
        db, project_id, status=status_filter, priority=priority_filter, skip=skip, limit=limit
    )


@router.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: uuid.UUID, db: Session = Depends(get_db)):
    task = task_crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.patch("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: uuid.UUID, task_in: TaskUpdate, db: Session = Depends(get_db)):
    task = task_crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    data = task_in.model_dump(exclude_unset=True)
    updated = task_crud.update_task(db, task, data)
    log_activity(db, task.id, action="TASK_UPDATED", detail=f"Fields updated: {', '.join(data.keys())}")
    return updated


@router.patch("/tasks/{task_id}/status", response_model=TaskOut)
def update_task_status(task_id: uuid.UUID, status_in: TaskStatusUpdate, db: Session = Depends(get_db)):
    task = task_crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    old_status = task.status.value
    updated = task_crud.update_task(db, task, {"status": status_in.status})
    log_activity(
        db,
        task.id,
        action="STATUS_CHANGED",
        detail=f"Status moved from '{old_status}' to '{status_in.status.value}'",
    )
    return updated


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: uuid.UUID, db: Session = Depends(get_db)):
    task = task_crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    task_crud.delete_task(db, task)
    return None