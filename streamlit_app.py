import streamlit as st, pathlib, json
from utils.ui import load_branding, inject_css, dark_mode_toggle

st.set_page_config(page_title="Brand N Bloom", page_icon="🌸", layout="wide")
b = load_branding()
inject_css()
dark_mode_toggle()

logo_path = pathlib.Path("assets/logo.png")
col1, col2 = st.columns([1,2])
with col1:
    if logo_path.exists():
        st.image(str(logo_path), width=180)
with col2:
    st.title("Brand N Bloom")
    st.caption(b.get("tagline","Because brands deserve to bloom."))

st.page_link("pages/05_📊_Dashboard.py", label="Go to Dashboard", icon="📊")
st.divider()
st.write("Use the left sidebar to navigate all features.")
