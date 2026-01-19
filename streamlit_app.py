# brandnbloom/streamlit_app.py

import streamlit as st
import pathlib

# =============================================================
# PAGE CONFIG
# =============================================================
st.set_page_config(
    page_title="Brand N Bloom",
    page_icon="🌸",
    layout="wide",
)

# =============================================================
# GLOBAL THEME-SAFE CSS
# =============================================================
st.markdown("""
<style>
.container {
    max-width: 1200px;
    margin: auto;
}

.hero-title {
    font-size: 44px;
    font-weight: 700;
}

.hero-subtitle {
    font-size: 18px;
    opacity: 0.85;
}

.card {
    background: var(--secondary-background-color);
    padding: 22px;
    border-radius: 16px;
    margin-bottom: 20px;
}

.tool-card {
    border: 1px solid rgba(255,255,255,0.08);
    padding: 18px;
    border-radius: 14px;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

# =============================================================
# TOP NAVIGATION
# =============================================================
menu = st.tabs([
    "🏠 Home",
    "🧰 Tools",
    "📊 Dashboard",
    "📝 Blog",
    "💰 Pricing",
    "ℹ️ About",
    "📩 Contact",
    "⚙️ Settings",
])

# =============================================================
# TOOL REGISTRY (OLD + NEW)
# =============================================================
TOOLS = {
    # EXISTING TOOLS
    "Competitor Analysis": "Compare your brand with competitors",
    "Social Media Analyzer": "Analyze growth, reach & engagement",

    # NEW TOOLS
    "BloomScore": "AI-powered brand health score",
    "Consumer Behaviour": "Understand customer intent & patterns",
    "Email Marketing": "Optimize campaigns & conversions",
    "Influencer Finder": "Discover relevant creators for your brand",
    "Business Compare": "Compare brands across KPIs",
    "Menu Pricing": "Optimize pricing for profitability",
    "Loyalty": "Retention & repeat customer insights",
}

# SESSION STATE
if "active_tool" not in st.session_state:
    st.session_state.active_tool = None

# =============================================================
# HOME
# =============================================================
with menu[0]:
    st.markdown("<div class='container'>", unsafe_allow_html=True)

    st.markdown("<div class='hero-title'>Brand N Bloom 🌸</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='hero-subtitle'>Marketing intelligence powered by data & AI</div>",
        unsafe_allow_html=True,
    )

    st.divider()

    c1, c2, c3 = st.columns(3)
    c1.markdown("<div class='card'>📊 Data-driven insights</div>", unsafe_allow_html=True)
    c2.markdown("<div class='card'>🤖 AI-powered tools</div>", unsafe_allow_html=True)
    c3.markdown("<div class='card'>🚀 Growth-focused analytics</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# =============================================================
# TOOLS
# =============================================================
with menu[1]:
    st.markdown("<div class='container'>", unsafe_allow_html=True)
    st.header("🧰 Tools")

    for tool, desc in TOOLS.items():
        if st.button(tool, use_container_width=True):
            st.session_state.active_tool = tool
        st.caption(desc)

    if st.session_state.active_tool:
        st.divider()
        st.subheader(st.session_state.active_tool)
        st.info(f"{st.session_state.active_tool} tool UI will load here.")

    st.markdown("</div>", unsafe_allow_html=True)

# =============================================================
# DASHBOARD
# =============================================================
with menu[2]:
    st.markdown("<div class='container'>", unsafe_allow_html=True)
    st.header("📊 Dashboard")

    c1, c2, c3 = st.columns(3)
    c1.metric("Active Tools", len(TOOLS))
    c2.metric("Reports Generated", "—")
    c3.metric("Growth Score", "—")

    st.info("Connect tools to activate live dashboards.")
    st.markdown("</div>", unsafe_allow_html=True)

# =============================================================
# BLOG
# =============================================================
with menu[3]:
    st.markdown("<div class='container'>", unsafe_allow_html=True)
    st.header("📝 Blog")
    st.info("Blogs will be loaded from Markdown / CMS.")
    st.markdown("</div>", unsafe_allow_html=True)

# =============================================================
# PRICING
# =============================================================
with menu[4]:
    st.markdown("<div class='container'>", unsafe_allow_html=True)
    st.header("💰 Pricing")

    c1, c2 = st.columns(2)
    c1.markdown("<div class='card'><h3>Starter</h3><p>Free</p></div>", unsafe_allow_html=True)
    c2.markdown("<div class='card'><h3>Pro</h3><p>₹1999 / month</p></div>", unsafe_allow_html=True)
    st.link_button("Pay with PayPal", "https://www.paypal.com")

    st.markdown("</div>", unsafe_allow_html=True)

# =============================================================
# ABOUT
# =============================================================
with menu[5]:
    st.markdown("<div class='container'>", unsafe_allow_html=True)
    st.header("ℹ️ About Brand N Bloom")
    st.write(
        "Brand N Bloom is a marketing analytics & intelligence platform "
        "built to help brands grow using data, AI, and clarity."
    )
    st.markdown("</div>", unsafe_allow_html=True)

# =============================================================
# CONTACT
# =============================================================
with menu[6]:
    st.markdown("<div class='container'>", unsafe_allow_html=True)
    st.header("📩 Contact")
    st.text_input("Your Email")
    st.text_area("Message")
    st.button("Send")
    st.markdown("</div>", unsafe_allow_html=True)

# =============================================================
# SETTINGS
# =============================================================
with menu[7]:
    st.markdown("<div class='container'>", unsafe_allow_html=True)
    st.header("⚙️ Settings")
    st.info("Use Streamlit Settings → Theme to switch Light / Dark mode.")
    st.markdown("</div>", unsafe_allow_html=True)
