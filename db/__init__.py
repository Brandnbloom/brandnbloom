# db.py
from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv

load_dotenv()

# Load DB URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./bnb.db")

# Create engine
engine = create_engine(DATABASE_URL, echo=False)

# Import models at module level (correct)
from .models import *   # OK here, NOT inside functions


def init_db():
    """Initialize DB and create all tables."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Get a new database session."""
    return Session(engine)
