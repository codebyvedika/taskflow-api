import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import project as project_crud
from app.db.session import get_db
from app.schemas.project import ProjectCreate, ProjectOut, ProjectUpdate, ProjectWithStats

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(project_in: ProjectCreate, db: Session = Depends(get_db)):
    return project_crud.create_project(db, project_in)


@router.get("", response_model=list[ProjectOut])
def list_projects(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return project_crud.list_projects(db, skip=skip, limit=limit)


@router.get("/{project_id}", response_model=ProjectWithStats)
def get_project(project_id: uuid.UUID, db: Session = Depends(get_db)):
    project = project_crud.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    stats = project_crud.get_project_task_stats(db, project_id)
    return ProjectWithStats(**ProjectOut.model_validate(project).model_dump(), **stats)


@router.patch("/{project_id}", response_model=ProjectOut)
def update_project(project_id: uuid.UUID, project_in: ProjectUpdate, db: Session = Depends(get_db)):
    project = project_crud.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    data = project_in.model_dump(exclude_unset=True)
    return project_crud.update_project(db, project, data)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: uuid.UUID, db: Session = Depends(get_db)):
    project = project_crud.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    project_crud.delete_project(db, project)
    return None