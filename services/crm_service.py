# services/crm_service.py
from db import get_session
from models import Lead, Event
import json

def capture_lead(data: dict):
    with get_session() as s:
        lead = Lead(**data)
        s.add(lead); s.commit(); s.refresh(lead)
        e = Event(type="lead_captured", payload=json.dumps({"lead_id": lead.id}))
        s.add(e); s.commit()
        return {"lead_id": lead.id}

def list_leads():
    with get_session() as s:
        rows = s.exec("SELECT * FROM lead ORDER BY created_at DESC").all()
        return rows

def add_note(lead_id, note):
    with get_session() as s:
        lead = s.get(Lead, lead_id)
        if not lead: return {"error":"not found"}
        lead.notes = (lead.notes or "") + f"\n{note}"
        s.add(lead); s.commit()
        return {"ok": True}

def trigger_automation(lead_id, template):
    # stub: send email/SMS via provider (SMTP/Twilio)
    with get_session() as s:
        e = Event(type="automation_fired", payload=json.dumps({"lead_id":lead_id, "template": template}))
        s.add(e); s.commit()
    return {"status":"scheduled"}
