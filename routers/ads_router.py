# routers/ads_router.py
from fastapi import APIRouter
from pydantic import BaseModel
from services.ads_service import create_campaign, optimize_budget, generate_ad_creative

router = APIRouter()

class CampaignReq(BaseModel):
    name: str
    platform: str
    budget: float

@router.post("/campaigns")
def create(c: CampaignReq):
    return create_campaign(c.name, c.platform, c.budget)

class OptimizeReq(BaseModel):
    campaign_id: int

@router.post("/optimize")
def optimize(req: OptimizeReq):
    return optimize_budget(req.campaign_id)

class CreativeReq(BaseModel):
    brief: str
    platform: str

@router.post("/creative")
def creative(req: CreativeReq):
    return generate_ad_creative(req.brief, req.platform)
