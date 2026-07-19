import uuid

from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base
from app.db.types import GUID


class Comment(Base):
    __tablename__ = "comments"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    task_id = Column(GUID(), ForeignKey("tasks.id"), nullable=False)
    author_name = Column(String(120), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    task = relationship("Task", back_populates="comments")