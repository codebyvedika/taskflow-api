import uuid
from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from app.models.task import TaskStatusEnum, TaskPriorityEnum


class TaskCreate(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    description: Optional[str] = None
    priority: TaskPriorityEnum = TaskPriorityEnum.MEDIUM
    assignee_name: Optional[str] = Field(default=None, max_length=120)
    due_date: Optional[date] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=2, max_length=200)
    description: Optional[str] = None
    priority: Optional[TaskPriorityEnum] = None
    assignee_name: Optional[str] = Field(default=None, max_length=120)
    due_date: Optional[date] = None


class TaskStatusUpdate(BaseModel):
    status: TaskStatusEnum


class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    project_id: uuid.UUID
    title: str
    description: Optional[str]
    status: TaskStatusEnum
    priority: TaskPriorityEnum
    assignee_name: Optional[str]
    due_date: Optional[date]
    created_at: datetime
    updated_at: datetime