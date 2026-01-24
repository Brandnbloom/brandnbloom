# services/ads_service.py

from db.db import get_session
from models.models import Campaign, Event
from services.ai_client import generate_text
import json
import pandas as pd



def log_event(event_type: str, payload: dict):
    """Utility to log system events."""
    with get_session() as session:
        ev = Event(type=event_type, payload=json.dumps(payload))
        session.add(ev)
        session.commit()
        return ev.id


def create_campaign(name: str, platform: str, budget: float):
    """Create a new ad campaign."""
    with get_session() as session:
        campaign = Campaign(name=name, platform=platform, budget=budget)
        session.add(campaign)
        session.commit()
        session.refresh(campaign)

        # Log event
        log_event("campaign_created", {
            "campaign_id": campaign.id,
            "name": name,
            "platform": platform,
            "budget": budget
        })

        return {
            "campaign_id": campaign.id,
            "name": campaign.name,
            "platform": campaign.platform,
            "budget": campaign.budget
        }


def optimize_budget(campaign_id: int):
    """Suggest a budget update (placeholder logic)."""
    with get_session() as session:
        campaign = session.get(Campaign, campaign_id)
        if not campaign:
            return {"error": "Campaign not found"}

        # Simple heuristic: increase by 5%
        suggested_budget = round(campaign.budget * 1.05, 2)

        suggestion = {
            "campaign_id": campaign_id,
            "current_budget": campaign.budget,
            "suggested_budget": suggested_budget,
            "note": "Replace with performance-based optimization."
        }

        log_event("budget_optimized", suggestion)

        return suggestion


def generate_ad_creative(brief: str, platform: str):
    """Generate AI-powered ad creative content."""
    prompt = (
        f"Generate ad creatives for {platform}.\n"
        f"BRIEF: {brief}\n\n"
        "- 10 ad headlines\n"
        "- 5 descriptions\n"
        "- 5 CTAs\n"
        "- 3 image prompts\n"
        "Return results in JSON format."
    )

    output = generate_text(prompt, max_tokens=500)

    log_event("ad_creative_generated", {"platform": platform, "brief": brief})

    return {"creative": output}

def get_ad_performance(campaign_id):
    data = [
        {"creative": "A", "CTR": 1.8, "CPA": 120},
        {"creative": "B", "CTR": 2.5, "CPA": 90},
    ]
    return pd.DataFrame(data)

