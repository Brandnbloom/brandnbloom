from fastapi import APIRouter, Depends, HTTPException
from fastapi import Header
from .utils.jwt_helper import decode_access_token

router = APIRouter()

# In-memory storage for simulation
user_ads = {}

def get_current_user(authorization: str = Header(...)):
    token = authorization.split(" ")[1]
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload["user_id"]

# ---------------- Ad Management ----------------
@router.post("/create-ad")
def create_ad(campaign_name: str, platform: str, budget: float, content: str, user_id: int = Depends(get_current_user)):
    """
    Create a simulated ad campaign
    """
    if user_id not in user_ads:
        user_ads[user_id] = []
    ad = {
        "campaign_name": campaign_name,
        "platform": platform,
        "budget": budget,
        "content": content,
        "status": "Active"
    }
    user_ads[user_id].append(ad)
    return {"status": "Ad created", "ad": ad}

@router.get("/my-ads")
def get_ads(user_id: int = Depends(get_current_user)):
    """
    Retrieve all ad campaigns for the user
    """
    return user_ads.get(user_id, [])

# ---------------- Creative Generator ----------------
@router.post("/generate-creative")
def generate_creative(ad_type: str, prompt: str, user_id: int = Depends(get_current_user)):
    """
    Generate ad copy or image (simulated)
    """
    # In real production, integrate GPT/Gemini for copy or stable-diffusion for images
    creative = {
        "ad_type": ad_type,
        "prompt": prompt,
        "suggested_copy": f"AI-generated copy based on: {prompt}",
        "suggested_image_url": f"https://dummyimage.com/600x400/000/fff&text={prompt.replace(' ', '+')}"
    }
    return creative

# ---------------- Budget Optimizer ----------------
@router.post("/optimize-budget")
def optimize_budget(ad_id: int, user_id: int = Depends(get_current_user)):
    """
    Suggest new budget (simulated logic)
    """
    ads = user_ads.get(user_id, [])
    if ad_id < 0 or ad_id >= len(ads):
        raise HTTPException(status_code=404, detail="Ad not found")
    ad = ads[ad_id]
    optimized_budget = ad["budget"] * 1.1  # example: increase by 10%
    return {"original_budget": ad["budget"], "optimized_budget": optimized_budget}
