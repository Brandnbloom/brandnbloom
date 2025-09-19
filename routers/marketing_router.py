# routers/marketing_router.py
from fastapi import APIRouter
from pydantic import BaseModel
from services.marketing_service import generate_hashtags, content_score_stub

router = APIRouter()

class HashtagReq(BaseModel):
    caption: str
    platform: str = "instagram"

@router.post("/hashtags")
def hashtags(req: HashtagReq):
    tags = generate_hashtags(req.caption, req.platform)
    return {"success": True, "hashtags": tags}

@router.post("/content-score")
def content_score(text: dict):
    # expects {"title": "...", "body": "..."}
    return {"success": True, "score": content_score_stub(text)}
