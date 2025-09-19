# routers/keyword_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.keyword_service import add_keyword, get_keywords, schedule_daily_rank_check, get_keyword_history

router = APIRouter()

class AddKeywordReq(BaseModel):
    keyword: str
    target_url: str | None = None

@router.post("/add")
def add_kw(req: AddKeywordReq):
    return add_keyword(req.keyword, req.target_url)

@router.get("/list")
def list_kws():
    return get_keywords()

@router.post("/schedule-daily")
def schedule_daily():
    job_id = schedule_daily_rank_check()
    return {"scheduled_job_id": job_id}

@router.get("/history/{keyword_id}")
def history(keyword_id: int):
    return get_keyword_history(keyword_id)
