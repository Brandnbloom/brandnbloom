# routers/crm_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.crm_service import capture_lead, list_leads, add_note, trigger_automation

router = APIRouter()

class LeadReq(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    source: str | None = None

@router.post("/capture")
def capture(req: LeadReq):
    return capture_lead(req.dict())

@router.get("/list")
def leads():
    return list_leads()

class NoteReq(BaseModel):
    lead_id: int
    note: str

@router.post("/note")
def note(req: NoteReq):
    return add_note(req.lead_id, req.note)

class AutomationReq(BaseModel):
    lead_id: int
    template: str

@router.post("/automation")
def automation(req: AutomationReq):
    return trigger_automation(req.lead_id, req.template)
