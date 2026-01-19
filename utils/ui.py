import streamlit as st import json import pathlib import time
BRANDING_PATH = pathlib.Path("branding.json") BRANDING_CACHE = {"timestamp": 0, "data": {}} BRANDING_CACHE_TTL = 5
def load_branding(force_reload=False): global BRANDING_CACHE now = time.time() expired = now - BRANDING_CACHE["timestamp"] > BRANDING_CACHE_TTL
if force_reload or expired:
    if BRANDING_PATH.exists():
        try:
            BRANDING_CACHE["data"] = json.loads(BRANDING_PATH.read_text())
        except Exception:
            BRANDING_CACHE["data"] = {}
    else:
        BRANDING_CACHE["data"] = {}
    BRANDING_CACHE["timestamp"] = now

return BRANDING_CACHE["data"]

def dark_mode_enabled(): return st.session_state.get("dark_mode", False)
def theme_vars(): b = load_branding() pal = b.get("palette", {})
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

def inject_css(): t = theme_vars()
st.markdown(f"""
<style>
:root {{
  --bnb-bg: {t['bg']};
  --bnb-text: {t['text']};
  --bnb-primary: {t['primary']};
  --bnb-accent: {t['accent']};
}}

body {{
  background: var(--bnb-bg);
  color: var(--bnb-text);
}}

h1, h2, h3, h4, h5, h6 {{
  color: var(--bnb-text);
}}

.bnb-card {{
  background: rgba(255,255,255,0.03);
  border-radius: 16px;
  padding: 1rem 1.2rem;
  border: 1px solid rgba(255,255,255,0.08);
  margin-bottom: 1rem;
}}
</style>
""", unsafe_allow_html=True)

def card(content: str): st.markdown(f"
{content}
", unsafe_allow_html=True)
def dark_mode_toggle(): st.checkbox("🌗 Dark mode", key="dark_mode")

