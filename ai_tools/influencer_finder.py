# ai_tools/influencer_finder.py

from typing import Dict, List

# Dummy influencer database
INFLUENCERS_DB = [
    {"name": "Alice Smith", "niche": "marketing", "followers": 12000, "engagement": 0.05},
    {"name": "Bob Johnson", "niche": "fashion", "followers": 50000, "engagement": 0.07},
    {"name": "Cara Lee", "niche": "food", "followers": 8000, "engagement": 0.08},
    {"name": "David Kim", "niche": "marketing", "followers": 25000, "engagement": 0.04},
    {"name": "Ella Chen", "niche": "fashion", "followers": 18000, "engagement": 0.06},
    {"name": "Frank Zhao", "niche": "food", "followers": 12000, "engagement": 0.05},
    {"name": "Grace Park", "niche": "marketing", "followers": 15000, "engagement": 0.07},
]

def find_influencers(niche: str, min_followers: int = 0, max_followers: int = 100000) -> List[Dict]:
    niche = niche.lower()
    results = [
        influencer for influencer in INFLUENCERS_DB
        if influencer["niche"] == niche
        and min_followers <= influencer["followers"] <= max_followers
    ]
    # Sort by engagement rate descending
    results.sort(key=lambda x: x["engagement"], reverse=True)
    return results
