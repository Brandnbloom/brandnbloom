# brandnbloom/streamlit_app.py

"""
Brand N Bloom - Streamlit frontend + FastAPI backend runner
"""

import os
import threading
import logging
import pathlib
import requests
import streamlit as st
from dotenv import load_dotenv

# =============================================================
# Load environment & logging
# =============================================================
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("brandnbloom")

# =============================================================
# Streamlit page config
# =============================================================
st.set_page_config(
    page_title="Brand N Bloom",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================
# Global Aesthetic CSS (DARK MODE SAFE)
# =============================================================
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.aesthetic-card {
    background: rgba(22,27,34,0.9);
    padding: 22px;
    border-radius: 16px;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.4);
}

.aesthetic-title {
    font-size: 42px;
    font-weight: 600;
    background: linear-gradient(to right, #C28F73, #E0BFA5);
    -webkit-background-clip: text;
    color: transparent;
    margin-bottom: 6px;
}
</style>
""", unsafe_allow_html=True)

# =============================================================
# Start FastAPI backend (thread)
# =============================================================
def _start_api():
    try:
        from fastapi import FastAPI
        import uvicorn

        app = FastAPI(title="Brand N Bloom API")

        @app.get("/health")
        async def health():
            return {"status": "ok"}

        uvicorn.run(
            app,
            host="0.0.0.0",
            port=int(os.getenv("PORT", 8000)),
            log_level="error",
        )
    except Exception as e:
        logger.exception("API failed: %s", e)

threading.Thread(target=_start_api, daemon=True).start()

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
c1, c2 = st.columns([1, 4])

with c1:
    if logo.exists():
        st.image(str(logo), width=120)

with c2:
    st.markdown("<h1 class='aesthetic-title'>Brand N Bloom</h1>", unsafe_allow_html=True)
    st.caption("AI-powered brand intelligence for creators & businesses")

st.divider()

# =============================================================
# Page Router (TEMP PLACEHOLDER)
# =============================================================
if choice == "Home":
    st.markdown("### Welcome to Brand N Bloom 🌸")
    st.write("Your all-in-one AI brand growth platform.")

elif choice == "Features":
    st.info("Features page coming next")

elif choice == "Pricing":
    st.info("Pricing + PayPal coming next")

elif choice == "Blog":
    st.info("Blog system coming next")

elif choice == "Dashboard":
    st.info("Dashboard data coming next")

elif choice == "BloomScore Pro v2":
    st.info("BloomScore tool here")

elif choice == "Settings":
    st.info("Settings page")

elif choice == "Login":
    st.info("Login page")

elif choice == "Signup":
    st.info("Signup page")

# =============================================================
# Footer
# =============================================================
st.divider()
try:
    r = requests.get("http://127.0.0.1:8000/health", timeout=2)
    if r.ok:
        st.success("API connected")
except Exception:
    st.warning("API offline")
