from __future__ import annotations
import requests
from typing import Dict, Any, List
from utils import get_env

GRAPH_VER = "v18.0"
BASE = f"https://graph.facebook.com/{GRAPH_VER}"

ACCESS_TOKEN = get_env("LONG_LIVED_TOKEN")
IG_BUSINESS_ID = get_env("IG_BUSINESS_ID")

# --- Core fetchers ---

def fetch_account_insights(metrics: List[str], period: str = "day") -> Dict[str, Any]:
    url = f"{BASE}/{IG_BUSINESS_ID}/insights"
    params = {
        "metric": ",".join(metrics),
        "period": period,
        "access_token": ACCESS_TOKEN,
    }
    return requests.get(url, params=params, timeout=60).json()


def fetch_media(limit: int = 50) -> Dict[str, Any]:
    # Pull recent media to compute top posts/hashtags
    fields = "id,caption,media_type,media_url,permalink,timestamp,like_count,comments_count"
    url = f"{BASE}/{IG_BUSINESS_ID}/media"
    params = {"fields": fields, "limit": limit, "access_token": ACCESS_TOKEN}
    return requests.get(url, params=params, timeout=60).json()


def fetch_media_insights(media_id: str) -> Dict[str, Any]:
    url = f"{BASE}/{media_id}/insights"
    params = {"metric": "impressions,reach,saved", "access_token": ACCESS_TOKEN}
    return requests.get(url, params=params, timeout=60).json()


def fetch_profile() -> Dict[str, Any]:
    fields = "username,name,biography,profile_picture_url,followers_count,follows_count,ig_id"
    url = f"{BASE}/{IG_BUSINESS_ID}"
    params = {"fields": fields, "access_token": ACCESS_TOKEN}
    return requests.get(url, params=params, timeout=60).json()
