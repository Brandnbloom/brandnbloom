import os
import requests
import pandas as pd

ACCESS_TOKEN = os.getenv("FB_ACCESS_TOKEN")
PIXEL_ID = os.getenv("FB_PIXEL_ID")

def get_meta_pixel_data():
    url = f"https://graph.facebook.com/v18.0/{PIXEL_ID}/events"
    params = {
        "access_token": ACCESS_TOKEN
    }

    res = requests.get(url, params=params).json()
    events = res.get("data", [])

    data = []
    for e in events:
        data.append({
            "email": e.get("user_data", {}).get("em"),
            "conversions": e.get("custom_data", {}).get("value", 0)
        })

    return pd.DataFrame(data)
