import streamlit as st
from utils import can_use_tool, increment_usage

st.title("📈 BloomInsight – Performance Dashboard")

if can_use_tool("BloomInsight"):
    st.markdown("This tool combines data from Instagram, Google My Business, and your website.")
    st.write("🛠️ Integration pending. Here’s a sample dashboard:")

    st.metric("Instagram Followers", "8,940", "+120")
    st.metric("Website Visitors (last 30d)", "12,350", "↑12%")
    st.metric("GMB Reviews", "421", "⭐ 4.5 avg")