# tools/analytics/events_store.py

from sqlmodel import SQLModel, Field, create_engine, Session, select
from datetime import datetime
import json

DB = "sqlite:///events.db"
engine = create_engine(DB, echo=False)


class Event(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    event_type: str = Field(default="event")
    payload: str
    created_at: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )


SQLModel.metadata.create_all(engine)


class EventStore:

    @staticmethod
    def log_event(data: dict):
        """
        Save an analytics event to the database.
        """
        try:
            payload = json.dumps(data)
        except Exception:
            payload = json.dumps({"error": "Invalid payload", "raw": str(data)})

        event_type = data.get("type") or data.get("event_type") or "event"

        with Session(engine) as session:
            event = Event(
                event_type=event_type,
                payload=payload
            )
            session.add(event)
            session.commit()
            session.refresh(event)
            return event.id

    @staticmethod
    def query_events(limit=100):
        """
        Fetch latest events, newest first.
        """
        with Session(engine) as session:
            stmt = select(Event).order_by(Event.id.desc()).limit(limit)
            return session.exec(stmt).all()
