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

# -----------------------
# SEO / Analytics / Chat injection
# -----------------------
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
def _start_api():
    try:
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        import uvicorn

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
# Import Streamlit UI modules (safe fallbacks)
# -----------------------
try:
    from utils.ui import load_branding, inject_css, dark_mode_toggle
except Exception:
    def load_branding():
        return {"tagline": "Because brands deserve to bloom."}
    def inject_css(): return None
    def dark_mode_toggle(): return None

# -----------------------
# Dynamic tool imports
# -----------------------
tools_modules = {}
for tool_name, import_path in [
    ("Website Builder", "tools.website_builder.builder_ui"),
    ("SEO Audit", "tools.seo.seo_audit"),
    ("Keyword Tracker", "tools.seo.keyword_tracker"),
    ("Ad Creative Generator", "tools.ads.creative_generator"),
    ("Social Scheduler", "tools.social.calendar_ui"),
    ("CRM / Leads", "tools.leads_crm.forms"),
    ("Analytics Dashboard", "tools.analytics.dashboard"),
]:
    try:
        module = __import__(import_path, fromlist=[""])
        tools_modules[tool_name] = module
    except Exception as e:
        logger.info(f"Tool '{tool_name}' not available: {e}")
        tools_modules[tool_name] = None

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
    try:
        from brandnbloom.bloomscore_pro_v2 import generate_full_report
    except Exception as e:
        st.error("BloomScore module not available. Please check installation.")
        logger.debug("bloomscore_pro_v2 import error: %s", e)
        generate_full_report = None

    st.markdown("<h2 class='aesthetic-title'>BloomScore Pro v2 — Aesthetic Brand Audit</h2>", unsafe_allow_html=True)
    st.write("Upload screenshot/sample image and paste captions. We'll generate BloomScore HTML+PDF report.")

    uploaded = st.file_uploader("Upload screenshot or image", type=["png","jpg","jpeg"])
    texts = st.text_area("Paste captions (one per line)", height=150)

    if uploaded and generate_full_report:
        with st.spinner("Generating BloomScore report…"):
            try:
                img_bytes = uploaded.read()
                sample_texts = [l.strip() for l in texts.splitlines() if l.strip()]
                profile = {"image_bytes": img_bytes, "sample_texts": sample_texts, "metrics": {}}

                report = generate_full_report(profile)

                st.markdown("### 🌸 BloomScore Report")
                st.metric("Final Score", report["payload"].get("score", "—"))
                st.markdown("#### Components")
                st.json(report["payload"].get("components", {}))

                st.markdown("### 🌷 HTML Preview")
                if report.get("html"):
                    st.components.v1.html(report["html"], height=650)

                pdf_path = report.get("pdf_path")
                if pdf_path and os.path.exists(pdf_path):
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            label="📄 Download PDF Report",
                            data=f,
                            file_name="BloomScore_Report.pdf",
                            mime="application/pdf"
                        )
            except Exception as e:
                st.error("Failed to generate report. Check logs.")
                logger.exception("Error generating BloomScore report: %s", e)

# -----------------------
# Other tool pages dynamically
# -----------------------
else:
    tool_module = tools_modules.get(choice)
    if tool_module:
        try:
            if hasattr(tool_module, "show_builder"): tool_module.show_builder()
            elif hasattr(tool_module, "show_seo_audit"): tool_module.show_seo_audit()
            elif hasattr(tool_module, "show_keyword_tracker"): tool_module.show_keyword_tracker()
            elif hasattr(tool_module, "show_creative_ui"): tool_module.show_creative_ui()
            elif hasattr(tool_module, "show_calendar"): tool_module.show_calendar()
            elif hasattr(tool_module, "show_forms_ui"): tool_module.show_forms_ui()
            elif hasattr(tool_module, "show_dashboard"): tool_module.show_dashboard()
        except Exception as e:
            st.error(f"{choice} currently unavailable.")
            logger.debug(f"{choice} error: {e}")
    else:
        st.info(f"{choice} tool not installed.")

# -----------------------
# Footer / API status
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
