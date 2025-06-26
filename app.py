import streamlit as st

st.set_page_config(page_title="Brand n Bloom", layout="wide")

# 👋 Welcome Section
st.title("🌸 Brand n Bloom")
st.markdown(
    "Welcome to **Brand n Bloom** — where brands blossom beyond borders."
)

st.markdown("---")

# 🛠️ Tools Section
st.header("✨ Try Our AI Tools")
st.markdown(
    "- 📝 [Review Reply Assistant](pages/review_reply_assistant.py)\n"
    "- 🎨 [Visual Brand Audit](pages/visual_brand_audit.py)\n"
    "- 📊 (More tools coming soon!)"
)

st.markdown("---")

# 📌 Info Section
st.info("Your website and AI tools loading correctly for public use.")
