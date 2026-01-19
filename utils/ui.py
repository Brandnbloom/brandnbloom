# utils/ui.py

import streamlit as st
import json
import pathlib
import time

# ---------------------------------------------------------------------
# Branding & Config
# ---------------------------------------------------------------------

BRANDING_PATH = pathlib.Path("branding.json")
BRANDING_CACHE = {"timestamp": 0, "data": {}}
BRANDING_CACHE_TTL = 5  # seconds


def load_branding(force_reload=False):
    """
    Loads branding.json with caching.
    """
    global BRANDING_CACHE

    now = time.time()
    cache_expired = now - BRANDING_CACHE["timestamp"] > BRANDING_CACHE_TTL

    if force_reload or cache_expired:
        if BRANDING_PATH.exists():
            try:
                BRANDING_CACHE["data"] = json.loads(
                    BRANDING_PATH.read_text(encoding="utf-8")
                )
            except Exception:
                BRANDING_CACHE["data"] = {}
        else:
            BRANDING_CACHE["data"] = {}

        BRANDING_CACHE["timestamp"] = now

    return BRANDING_CACHE["data"]


# ---------------------------------------------------------------------
# Theme Handling
# ---------------------------------------------------------------------

def dark_mode_enabled():
    return st.session_state.get("dark_mode", False)


def theme_vars():
    light = {
        "bg": "#F6F5FB",
        "text": "#1F2937",
        "primary": "#8B5CF6",
        "accent": "#22C55E",
    }

    dark = {
        "bg": "#0B1020",
        "text": "#E5E7EB",
        "primary": "#8B5CF6",
        "accent": "#22C55E",
    }

    return dark if dark_mode_enabled() else light


# ---------------------------------------------------------------------
# CSS Injection
# ---------------------------------------------------------------------

def inject_css():
    t = theme_vars()

    st.markdown(
        f"""
        <style>
        :root {{
            --bnb-bg: {t["bg"]};
            --bnb-text: {t["text"]};
            --bnb-primary: {t["primary"]};
            --bnb-accent: {t["accent"]};
        }}

        body {{
            background-color: var(--bnb-bg) !important;
            color: var(--bnb-text) !important;
        }}

        .bnb-card {{
            background: var(--bnb-bg);
            color: var(--bnb-text);
            border-radius: 16px;
            padding: 1rem 1.2rem;
            border: 1px solid rgba(128,128,128,0.15);
            margin-bottom: 1rem;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------
# UI Components
# ---------------------------------------------------------------------

def card(content: str):
    st.markdown(f"<div class='bnb-card'>{content}</div>", unsafe_allow_html=True)


# ---------------------------------------------------------------------
# Dark Mode Toggle
# ---------------------------------------------------------------------

def dark_mode_toggle():
    st.checkbox("🌗 Dark mode", key="dark_mode", on_change=inject_css)


# ---------------------------------------------------------------------
# Initialize
# ---------------------------------------------------------------------

if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = False

inject_css()
