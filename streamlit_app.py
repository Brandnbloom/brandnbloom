# streamlit_app.py
import streamlit as st

from utils.ui import (
    inject_css,
    dark_mode_toggle,
    card,
)

# -------------------------------------------------
# Page config (MUST be first Streamlit command)
# -------------------------------------------------
st.set_page_config(
    page_title="Brand n Bloom",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -------------------------------------------------
# Global UI setup
# -------------------------------------------------
inject_css()
dark_mode_toggle()

# -------------------------------------------------
# Header / Banner
# -------------------------------------------------
st.markdown(
    """
    <div style="text-align:center; padding: 1.5rem 0;">
        <h1>🌸 Brand n Bloom</h1>
        <p style="font-size:1.1rem; opacity:0.8;">
            AI-powered growth & marketing intelligence for modern brands
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

# -------------------------------------------------
# Top Navigation (NO sidebar)
# -------------------------------------------------
tabs = st.tabs([
    "🏠 Home",
    "🧰 Tools",
    "📊 Dashboard",
    "📰 Blog",
    "💰 Pricing",
    "📨 Contact",
    "ℹ️ About",
])

# -------------------------------------------------
# HOME
# -------------------------------------------------
with tabs[0]:
    st.markdown("## Grow smarter. Scale faster. 🌱")

    cols = st.columns(3)
    with cols[0]:
        card("🔬 **Data-backed insights** for confident decisions")
    with cols[1]:
        card("📈 **Marketing analytics** that actually make sense")
    with cols[2]:
        card("🤖 **AI tools** built for founders & marketers")

    st.markdown(
        """
        Brand n Bloom helps you understand **what to do next**,  
        not just what happened.
        """
    )

# -------------------------------------------------
# TOOLS
# -------------------------------------------------
with tabs[1]:
    st.markdown("## 🧰 Our Tools")

    TOOLS = {
        "BloomScore": "Instant brand health score for social profiles",
        "Consumer Behavior": "Understand how customers think, feel & buy",
        "Email Marketing": "AI-written high-conversion email campaigns",
        "Influencer Finder": "Find creators aligned with your brand",
        "Business Compare": "Benchmark your brand against competitors",
        "Menu Pricing": "Optimize menu prices using demand psychology",
        "Loyalty": "Design loyalty programs that actually retain customers",
    }

    cols = st.columns(3)
    for i, (tool, desc) in enumerate(TOOLS.items()):
        with cols[i % 3]:
            card(f"### {tool}\n\n{desc}")

    st.info("🔧 Tool logic will be connected one by one.")

# -------------------------------------------------
# DASHBOARD
# -------------------------------------------------
with tabs[2]:
    st.markdown("## 📊 Dashboard")
    st.warning("No data yet. Connect tools to activate analytics.")

# -------------------------------------------------
# BLOG
# -------------------------------------------------
with tabs[3]:
    st.markdown("## 📰 Blog")
    st.info("Blog system coming soon (Markdown / CMS based).")

# -------------------------------------------------
# PRICING
# -------------------------------------------------
with tabs[4]:
    st.markdown("## 💰 Pricing")

    c1, c2 = st.columns(2)
    with c1:
        card("### Starter\n\n₹0 / month\n\nBasic access")
    with c2:
        card("### Pro\n\n₹1999 / month\n\nFull tool access")

        st.markdown(
            "[Pay with PayPal](https://www.paypal.com)",
            unsafe_allow_html=True,
        )

# -------------------------------------------------
# CONTACT
# -------------------------------------------------
with tabs[5]:
    st.markdown("## 📨 Contact")
    st.text_input("Your email")
    st.text_area("Message")
    st.button("Send")

# -------------------------------------------------
# ABOUT
# -------------------------------------------------
with tabs[6]:
    st.markdown("## ℹ️ About Brand n Bloom")
    st.markdown(
        """
        Brand n Bloom is a **marketing + data science platform**  
        built to help brands grow with clarity, not guesswork.
        """
    )

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.divider()
st.markdown(
    "<center>© 2026 Brand n Bloom • Built with ❤️</center>",
    unsafe_allow_html=True,
)
