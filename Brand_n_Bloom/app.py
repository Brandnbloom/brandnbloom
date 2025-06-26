import streamlit as st

st.set_page_config(page_title="Brand n Bloom", layout="wide")

st.title("🌸 Brand n Bloom")
st.markdown("Welcome to **Brand n Bloom** — where brands blossom beyond borders.")

st.header("✨ Try Our AI Tools")
st.page_link("pages/review_reply_assistant.py", label="📝 Review Reply Assistant")
st.page_link("pages/visual_brand_audit.py", label="🎨 Visual Brand Audit")

st.info("More tools coming soon: BloomScore, Menu Creator, and more 🚀")
