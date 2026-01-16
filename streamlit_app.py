# brandnbloom/streamlit_app.py

"""
Brand N Bloom – Streamlit Frontend
Light & Dark themes handled via .streamlit/config.toml
"""

import pathlib
import logging
import streamlit as st
from dotenv import load_dotenv

# =============================================================
# Setup
# =============================================================
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("brandnbloom")

st.set_page_config(
    page_title="Brand N Bloom",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================
# Global CSS (Theme-aware, NO hardcoded colors)
# =============================================================
st.markdown(
    """
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">

<style>
html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.aesthetic-card {
    background: var(--secondary-background-color);
    padding: 24px;
    border-radius: 16px;
    box-shadow: 0px 8px 28px rgba(0,0,0,0.15);
    margin-bottom: 16px;
}

.aesthetic-title {
    font-size: 42px;
    font-weight: 600;
    background: linear-gradient(
        to right,
        var(--primary-color),
        var(--text-color)
    );
    -webkit-background-clip: text;
    color: transparent;
    margin-bottom: 6px;
}

.hero-subtitle {
    font-size: 18px;
    opacity: 0.85;
}
</style>
""",
    unsafe_allow_html=True,
)

# =============================================================
# Sidebar Navigation
# =============================================================
st.sidebar.title("🌸 Brand N Bloom")

choice = st.sidebar.radio(
    "Navigate",
    [
        "Home",
        "Features",
        "Pricing",
        "Blog",
        "Dashboard",
        "BloomScore Pro v2",
        "Settings",
        "Login",
        "Signup",
    ],
)

# =============================================================
# Header
# =============================================================
logo = pathlib.Path("assets/logo.png")

col1, col2 = st.columns([1, 4])

with col1:
    if logo.exists():
        st.image(str(logo), width=120)

with col2:
    st.markdown(
        "<h1 class='aesthetic-title'>Brand N Bloom</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='hero-subtitle'>AI-powered brand intelligence for creators & businesses</div>",
        unsafe_allow_html=True,
    )

st.divider()

# =============================================================
# Pages
# =============================================================
if choice == "Home":
    st.markdown("## Grow your brand with clarity 🌱")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            "<div class='aesthetic-card'>🔍 <b>AI Brand Audits</b><br/>Understand your brand strength</div>",
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            "<div class='aesthetic-card'>📊 <b>Smart Analytics</b><br/>Track growth & engagement</div>",
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            "<div class='aesthetic-card'>✨ <b>Creative Automation</b><br/>Content & ideas powered by AI</div>",
            unsafe_allow_html=True,
        )

    st.button("Get Started →")

# -------------------------------------------------------------

elif choice == "Features":
    st.markdown("## Features")

    features = {
        "BloomScore Pro": "AI-powered brand audit & scoring",
        "SEO Toolkit": "SEO audits & keyword tracking",
        "Content Studio": "Captions, ads & creatives",
        "Analytics": "Growth & engagement dashboards",
    }

    for name, desc in features.items():
        with st.container():
            st.markdown(
                f"<div class='aesthetic-card'><b>{name}</b><br/>{desc}</div>",
                unsafe_allow_html=True,
            )

# -------------------------------------------------------------

elif choice == "Pricing":
    st.markdown("## Pricing")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            "<div class='aesthetic-card'><h3>Starter</h3><p>₹0 / month</p><p>Basic tools</p></div>",
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            "<div class='aesthetic-card'><h3>Pro</h3><p>₹1999 / month</p><p>All AI tools</p></div>",
            unsafe_allow_html=True,
        )
        st.link_button("Pay with PayPal", "https://www.paypal.com")

# -------------------------------------------------------------

elif choice == "Blog":
    st.markdown("## Blog")
    st.info("Blog system coming soon (Markdown / CMS based)")

# -------------------------------------------------------------

elif choice == "Dashboard":
    st.markdown("## Dashboard")
    st.warning("No data yet. Connect tools to activate your dashboard.")

# -------------------------------------------------------------

elif choice == "BloomScore Pro v2":
    st.markdown("## BloomScore Pro v2")
    st.info("Upload brand details to generate an AI-powered audit")

# -------------------------------------------------------------

elif choice == "Settings":
    st.markdown("## Settings")
    st.info("Theme, account & integrations will appear here")

# -------------------------------------------------------------

elif choice == "Login":
    st.markdown("## Login")
    st.text_input("Email")
    st.text_input("Password", type="password")
    st.button("Login")

# -------------------------------------------------------------

elif choice == "Signup":
    st.markdown("## Create Account")
    st.text_input("Name")
    st.text_input("Email")
    st.text_input("Password", type="password")
    st.button("Signup")

# =============================================================
# Footer
# =============================================================
st.divider()
st.caption("© 2026 Brand N Bloom · Built with ❤️ using Streamlit")
