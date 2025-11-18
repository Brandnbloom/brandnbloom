# db/db.py

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

# DATABASE_URL from environment or fallback to SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./bnb.sqlite3")

# If using SQLite, add extra connection args
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

# SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args)

# Session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base for ORM models
Base = declarative_base()


def get_db():
    """FastAPI session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

engine = create_engine(DATABASE_URL, echo=False)

from models.models import *  # import SQLModel tables AFTER engine

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)

