# services/ads_service.py
from db import get_session
from models import Campaign, Event
import json
from services.ai_client import generate_text

def create_campaign(name, platform, budget):
    with get_session() as s:
        c = Campaign(name=name, platform=platform, budget=budget)
        s.add(c); s.commit(); s.refresh(c)
        return {"campaign_id": c.id, "name": c.name}

def optimize_budget(campaign_id):
    # Fetch campaign & events, run simple heuristic: lower budget to underperformers
    with get_session() as s:
        c = s.get(Campaign, campaign_id)
        if not c: return {"error": "Campaign not found"}
        # stub: suggest +/-10%
        suggestion = {"campaign_id": campaign_id, "suggested_budget": round(c.budget * 1.05, 2), "note":"Use ROI metrics for real suggestions."}
        return suggestion

def generate_ad_creative(brief, platform):
    prompt = f"Create 10 ad headlines, 5 descriptions, CTAs and 3 image prompts for platform {platform}. Brief: {brief}"
    out = generate_text(prompt, max_tokens=400)
    return {"creative": out}
