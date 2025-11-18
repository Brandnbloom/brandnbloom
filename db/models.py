from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime


# -----------------------
# USER MODEL
# -----------------------

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    name: Optional[str] = None
    hashed_password: str
    stripe_customer_id: Optional[str] = None
    plan: str = "free"
    role: str = "user"
    created_at: datetime = Field(default_factory=datetime.utcnow)


# -----------------------
# LEADS
# -----------------------

class Lead(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    source: Optional[str]
    pipeline_stage: str = "new"
    notes: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)


# -----------------------
# EVENTS (System Logs / Webhooks)
# -----------------------

class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: str
    payload: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


# -----------------------
# PAGE RECORDS (SEO Crawler)
# -----------------------

class PageRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str
    html: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)


# -----------------------
# KEYWORD MANAGEMENT
# -----------------------

class Keyword(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    keyword: str
    target_url: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)


class KeywordRank(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    keyword_id: int = Field(foreign_key="keyword.id")
    rank: Optional[int]
    checked_at: datetime = Field(default_factory=datetime.utcnow)


# -----------------------
# AD CAMPAIGNS
# -----------------------

class Campaign(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    platform: str
    status: str = "paused"
    budget: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)


# -----------------------
# REVIEWS
# -----------------------

class Review(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    source: str
    author: Optional[str]
    rating: Optional[float]
    text: Optional[str]
    fetched_at: datetime = Field(default_factory=datetime.utcnow)


# -----------------------
# PROJECT TASKS
# -----------------------

class ProjectTask(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str]
    status: str = "todo"
    assignee_id: Optional[int] = Field(default=None, foreign_key="user.id")
    due_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
