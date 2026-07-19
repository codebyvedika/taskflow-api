import uuid

from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base
from app.db.types import GUID


class Project(Base):
    __tablename__ = "projects"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")