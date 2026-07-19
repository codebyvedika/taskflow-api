from typing import Optional

from sqlalchemy.orm import Session

from app.models.activity_log import ActivityLog


def log_activity(db: Session, task_id, action: str, detail: Optional[str] = None) -> ActivityLog:
    entry = ActivityLog(task_id=task_id, action=action, detail=detail)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry