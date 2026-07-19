import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class CommentCreate(BaseModel):
    author_name: str = Field(min_length=2, max_length=120)
    content: str = Field(min_length=1)


class CommentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    task_id: uuid.UUID
    author_name: str
    content: str
    created_at: datetime


class ActivityLogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    task_id: uuid.UUID
    action: str
    detail: Optional[str]
    created_at: datetime