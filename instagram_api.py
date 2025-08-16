# instagram_api.py
import requests

ACCESS_TOKEN = "YOUR_LONG_LIVED_ACCESS_TOKEN"
IG_BUSINESS_ID = "YOUR_INSTAGRAM_BUSINESS_ID"

def get_insights(metrics):
    url = f"https://graph.facebook.com/v18.0/{IG_BUSINESS_ID}/insights"
    params = {
        "metric": ",".join(metrics),
        "period": "day",
        "access_token": ACCESS_TOKEN
    }
    r = requests.get(url, params=params)
    return r.json()
