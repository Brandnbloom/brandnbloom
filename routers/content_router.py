# routers/content_router.py
from fastapi import APIRouter
from pydantic import BaseModel
from services.content_service import optimize_content, analyze_readability

router = APIRouter()

class ContentReq(BaseModel):
    title: str | None = None
    body: str

@router.post("/optimize")
def content_opt(req: ContentReq):
    return optimize_content(req.title, req.body)

@router.post("/readability")
def readability(req: ContentReq):
    return analyze_readability(req.body)
