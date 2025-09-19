# routers/reputation_router.py
from fastapi import APIRouter
from services.reputation_service import fetch_reviews, analyze_sentiment, auto_respond

router = APIRouter()

@router.post("/fetch")
def fetch(q: dict):
    return fetch_reviews(q.get("source_urls", []))

@router.post("/sentiment")
def sentiment(q: dict):
    return analyze_sentiment(q.get("texts", []))

@router.post("/auto-reply")
def auto_reply(q: dict):
    return auto_respond(q)
