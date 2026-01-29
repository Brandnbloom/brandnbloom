import streamlit as st
import pandas as pd
import plotly.express as px
from services.customer_api import get_customer_data
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_ai_caption(tool_name, df):
    try:
        prompt = f"Provide insights from {tool_name} dataset: {df.head(10).to_dict()}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        return response.choices[0].message.content
    except:
        return "AI Insight not available"

def run():
    st.header("🌊 Market Trend Analyzer")

    if st.button("Fetch & Analyze Trends"):
        df = get_customer_data()
        if df.empty:
            st.warning("No customer data available.")
            return
        st.success("✅ Customer data loaded")
        st.dataframe(df.head(10))

        # Example: Monthly total spend trend
        if "LastPurchaseDate" in df.columns and "TotalSpent" in df.columns:
            df["LastPurchaseDate"] = pd.to_datetime(df["LastPurchaseDate"])
            trend = df.groupby(df["LastPurchaseDate"].dt.to_period("M"))["TotalSpent"].sum().reset_index()
            trend["LastPurchaseDate"] = trend["LastPurchaseDate"].dt.to_timestamp()

            fig = px.line(trend, x="LastPurchaseDate", y="TotalSpent", title="Monthly Total Spend Trend")
            st.plotly_chart(fig)

        # AI Caption
        caption = generate_ai_caption("Market Trends", df)
        st.success(f"💡 AI Insight: {caption}")

        # Save to dashboard
        df["AI_Insight"] = caption
        if "dashboard_data" not in st.session_state:
            st.session_state["dashboard_data"] = {}
        st.session_state["dashboard_data"]["market_trends"] = df

