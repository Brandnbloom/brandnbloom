# routers/crm_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.crm_service import create_lead, get_leads, update_lead_status
from utils.jwt_helper import decode_access_token import capture_lead, list_leads, add_note, trigger_automation

router = APIRouter()

class LeadReq(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    source: str | None = None

def get_current_user(authorization: str = Header(...)):
    token = authorization.split(" ")[1]
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload["user_id"]

@router.post("/create-lead")
def api_create_lead(name: str, email: str, phone: str, source: str, user_id: int = Depends(get_current_user)):
    lead = create_lead(user_id, name, email, phone, source)
    return {"status": "Lead created", "lead": lead}

@router.get("/leads")
def api_get_leads(user_id: int = Depends(get_current_user)):
    return get_leads(user_id)

@router.put("/update-status")
def api_update_status(lead_index: int, status: str, user_id: int = Depends(get_current_user)):
    lead = update_lead_status(user_id, lead_index, status)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return {"status": "Updated", "lead": lead}
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
