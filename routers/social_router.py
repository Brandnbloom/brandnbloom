# routers/social_router.py
from fastapi import APIRouter
from pydantic import BaseModel
from services.social_service import schedule_post, publish_now, get_metrics, reply_comment, get_posts, get_engagements
from utils.jwt_helper import decode_access_token

router = APIRouter()

def get_current_user(authorization: str = Header(...)):
    token = authorization.split(" ")[1]
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload["user_id"]

@router.post("/schedule-post")
def api_schedule_post(platform: str, content: str, schedule_time: str, user_id: int = Depends(get_current_user)):
    post = schedule_post(user_id, platform, content, schedule_time)
    return {"status": "Post scheduled", "post": post}

@router.get("/posts")
def api_get_posts(user_id: int = Depends(get_current_user)):
    return get_posts(user_id)

@router.get("/engagements")
def api_get_engagements(user_id: int = Depends(get_current_user)):
    return get_engagements(user_id)
class ScheduleReq(BaseModel):
    platform: str
    content: str
    publish_at: str  # ISO timestamp

@router.post("/schedule")
def schedule(req: ScheduleReq):
    return schedule_post(req.platform, req.content, req.publish_at)

class PublishReq(BaseModel):
    platform: str
    content: str

@router.post("/publish")
def publish(req: PublishReq):
    return publish_now(req.platform, req.content)

@router.post("/metrics")
def metrics(q: dict):
    # expects {"platform":"instagram", "since":"2025-09-01"}
    return get_metrics(q)

class ReplyReq(BaseModel):
    platform: str
    conversation_id: str
    message: str

@router.post("/reply")
def reply(req: ReplyReq):
    return reply_comment(req.platform, req.conversation_id, req.message)
