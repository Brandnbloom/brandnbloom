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
# Aesthetic CSS
# =============================================================
st.markdown("""
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

        # DB optional
        try:
            from db import init_db
            init_db()
        except Exception:
            logger.debug("init_db missing or failed.")

        app = FastAPI(title="Brand N Bloom - API Suite")
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Router imports
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

            app.include_router(seo_router, prefix="/api/seo")
            app.include_router(keyword_router, prefix="/api/keywords")
            app.include_router(content_router, prefix="/api/content")
            app.include_router(social_router, prefix="/api/social")
            app.include_router(ads_router, prefix="/api/ads")
            app.include_router(crm_router, prefix="/api/crm")
            app.include_router(analytics_router, prefix="/api/analytics")
            app.include_router(reputation_router, prefix="/api/reputation")
            app.include_router(advanced_router, prefix="/api/advanced")
            app.include_router(internal_router, prefix="/api/internal")

        except Exception as e:
            logger.info("Router import error: %s", e)

        @app.get("/health")
        async def health_check():
            return {"service": "brand-n-bloom", "status": "ok"}

        uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)), log_level="error")

    except Exception as exc:
        logger.exception("API failed: %s", exc)


threading.Thread(target=_start_api, daemon=True).start()

# =============================================================
# UI helpers (fallback safe)
# =============================================================
try:
    from utils.ui import load_branding, inject_css, dark_mode_toggle
except Exception:
    def load_branding(): return {"tagline": "Because brands deserve to bloom."}
    def inject_css(): pass
    def dark_mode_toggle(): pass

# =============================================================
# Dynamic tool imports
# =============================================================
tools_modules = {}
for name, path in [
    ("Website Builder", "tools.website_builder.builder_ui"),
    ("SEO Audit", "tools.seo.seo_audit"),
    ("Keyword Tracker", "tools.seo.keyword_tracker"),
    ("Ad Creative Generator", "tools.ads.creative_generator"),
    ("Social Scheduler", "tools.social.calendar_ui"),
    ("CRM / Leads", "tools.leads_crm.forms"),
    ("Analytics Dashboard", "tools.analytics.dashboard"),
]:
    try:
        tools_modules[name] = __import__(path, fromlist=[""])
    except Exception as e:
        logger.info(f"Tool {name} unavailable: {e}")
        tools_modules[name] = None

# =============================================================
# Header / Branding
# =============================================================
branding = load_branding()
inject_css()
dark_mode_toggle()

logo = pathlib.Path("assets/logo.png")
c1, c2 = st.columns([1, 3])

with c1:
    if logo.exists():
        st.image(str(logo), width=150)

with c2:
    st.markdown("<h1 class='aesthetic-title'>Brand N Bloom</h1>", unsafe_allow_html=True)
    st.caption(branding["tagline"])

st.divider()

# =============================================================
# Sidebar navigation
# =============================================================
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

# =============================================================
# Path Injection Safe Directory
# =============================================================
SAFE_REPORT_DIR = pathlib.Path("reports").resolve()
SAFE_REPORT_DIR.mkdir(exist_ok=True)

def is_safe_report_path(path: str) -> bool:
    """Ensure the PDF path stays inside the reports/ folder."""
    try:
        resolved = pathlib.Path(path).resolve()
        return SAFE_REPORT_DIR in resolved.parents
    except Exception:
        return False

# =============================================================
# BloomScore Pro v2 Page
# =============================================================
if choice == "BloomScore Pro v2":

    try:
        from brandnbloom.bloomscore_pro_v2 import generate_full_report
    except Exception as e:
        st.error("BloomScore module missing.")
        logger.error(e)
        generate_full_report = None

    st.markdown("<h2 class='aesthetic-title'>BloomScore Pro v2 — Aesthetic Brand Audit</h2>", unsafe_allow_html=True)

    uploaded = st.file_uploader("Upload image", ["png", "jpg", "jpeg"])
    texts = st.text_area("Paste captions (one per line)", height=150)

    if uploaded and generate_full_report:
        with st.spinner("Generating report…"):
            try:
                img_bytes = uploaded.read()
                caption_list = [l.strip() for l in texts.splitlines() if l.strip()]

                profile = {
                    "image_bytes": img_bytes,
                    "sample_texts": caption_list,
                    "metrics": {}
                }

                report = generate_full_report(profile)

                st.metric("Final Score", report["payload"].get("score", "—"))
                st.json(report["payload"].get("components", {}))

                # HTML
                if report.get("html"):
                    st.components.v1.html(report["html"], height=650)

                # Safe PDF download
               pdf_path = report.get("pdf_path")

if pdf_path:
    # Extract only filename (prevents traversal)
    filename = os.path.basename(pdf_path)

    # Rebuild absolute safe path
    safe_path = SAFE_REPORT_DIR / filename

    # Extra safety: ensure final path is inside reports/
    if safe_path.exists() and is_safe_report_path(str(safe_path)):
        with safe_path.open("rb") as f:
            st.download_button(
                label="📄 Download PDF Report",
                data=f.read(),
                file_name=filename,
                mime="application/pdf"
            )


            except Exception as e:
                st.error("Report generation failed.")
                logger.exception(e)

# =============================================================
# Other tools
# =============================================================
else:
    module = tools_modules.get(choice)
    if module:
        try:
            for method in [
                "show_builder",
                "show_seo_audit",
                "show_keyword_tracker",
                "show_creative_ui",
                "show_calendar",
                "show_forms_ui",
                "show_dashboard"
            ]:
                if hasattr(module, method):
                    getattr(module, method)()
        except Exception as e:
            st.error(f"{choice} failed.")
            logger.error(e)
    else:
        st.info(f"{choice} not installed.")

# =============================================================
# Footer / Safe API Health Check (No SSRF)
# =============================================================
st.divider()

BASE_URL = "http://127.0.0.1:" + str(int(os.getenv("PORT", 8000)))

try:
    # SAFE: Only allow localhost, not user-controlled input
    r = requests.get(f"{BASE_URL}/health", timeout=3)
    if r.ok:
        st.success("Connected to API backend")
    else:
        st.warning("API reachable but returned error.")
except Exception:
    st.error("API offline")
