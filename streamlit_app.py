# brandnbloom/streamlit_app.py

"""
Brand N Bloom - Streamlit frontend + FastAPI backend runner
Includes: SEO, analytics, chat widgets, BloomScore Pro v2, and other tools.
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
# Theme injector (LIGHT / DARK)
# =============================================================
def inject_theme():
    if st.session_state.dark_mode:
        st.markdown("""
        <style>
        html, body, [class*="css"] {
            background-color: #0F1117 !important;
            color: #FAFAFA !important;
            font-family: 'Poppins', sans-serif;
        }
        [data-testid="stSidebar"] {
            background-color: #161B22 !important;
        }
        .aesthetic-card {
            background: rgba(22,27,34,0.9);
            color: #FAFAFA;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        html, body, [class*="css"] {
            background-color: #FFF9F5;
            color: #2C2C2C;
            font-family: 'Poppins', sans-serif;
        }
        [data-testid="stSidebar"] {
            background-color: #F7F1EB !important;
        }
        </style>
        """, unsafe_allow_html=True)

inject_theme()

# =============================================================
# Base Aesthetic CSS
# =============================================================
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
.aesthetic-card {
    padding: 22px;
    border-radius: 14px;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.06);
    backdrop-filter: blur(6px);
}
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
# SEO / Analytics injection (safe)
# =============================================================
try:
    from components.seo import inject_all
    inject_all(
        title="Brand N Bloom — AI Brand Intelligence",
        description="AI-powered audits, BloomScore analytics, social tools and creative assistance for creators & SMBs.",
        url=os.getenv("SITE_URL", "https://www.brandnbloom.com"),
        image_url=os.getenv("SITE_IMAGE", "https://www.brandnbloom.com/assets/banner.png"),
        keywords="branding audit, instagram analytics, ai marketing, bloomscore, seo, restaurant marketing",
        favicon_url=os.getenv("FAVICON_URL", "https://www.brandnbloom.com/assets/favicon.png"),
        google_analytics_id=os.getenv("GA_ID", "G-ABCD1234"),
        facebook_pixel_id=os.getenv("FB_PIXEL_ID", "123456789012345"),
        intercom_app_id=os.getenv("INTERCOM_APP_ID", "abc123"),
        enable_intercom=True,
        enable_tawk=False,
    )
except Exception as e:
    logger.warning("SEO injection failed: %s", e)

# =============================================================
# Start FastAPI backend (thread)
# =============================================================
def _start_api():
    try:
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        import uvicorn

        app = FastAPI(title="Brand N Bloom - API Suite")
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )

        @app.get("/health")
        async def health_check():
            return {"service": "brand-n-bloom", "status": "ok"}

        uvicorn.run(
            app,
            host="0.0.0.0",
            port=int(os.getenv("PORT", 8000)),
            log_level="error"
        )

    except Exception as exc:
        logger.exception("API failed: %s", exc)

threading.Thread(target=_start_api, daemon=True).start()

# =============================================================
# Sidebar
# =============================================================
st.sidebar.title("✨ Tools")

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
# Header
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
                                filename,
                                mime="application/pdf"
                            )

            except Exception as e:
                st.error("Report generation failed.")
                logger.exception(e)

# =============================================================
# Footer API health
# =============================================================
st.divider()
try:
    r = requests.get("http://127.0.0.1:8000/health", timeout=3)
    st.success("Connected to API backend") if r.ok else st.warning("API error")
except Exception:
    st.error("API offline")
