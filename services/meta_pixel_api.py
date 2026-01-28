from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
import os
import pandas as pd

FB_ACCESS_TOKEN = os.getenv("FB_ACCESS_TOKEN")
FB_AD_ACCOUNT_ID = os.getenv("FB_AD_ACCOUNT_ID")
FB_APP_ID = os.getenv("FB_APP_ID")
FB_APP_SECRET = os.getenv("FB_APP_SECRET")

FacebookAdsApi.init(FB_APP_ID, FB_APP_SECRET, FB_ACCESS_TOKEN)

def get_meta_pixel_data():
    account = AdAccount(FB_AD_ACCOUNT_ID)
    insights = account.get_insights(fields=[
        "campaign_name", "spend", "impressions", "clicks", "actions"
    ])

    data = []
    for row in insights:
        data.append({
            "campaign": row["campaign_name"],
            "spend": float(row.get("spend", 0)),
            "clicks": int(row.get("clicks", 0)),
            "conversions": sum([a["value"] for a in row.get("actions", []) if a["action_type"]=="offsite_conversion"])
        })

    return pd.DataFrame(data)

