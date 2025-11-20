# services/crm_service.py

from sqlmodel import select
from db import get_session
from models import Lead, Event
import json
from datetime import datetime


# -------------------------------------------------------
# CREATE LEAD
# -------------------------------------------------------
def create_lead(user_id: int, name: str, email: str, phone: str, source: str):
    """Create a lead in the database."""
    with get_session() as s:
        lead = Lead(
            name=name,
            email=email,
            phone=phone,
            source=source,
            pipeline_stage="new",
            notes=None
        )
        s.add(lead)
        s.commit()
        s.refresh(lead)

        # Log event
        log_event = Event(
            type="lead_created",
            payload=json.dumps({"lead_id": lead.id, "user_id": user_id})
        )
        s.add(log_event)
        s.commit()

        return lead


# -------------------------------------------------------
# LIST ALL LEADS
# -------------------------------------------------------
def list_leads():
    """Return all leads sorted by recency."""
    with get_session() as s:
        stmt = select(Lead).order_by(Lead.created_at.desc())
        return list(s.exec(stmt))


# -------------------------------------------------------
# GET LEADS FOR SPECIFIC USER (if needed)
# -------------------------------------------------------
def get_leads_for_user(user_id: int):
    """Not all leads belong to a user, but using filter if needed."""
    with get_session() as s:
        stmt = select(Lead).where(Lead.id == user_id).order_by(Lead.created_at.desc())
        return list(s.exec(stmt))


# -------------------------------------------------------
# UPDATE LEAD STATUS (pipeline stage)
# -------------------------------------------------------
def update_lead_status(lead_id: int, stage: str):
    """Update pipeline stage (new, contacted, qualified, converted, lost)."""
    with get_session() as s:
        lead = s.get(Lead, lead_id)
        if not lead:
            return {"error": "Lead not found"}

        lead.pipeline_stage = stage
        s.add(lead)
        s.commit()
        s.refresh(lead)

        log = Event(
            type="lead_stage_updated",
            payload=json.dumps({"lead_id": lead_id, "stage": stage})
        )
        s.add(log)
        s.commit()

        return {"ok": True, "lead": lead}


# -------------------------------------------------------
# ADD NOTE TO LEAD
# -------------------------------------------------------
def add_note(lead_id: int, note: str):
    """Append a note to a lead with timestamp."""
    with get_session() as s:
        lead = s.get(Lead, lead_id)
        if not lead:
            return {"error": "Lead not found"}

        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M")

        added_note = f"\n[{timestamp}] {note}"
        lead.notes = (lead.notes or "") + added_note

        s.add(lead)
        s.commit()

        event = Event(
            type="lead_noted",
            payload=json.dumps({"lead_id": lead_id, "note": note})
        )
        s.add(event)
        s.commit()

        return {"ok": True}


# -------------------------------------------------------
# CAPTURE LEAD (API/Webhook)
# -------------------------------------------------------
def capture_lead(data: dict):
    """
    API-style capture: Accept raw dict input.
    Expects keys matching Lead model.
    """
    with get_session() as s:
        lead = Lead(**data)
        s.add(lead)
        s.commit()
        s.refresh(lead)

        log = Event(
            type="lead_captured",
            payload=json.dumps({"lead_id": lead.id})
        )
        s.add(log)
        s.commit()

        return {"lead_id": lead.id}


# -------------------------------------------------------
# AUTOMATION: email/SMS (stub)
# -------------------------------------------------------
def trigger_automation(lead_id: int, template: str):
    """
    Trigger an automated email/SMS workflow.
    Implementation stub (use SendGrid/Twilio/etc).
    """
    with get_session() as s:
        event = Event(
            type="automation_triggered",
            payload=json.dumps({"lead_id": lead_id, "template": template})
        )
        s.add(event)
        s.commit()

    return {"status": "scheduled"}
