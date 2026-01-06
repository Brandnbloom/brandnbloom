# db/models.py

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import json
import os


# =========================================================
#   JSON USAGE TRACKING (for dashboard KPIs)
# =========================================================

USAGE_FILE = "usage.json"

DEFAULT_STRUCTURE = {
    "BloomScore": 0,
    "Consumer_Behavior": 0,
    "Visual_Audit": 0,
    "Review_Reply": 0,
    "Digital_Menu": 0,
    "BloomInsight": 0
}


def load_usage():
    """Load usage.json or create if missing"""
    if not os.path.exists(USAGE_FILE):
        with open(USAGE_FILE, "w") as f:
            json.dump({}, f, indent=4)

    with open(USAGE_FILE, "r") as f:
        return json.load(f)


def save_usage(data):
    """Save updated usage.json"""
    with open(USAGE_FILE, "w") as f:
        json.dump(data, f, indent=4)


def log_kpis(email: str, feature_name: str):
    """
    Increase count of a feature when a user uses a tool.
    Creates the user entry if not present.
    """
    data = load_usage()

    if email not in data:
        data[email] = DEFAULT_STRUCTURE.copy()

    if feature_name not in data[email]:
        data[email][feature_name] = 0

    data[email][feature_name] += 1
    save_usage(data)


def get_kpis():
    """
    Return the full KPI usage dictionary.
    Used in Streamlit dashboard.
    """
    return load_usage()


# =========================================================
#   DATABASE MODELS
# =========================================================

# -------------------------
# USERS
# -------------------------
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    name: Optional[str] = None
    hashed_password: str
    stripe_customer_id: Optional[str] = None
    plan: str = "free"
    role: str = "user"
    created_at: datetime = Field(default_factory=datetime.utcnow)

    tasks: List["ProjectTask"] = Relationship(back_populates="assignee")
    ig_accounts: List["IGAccount"] = Relationship(back_populates="owner")
    reports: List["Report"] = Relationship(back_populates="user")


# -------------------------
# IG ACCOUNTS
# -------------------------
class IGAccount(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    handle: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    owner: Optional[User] = Relationship(back_populates="ig_accounts")
    kpis: List["KPILog"] = Relationship(back_populates="account")


# -------------------------
# KPI LOGS
# -------------------------
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


# -------------------------
# REPORTS
# -------------------------
class Report(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    ig_handle: Optional[str]
    pdf_path: str
    sent_at: datetime = Field(default_factory=datetime.utcnow)

    user: Optional[User] = Relationship(back_populates="reports")


# -------------------------
# PROJECT TASKS
# -------------------------
class ProjectTask(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    status: str = "todo"

    assignee_id: Optional[int] = Field(default=None, foreign_key="user.id")
    assignee: Optional[User] = Relationship(back_populates="tasks")

    due_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


# -------------------------
# LEADS (CRM)
# -------------------------
class Lead(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    source: Optional[str]
    pipeline_stage: str = "new"
    notes: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)


# -------------------------
# EVENT LOGS
# -------------------------
class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: str
    payload: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


# -------------------------
# PAGE RECORDS
# -------------------------
class PageRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str
    html: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)


# -------------------------
# KEYWORDS
# -------------------------
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


# -------------------------
# AD CAMPAIGNS
# -------------------------
class Campaign(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    platform: str
    status: str = "paused"
    budget: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)


# -------------------------
# REVIEWS
# -------------------------
class Review(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    source: str
    author: Optional[str]
    rating: Optional[float]
    text: Optional[str]
    fetched_at: datetime = Field(default_factory=datetime.utcnow)

# =========================================================
#   REPORT STORAGE (File-based fallback, production-safe)
# =========================================================

from pathlib import Path
from typing import Dict, Any

REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(exist_ok=True)


def save_report(report_data: Dict[str, Any]) -> str:
    """
    Save report metadata safely to disk.
    Used by BloomInsight / Dashboard / Weekly reports.
    Returns the saved file path.
    """

    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"report_{ts}.json"
    file_path = REPORTS_DIR / filename

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2)

    return str(file_path)

