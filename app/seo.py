# app/seo.py

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List, Dict
from .database import get_db
from .utils.jwt_helper import decode_access_token

router = APIRouter()

# -------------------------------------------------------------------
# Auth Helper
# -------------------------------------------------------------------
def get_current_user(
    authorization: str = Header(...),
    db: Session = Depends(get_db)
) -> int:
    """
    Extract and validate Bearer JWT token → return user_id.
    """
    if not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Authorization header malformed")

    token = authorization.split(" ")[1]
    payload = decode_access_token(token)

    if not payload or "user_id" not in payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")

    return payload["user_id"]


# -------------------------------------------------------------------
# Pydantic Models
# -------------------------------------------------------------------
class KeywordTrackRequest(BaseModel):
    url: str = Field(..., min_length=4)
    keyword: str = Field(..., min_length=2)


# -------------------------------------------------------------------
# SEO Audit (Simulated)
# -------------------------------------------------------------------
@router.get("/seo-audit")
def seo_audit(url: str, user_id: int = Depends(get_current_user)):
    """
    Simulated SEO audit. Replace with Lighthouse API, Ahrefs, Semrush, or custom scraper later.
    """
    try:
        audit = {
            "url": url,
            "page_speed": "85/100",
            "title_length": 55,
            "meta_description_length": 160,
            "h1_tags": 1,
            "issues": [
                "No sitemap found",
                "Missing alt text on 1 image"
            ]
        }
        return {"status": "success", "seo_audit": audit}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------------------------------------------------
# Keyword Tracker (In-Memory)
# -------------------------------------------------------------------
user_keywords: Dict[int, List[dict]] = {}


@router.post("/keyword-track")
def add_keyword(
    data: KeywordTrackRequest,
    user_id: int = Depends(get_current_user)
):
    """
    Add a keyword to track ranking daily.
    """
    user_keywords.setdefault(user_id, [])

    # Avoid duplicate entries
    for item in user_keywords[user_id]:
        if item["url"] == data.url and item["keyword"].lower() == data.keyword.lower():
            return {
                "status": "exists",
                "message": "Keyword already tracked",
                "data": user_keywords[user_id]
            }

    entry = {
        "url": data.url,
        "keyword": data.keyword,
        "rank": "Simulated"
    }

    user_keywords[user_id].append(entry)

    return {
        "status": "added",
        "data": user_keywords[user_id]
    }


@router.get("/keyword-track")
def get_keywords(user_id: int = Depends(get_current_user)):
    """
    Get all tracked keywords for the current user.
    """
    return {
        "status": "success",
        "keywords": user_keywords.get(user_id, [])
    }
