# db/__init__.py

from .database import engine, get_db
from .models import *
from sqlmodel import SQLModel


def init_db():
    """
    Initializes the database by creating all SQLModel tables.
    This is typically called once at application startup.
    """
    SQLModel.metadata.create_all(bind=engine)


__all__ = [
    "init_db",
    "engine",
    "get_db",
    *[name for name in globals() if not name.startswith("_") and name not in {"SQLModel"}]
]
