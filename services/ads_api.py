import os
import requests
import pandas as pd

from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adsinsights import AdsInsights
import os
from dotenv import load_dotenv

load_dotenv()

# ----------------- Initialize API -----------------
FB_APP_ID = os.getenv("FB_APP_ID")
FB_APP_SECRET = os.getenv("FB_APP_SECRET")
FB_ACCESS_TOKEN = os.getenv("FB_ACCESS_TOKEN")
FB_AD_ACCOUNT_ID = os.getenv("FB_AD_ACCOUNT_ID")

FacebookAdsApi.init(FB_APP_ID, FB_APP_SECRET, FB_ACCESS_TOKEN)

# ----------------- Fetch Real Ad Performance -----------------
def get_ad_performance(campaign_id: str, limit: int = 10) -> pd.DataFrame:
    """
    Fetch real ad performance metrics from Meta Ads API for a given campaign.
    """
    try:
        account = AdAccount(FB_AD_ACCOUNT_ID)

        params = {
            'level': 'ad',
            'filtering': [{'field':'campaign.name','operator':'EQUAL','value':campaign_id}],
            'time_range': {'since':'2025-01-01','until':'2026-01-21'},  # adjust dynamically if needed
            'fields': [
                AdsInsights.Field.ad_name,
                AdsInsights.Field.date_start,
                AdsInsights.Field.impressions,
                AdsInsights.Field.clicks,
                AdsInsights.Field.spend,
                AdsInsights.Field.conversions
            ],
            'limit': limit
        }

        insights = account.get_insights(params=params)
        data = []

        for ad in insights:
            impressions = int(ad.get('impressions', 0))
            clicks = int(ad.get('clicks', 0))
            conversions = int(ad.get('conversions', 0)) if ad.get('conversions') else 0
            spend = float(ad.get('spend', 0.0))
            ctr = round((clicks / impressions * 100) if impressions else 0, 2)
            cpc = round((spend / clicks) if clicks else 0, 2)
            cpa = round((spend / conversions) if conversions else 0, 2)

            data.append({
                "Ad Name": ad.get('ad_name', ''),
                "Date": ad.get('date_start', ''),
                "Impressions": impressions,
                "Clicks": clicks,
                "CTR (%)": ctr,
                "Conversions": conversions,
                "Spend ($)": spend,
                "CPC ($)": cpc,
                "CPA ($)": cpa
            })

        df = pd.DataFrame(data)
        df.sort_values("Date", ascending=False, inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df

    except Exception as e:
        print(f"Error fetching ads: {e}")
        return pd.DataFrame()  # return empty df on error


