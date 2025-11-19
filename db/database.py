# db/database.py

import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session

load_dotenv()

# Load DB URL, fallback to local SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./bnb.sqlite3")

# Engine
engine = create_engine(DATABASE_URL, echo=False)

# Import SQLModel tables AFTER engine is defined
from models.models import *  # noqa


def init_db():
    """Create all tables."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Dependency for FastAPI."""
    with Session(engine) as session:
        yield session
