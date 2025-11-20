# services/internal_services.py

from db import get_session
from models import ProjectTask


def create_task(payload: dict) -> dict:
    """
    Create a new project task using payload containing title & description.
    """
    title = payload.get("title")
    description = payload.get("description")

    with get_session() as s:
        task = ProjectTask(title=title, description=description)
        s.add(task)
        s.commit()
        s.refresh(task)

        return {"task_id": task.id}


def list_tasks():
    """
    List all project tasks ordered by creation time (latest first).
    Uses SQLModel ORM instead of raw SQL.
    """
    with get_session() as s:
        tasks = s.query(ProjectTask).order_by(ProjectTask.created_at.desc()).all()
        return tasks
