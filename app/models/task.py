import enum
import uuid

from sqlalchemy import Column, String, Text, Enum, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base
from app.db.types import GUID


class TaskStatusEnum(str, enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    DONE = "done"


class TaskPriorityEnum(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    project_id = Column(GUID(), ForeignKey("projects.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatusEnum), default=TaskStatusEnum.TODO, nullable=False)
    priority = Column(Enum(TaskPriorityEnum), default=TaskPriorityEnum.MEDIUM, nullable=False)
    assignee_name = Column(String(120), nullable=True)
    due_date = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    project = relationship("Project", back_populates="tasks")
    comments = relationship("Comment", back_populates="task", cascade="all, delete-orphan")
    activity_logs = relationship("ActivityLog", back_populates="task", cascade="all, delete-orphan")