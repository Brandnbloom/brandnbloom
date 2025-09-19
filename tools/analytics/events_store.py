from sqlmodel import SQLModel, Field, create_engine, Session, select
from datetime import datetime
DB = "sqlite:///events.db"
engine = create_engine(DB, echo=False)

class Event(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    type: str
    payload: str
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

SQLModel.metadata.create_all(engine)

class EventStore:
    @staticmethod
    def log_event(obj):
        import json
        with Session(engine) as s:
            e = Event(type=obj.get("type","event"), payload=json.dumps(obj))
            s.add(e); s.commit(); s.refresh(e)
            return e.id

    @staticmethod
    def query_events(limit=100):
        with Session(engine) as s:
            q = s.exec(select(Event).order_by(Event.id.desc()).limit(limit))
            return q.all()
