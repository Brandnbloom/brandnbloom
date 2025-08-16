# dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
from instagram_api import get_insights

st.set_page_config(page_title="BloomInsight Dashboard", layout="wide")

st.title("📊 BloomInsight Instagram Dashboard")

metrics = ["impressions", "reach", "profile_views", "followers_count"]
data = get_insights(metrics)

if "data" in data:
    for metric in data["data"]:
        df = pd.DataFrame(metric["values"])
        st.subheader(metric["name"].replace("_", " ").title())
        fig = px.line(df, x="end_time", y="value", title=f"{metric['name']} Over Time")
        st.plotly_chart(fig, use_container_width=True)
else:
    st.error("Could not fetch data. Check your token or API permissions.")
