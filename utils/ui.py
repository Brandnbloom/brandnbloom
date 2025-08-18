import streamlit as st
import json
import pathlib

# Load branding.json
BRANDING_PATH = pathlib.Path("branding.json")
BRANDING = json.loads(BRANDING_PATH.read_text(encoding="utf-8")) if BRANDING_PATH.exists() else {}

def load_branding():
    return BRANDING or {}

def dark_mode_enabled():
    return st.session_state.get("dark_mode", False)

def theme_vars():
    b = load_branding()
    pal = b.get("palette", {})
    if dark_mode_enabled():
        return {
            "bg": pal.get("bg_dark", "#0B1020"),
            "text": pal.get("text_dark", "#E5E7EB"),
            "primary": pal.get("primary", "#8B5CF6"),
            "accent": pal.get("accent", "#22C55E"),
        }
    else:
        return {
            "bg": pal.get("bg_light", "#F6F5FB"),
            "text": pal.get("text_light", "#1F2937"),
            "primary": pal.get("primary", "#8B5CF6"),
            "accent": pal.get("accent", "#22C55E"),
        }

def inject_css():
    t = theme_vars()
    b = load_branding()
    fonts = b.get("fonts", {})
    heading_font = fonts.get("heading", "Playfair+Display")
    body_font = fonts.get("body", "Inter")

    st.markdown(f"""
    <link href="https://fonts.googleapis.com/css2?family={heading_font}&family={body_font}&display=swap" rel="stylesheet">
    <style>
    :root {{
      --bnb-bg: {t["bg"]};
      --bnb-text: {t["text"]};
      --bnb-primary: {t["primary"]};
      --bnb-accent: {t["accent"]};
    }}
    body {{
      font-family: '{body_font.replace('+', ' ')}', sans-serif;
    }}
    h1, h2, h3, h4, h5, h6 {{
      font-family: '{heading_font.replace('+', ' ')}', serif;
    }}
    .bnb-card {{
      background: var(--bnb-bg);
      color: var(--bnb-text);
      border-radius: 16px;
      padding: 1.0rem 1.2rem;
      border: 1px solid rgba(128,128,128,0.15);
    }}
    .bnb-badge {{
      display:inline-block; padding: 2px 10px; border-radius: 999px;
      background: var(--bnb-primary); color: white; font-size: 0.8rem;
    }}
    .bnb-cta {{
      background: var(--bnb-primary); color: white; padding: 10px 16px;
      border-radius: 12px; text-decoration: none; font-weight: 600;
      display:inline-block;
    }}
    .bnb-cta:hover {{ filter: brightness(1.05); }}
    </style>
    """, unsafe_allow_html=True)

def dark_mode_toggle():
    # Callback to re-inject CSS on toggle
    def _callback():
        inject_css()
    st.checkbox("🌗 Dark mode", key="dark_mode", on_change=_callback)

# --- Auto-inject CSS on app start ---
if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = False

inject_css()
