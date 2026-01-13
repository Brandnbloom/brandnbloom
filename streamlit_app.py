"""
Brand N Bloom - Streamlit frontend + FastAPI backend runner
Includes: SEO, analytics, BloomScore Pro v2, and other tools.
"""

import os
import threading
import logging
import pathlib
import requests
import streamlit as st
from dotenv import load_dotenv

# =============================================================
# Dark mode state
# =============================================================
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

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
    page_title="Brand N Bloom — Dashboard",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================
# THEME INJECTOR (REAL DARK MODE)
# =============================================================
def inject_theme():
    if st.session_state.dark_mode:
        st.markdown("""
        <style>
        html, body, [data-testid="stApp"] {
            background-color: #0E1117 !important;
            color: #FAFAFA !important;
            font-family: 'Poppins', sans-serif;
        }

        [data-testid="stSidebar"] {
            background-color: #161B22 !important;
        }

        .aesthetic-card {
            background-color: #161B22 !important;
            color: #FAFAFA !important;
            border-radius: 14px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.6);
            padding: 22px;
        }

        input, textarea, select {
            background-color: #0E1117 !important;
            color: #FAFAFA !important;
            border: 1px solid #30363D !important;
        }

        div[data-baseweb="select"] > div {
            background-color: #0E1117 !important;
            color: #FAFAFA !important;
        }

        .stButton > button {
            background-color: #A25A3C !important;
            color: white !important;
            border-radius: 10px;
            border: none;
            padding: 8px 16px;
        }

        [data-testid="stMetric"] {
            background-color: #161B22;
            padding: 12px;
            border-radius: 12px;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        html, body, [data-testid="stApp"] {
            background-color: #FFF9F5 !important;
            color: #2C2C2C !important;
            font-family: 'Poppins', sans-serif;
        }

        [data-testid="stSidebar"] {
            background-color: #F7F1EB !important;
        }

        .aesthetic-card {
            background: rgba(255,255,255,0.6);
            padding: 22px;
            border-radius: 14px;
            box-shadow: 0px 6px 20px rgba(0,0,0,0.06);
        }
        </style>
        """, unsafe_allow_html=True)

inject_theme()

# =============================================================
# Fonts & Titles
# =============================================================
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
.aesthetic-title {
    font-size: 40px;
    font-weight: 600;
    background: linear-gradient(to right, #A25A3C, #C28F73);
    -webkit-background-clip: text;
    color: transparent;
    margin: 0;
}
</style>
""", unsafe_allow_html=True)

# =============================================================
# Start FastAPI backend (thread)
# =============================================================
def _start_api():
    try:
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        import uvicorn

        app = FastAPI(title="Brand N Bloom API")

        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )

        @app.get("/health")
        async def health():
            return {"status": "ok"}

        uvicorn.run(
            app,
            host="0.0.0.0",
            port=int(os.getenv("PORT", 8000)),
            log_level="error"
        )
    except Exception as e:
        logger.exception("API failed: %s", e)

threading.Thread(target=_start_api, daemon=True).start()

# =============================================================
# SIDEBAR
# =============================================================
st.sidebar.title("✨ Brand N Bloom")

st.sidebar.markdown("### 🎨 Appearance")
toggle = st.sidebar.toggle("Dark Mode", value=st.session_state.dark_mode)
if toggle != st.session_state.dark_mode:
    st.session_state.dark_mode = toggle
    st.rerun()

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

# =============================================================
# HEADER
# =============================================================
logo = pathlib.Path("assets/logo.png")
c1, c2 = st.columns([1, 3])

with c1:
    if logo.exists():
        st.image(str(logo), width=150)

with c2:
    st.markdown("<h1 class='aesthetic-title'>Brand N Bloom</h1>", unsafe_allow_html=True)
    st.caption("Because brands deserve to bloom.")

st.divider()

# =============================================================
# SAFE REPORT DIRECTORY
# =============================================================
SAFE_REPORT_DIR = pathlib.Path("reports").resolve()
SAFE_REPORT_DIR.mkdir(exist_ok=True)

def is_safe_report_path(path: str) -> bool:
    try:
        resolved = pathlib.Path(path).resolve()
        return SAFE_REPORT_DIR in resolved.parents
    except Exception:
        return False

# =============================================================
# BloomScore Pro v2
# =============================================================
if choice == "BloomScore Pro v2":
    try:
        from brandnbloom.bloomscore_pro_v2 import generate_full_report
    except Exception as e:
        st.error("BloomScore module missing.")
        logger.error(e)
        generate_full_report = None

    uploaded = st.file_uploader("Upload image", ["png", "jpg", "jpeg"])
    texts = st.text_area("Paste captions (one per line)", height=150)

    if uploaded and generate_full_report:
        with st.spinner("Generating report…"):
            try:
                profile = {
                    "image_bytes": uploaded.read(),
                    "sample_texts": [l.strip() for l in texts.splitlines() if l.strip()],
                    "metrics": {}
                }

                report = generate_full_report(profile)

                st.metric("Final Score", report["payload"].get("score", "—"))
                st.json(report["payload"].get("components", {}))

                if report.get("html"):
                    st.components.v1.html(report["html"], height=650)

                pdf_path = report.get("pdf_path")
                if pdf_path:
                    filename = os.path.basename(pdf_path)
                    safe_path = SAFE_REPORT_DIR / filename
                    if safe_path.exists() and is_safe_report_path(str(safe_path)):
                        with safe_path.open("rb") as f:
                            st.download_button(
                                "📄 Download PDF Report",
                                f.read(),
                                file_name=filename,
                                mime="application/pdf"
                            )

            except Exception as e:
                st.error("Report generation failed.")
                logger.exception(e)
else:
    st.info(f"{choice} coming soon 🚧")

# =============================================================
# FOOTER API HEALTH
# =============================================================
st.divider()
try:
    r = requests.get("http://127.0.0.1:8000/health", timeout=3)
    st.success("Connected to API backend") if r.ok else st.warning("API error")
except Exception:
    st.error("API offline")
