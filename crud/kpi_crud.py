# crud/kpi_crud.py

from sqlmodel import select
from db.db import get_session
from models.models import Event


def log_event(event_type: str, payload: dict):
    """
    Stores any KPI / analytics event in the database.

    Args:
        event_type (str): Name of event (e.g., 'seo_audit_run', 'page_view', 'bloomscore_generated')
        payload (dict): Additional data about event

    Returns:
        Event: The stored event model object
    """
    with get_session() as session:
        ev = Event(
            type=event_type,
            payload=str(payload)  # stored as text; can convert to JSON column later if needed
        )
        session.add(ev)
        session.commit()
        session.refresh(ev)
        return ev


def get_events(limit: int = 50):
    """
    Fetch the latest events for analytics dashboard.

    Args:
        limit (int): Number of events to fetch

    Returns:
        list[Event]
    """
    with get_session() as session:
        stmt = select(Event).order_by(Event.timestamp.desc()).limit(limit)
        return session.exec(stmt).all()


def get_events_by_type(event_type: str, limit: int = 50):
    """
    Fetch events filtered by type (e.g., only BloomScore events)

    Args:
        event_type (str): The event type to filter
        limit (int): Number of events to fetch

    Returns:
        list[Event]
    """
    with get_session() as session:
        stmt = (
            select(Event)
            .where(Event.type == event_type)
            .order_by(Event.timestamp.desc())
            .limit(limit)
        )
        return session.exec(stmt).all()


def count_events():
    """
    Count total events in the system.
    Helpful for showing total usage metrics.

    Returns:
        int
    """
    with get_session() as session:
        stmt = select(Event)
        return len(session.exec(stmt).all())
