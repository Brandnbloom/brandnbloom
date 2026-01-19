# streamlit_app.py
import streamlit as st
from utils.ui import inject_css, dark_mode_toggle, card

# ---------------------------------------------------------
# Page Config
# ---------------------------------------------------------
st.set_page_config(
    page_title="Brand n Bloom",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------
# Inject Theme + Dark Mode
# ---------------------------------------------------------
inject_css()

# ---------------------------------------------------------
# App State
# ---------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"

# ---------------------------------------------------------
# Top Navigation Bar
# ---------------------------------------------------------
with st.container():
    nav_cols = st.columns([2, 1, 1, 1, 1, 1, 1, 1])

    with nav_cols[0]:
        st.markdown("### 🌸 Brand n Bloom")

    with nav_cols[1]:
        if st.button("Home"):
            st.session_state.page = "Home"

    with nav_cols[2]:
        if st.button("Features"):
            st.session_state.page = "Features"

    with nav_cols[3]:
        if st.button("Pricing"):
            st.session_state.page = "Pricing"

    with nav_cols[4]:
        if st.button("Blog"):
            st.session_state.page = "Blog"

    with nav_cols[5]:
        if st.button("Tools"):
            st.session_state.page = "Tools"

    with nav_cols[6]:
        if st.button("Dashboard"):
            st.session_state.page = "Dashboard"

    with nav_cols[7]:
        dark_mode_toggle()

st.markdown("---")

# ---------------------------------------------------------
# MAX WIDTH CONTAINER
# ---------------------------------------------------------
def page_container():
    return st.container()

# ---------------------------------------------------------
# HOME
# ---------------------------------------------------------
if st.session_state.page == "Home":
    with page_container():
        st.image("assets/banner.png", use_container_width=True)

        st.markdown(
            """
            ## AI-powered growth tools for modern brands  
            **Clarity. Strategy. Scale.**  
            Turn data into marketing decisions that actually work.
            """
        )

        st.markdown("### What you can do with Brand n Bloom")

        cols = st.columns(3)
        with cols[0]:
            card("🔬 **BloomScore**<br/>Instant brand health score")
        with cols[1]:
            card("🧠 **Consumer Behavior**<br/>Understand how customers think & buy")
        with cols[2]:
            card("📧 **Email Marketing**<br/>High-conversion AI campaigns")

# ---------------------------------------------------------
# FEATURES
# ---------------------------------------------------------
elif st.session_state.page == "Features":
    with page_container():
        st.markdown("## ✨ Features")

        FEATURES = [
            "AI-driven marketing intelligence",
            "Data-backed decision making",
            "Plug-and-play growth tools",
            "Designed for founders & marketers",
        ]

        for f in FEATURES:
            card(f"✅ {f}")

# ---------------------------------------------------------
# PRICING
# ---------------------------------------------------------
elif st.session_state.page == "Pricing":
    with page_container():
        st.markdown("## 💰 Pricing")

        cols = st.columns(2)

        with cols[0]:
            card("### Starter<br/>₹0 / month<br/>Basic insights")

        with cols[1]:
            card("### Pro<br/>₹1999 / month<br/>Full access")
            st.link_button("Pay with PayPal", "https://www.paypal.com")

# ---------------------------------------------------------
# BLOG
# ---------------------------------------------------------
elif st.session_state.page == "Blog":
    with page_container():
        st.markdown("## 📰 Blog")
        card("Coming soon: marketing, analytics & growth insights.")

# ---------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------
elif st.session_state.page == "Dashboard":
    with page_container():
        st.markdown("## 📊 Dashboard")
        card("Connect tools to start seeing insights here.")

# ---------------------------------------------------------
# TOOLS
# ---------------------------------------------------------
elif st.session_state.page == "Tools":
    with page_container():
        st.markdown("## 🧰 Marketing & Analytics Tools")

        TOOLS = {
            "BloomScore": "Instant brand health score for social profiles",
            "Consumer Behavior": "Understand how customers think, feel & buy",
            "Email Marketing": "AI-written high-conversion email campaigns",
            "Influencer Finder": "Find creators aligned with your brand",
            "Business Compare": "Benchmark your brand against competitors",
            "Menu Pricing": "Optimize prices using demand psychology",
            "Loyalty": "Design loyalty programs that retain customers",
        }

        cols = st.columns(3)
        for i, (tool, desc) in enumerate(TOOLS.items()):
            with cols[i % 3]:
                card(f"### {tool}<br/>{desc}")

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown("---")
st.markdown(
    """
    <div style="text-align:center; opacity:0.7;">
    © 2026 Brand n Bloom • Built with ❤️
    </div>
    """,
    unsafe_allow_html=True,
)
