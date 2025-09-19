import os, threading, requests, pathlib
import streamlit as st
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# --------------------------
# FastAPI backend
# --------------------------
load_dotenv()

from db import init_db
init_db()

app = FastAPI(title="Brand n Bloom - API Suite")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import Routers
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

# Register Routers
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

# Run FastAPI in background thread
def run_api():
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        log_level="error",
        reload=False
    )

thread = threading.Thread(target=run_api, daemon=True)
thread.start()

# --------------------------
# Streamlit frontend setup
# --------------------------
from utils.ui import load_branding, inject_css, dark_mode_toggle
from tools.website_builder import builder_ui
from tools.seo import seo_audit, keyword_tracker
from tools.ads import creative_generator
from tools.social import calendar_ui
from tools.leads_crm import forms, crm_db
from tools.analytics import dashboard

st.set_page_config(page_title="Brand N Bloom", page_icon="🌸", layout="wide")

# Branding + Theme
b = load_branding()
inject_css()
dark_mode_toggle()

logo_path = pathlib.Path("assets/logo.png")
col1, col2 = st.columns([1,2])
with col1:
    if logo_path.exists():
        st.image(str(logo_path), width=180)
with col2:
    st.title("Brand N Bloom")
    st.caption(b.get("tagline", "Because brands deserve to bloom."))

st.divider()

# --------------------------
# Sidebar Tools
# --------------------------
st.sidebar.title("Brand n Bloom Tools")
choice = st.sidebar.radio("Select tool", [
    "Website Builder", "SEO Audit", "Keyword Tracker",
    "Ad Creative Generator", "Social Scheduler",
    "CRM / Leads", "Analytics Dashboard", "Reputation"
])

if choice == "Website Builder":
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
else:
    st.info("Tool coming soon — select another tool.")

st.divider()

# --------------------------
# API connection check
# --------------------------
BASE_URL = f"http://localhost:{os.getenv('PORT',8000)}"

try:
    resp = requests.get(f"{BASE_URL}/health", timeout=5)
    if resp.ok:
        st.success("✅ Connected to API!")
    else:
        st.warning("⚠️ API reachable but returned an error.")
except Exception as e:
    st.error(f"❌ Could not reach API: {e}")
