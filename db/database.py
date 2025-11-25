# db/database.py

import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel import Session, select
from .models import User
from .database import engine  # if needed

def get_user_by_email(email: str):
    with Session(engine) as session:
        statement = select(User).where(User.email == email)
        return session.exec(statement).first()


def create_user(email: str, name: str, hashed_password: str):
    with Session(engine) as session:
        user = User(
            email=email,
            name=name,
            hashed_password=hashed_password,
            plan="free",
            role="user"
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

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
from db.models import *  # noqa


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
