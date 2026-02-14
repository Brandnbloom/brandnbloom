import streamlit as st, json
from utils.ui import load_branding, inject_css, dark_mode_toggle

b = load_branding()
inject_css()

st.title("🏠 Home")
dark_mode_toggle()

st.markdown(f"### {b.get('tagline','Your AI co-pilot for brand growth')}")
st.write("Welcome to **Brand N Bloom** — your all-in-one AI marketing co-pilot for SMBs, startups, and creators.")
st.markdown('<span class="bnb-badge">New</span> Visual Audit, Templates Library, and Automations are ready to explore!',
            unsafe_allow_html=True)
st.write("Use the left sidebar to navigate.")
