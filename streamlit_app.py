import streamlit as st
from utils.ui import inject_css, dark_mode_toggle, card
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()

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

# =============================================================
# Header & Banner
# =============================================================
st.image("assets/banner.png", use_container_width=True)

st.markdown(
    """
# 🌸 Brand N Bloom
**AI-powered growth tools for modern brands**
""",
    unsafe_allow_html=True,
)

# =============================================================
# Top Menu Bar (Horizontal)
# =============================================================
TOP_MENU = [
    "Home", "Features", "Pricing", "Blog", "Dashboard",
    "Contact", "About", "Login", "Signup", "Settings",
    "Audit Tools",
    "BloomScore",
    "Business Compare",
    "Ad Creative Tester",
    "Churn Predictor",
    "CLV Calculator",
    "Market Trend Analyzer",
    "Marketing ROI Tracker",
    "Segmentation",
    "Sentiment Analyzer"
]

st.session_state.page = st.radio(
    "Navigate",
    TOP_MENU,
    horizontal=True,
    index=TOP_MENU.index(st.session_state.page)
)

page = st.session_state.page
# Initialize dashboard storage
if "dashboard_data" not in st.session_state:
    st.session_state.dashboard_data = {
        "ab_test": [],
        "churn": [],
        "clv": [],
        "market_trends": [],
        "roi": []
    }

# Function to save results from any tool
def save_to_dashboard(tool_name, df):
    if tool_name in st.session_state.dashboard_data:
        st.session_state.dashboard_data[tool_name].append(df)
    else:
        st.session_state.dashboard_data[tool_name] = [df]

def generate_ai_caption(tool_name, df):
    # Placeholder: for now, simple textual insight
    if tool_name == "ab_test":
        best_ad = df.loc[df['ctr'].idxmax(), 'ad_version']
        return f"Ad version {best_ad} performed best based on CTR."
    elif tool_name == "churn":
        churn_rate = df['churn'].mean()
        return f"Predicted churn rate: {churn_rate*100:.2f}%."
    elif tool_name == "clv":
        top_customer = df.loc[df['clv'].idxmax(), 'customer_id']
        return f"Customer {top_customer} has highest predicted CLV."
    elif tool_name == "roi":
        top_campaign = df.loc[df['roi'].idxmax(), 'campaign']
        return f"Campaign {top_campaign} delivered highest ROI."
    else:
        return "AI insights not available for this tool yet."

# =============================================================
# ---------------- HOME ----------------
# =============================================================
if page == "Home":
    st.markdown("## Welcome to Brand N Bloom 🌱")
    st.markdown("Grow your brand with clarity, data & AI.")

    if st.button("Get Started →"):
        st.session_state.page = "Features"
        st.experimental_rerun()

# =============================================================
# ---------------- FEATURES ----------------
# =============================================================
elif page == "Features":
    st.markdown("## 🧰 Explore Our Tools")
    # Cards layout
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

# =============================================================
# ---------------- PRICING ----------------
# =============================================================
elif page == "Pricing":
    st.markdown("## 💰 Pricing")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='bnb-card'><h3>Starter</h3><p>₹0 / month</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='bnb-card'><h3>Pro</h3><p>₹1999 / month</p></div>", unsafe_allow_html=True)
        st.markdown("<a class='bnb-cta' href='https://www.paypal.com' target='_blank'>Pay with PayPal</a>", unsafe_allow_html=True)

# =============================================================
# ---------------- BLOG ----------------
# =============================================================
elif page == "Blog":
    st.markdown("## 📰 Blog & Prompts")
    try:
        from ai_tools.prompts import run
        run()
    except Exception as e:
        st.error(f"Blog module error: {e}")

# =============================================================
# ---------------- DASHBOARD ----------------
# =============================================================
elif page == "Dashboard":
    st.markdown("## 📊 Dashboard")
    st.info("Analytics from all tools will appear here.")
    # Placeholder for consolidated dashboard

# =============================================================
# ---------------- CONTACT ----------------
# =============================================================
elif page == "Contact":
    st.markdown("## 📩 Contact Us")
    st.text_input("Email")
    st.text_area("Message")
    st.button("Send")

# =============================================================
# ---------------- ABOUT ----------------
# =============================================================
elif page == "About":
    st.markdown("## ℹ️ About")
    st.markdown("Brand N Bloom is an AI-powered marketing & analytics platform for brands, creators, and businesses.")

# =============================================================
# ---------------- LOGIN ----------------
# =============================================================
elif page == "Login":
    st.markdown("## 🔐 Login")
    st.text_input("Email")
    st.text_input("Password", type="password")
    st.button("Login")

# =============================================================
# ---------------- SIGNUP ----------------
# =============================================================
elif page == "Signup":
    st.markdown("## 🆕 Signup")
    st.text_input("Name")
    st.text_input("Email")
    st.text_input("Password", type="password")
    st.button("Create Account")

# =============================================================
# ---------------- SETTINGS ----------------
# =============================================================
elif page == "Settings":
    st.markdown("## ⚙️ Settings")
    st.info("Theme, account & integrations.")

# =============================================================
# ---------------- TOOLS MAPPING ----------------
# =============================================================
# Legacy + Phase 2 Tools
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
    TOOLS_MAPPING[page]()

# =============================================================
# Footer
# =============================================================
st.markdown("""
---
© 2026 Brand N Bloom • Built with ❤️
""", unsafe_allow_html=True)

