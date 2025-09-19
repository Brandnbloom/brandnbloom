from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .utils.jwt_helper import decode_access_token
from fastapi import Header
import requests

router = APIRouter()

def get_current_user(authorization: str = Header(...), db: Session = Depends(get_db)):
    token = authorization.split(" ")[1]
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload["user_id"]

# ---------------- SEO Audit ----------------
@router.get("/seo-audit")
def seo_audit(url: str, user_id: int = Depends(get_current_user)):
    """
    Simulated SEO Audit:
    Returns page speed, title length, meta description length
    """
    try:
        # Placeholder for real SEO API or Lighthouse integration
        audit = {
            "url": url,
            "page_speed": "85/100",
            "title_length": 55,
            "meta_description_length": 160,
            "h1_tags": 1,
            "issues": ["No sitemap found", "Missing alt on 1 image"]
        }
        return audit
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------- Keyword Tracker ----------------
user_keywords = {}  # in-memory storage, replace with DB in prod

@router.post("/keyword-track")
def add_keyword(url: str, keyword: str, user_id: int = Depends(get_current_user)):
    """
    Add a keyword for a website to track daily ranking
    """
    if user_id not in user_keywords:
        user_keywords[user_id] = []
    user_keywords[user_id].append({"url": url, "keyword": keyword, "rank": "Simulated"})
    return {"status": "Keyword added", "data": user_keywords[user_id]}

@router.get("/keyword-track")
def get_keywords(user_id: int = Depends(get_current_user)):
    """
    Get all keywords for a user
    """
    return user_keywords.get(user_id, [])
