import uuid

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base
from app.db.types import GUID


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    task_id = Column(GUID(), ForeignKey("tasks.id"), nullable=False)
    action = Column(String(100), nullable=False)
    detail = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    task = relationship("Task", back_populates="activity_logs")