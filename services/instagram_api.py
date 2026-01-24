import os
import requests
import pandas as pd

ACCESS_TOKEN = os.getenv("FB_ACCESS_TOKEN")
BASE_URL = "https://graph.facebook.com/v18.0"

def get_posts(ig_user_id, limit=25):
    url = f"{BASE_URL}/{ig_user_id}/media"
    params = {
        "fields": "caption,like_count,comments_count,media_type,timestamp",
        "limit": limit,
        "access_token": ACCESS_TOKEN
    }

    res = requests.get(url, params=params).json()
    return pd.DataFrame(res.get("data", []))
