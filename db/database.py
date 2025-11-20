# db/database.py

import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session

load_dotenv()

# -------------------------------------------------------
# DATABASE URL (Uses ENV if present; otherwise SQLite)
# -------------------------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./bnb.sqlite3")

# -------------------------------------------------------
# ENGINE
# -------------------------------------------------------
engine = create_engine(
    DATABASE_URL,
    echo=False,    # Set to True only if you want SQL logs
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

# -------------------------------------------------------
# IMPORT MODELS AFTER ENGINE IS DEFINED
# Prevents circular imports
# -------------------------------------------------------
from models.models import *  # noqa


# -------------------------------------------------------
# INITIALIZE TABLES
# -------------------------------------------------------
def init_db():
    """Create all database tables."""
    SQLModel.metadata.create_all(engine)


# -------------------------------------------------------
# SESSION PROVIDER FOR FASTAPI
# -------------------------------------------------------
def get_session():
    """FastAPI dependency to provide DB session."""
    with Session(engine) as session:
        yield session
