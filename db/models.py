from db.database import get_cursor
from utils.security import hash_password, check_password
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    stripe_customer_id = Column(String, nullable=True)
    plan = Column(String, default="free")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

def create_user(email, name, password):
    """
    Store a new user with a securely hashed password.
    """
    password_hash = hash_password(password)
    with get_cursor() as cur:
        cur.execute(
            "INSERT INTO users(email, name, password_hash) VALUES(?,?,?)",
            (email, name, password_hash)
        )
        return cur.lastrowid

def get_user_by_email(email):
    with get_cursor() as cur:
        cur.execute("SELECT * FROM users WHERE email = ?", (email,))
        return cur.fetchone()

def verify_user(email, password) -> bool:
    """
    Check if the given password matches the stored hash.
    """
    user = get_user_by_email(email)
    if not user:
        return False
    return check_password(password, user["password_hash"])

def log_kpis(ig_handle, followers, likes, reach, impressions, er):
    with get_cursor() as cur:
        cur.execute(
            '''INSERT INTO kpi_logs(ig_handle, followers, likes, reach, impressions, engagement_rate)
               VALUES(?,?,?,?,?,?)''',
            (ig_handle, followers, likes, reach, impressions, er)
        )
        return cur.lastrowid

def get_kpis(ig_handle, limit=50):
    with get_cursor() as cur:
        cur.execute(
            "SELECT * FROM kpi_logs WHERE ig_handle=? ORDER BY timestamp DESC LIMIT ?",
            (ig_handle, limit)
        )
        return cur.fetchall()

def save_report(user_id, ig_handle, pdf_path):
    with get_cursor() as cur:
        cur.execute(
            "INSERT INTO reports(user_id, ig_handle, pdf_path) VALUES(?,?,?)",
            (user_id, ig_handle, pdf_path)
        )
        return cur.lastrowid

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    name: Optional[str] = None
    role: str = "user"  # admin/agent/user
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Lead(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    source: Optional[str] = None
    pipeline_stage: str = "new"
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: str
    payload: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class PageRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str
    html: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Keyword(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    keyword: str
    target_url: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)

class KeywordRank(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    keyword_id: int
    rank: Optional[int] = None
    checked_at: datetime = Field(default_factory=datetime.utcnow)

class Campaign(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    platform: str
    status: str = "paused"
    budget: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Review(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    source: str
    author: Optional[str]
    rating: Optional[float]
    text: Optional[str]
    fetched_at: datetime = Field(default_factory=datetime.utcnow)

class ProjectTask(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    status: str = "todo"
    assignee_id: Optional[int] = None
    due_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
