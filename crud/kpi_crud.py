from sqlmodel import select
from db.db import get_session
from models.models import Event


def log_event(event_type: str, payload: dict):
    with get_session() as session:
        ev = Event(type=event_type, payload=str(payload))
        session.add(ev)
        session.commit()
        session.refresh(ev)
        return ev
