# services/crm_service.py
from db import get_session
from models import Lead, Event
import json

# In-memory simulation; replace with DB models in production
leads_db = {}

def create_lead(user_id: int, name: str, email: str, phone: str, source: str):
    if user_id not in leads_db:
        leads_db[user_id] = []
    lead = {"name": name, "email": email, "phone": phone, "source": source, "status": "New"}
    leads_db[user_id].append(lead)
    return lead

def get_leads(user_id: int):
    return leads_db.get(user_id, [])

def update_lead_status(user_id: int, lead_index: int, status: str):
    if user_id not in leads_db or lead_index >= len(leads_db[user_id]):
        return None
    leads_db[user_id][lead_index]["status"] = status
    return leads_db[user_id][lead_index]

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
