# add to services/internal_services.py
from db import get_session
from models import ProjectTask

def create_task(payload):
    with get_session() as s:
        t = ProjectTask(title=payload.get("title"), description=payload.get("description"))
        s.add(t); s.commit(); s.refresh(t)
        return {"task_id": t.id}

def list_tasks():
    with get_session() as s:
        rows = s.exec("SELECT * FROM projecttask ORDER BY created_at DESC").all()
        return rows
