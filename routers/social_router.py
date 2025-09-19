# routers/social_router.py
from fastapi import APIRouter
from pydantic import BaseModel
from services.social_service import schedule_post, publish_now, get_metrics, reply_comment

router = APIRouter()

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
