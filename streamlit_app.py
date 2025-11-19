# --------------------------
# brandnbloom/streamlit_app.py
# --------------------------
import os, threading, requests, pathlib
import streamlit as st
from dotenv import load_dotenv

# --------------------------
# PAGE SETTINGS
# --------------------------
st.set_page_config(
    page_title="Brand N Bloom — Dashboard",
    page_icon="🌸",
    layout="wide"
)

# --------------------------
# GLOBAL AESTHETIC CSS
# --------------------------
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">

<style>
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background-color: #FFF9F5;
    }

    [data-testid="stSidebar"] {
        background-color: #F7F1EB !important;
        padding-top: 30px;
    }

    .aesthetic-card {
        background: rgba(255,255,255,0.6);
        padding: 25px;
        border-radius: 18px;
        box-shadow: 0px 4px 18px rgba(0,0,0,0.06);
        backdrop-filter: blur(8px);
    }

    .aesthetic-title {
        font-size: 42px;
        font-weight: 600;
        background: linear-gradient(to right, #A25A3C, #C28F73);
        -webkit-background-clip: text;
        color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------
# FASTAPI BACKEND
# --------------------------
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from db import init_db

init_db()

app = FastAPI(title="Brand N Bloom - API Suite")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
from routers.seo_router import router as seo_router
from routers.keyword_router import router as keyword_router
from routers.content_router import router as content_router
from routers.social_router import router as social_router
from routers.ads_router import router as ads_router
from routers.crm_router import router as crm_router
from routers.analytics_router import router as analytics_router
from routers.reputation_router import router as reputation_router
from routers.advanced_router import router as advanced_router
from routers.internal_router import router as internal_router

app.include_router(seo_router, prefix="/api/seo", tags=["SEO"])
app.include_router(keyword_router, prefix="/api/keywords", tags=["Keywords"])
app.include_router(content_router, prefix="/api/content", tags=["Content"])
app.include_router(social_router, prefix="/api/social", tags=["Social"])
app.include_router(ads_router, prefix="/api/ads", tags=["Ads"])
app.include_router(crm_router, prefix="/api/crm", tags=["CRM"])
app.include_router(analytics_router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(reputation_router, prefix="/api/reputation", tags=["Reputation"])
app.include_router(advanced_router, prefix="/api/advanced", tags=["Advanced"])
app.include_router(internal_router, prefix="/api/internal", tags=["Internal"])

@app.get("/health")
async def health_check():
    return {"service": "brand-n-bloom", "status": "ok"}

def run_api():
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)), log_level="error")

thread = threading.Thread(target=run_api, daemon=True)
thread.start()

# --------------------------
# IMPORT UI MODULES
# --------------------------
from utils.ui import load_branding, inject_css, dark_mode_toggle
from tools.website_builder import builder_ui
from tools.seo import seo_audit, keyword_tracker
from tools.ads import creative_generator
from tools.social import calendar_ui
from tools.leads_crm import forms
from tools.analytics import dashboard

# --------------------------
# HEADER
# --------------------------
branding = load_branding()
inject_css()
dark_mode_toggle()

logo_path = pathlib.Path("assets/logo.png")

col1, col2 = st.columns([1,2])
with col1:
    if logo_path.exists():
        st.image(str(logo_path), width=150)

with col2:
    st.markdown("<h1 class='aesthetic-title'>Brand N Bloom</h1>", unsafe_allow_html=True)
    st.caption(branding.get("tagline", "Because brands deserve to bloom."))

st.divider()

# --------------------------
# SIDEBAR NAVIGATION
# --------------------------
st.sidebar.title("✨ Tools")
choice = st.sidebar.radio("Choose tool", [
    "BloomScore Pro v2",
    "Website Builder",
    "SEO Audit",
    "Keyword Tracker",
    "Ad Creative Generator",
    "Social Scheduler",
    "CRM / Leads",
    "Analytics Dashboard",
])

# --------------------------
# BLOOMSCORE PRO v2 PAGE
# --------------------------
if choice == "BloomScore Pro v2":
    from brandnbloom.bloomscore_pro_v2 import generate_full_report

    st.markdown("<h2 class='aesthetic-title'>BloomScore Pro v2 — Aesthetic Brand Audit</h2>", unsafe_allow_html=True)

    uploaded = st.file_uploader("Upload screenshot or sample image", type=["png", "jpg", "jpeg"])
    texts = st.text_area("Paste sample captions (one per line)", height=150)

    if uploaded:
        img_bytes = uploaded.read()
        sample_texts = [l.strip() for l in texts.splitlines() if l.strip()]

        profile = {
            "image_bytes": img_bytes,
            "sample_texts": sample_texts,
            "metrics": {}
        }

        report = generate_full_report(profile)

        st.markdown("### 🌸 BloomScore Report")
        st.metric("Final Score", report["payload"]["score"])

        st.json(report["payload"]["components"])

        st.markdown("### 🌷 HTML Preview")
        st.components.v1.html(report["html"], height=650)

        if report["pdf_path"]:
            st.success(f"📄 PDF saved at: {report['pdf_path']}")

# --------------------------
# OTHER TOOLS
# --------------------------
elif choice == "Website Builder":
    builder_ui.show_builder()

elif choice == "SEO Audit":
    seo_audit.show_seo_audit()

elif choice == "Keyword Tracker":
    keyword_tracker.show_keyword_tracker()

elif choice == "Ad Creative Generator":
    creative_generator.show_creative_ui()

elif choice == "Social Scheduler":
    calendar_ui.show_calendar()

elif choice == "CRM / Leads":
    forms.show_forms_ui()

elif choice == "Analytics Dashboard":
    dashboard.show_dashboard()

st.divider()

# --------------------------
# API CONNECTION CHECK
# --------------------------
BASE_URL = f"http://localhost:{os.getenv('PORT',8000)}"

try:
    r = requests.get(f"{BASE_URL}/health", timeout=4)
    if r.ok:
        st.success("Connected to API backend!")
    else:
        st.warning("API reachable but returned an error.")
except Exception as e:
    st.error(f"API offline: {e}")
