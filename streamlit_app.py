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
# Navigation Data (DEFINE FIRST!)
# =============================================================
PAGES = [
    "Home", "Features", "Pricing", "Blog", "Dashboard",
    "Contact", "About", "Login", "Signup", "Settings"
]

TOOLS = {
    "Audit Tools": "Analyze your brand’s website and social media performance",
    "BloomScore": "Instant brand health score for social profiles",
    "Business Compare": "Benchmark your brand against competitors",
    "Color Extractor": "Extract and analyze your brand’s color palette",
    "Consumer Behavior": "Understand how customers think, feel & buy",
    "Hashtag Recommender": "Generate high-performing hashtags",
    "Influencer Finder": "Find creators aligned with your brand",
    "Insights to Caption": "AI-assisted caption suggestions",
    "Loyalty": "Design loyalty programs that retain customers",
    "OCR Sentiment": "Extract and analyze text sentiment from images",
    "Profile Mock": "Simulate social profiles for testing",
    "Prompts": "AI prompts library for marketing",
}

TOP_MENU = PAGES + list(TOOLS.keys())

# =============================================================
# Top Navigation Bar
# =============================================================
st.session_state.page = st.radio(
    "Navigate",
    TOP_MENU,
    horizontal=True,
    index=TOP_MENU.index(st.session_state.page)
)

page = st.session_state.page

# =============================================================
# ---------------- HOME ----------------
# =============================================================
if page == "Home":
    st.markdown("## Welcome to Brand N Bloom 🌱")
    st.markdown("Grow your brand with clarity, data & AI.")

    if st.button("Get Started →"):
        st.session_state.page = "Features"
        st.rerun()

# =============================================================
# ---------------- FEATURES ----------------
# =============================================================
elif page == "Features":
    st.markdown("## 🧰 Explore Our Tools")

    cols = st.columns(3)
    for i, (tool, desc) in enumerate(TOOLS.items()):
        with cols[i % 3]:
            if st.button(tool, use_container_width=True):
                st.session_state.page = tool
                st.rerun()
            card(f"**{tool}**\n\n{desc}")

# =============================================================
# ---------------- PRICING ----------------
# =============================================================
elif page == "Pricing":
    st.markdown("## 💰 Pricing")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            "<div class='bnb-card'><h3>Starter</h3><p>₹0 / month</p></div>",
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            "<div class='bnb-card'><h3>Pro</h3><p>₹1999 / month</p></div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<a class='bnb-cta' href='https://www.paypal.com' target='_blank'>Pay with PayPal</a>",
            unsafe_allow_html=True,
        )

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
    st.info("Analytics will appear once tools are connected.")

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
    st.markdown(
        "Brand N Bloom is an AI-powered marketing & analytics platform "
        "for brands, creators, and businesses."
    )

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
# ---------------- TOOLS ROUTER ----------------
# =============================================================
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
    "OCR Sentiment": "ocr_sentiment",
    "Profile Mock": "profile_mock",
    "Prompts": "prompts",
}

if page in TOOL_MAPPING:
    st.markdown(f"## 🔧 {page}")

    try:
        module = __import__(
            f"ai_tools.{TOOL_MAPPING[page]}",
            fromlist=["run"]
        )

        if hasattr(module, "run"):
            module.run()
        else:
            st.warning("This tool is under development.")

    except Exception as e:
        st.error(f"Failed to load {page}")
        st.exception(e)

# =============================================================
# Footer
# =============================================================
st.markdown(
    """
---
© 2026 Brand N Bloom • Built with ❤️
""",
    unsafe_allow_html=True,
)
