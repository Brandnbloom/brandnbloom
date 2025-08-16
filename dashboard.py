import streamlit as st
import requests
import plotly.express as px

st.set_page_config(page_title="BloomInsight", layout="wide")
st.title("📊 BloomInsight – Instagram Insights Dashboard")

api_base = "https://your-api-url.onrender.com"

access_token = st.text_input("Enter your access token")
ig_user_id = st.text_input("Enter your Instagram User ID")

if st.button("Get Report"):
    data = requests.get(f"{api_base}/insights", params={
        "token": access_token,
        "ig_user_id": ig_user_id
    }).json()

    # Example chart
    for metric in data.get("data", []):
        st.subheader(metric["name"])
        df = [{"date": v["end_time"], "value": v["value"]} for v in metric["values"]]
        fig = px.line(df, x="date", y="value", title=metric["name"])
        st.plotly_chart(fig)

    # KPI example
    st.metric("Latest Reach", df[-1]["value"])

