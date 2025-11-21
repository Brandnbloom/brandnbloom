import os, threading, requests, pathlib
import streamlit as st
from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# --------------------------
# Load env + Init DB
# --------------------------
load_dotenv()
from db import init_db
init_db()

# --------------------------
# FastAPI backend
# --------------------------
app = FastAPI(title="Brand n Bloom SaaS API", version="1.0")

origins = ["*"]  # ⚠️ Replace with frontend domain in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
from routers import (
    seo_router,
    keyword_router,
    content_router,
    social_router,
    ads_router,
    crm_router,
    analytics_router,
    reputation_router,
    advanced_router,
    internal_router
)

# Register all routers
app.include_router(seo_router.router, prefix="/api/seo", tags=["SEO Tools"])
app.include_router(keyword_router.router, prefix="/api/keywords", tags=["Keyword Tools"])
app.include_router(content_router.router, prefix="/api/content", tags=["Content Tools"])
app.include_router(social_router.router, prefix="/api/social", tags=["Social Media Tools"])
app.include_router(ads_router.router, prefix="/api/ads", tags=["Ads & Marketing Tools"])
app.include_router(crm_router.router, prefix="/api/crm", tags=["CRM & Leads"])
app.include_router(analytics_router.router, prefix="/api/analytics", tags=["Analytics & Reporting"])
app.include_router(reputation_router.router, prefix="/api/reputation", tags=["Reputation Tools"])
app.include_router(advanced_router.router, prefix="/api/advanced", tags=["Advanced AI Tools"])
app.include_router(internal_router.router, prefix="/api/internal", tags=["Agency Management Tools"])

@app.get("/")
def root():
    return {"message": "Welcome to Brand n Bloom SaaS API"}

@app.get("/health")
async def health_check():
    return {"service": "brand-n-bloom", "status": "ok"}

# Background FastAPI thread
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
# Streamlit UI Setup
# --------------------------
from utils.ui import load_branding, inject_css, dark_mode_toggle
from tools.website_builder import builder_ui
from tools.seo import seo_audit, keyword_tracker
from tools.ads import creative_generator
from tools.social import calendar_ui
from tools.leads_crm import forms
from tools.analytics import dashboard

st.set_page_config(page_title="Brand N Bloom", page_icon="🌸", layout="wide")

# Branding + Theme
branding = load_branding()
inject_css()
dark_mode_toggle()

# Logo + Title
logo_path = pathlib.Path("assets/logo.png")
col1, col2 = st.columns([1, 2])
with col1:
    if logo_path.exists():
        st.image(str(logo_path), width=180)
with col2:
    st.title("Brand N Bloom")
    st.caption(branding.get("tagline", "Because brands deserve to bloom."))

st.divider()

# --------------------------
# Sidebar Menu
# --------------------------
st.sidebar.title("Brand n Bloom Tools")

menu = [
    "Home",
    "Register",
    "Login",
    "Dashboard",
    "SEO Tools",
    "Social Tools",
    "Ads Tools",
    "CRM Tools",
    "Analytics Tools"
]

choice = st.sidebar.selectbox("Menu", menu)

# --------------------------
# Page Routing
# --------------------------
if choice == "Home":
    st.subheader("🏠 Welcome to Brand n Bloom")
    st.write("Your all-in-one SaaS platform for brand growth.")

elif choice == "Register":
    st.subheader("📝 Register")
    st.write("User registration form goes here.")

elif choice == "Login":
    st.subheader("🔑 Login")
    st.write("User login form goes here.")

elif choice == "Dashboard":
    st.subheader("📊 Dashboard")
    dashboard.show_dashboard()

elif choice == "SEO Tools":
    st.subheader("🔍 SEO Tools")
    seo_audit.show_seo_audit()
    keyword_tracker.show_keyword_tracker()

elif choice == "Social Tools":
    st.subheader("📅 Social Media Tools")
    calendar_ui.show_calendar()

elif choice == "Ads Tools":
    st.subheader("🎨 Ads & Creative Tools")
    creative_generator.show_creative_ui()

elif choice == "CRM Tools":
    st.subheader("🤝 CRM & Leads")
    forms.show_forms_ui()

elif choice == "Analytics Tools":
    import AnalyticsTools  # your external module
    st.subheader("📈 Analytics Tools")

else:
    st.info("Tool coming soon — select another tool.")

st.divider()

# --------------------------
# API Health Check
# --------------------------
BASE_URL = f"http://localhost:{os.getenv('PORT', 8000)}"

try:
    resp = requests.get(f"{BASE_URL}/health", timeout=5)
    if resp.ok:
        st.success("✅ Connected to API!")
    else:
        st.warning("⚠️ API reachable but returned an error.")
except Exception as e:
    st.error(f"❌ Could not reach API: {e}")
