import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class ProjectCreate(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    description: Optional[str] = None


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=150)
    description: Optional[str] = None


class ProjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: Optional[str]
    created_at: datetime


class ProjectWithStats(ProjectOut):
    total_tasks: int = 0
    done_tasks: int = 0