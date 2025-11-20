# brandnbloom/streamlit_app.py
"""
Brand N Bloom - Streamlit frontend + FastAPI backend runner

This file acts as the Streamlit UI entrypoint and starts a FastAPI backend
in a background thread. It injects SEO, analytics, and chat widgets, and
provides a clean sidebar to access tools including BloomScore Pro v2.
"""

import os
import threading
import logging
import pathlib
from typing import Optional

import requests
import streamlit as st
from dotenv import load_dotenv

# -----------------------
# Load environment & logging
# -----------------------
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("brandnbloom")

# -----------------------
# Streamlit page config
# -----------------------
st.set_page_config(
    page_title="Brand N Bloom — Dashboard",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------
# Aesthetic CSS (global)
# -----------------------
st.markdown(
    """
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background-color: #FFF9F5;
    }
    [data-testid="stSidebar"] {
        background-color: #F7F1EB !important;
        padding-top: 28px;
    }
    .aesthetic-card {
        background: rgba(255,255,255,0.6);
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
""",
    unsafe_allow_html=True,
)

# -----------------------
# Inject SEO / Analytics / Chat (components.seo.inject_all)
# -----------------------
# NOTE: Replace IDs with your real keys in production
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
    logger.warning("SEO injection failed or components.seo missing: %s", e)

# -----------------------
# Start FastAPI backend in background thread
# -----------------------
# Importing FastAPI/uvicorn lazily to avoid import overhead in Streamlit when not needed
def _start_api():
    try:
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        import uvicorn

        # Initialize DB (if present)
        try:
            from db import init_db
            init_db()
        except Exception:
            logger.debug("No db.init_db() available or failed to run init_db.")

        app = FastAPI(title="Brand N Bloom - API Suite")

        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Register routers if available - import inside function to avoid circular imports
        try:
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
        except Exception as e:
            logger.info("One or more routers failed to import; continuing without them: %s", e)

        @app.get("/health")
        async def health_check():
            return {"service": "brand-n-bloom", "status": "ok"}

        port = int(os.getenv("PORT", 8000))
        uvicorn.run(app, host="0.0.0.0", port=port, log_level="error")
    except Exception as exc:
        logger.exception("Failed to start API thread: %s", exc)


_api_thread = threading.Thread(target=_start_api, daemon=True)
_api_thread.start()

# -----------------------
# Import Streamlit UI modules (after starting backend)
# -----------------------
# Importing UI modules; keep these imports local so restarting Streamlit won't re-run backend init issues
try:
    from utils.ui import load_branding, inject_css, dark_mode_toggle
except Exception:
    # Fallbacks if utils.ui is not available
    def load_branding():
        return {"tagline": "Because brands deserve to bloom."}

    def inject_css():
        return None

    def dark_mode_toggle():
        return None

# Tool modules (best-effort imports; pages will handle missing modules)
try:
    from tools.website_builder import builder_ui
except Exception:
    builder_ui = None

try:
    from tools.seo import seo_audit, keyword_tracker
except Exception:
    seo_audit = keyword_tracker = None

try:
    from tools.ads import creative_generator
except Exception:
    creative_generator = None

try:
    from tools.social import calendar_ui
except Exception:
    calendar_ui = None

try:
    from tools.leads_crm import forms
except Exception:
    forms = None

try:
    from tools.analytics import dashboard
except Exception:
    dashboard = None

# -----------------------
# Header / Branding
# -----------------------
branding = load_branding()
inject_css()
dark_mode_toggle()

logo_path = pathlib.Path("assets/logo.png")

left_col, right_col = st.columns([1, 3])
with left_col:
    if logo_path.exists():
        st.image(str(logo_path), width=150)
with right_col:
    st.markdown("<h1 class='aesthetic-title'>Brand N Bloom</h1>", unsafe_allow_html=True)
    st.caption(branding.get("tagline", "Because brands deserve to bloom."))

st.divider()

# -----------------------
# Sidebar navigation
# -----------------------
st.sidebar.title("✨ Tools")
tools_list = [
    "BloomScore Pro v2",
    "Website Builder",
    "SEO Audit",
    "Keyword Tracker",
    "Ad Creative Generator",
    "Social Scheduler",
    "CRM / Leads",
    "Analytics Dashboard",
]
choice = st.sidebar.radio("Choose tool", tools_list)

# -----------------------
# BloomScore Pro v2 page
# -----------------------
if choice == "BloomScore Pro v2":
    # Late import to avoid heavy dependencies unless used
    try:
        from brandnbloom.bloomscore_pro_v2 import generate_full_report
    except Exception as e:
        st.error("BloomScore module not available. Please check installation.")
        logger.debug("bloomscore_pro_v2 import error: %s", e)
        generate_full_report = None

    st.markdown("<h2 class='aesthetic-title'>BloomScore Pro v2 — Aesthetic Brand Audit</h2>", unsafe_allow_html=True)
    st.write("Upload a screenshot or sample image and paste sample captions. We'll generate a BloomScore audit and an HTML+PDF report.")

    uploaded = st.file_uploader("Upload screenshot or sample image", type=["png", "jpg", "jpeg"])
    texts = st.text_area("Paste sample captions (one per line)", height=150)

    if uploaded and generate_full_report:
        with st.spinner("Generating BloomScore report…"):
            try:
                img_bytes = uploaded.read()
                sample_texts = [l.strip() for l in texts.splitlines() if l.strip()]
                profile = {"image_bytes": img_bytes, "sample_texts": sample_texts, "metrics": {}}

                report = generate_full_report(profile)

                # Render results
                st.markdown("### 🌸 BloomScore Report")
                st.metric("Final Score", report["payload"].get("score", "—"))
                st.markdown("#### Components")
                st.json(report["payload"].get("components", {}))

                st.markdown("### 🌷 HTML Preview")
                if report.get("html"):
                    st.components.v1.html(report["html"], height=650)
                if report.get("pdf_path"):
                    st.success(f"📄 PDF saved at: {report['pdf_path']}")
            except Exception as e:
                st.error("Failed to generate report. Check logs.")
                logger.exception("Error generating BloomScore report: %s", e)

# -----------------------
# Other tool pages
# -----------------------
elif choice == "Website Builder":
    if builder_ui:
        try:
            builder_ui.show_builder()
        except Exception as e:
            st.error("Website Builder currently unavailable.")
            logger.debug("builder_ui error: %s", e)
    else:
        st.info("Website Builder tool not installed.")

elif choice == "SEO Audit":
    if seo_audit:
        try:
            seo_audit.show_seo_audit()
        except Exception as e:
            st.error("SEO Audit currently unavailable.")
            logger.debug("seo_audit error: %s", e)
    else:
        st.info("SEO Audit tool not installed.")

elif choice == "Keyword Tracker":
    if keyword_tracker:
        try:
            keyword_tracker.show_keyword_tracker()
        except Exception as e:
            st.error("Keyword Tracker currently unavailable.")
            logger.debug("keyword_tracker error: %s", e)
    else:
        st.info("Keyword Tracker tool not installed.")

elif choice == "Ad Creative Generator":
    if creative_generator:
        try:
            creative_generator.show_creative_ui()
        except Exception as e:
            st.error("Ad Creative Generator currently unavailable.")
            logger.debug("creative_generator error: %s", e)
    else:
        st.info("Ad Creative Generator not installed.")

elif choice == "Social Scheduler":
    if calendar_ui:
        try:
            calendar_ui.show_calendar()
        except Exception as e:
            st.error("Social Scheduler currently unavailable.")
            logger.debug("calendar_ui error: %s", e)
    else:
        st.info("Social Scheduler tool not installed.")

elif choice == "CRM / Leads":
    if forms:
        try:
            forms.show_forms_ui()
        except Exception as e:
            st.error("CRM/Leads currently unavailable.")
            logger.debug("forms error: %s", e)
    else:
        st.info("CRM / Leads tool not installed.")

elif choice == "Analytics Dashboard":
    if dashboard:
        try:
            dashboard.show_dashboard()
        except Exception as e:
            st.error("Analytics Dashboard currently unavailable.")
            logger.debug("dashboard error: %s", e)
    else:
        st.info("Analytics Dashboard not installed.")

# -----------------------
# Footer / status
# -----------------------
st.divider()
BASE_URL = f"http://localhost:{int(os.getenv('PORT',8000))}"

try:
    r = requests.get(f"{BASE_URL}/health", timeout=4)
    if r.ok:
        st.success("Connected to API backend!")
    else:
        st.warning("API reachable but returned an error.")
except Exception as e:
    st.error(f"API offline: {e}")
