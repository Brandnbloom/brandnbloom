import streamlit as st, json, pathlib
from utils.ui import inject_css, dark_mode_toggle, load_branding

inject_css(); st.title("⚙️ Settings"); dark_mode_toggle()

st.subheader("Profile")
st.text_input("Business name")
st.text_input("Website")
st.text_input("Primary email")

st.subheader("Branding")
b = load_branding()
st.write("Tagline:", b.get("tagline"))
st.color_picker("Primary color", b.get("palette",{}).get("primary","#8B5CF6"))
st.color_picker("Accent color", b.get("palette",{}).get("accent","#22C55E"))
st.info("For now, edit branding.json directly to persist changes.")
