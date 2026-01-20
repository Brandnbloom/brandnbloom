# streamlit_app.py

import streamlit as st
from utils.ui import inject_css, dark_mode_toggle, card

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
# Header & Banner
# =============================================================
st.image("assets/banner.png", use_column_width=True)
st.markdown("""
# 🌸 Brand N Bloom
AI-powered growth tools for modern brands
""", unsafe_allow_html=True)

# =============================================================
# Top Menu Bar (Pages + Tools)
# =============================================================
PAGES = [
    "Home", "Features", "Pricing", "Blog", "Dashboard", 
    "Contact", "About", "Login", "Signup", "Settings"
]

TOOLS = [
    "Audit Tools",
    "BloomScore",
    "Business Compare",
    "Color Extractor",
    "Consumer Behavior",
    "Hashtag Recommender",
    "Influencer Finder",
    "Insights to Caption",
    "Loyalty",
    "Menu Pricing",
    "OCR Sentiment",
    "Profile Mock",
    "Prompts"
]

# Combine Pages + Tools for top menu
TOP_MENU = PAGES + TOOLS

st.session_state.page = st.radio(
    "Navigate",
    TOP_MENU,
    horizontal=True,
    index=0
)

# =============================================================
# Helper: Page Container
# =============================================================
def page_container():
    return st.container()

# =============================================================
# Page Routing
# =============================================================
page = st.session_state.page

# ---------------- Home ----------------
if page == "Home":
    with page_container():
        st.markdown("## Welcome to Brand N Bloom 🌱")
        st.markdown("Grow your brand with AI-powered clarity.")
        st.button("Get Started →"):
        st.session_state.page = "Tools"
        st.rerun()

# ---------------- Features ----------------
elif page == "Features":
    from ai_tools.audit_tools import run as audit_run
    with page_container():
        st.markdown("## Features")
        st.markdown("Click a tool below to explore its capabilities:")
        cols = st.columns(3)
        for i, tool in enumerate(TOOLS):
            with cols[i % 3]:
                if st.button(tool, use_container_width=True):
                    st.session_state.page = tool
                card(tool)

# ---------------- Pricing ----------------
elif page == "Pricing":
    with page_container():
        st.markdown("## Pricing Plans")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div class='bnb-card'><h3>Starter</h3><p>₹0 / month</p></div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div class='bnb-card'><h3>Pro</h3><p>₹1999 / month</p></div>", unsafe_allow_html=True)
            st.markdown("<a class='bnb-cta' href='https://www.paypal.com'>Pay with PayPal</a>", unsafe_allow_html=True)

# ---------------- Blog ----------------
elif page == "Blog":
    from ai_tools.prompts import run as prompts_run
    with page_container():
        st.markdown("## Blog / Ideas")
        prompts_run()

# ---------------- Dashboard ----------------
elif page == "Dashboard":
    with page_container():
        st.markdown("## Dashboard")
        st.warning("Connect tools to activate dashboard analytics.")

# ---------------- Contact ----------------
elif page == "Contact":
    from ai_tools.profile_mock import run as profile_run
    with page_container():
        st.markdown("## Contact Us")
        profile_run()

# ---------------- About ----------------
elif page == "About":
    with page_container():
        st.markdown("## About Brand N Bloom")
        st.markdown("AI-powered brand growth platform for creators and businesses.")

# ---------------- Login ----------------
elif page == "Login":
    with page_container():
        st.markdown("## Login")
        st.text_input("Email")
        st.text_input("Password", type="password")
        st.button("Login")

# ---------------- Signup ----------------
elif page == "Signup":
    with page_container():
        st.markdown("## Signup")
        st.text_input("Name")
        st.text_input("Email")
        st.text_input("Password", type="password")
        st.button("Signup")

# ---------------- Settings ----------------
elif page == "Settings":
    with page_container():
        st.markdown("## Settings")
        st.info("Theme, account & integrations.")

# =============================================================
# ---------------- Tools Routing ----------------
# =============================================================
# Mapping tool name → run function
TOOL_MAPPING = {
    "Audit Tools": "audit_tools",
    "BloomScore": "bloomscore",
    "Business Compare": "business_compare",
    "Color Extractor": "color_extractor",
    "Consumer Behavior": "consumer_behavior",
    "Hashtag Recommender": "hashtag_recommender",
    "Influencer Finder": "influencer_finder",
    "Insights to Caption": "insights_caption",
    "Loyalty": "loyalty",
    "Menu Pricing": "menu_pricing",
    "OCR Sentiment": "ocr_sentiment",
    "Profile Mock": "profile_mock",
    "Prompts": "prompts",
}

if page in TOOL_MAPPING:
    tool_module_name = TOOL_MAPPING[page]
    with page_container():
        st.markdown(f"## 🧰 {page}")
        st.markdown("Loading tool...")
        try:
            tool_module = __import__(f"ai_tools.{tool_module_name}", fromlist=["run"])
            tool_module.run()
        except Exception as e:
            st.error(f"Failed to load {page}. Error: {e}")

# =============================================================
# Footer
# =============================================================
st.markdown("""
---
© 2026 Brand N Bloom • Built with ❤️
""", unsafe_allow_html=True)
