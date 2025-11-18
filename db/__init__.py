# db/__init__.py

from .database import engine, Base, get_db
from .models import *

# Create tables when imported
def init_db():
    Base.metadata.create_all(bind=engine)


__all__ = [
    "init_db",
    "engine",
    "Base",
    "get_db",
    *[name for name in globals() if not name.startswith("_")]
]

