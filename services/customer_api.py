import os
import pandas as pd
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.api import FacebookAdsApi
import razorpay
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest
import json
from services.customer_api import get_customer_data

df = get_customer_data()

# Load environment variables
GA4_PROPERTY_ID = os.getenv("GA4_PROPERTY_ID")
GA4_KEY_FILE_PATH = os.getenv("GA4_KEY_FILE_PATH")
RAZORPAY_SECRET_KEY = os.getenv("RAZORPAY_SECRET_KEY")
FB_APP_ID = os.getenv("FB_APP_ID")
FB_APP_SECRET = os.getenv("FB_APP_SECRET")
FB_ACCESS_TOKEN = os.getenv("FB_ACCESS_TOKEN")
FB_AD_ACCOUNT_ID = os.getenv("FB_AD_ACCOUNT_ID")


def get_ga4_data():
    """
    Fetch user engagement from GA4.
    """
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GA4_KEY_FILE_PATH
    client = BetaAnalyticsDataClient()
    request = RunReportRequest(
        property=f"properties/{GA4_PROPERTY_ID}",
        dimensions=[{"name": "userId"}],
        metrics=[{"name": "activeUsers"}, {"name": "totalRevenue"}]
    )
    response = client.run_report(request)
    data = []
    for row in response.rows:
        data.append({
            "CustomerID": row.dimension_values[0].value,
            "GA_ActiveUsers": int(row.metric_values[0].value),
            "GA_Revenue": float(row.metric_values[1].value)
        })
    return pd.DataFrame(data)


def get_razorpay_data(limit=500):
    """
    Fetch customer payments from Razorpay
    """
    razorpay.api_key = RAZORPAY_SECRET_KEY
    customers = stripe.Customer.list(limit=limit)
    data = []
    for c in customers.data:
        charges = stripe.Charge.list(customer=c.id, limit=100)
        total_spent = sum([ch.amount for ch in charges.data]) / 100
        num_purchases = len(charges.data)
        last_purchase = max([ch.created for ch in charges.data]) if charges.data else None
        data.append({
            "CustomerID": c.id,
            "TotalSpent": total_spent,
            "NumberOfPurchases": num_purchases,
            "LastPurchaseDate": pd.to_datetime(last_purchase, unit='s') if last_purchase else None
        })
    return pd.DataFrame(data)


def get_meta_pixel_data(campaign_id=None):
    """
    Fetch Meta Ads / Pixel data
    """
    FacebookAdsApi.init(FB_APP_ID, FB_APP_SECRET, FB_ACCESS_TOKEN)
    account = AdAccount(FB_AD_ACCOUNT_ID)
    params = {
        'level': 'ad',
        'fields': ['ad_name', 'impressions', 'clicks', 'conversions', 'actions'],
        'limit': 100
    }
    insights = account.get_insights(params=params)
    data = []
    for ad in insights:
        data.append({
            "CustomerID": ad.get('ad_id'),
            "Ad_Impressions": int(ad.get('impressions', 0)),
            "Ad_Clicks": int(ad.get('clicks', 0)),
            "Ad_Conversions": int(ad.get('conversions', 0) if ad.get('conversions') else 0)
        })
    return pd.DataFrame(data)


def get_customer_data():
    """
    Combine GA4, Razorpay, and Meta Pixel into one dataframe
    """
    try:
        df_ga = get_ga4_data()
    except Exception as e:
        print(f"GA4 fetch error: {e}")
        df_ga = pd.DataFrame()

    try:
        df_razorpay = get_razorpay_data()
    except Exception as e:
        print(f"Razorpay fetch error: {e}")
        df_razorpay = pd.DataFrame()

    try:
        df_meta = get_meta_pixel_data()
    except Exception as e:
        print(f"Meta Pixel fetch error: {e}")
        df_meta = pd.DataFrame()

    # Merge dataframes on CustomerID
    dfs = [df for df in [df_ga, df_stripe, df_meta] if not df.empty]
    if dfs:
        df = dfs[0]
        for df_next in dfs[1:]:
            df = df.merge(df_next, on='CustomerID', how='outer')
        return df
    else:
        return pd.DataFrame()


---
