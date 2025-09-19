from fastapi import APIRouter, Depends, Header, HTTPException
from services.analytics_service import log_event, get_user_analytics, generate_report
from utils.jwt_helper import decode_access_token

router = APIRouter()

def get_current_user(authorization: str = Header(...)):
    token = authorization.split(" ")[1]
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload["user_id"]

@router.post("/log-event")
def api_log_event(event_name: str, value: float, user_id: int = Depends(get_current_user)):
    event = log_event(user_id, event_name, value)
    return {"status": "Event logged", "event": event}

@router.get("/analytics")
def api_get_analytics(user_id: int = Depends(get_current_user)):
    data = get_user_analytics(user_id)
    return {"analytics": data}

@router.get("/report")
def api_generate_report(user_id: int = Depends(get_current_user)):
    report = generate_report(user_id)
    return {"report": report}
