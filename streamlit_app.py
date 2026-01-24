import streamlit as st
from utils.ui import inject_css, dark_mode_toggle, card
from dotenv import load_dotenv
import pandas as pd
import plotly.express as px
import openai
import os

# Load env variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# =============================================================
# Page Setup
# =============================================================
st.set_page_config(
    page_title="Brand N Bloom",
    layout="wide",
    initial_sidebar_state="collapsed"
)

inject_css()
dark_mode_toggle()

# =============================================================
# Session State Init
# =============================================================
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Dashboard storage
if "dashboard_data" not in st.session_state:
    st.session_state.dashboard_data = {
        "ab_test": [],
        "churn": [],
        "clv": [],
        "market_trends": [],
        "roi": [],
        "social_posts": []
    }

def save_to_dashboard(tool_name, df):
    if tool_name in st.session_state.dashboard_data:
        st.session_state.dashboard_data[tool_name].append(df)
    else:
        st.session_state.dashboard_data[tool_name] = [df]

def visualize_data(tool_name, df):
    st.markdown(f"#### Data Visualization: {tool_name.replace('_',' ').title()}")
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    if len(numeric_cols) >= 2:
        fig = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1],
                         color=df.columns[0], title=f"{tool_name.replace('_',' ').title()} Analysis")
        st.plotly_chart(fig, use_container_width=True)
    elif numeric_cols:
        fig = px.bar(df, x=df.index, y=numeric_cols[0], title=f"{tool_name.replace('_',' ').title()} Metrics")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No numeric data available for visualization.")

def generate_ai_caption(tool_name, df):
    try:
        preview = df.head(5).to_dict()
        prompt = f"Provide actionable marketing insights based on the following {tool_name} data: {preview}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role":"system","content":"You are a marketing analyst."},
                {"role":"user","content":prompt}
            ],
            temperature=0.7,
            max_tokens=150
        )
        caption = response.choices[0].message.content.strip()
        return caption
    except Exception as e:
        return f"AI Caption generation failed: {e}"

# =============================================================
# Header & Banner
# =============================================================
st.image("assets/banner.png", use_container_width=True)
st.markdown("# 🌸 Brand N Bloom\n**AI-powered growth tools for modern brands**", unsafe_allow_html=True)

# =============================================================
# Top Menu
# =============================================================
TOP_MENU = [
    "Home", "Features", "Pricing", "Blog", "Dashboard",
    "Contact", "About", "Login", "Signup", "Settings",
    "Audit Tools", "BloomScore", "Business Compare",
    "Ad Creative Tester", "Churn Predictor", "CLV Calculator",
    "Market Trend Analyzer", "Marketing ROI Tracker",
    "Segmentation", "Sentiment Analyzer"
]

st.session_state.page = st.radio(
    "Navigate",
    TOP_MENU,
    horizontal=True,
    index=TOP_MENU.index(st.session_state.page)
)

page = st.session_state.page

# =============================================================
# ---------------- PAGES ----------------
# =============================================================
if page == "Home":
    st.markdown("## Welcome to Brand N Bloom 🌱")
    st.markdown("Grow your brand with clarity, data & AI.")
    if st.button("Get Started →"):
        st.session_state.page = "Features"
        st.experimental_rerun()

elif page == "Features":
    st.markdown("## 🧰 Explore Our Tools")
    TOOLS_DESCRIPTIONS = {
        "Audit Tools": "Analyze your brand’s website and social media performance",
        "BloomScore": "Instant brand health score for social profiles",
        "Business Compare": "Benchmark your brand against competitors",
        "Ad Creative Tester": "A/B testing simulation for ads",
        "Churn Predictor": "Predict customer churn using ML",
        "CLV Calculator": "Forecast customer lifetime value",
        "Market Trend Analyzer": "Time-series analysis of emerging niches",
        "Marketing ROI Tracker": "Multi-touch attribution modeling",
        "Segmentation": "Customer RFM segmentation",
        "Sentiment Analyzer": "NLP-driven social sentiment analysis"
    }
    cols = st.columns(3)
    for i, (tool, desc) in enumerate(TOOLS_DESCRIPTIONS.items()):
        with cols[i % 3]:
            if st.button(tool, use_container_width=True):
                st.session_state.page = tool
                st.experimental_rerun()
            card(f"**{tool}**\n\n{desc}")

elif page == "Pricing":
    st.markdown("## 💰 Pricing")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='bnb-card'><h3>Starter</h3><p>₹0 / month</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='bnb-card'><h3>Pro</h3><p>₹1999 / month</p></div>", unsafe_allow_html=True)
        st.markdown("<a class='bnb-cta' href='https://www.paypal.com' target='_blank'>Pay with PayPal</a>", unsafe_allow_html=True)

elif page == "Blog":
    st.markdown("## 📰 Blog & Prompts")
    try:
        from ai_tools.prompts import run
        run()
    except Exception as e:
        st.error(f"Blog module error: {e}")

elif page == "Dashboard":
    st.markdown("## 📊 Centralized Dashboard")
    st.info("All tool results and AI insights in one place")
    for tool_name, data_list in st.session_state.dashboard_data.items():
        if data_list:
            st.markdown(f"### 🛠 {tool_name.replace('_',' ').title()}")
            for i, df in enumerate(data_list):
                st.write(f"Result {i+1}")
                st.dataframe(df)
                visualize_data(tool_name, df)
                caption = generate_ai_caption(tool_name, df)
                st.success(f"💡 AI Insight: {caption}")

# Other legacy pages: Contact, About, Login, Signup, Settings
# (unchanged)

# =============================================================
# ---------------- TOOLS MAPPING ----------------
# =============================================================
from ai_tools.audit_tools import run as run_audit
from ai_tools.bloomscore import run as run_bloomscore
from ai_tools.business_compare import run as run_business_compare
from ai_tools.ad_creative_tester import run as run_ad_creative_tester
from ai_tools.churn_predictor import run as run_churn_predictor
from ai_tools.clv_calculator import run as run_clv_calculator
from ai_tools.market_trends import run as run_market_trends
from ai_tools.marketing_roi import run as run_marketing_roi
from ai_tools.segmentation import run_rfm_analysis
from ai_tools.sentiment import run_sentiment_analyzer

TOOLS_MAPPING = {
    "Audit Tools": run_audit,
    "BloomScore": run_bloomscore,
    "Business Compare": run_business_compare,
    "Ad Creative Tester": run_ad_creative_tester,
    "Churn Predictor": run_churn_predictor,
    "CLV Calculator": run_clv_calculator,
    "Market Trend Analyzer": run_market_trends,
    "Marketing ROI Tracker": run_marketing_roi,
    "Segmentation": run_rfm_analysis,
    "Sentiment Analyzer": run_sentiment_analyzer
}

if page in TOOLS_MAPPING:
    TOOLS_MAPPING[page]()  # Each tool now fetches real data from APIs / DB

# =============================================================
# Footer
# =============================================================
st.markdown("""
---
© 2026 Brand N Bloom • Built with ❤️
""", unsafe_allow_html=True)

