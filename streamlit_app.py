import os, threading, requests, pathlib
import streamlit as st
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# --------------------------
# FastAPI backend
# --------------------------
app = FastAPI(title="Brand n Bloom - SaaS Tools", version="0.1.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"service": "brand-n-bloom", "status": "ok"}

@app.post("/send-reports")
async def send_reports():
    return {"pdf": "reports/weekly_report.pdf", "status": "sent"}

# Run FastAPI in background thread
def run_api():
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="error")

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
BASE_URL = "http://localhost:8000"

try:
    resp = requests.get(f"{BASE_URL}/health", timeout=5)
    if resp.ok:
        st.success("✅ Connected to API!")
    else:
        st.warning("⚠️ API reachable but returned an error.")
except Exception as e:
    st.error(f"❌ Could not reach API: {e}")

if st.button("Send Weekly Report (Demo)"):
    try:
        resp = requests.post(f"{BASE_URL}/send-reports", timeout=10)
        if resp.ok:
            data = resp.json()
            st.success(f"Report sent! PDF saved at: {data['pdf']}")
        else:
            st.error(f"Error: {resp.text}")
    except Exception as e:
        st.error(f"Request failed: {e}")
