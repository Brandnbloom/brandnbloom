import streamlit as st

st.set_page_config(page_title="Brand n Bloom", layout="wide")

st.title("🌸 Brand n Bloom")
st.markdown("Welcome to **Brand n Bloom** — where brands blossom beyond borders.")

st.header("✨ Try Our AI Tools")
st.page_link("pages/review_reply_assistant.py", label="📝 Review Reply Assistant")
st.page_link("pages/visual_brand_audit.py", label="🎨 Visual Brand Audit")
# Main homepage
import streamlit as st

st.set_page_config(page_title="Brand n Bloom", layout="wide")

st.title("🌸 Brand n Bloom")
st.markdown("Welcome to **Brand n Bloom** — where brands blossom beyond borders.")

st.image("https://images.unsplash.com/photo-1556740749-887f6717d7e4", use_column_width=True)

st.header("✨ Try Our AI Tools")
st.page_link("pages/review_reply_assistant.py", label="📝 Review Reply Assistant", icon="💬")
st.page_link("pages/visual_brand_audit.py", label="🎨 Visual Brand Audit", icon="🎨")

st.info("More tools coming soon: BloomScore, Competitor Snapshots, and more 🚀")
