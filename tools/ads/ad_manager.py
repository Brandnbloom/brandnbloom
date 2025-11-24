# tools/ads/ad_manager.py

from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import Optional, List

# ------------------------
# Database Setup
# ------------------------
DB_URL = "sqlite:///ads.db"
engine = create_engine(DB_URL, echo=False)


# ------------------------
# Campaign Model
# ------------------------
class Campaign(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    platform: str
    budget: float
    status: str = "paused"  # paused / active / completed


# Create table
SQLModel.metadata.create_all(engine)


# ------------------------
# CRUD Functions
# ------------------------

def create_campaign(name: str, platform: str, budget: float) -> Campaign:
    """Create a new ad campaign."""
    with Session(engine) as session:
        c = Campaign(name=name, platform=platform, budget=budget)
        session.add(c)
        session.commit()
        session.refresh(c)
        return c


def get_all_campaigns() -> List[Campaign]:
    """Return all campaigns."""
    with Session(engine) as session:
        return session.exec(select(Campaign)).all()


def get_campaign_by_id(campaign_id: int) -> Optional[Campaign]:
    """Fetch a single campaign by ID."""
    with Session(engine) as session:
        return session.get(Campaign, campaign_id)


def update_campaign(campaign_id: int, **updates) -> Optional[Campaign]:
    """Update campaign fields like status, budget, name, etc."""
    with Session(engine) as session:
        c = session.get(Campaign, campaign_id)
        if not c:
            return None

        for key, value in updates.items():
            if hasattr(c, key) and value is not None:
                setattr(c, key, value)

        session.add(c)
        session.commit()
        session.refresh(c)
        return c


def delete_campaign(campaign_id: int) -> bool:
    """Delete a campaign."""
    with Session(engine) as session:
        c = session.get(Campaign, campaign_id)
        if not c:
            return False
        
        session.delete(c)
        session.commit()
        return True
