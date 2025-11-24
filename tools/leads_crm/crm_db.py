# tools/leads_crm/crm_db.py

from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional
import os

DB_URL = os.getenv("BNB_CRM_DB", "sqlite:///crm.db")
engine = create_engine(DB_URL, echo=False)


class Lead(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    phone: Optional[str] = None
    source: Optional[str] = None
    stage: str = "new"  # new → contacted → follow-up → closed/won/lost


SQLModel.metadata.create_all(engine)


# --------------------------------------------------------
# Create Lead
# --------------------------------------------------------
def create_lead(data: dict) -> Lead:
    """
    Safely create a CRM lead.

    Required fields: name, email
    Optional: phone, source, stage
    """
    cleaned = {
        "name": data.get("name", "").strip(),
        "email": data.get("email", "").strip(),
        "phone": (data.get("phone") or "").strip(),
        "source": (data.get("source") or "").strip(),
        "stage": data.get("stage", "new"),
    }

    if not cleaned["name"] or not cleaned["email"]:
        raise ValueError("Name and Email are required to create a lead.")

    with Session(engine) as session:
        lead = Lead(**cleaned)
        session.add(lead)
        session.commit()
        session.refresh(lead)
        return lead


# --------------------------------------------------------
# Fetch All Leads
# --------------------------------------------------------
def list_leads(limit: int = 200):
    """
    Returns latest leads first.
    """
    with Session(engine) as session:
        stmt = select(Lead).order_by(Lead.id.desc()).limit(limit)
        return session.exec(stmt).all()


# --------------------------------------------------------
# Update Lead Stage
# --------------------------------------------------------
def update_lead_stage(lead_id: int, new_stage: str) -> Lead:
    """
    Update the stage/status of a lead.
    """
    with Session(engine) as session:
        lead = session.get(Lead, lead_id)
        if not lead:
            raise ValueError("Lead not found.")

        lead.stage = new_stage
        session.add(lead)
        session.commit()
        session.refresh(lead)
        return lead
