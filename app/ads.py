from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from .utils.jwt_helper import decode_access_token

router = APIRouter()

# -------------------------------------------------------------------
# Temporary in-memory store (replace later with DB)
# -------------------------------------------------------------------
user_ads: Dict[int, List[dict]] = {}


# -------------------------------------------------------------------
# Auth Helper
# -------------------------------------------------------------------
def get_current_user(authorization: str = Header(...)) -> int:
    """
    Extract user ID from JWT Bearer token.
    Expects: Authorization: Bearer <token>
    """
    if not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    token = authorization.split(" ")[1]
    payload = decode_access_token(token)

    if not payload or "user_id" not in payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload["user_id"]


# -------------------------------------------------------------------
# Pydantic Models
# -------------------------------------------------------------------
class AdCreate(BaseModel):
    campaign_name: str = Field(..., max_length=60)
    platform: str = Field(..., regex="^(instagram|facebook|google|youtube|linkedin)$")
    budget: float = Field(..., gt=0)
    content: str = Field(..., max_length=500)


class CreativeRequest(BaseModel):
    ad_type: str = Field(..., regex="^(copy|image)$")
    prompt: str = Field(..., max_length=200)


# -------------------------------------------------------------------
# Ad Management
# -------------------------------------------------------------------
@router.post("/create-ad")
def create_ad(data: AdCreate, user_id: int = Depends(get_current_user)):
    """
    Create a simulated ad campaign for the logged-in user.
    """
    user_ads.setdefault(user_id, [])

    ad = {
        "campaign_name": data.campaign_name,
        "platform": data.platform,
        "budget": data.budget,
        "content": data.content,
        "status": "Active"
    }

    user_ads[user_id].append(ad)

    return {"status": "Ad created", "ad": ad}


@router.get("/my-ads")
def get_ads(user_id: int = Depends(get_current_user)):
    """
    Retrieve all ads for the current user.
    """
    return user_ads.get(user_id, [])


# -------------------------------------------------------------------
# Creative Generator
# -------------------------------------------------------------------
@router.post("/generate-creative")
def generate_creative(data: CreativeRequest, user_id: int = Depends(get_current_user)):
    """
    Generate ad creative using AI (stub version).
    """
    creative = {
        "ad_type": data.ad_type,
        "prompt": data.prompt,
        "suggested_copy": f"✨ AI-generated copy for: {data.prompt}",
        "suggested_image_url": (
            f"https://dummyimage.com/600x400/000/fff&text={data.prompt.replace(' ', '+')}"
            if data.ad_type == "image"
            else None
        ),
    }
    return creative


# -------------------------------------------------------------------
# Budget Optimizer
# -------------------------------------------------------------------
@router.post("/optimize-budget")
def optimize_budget(ad_id: int, user_id: int = Depends(get_current_user)):
    """
    Suggest a new optimized budget using simple heuristic logic.
    """
    ads = user_ads.get(user_id, [])

    if ad_id < 0 or ad_id >= len(ads):
        raise HTTPException(status_code=404, detail="Ad not found")

    ad = ads[ad_id]
    optimized_budget = round(ad["budget"] * 1.10, 2)  # +10%

    return {
        "campaign_name": ad["campaign_name"],
        "original_budget": ad["budget"],
        "optimized_budget": optimized_budget,
        "strategy": "scale-up (10% increase for better reach)"
    }
