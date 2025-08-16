import streamlit as st
import pandas as pd
import plotly.express as px
import requests

ACCESS_TOKEN = "YOUR_LONG_LIVED_ACCESS_TOKEN"
IG_BUSINESS_ID = "YOUR_INSTAGRAM_BUSINESS_ID"

st.title("📊 BloomInsight Instagram Dashboard")

# Fetch data
url = f"https://graph.facebook.com/v18.0/{IG_BUSINESS_ID}/insights"
params = {
    "metric": "impressions,reach,profile_views,followers_count",
    "period": "day",
    "access_token": ACCESS_TOKEN
}
data = requests.get(url, params=params).json()

# Convert to DataFrame
df = pd.DataFrame(data['data'][0]['values'])  # Example for impressions
st.write(df)

# Chart
fig = px.line(df, x="end_time", y="value", title="Daily Impressions")
st.plotly_chart(fig)
