import os
import requests
import pandas as pd

ACCESS_TOKEN = os.getenv("FB_ACCESS_TOKEN")
AD_ACCOUNT_ID = os.getenv("FB_AD_ACCOUNT_ID")

BASE_URL = "https://graph.facebook.com/v18.0"

def get_ad_performance(campaign_id):
    url = f"{BASE_URL}/{AD_ACCOUNT_ID}/insights"
    params = {
        "fields": "campaign_name,ad_name,impressions,clicks,spend,ctr,cpc",
        "filtering": [{
            "field": "campaign.id",
            "operator": "EQUAL",
            "value": campaign_id
        }],
        "access_token": ACCESS_TOKEN
    }

    res = requests.get(url, params=params).json()
    return pd.DataFrame(res.get("data", []))

