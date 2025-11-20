# db/models.py

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime


# ---------------------------------------------------------
# USERS
# ---------------------------------------------------------

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    name: Optional[str] = None
    hashed_password: str
    stripe_customer_id: Optional[str] = None
    plan: str = "free"
    role: str = "user"
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    tasks: List["ProjectTask"] = Relationship(back_populates="assignee")
    ig_accounts: List["IGAccount"] = Relationship(back_populates="owner")
    reports: List["Report"] = Relationship(back_populates="user")


# ---------------------------------------------------------
# IG ACCOUNTS
# ---------------------------------------------------------

class IGAccount(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    handle: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    owner: Optional[User] = Relationship(back_populates="ig_accounts")
    kpis: List["KPILog"] = Relationship(back_populates="account")


# ---------------------------------------------------------
# KPI LOGS
# ---------------------------------------------------------

class KPILog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ig_handle: str
    followers: int = 0
    likes: int = 0
    reach: int = 0
    impressions: int = 0
    engagement_rate: float = 0.0
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    ig_account_id: Optional[int] = Field(default=None, foreign_key="igaccount.id")
    account: Optional[IGAccount] = Relationship(back_populates="kpis")


# ---------------------------------------------------------
# REPORTS
# ---------------------------------------------------------

class Report(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    ig_handle: Optional[str]
    pdf_path: str
    sent_at: datetime = Field(default_factory=datetime.utcnow)

    user: Optional[User] = Relationship(back_populates="reports")


# ---------------------------------------------------------
# PROJECT TASKS
# ---------------------------------------------------------

class ProjectTask(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    status: str = "todo"

    assignee_id: Optional[int] = Field(default=None, foreign_key="user.id")
    assignee: Optional[User] = Relationship(back_populates="tasks")

    due_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------
# LEADS (CRM)
# ---------------------------------------------------------

class Lead(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    source: Optional[str]
    pipeline_stage: str = "new"
    notes: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------
# EVENT LOGS
# ---------------------------------------------------------

class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: str
    payload: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------
# PAGE RECORDS (SEO Crawler)
# ---------------------------------------------------------

class PageRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str
    html: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------
# KEYWORD TRACKING
# ---------------------------------------------------------

class Keyword(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    keyword: str
    target_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    ranks: List["KeywordRank"] = Relationship(back_populates="keyword")


class KeywordRank(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    keyword_id: int = Field(foreign_key="keyword.id")
    rank: Optional[int]
    checked_at: datetime = Field(default_factory=datetime.utcnow)

    keyword: Optional[Keyword] = Relationship(back_populates="ranks")


# ---------------------------------------------------------
# AD CAMPAIGNS
# ---------------------------------------------------------

class Campaign(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    platform: str
    status: str = "paused"
    budget: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------
# REVIEWS
# ---------------------------------------------------------

class Review(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    source: str
    author: Optional[str]
    rating: Optional[float]
    text: Optional[str]
    fetched_at: datetime = Field(default_factory=datetime.utcnow)
