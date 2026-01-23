import streamlit as st
from utils.ui import inject_css, dark_mode_toggle, card
from dotenv import load_dotenv
import os

# ------------------------------
# Load environment variables
# ------------------------------
load_dotenv()
INSTAGRAM_API_KEY = os.getenv("INSTAGRAM_API_KEY")

# ------------------------------
# Page Setup
# ------------------------------
st.set_page_config(
    page_title="Brand N Bloom",
    layout="wide",
    initial_sidebar_state="collapsed"
)

inject_css()
dark_mode_toggle()

# ------------------------------
# Session State Init
# ------------------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"

if "user_id" not in st.session_state:
    st.session_state.user_id = "guest"

# ------------------------------
# Header & Banner
# ------------------------------
st.image("assets/banner.png", use_container_width=True)
st.markdown("# 🌸 Brand N Bloom\n**AI-powered growth tools for modern brands**", unsafe_allow_html=True)

# ------------------------------
# Navigation Data
# ------------------------------
PAGES = ["Home", "Features", "Pricing", "Blog", "Dashboard", "Contact", "About", "Login", "Signup", "Settings"]

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
    "Dashboard": "View & export all insights"
}

TOP_MENU = PAGES + list(TOOLS.keys())

# ------------------------------
# Top Navigation Bar
# ------------------------------
st.session_state.page = st.radio(
    "Navigate",
    TOP_MENU,
    horizontal=True,
    index=TOP_MENU.index(st.session_state.page)
)

page = st.session_state.page

# ------------------------------
# Page Router
# ------------------------------
if page == "Home":
    st.markdown("## Welcome to Brand N Bloom 🌱")
    st.markdown("Grow your brand with clarity, data & AI.")
    if st.button("Get Started →"):
        st.session_state.page = "Features"
        st.experimental_rerun()

elif page == "Features":
    st.markdown("## 🧰 Explore Our Tools")
    cols = st.columns(3)
    for i, (tool, desc) in enumerate(TOOLS.items()):
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
    from ai_tools.prompts import run
    run()

elif page == "Dashboard":
    from ai_tools.dashboard import run
    run()

elif page == "Contact":
    st.markdown("## 📩 Contact Us")
    st.text_input("Email")
    st.text_area("Message")
    st.button("Send")

elif page == "About":
    st.markdown("## ℹ️ About")
    st.markdown("Brand N Bloom is an AI-powered marketing & analytics platform for brands, creators, and businesses.")

elif page == "Login":
    st.markdown("## 🔐 Login")
    email = st.text_input("Email")
    if st.button("Login"):
        from services.user_store import get_user
        user = get_user(email.lower())
        if user:
            st.session_state.user_id = email.lower()
            st.success(f"Logged in as {user['name']}")
        else:
            st.error("User not found")

elif page == "Signup":
    st.markdown("## 🆕 Signup")
    name = st.text_input("Name")
    email = st.text_input("Email")
    if st.button("Create Account"):
        if not name or not email:
            st.warning("Enter both name and email")
        else:
            from services.user_store import create_user
            user_id = create_user(name, email)
            st.session_state.user_id = user_id
            st.success(f"Account created! Logged in as {name}")

elif page == "Settings":
    st.markdown("## ⚙️ Settings")
    st.info("Theme, account & integrations.")
# Legacy tools
from ai_tools.audit_tools import run as run_audit
from ai_tools.bloomscore import run as run_bloomscore

# New Marketing & Data Science tools
from ai_tools.segmentation import run_rfm_analysis
from ai_tools.sentiment import run_sentiment_analyzer
from ai_tools.churn import run_churn_predictor

TOOLS = {
    "Audit Tools": run_audit,
    "BloomScore": run_bloomscore,
    "Business Compare": run_business_compare,
    "Segmentation": run_rfm_analysis,
    "Sentiment Analyzer": run_sentiment_analyzer,
    "Churn Prediction": run_churn_predictor,
    "Dashboard": run_dashboard,
    # ... other tools
}

selected = st.sidebar.radio("Navigate", list(TOOLS.keys()))

# Run the selected tool
TOOLS[selected]()

# ------------------------------
# Tools Router
# ------------------------------
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
    "Dashboard": "dashboard"
}

if page in TOOL_MAPPING:
    st.markdown(f"## 🔧 {page}")
    try:
        module = __import__(f"ai_tools.{TOOL_MAPPING[page]}", fromlist=["run"])
        if hasattr(module, "run"):
            module.run()
        else:
            st.warning("This tool is under development.")
    except Exception as e:
        st.error(f"Failed to load {page}")
        st.exception(e)

# ------------------------------
# Footer
# ------------------------------
st.markdown("---\n© 2026 Brand N Bloom • Built with ❤️", unsafe_allow_html=True)

