import os
import requests
import streamlit as st
import pathlib, json
from utils.ui import load_branding, inject_css, dark_mode_toggle

# -------------------------------
# Streamlit setup
# -------------------------------
st.set_page_config(page_title="Brand N Bloom", page_icon="🌸", layout="wide")
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
    st.caption(b.get("tagline","Because brands deserve to bloom."))

st.page_link("pages/05_📊_Dashboard.py", label="Go to Dashboard", icon="📊")
st.divider()
st.write("Use the left sidebar to navigate all features.")

# -------------------------------
# API connection
# -------------------------------
BASE_URL = os.getenv("BASE_URL", "http://localhost:10000")  # Render injects BASE_URL

# Simple health check
try:
    resp = requests.get(f"{BASE_URL}/health", timeout=5)
    if resp.ok:
        st.success("✅ Connected to API!")
    else:
        st.warning("⚠️ API reachable but returned an error.")
except Exception as e:
    st.error(f"❌ Could not reach API: {e}")

# Example: trigger weekly report
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
import os, threading, requests, streamlit as st, pathlib
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
    # Demo response (replace with real PDF generation later)
    return {"pdf": "reports/weekly_report.pdf", "status": "sent"}

# Run FastAPI in background thread
def run_api():
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="error")

thread = threading.Thread(target=run_api, daemon=True)
thread.start()

# --------------------------
# Streamlit frontend
# --------------------------
st.set_page_config(page_title="Brand N Bloom", page_icon="🌸", layout="wide")

# Branding + Logo
logo_path = pathlib.Path("assets/logo.png")
col1, col2 = st.columns([1,2])
with col1:
    if logo_path.exists():
        st.image(str(logo_path), width=180)
with col2:
    st.title("Brand N Bloom")
    st.caption("Because brands deserve to bloom.")

st.divider()
st.write("Use the left sidebar to navigate all features.")

# --------------------------
# API connection
# --------------------------
BASE_URL = "http://localhost:8000"

# Health check
try:
    resp = requests.get(f"{BASE_URL}/health", timeout=5)
    if resp.ok:
        st.success("✅ Connected to API!")
    else:
        st.warning("⚠️ API reachable but returned an error.")
except Exception as e:
    st.error(f"❌ Could not reach API: {e}")

# Trigger weekly report
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
