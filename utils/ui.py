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
    Prevents re-reading file on every rerun.
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
    """Returns True if dark mode toggle is ON."""
    return st.session_state.get("dark_mode", False)


def theme_vars():
    """Returns color variables for selected theme."""
    b = load_branding()
    pal = b.get("palette", {})

    light = {
        "bg": pal.get("bg_light", "#F6F5FB"),
        "text": pal.get("text_light", "#1F2937"),
        "primary": pal.get("primary", "#8B5CF6"),
        "accent": pal.get("accent", "#22C55E"),
    }

    dark = {
        "bg": pal.get("bg_dark", "#0B1020"),
        "text": pal.get("text_dark", "#E5E7EB"),
        "primary": pal.get("primary", "#8B5CF6"),
        "accent": pal.get("accent", "#22C55E"),
    }

    return dark if dark_mode_enabled() else light


# ---------------------------------------------------------------------
# CSS Injection
# ---------------------------------------------------------------------

def inject_css():
    t = theme_vars()
    b = load_branding()
    fonts = b.get("fonts", {})

    heading_font = fonts.get("heading", "Playfair+Display")
    body_font = fonts.get("body", "Inter")

    favicon = b.get("favicon")
    logo = b.get("logo")

    st.markdown(f"""
    <link href="https://fonts.googleapis.com/css2?family={heading_font}&family={body_font}&display=swap" rel="stylesheet">

    {f'<link rel="icon" href="{favicon}">' if favicon else ""}

    <style>
    :root {{
      --bnb-bg: {t["bg"]};
      --bnb-text: {t["text"]};
      --bnb-primary: {t["primary"]};
      --bnb-accent: {t["accent"]};
    }}

    body {{
      font-family: '{body_font.replace('+', ' ')}', sans-serif;
      background: var(--bnb-bg) !important;
      color: var(--bnb-text) !important;
    }}

    h1, h2, h3, h4, h5, h6 {{
      font-family: '{heading_font.replace('+', ' ')}', serif;
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

    .bnb-badge {{
      display:inline-block;
      padding: 3px 10px;
      border-radius: 999px;
      background: var(--bnb-primary);
      color: #fff;
      font-size: 0.75rem;
      font-weight: 600;
    }}

    .bnb-cta {{
      background: var(--bnb-primary);
      color: white;
      padding: 10px 16px;
      border-radius: 12px;
      text-decoration: none;
      font-weight: 600;
      display:inline-block;
      transition: 0.2s;
    }}

    .bnb-cta:hover {{
      filter: brightness(1.08);
    }}

    .bnb-shadow {{
      box-shadow: 0px 4px 14px rgba(0,0,0,0.12);
    }}
    </style>
    """, unsafe_allow_html=True)

    if logo:
        st.session_state["bnb_logo"] = logo


# ---------------------------------------------------------------------
# UI Components
# ---------------------------------------------------------------------

def card(content: str):
    """Reusable styled card"""
    st.markdown(f"<div class='bnb-card'>{content}</div>", unsafe_allow_html=True)


def badge(text: str):
    st.markdown(f"<span class='bnb-badge'>{text}</span>", unsafe_allow_html=True)


def cta(label: str, link: str):
    st.markdown(
        f"<a class='bnb-cta bnb-shadow' href='{link}' target='_blank'>{label}</a>",
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------
# Dark Mode Toggle
# ---------------------------------------------------------------------

def dark_mode_toggle():
    def _callback():
        inject_css()

    st.checkbox("🌗 Dark mode", key="dark_mode", on_change=_callback)


# ---------------------------------------------------------------------
# Initialize CSS on App Load
# ---------------------------------------------------------------------

if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = False

inject_css()
