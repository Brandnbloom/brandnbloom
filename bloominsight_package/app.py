import streamlit as st
import requests
import pandas as pd
from db import Database
import os
st.set_page_config(layout="wide", page_title="BloomInsight Dashboard")

db = Database(os.environ.get("DATABASE_PATH","data/bloominsight.db"))

st.title("BloomInsight - Instagram Analytics")
col1, col2 = st.columns([2,1])
with col1:
    username = st.text_input("Instagram username (without @)", value="natgeo")
    if st.button("Fetch & Analyze"):
        with st.spinner("Fetching..."):
            r = requests.post("http://localhost:8000/scrape/profile", json={"username":username,"limit":20}, timeout=30)
            data = r.json()
            st.session_state['latest'] = data
if 'latest' in st.session_state:
    data = st.session_state['latest']
    profile = data.get('profile',{})
    kpis = data.get('kpis',{})
    st.subheader(f"Profile: {profile.get('full_name')} (@{profile.get('username')})")
    st.write(profile.get('biography'))
    st.metric("Followers", profile.get('followers',0), delta=None)
    st.metric("Posts", profile.get('posts_count',0))
    st.metric("Brand Health %", data.get('brand_health',{}).get('score',0))
    st.markdown("---")
    st.subheader("KPIs / Summary")
    st.write(kpis)
    # simple charts
    posts = data.get('profile') and db.get_history(profile.get('username'), limit=10)
    st.subheader("Recommendations")
    st.info("Caption optimization and best hashtags are generated per-post in analysis module.")
else:
    st.info("Enter a username and click Fetch & Analyze (ensure the local API is running).")

st.sidebar.title("Controls")
st.sidebar.button("Start Local Scheduler (dev)")
