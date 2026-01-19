import streamlit as st from utils.ui import inject_css, dark_mode_toggle, card
st.set_page_config( page_title="Brand n Bloom", layout="wide", initial_sidebar_state="collapsed" )
st.markdown("""
""", unsafe_allow_html=True)
inject_css()
dark_mode_toggle()

st.markdown("""
🌸 Brand n Bloom
AI-powered growth tools for modern brands
""", unsafe_allow_html=True)

TOOLS = { "BloomScore": "Instant brand health score for social profiles", "Consumer Behavior": "Understand how customers think, feel & buy", "Email Marketing": "AI-written high-conversion email campaigns", "Influencer Finder": "Find creators aligned with your brand", "Business Compare": "Benchmark your brand against competitors", "Menu Pricing": "Optimize menu prices using demand psychology", "Loyalty": "Design loyalty programs that actually retain customers", }

st.markdown("## 🧰 Tools")
cols = st.columns(3) for i, (tool, desc) in enumerate(TOOLS.items()): with cols[i % 3]: card(f"
{tool}
{desc}
")

st.markdown("""

© 2026 Brand n Bloom • Built with ❤️
""", unsafe_allow_html=True)


