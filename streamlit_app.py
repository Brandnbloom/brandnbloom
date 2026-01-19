# streamlit_app.py
"""
Brand N Bloom – Marketing & Data Intelligence Platform
Architected for stability, scalability, and clean UX
"""

import streamlit as st
import time

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Brand N Bloom",
    page_icon="🌸",
    layout="wide",
)

# =========================================================
# GLOBAL CSS (SAFE FOR LIGHT + DARK)
# =========================================================
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.main-container {
    padding: 2rem 4rem;
}

.hero-title {
    font-size: 3rem;
    font-weight: 600;
}

.hero-subtitle {
    font-size: 1.1rem;
    opacity: 0.85;
}

.tool-card {
    padding: 1.4rem;
    border-radius: 14px;
    background: var(--secondary-background-color);
    border: 1px solid rgba(128,128,128,0.15);
    transition: transform 0.15s ease;
}

.tool-card:hover {
    transform: translateY(-4px);
}

.center {
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# TOP NAVIGATION
# =========================================================
menu = st.columns([1,1,1,1,1,1,1,1])

pages = [
    "Home", "Features", "Pricing", "Blog",
    "Dashboard", "Tools", "About", "Contact",
    "Login", "Signup"
]

if "page" not in st.session_state:
    st.session_state.page = "Home"

for i, page in enumerate(pages[:8]):
    if menu[i].button(page):
        st.session_state.page = page

# =========================================================
# BANNER
# =========================================================
st.markdown("<div class='main-container'>", unsafe_allow_html=True)

st.markdown("""
<div class="center">
    <h1 class="hero-title">Brand N Bloom 🌸</h1>
    <p class="hero-subtitle">
        Marketing intelligence, consumer insights & data-driven growth tools
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# =========================================================
# TOOLS REGISTRY (SINGLE SOURCE OF TRUTH)
# =========================================================
TOOLS = {
    "BloomScore": "AI-powered brand health & growth score",
    "Consumer Behaviour": "Understand audience psychology & intent",
    "Email Marketing": "Campaign analysis & optimization insights",
    "Influencer Finder": "Discover the right creators for your brand",
    "Business Compare": "Compare brands, markets & competitors",
    "Menu Pricing": "Data-backed pricing strategy & optimization",
    "Loyalty Engine": "Retention, repeat purchase & loyalty analytics",
}

# =========================================================
# PAGE ROUTING
# =========================================================
page = st.session_state.page

# ---------------- HOME ----------------
if page == "Home":
    c1, c2, c3 = st.columns(3)
    for col, text in zip([c1,c2,c3], [
        "📊 Data-Driven Decisions",
        "🎯 Smarter Marketing",
        "🚀 Scalable Growth"
    ]):
        with col:
            st.markdown(f"<div class='tool-card center'>{text}</div>", unsafe_allow_html=True)

# ---------------- FEATURES ----------------
elif page == "Features":
    st.subheader("Platform Features")
    for tool, desc in TOOLS.items():
        if st.button(tool):
            st.session_state.page = "Tools"
            st.session_state.selected_tool = tool
        st.caption(desc)

# ---------------- PRICING ----------------
elif page == "Pricing":
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='tool-card'><h3>Starter</h3><p>₹0 / month</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='tool-card'><h3>Pro</h3><p>₹1999 / month</p></div>", unsafe_allow_html=True)
        st.link_button("Pay with PayPal", "https://www.paypal.com")

# ---------------- BLOG ----------------
elif page == "Blog":
    st.info("Blogs will be loaded from markdown / CMS")

# ---------------- DASHBOARD ----------------
elif page == "Dashboard":
    st.warning("Dashboard activates once tools start generating data")

# ---------------- TOOLS ----------------
elif page == "Tools":
    st.subheader("Marketing & Analytics Tools")

    for tool, desc in TOOLS.items():
        with st.container():
            st.markdown(f"<div class='tool-card'><h4>{tool}</h4><p>{desc}</p></div>", unsafe_allow_html=True)

# ---------------- ABOUT ----------------
elif page == "About":
    st.write(
        "Brand N Bloom is built to empower founders, marketers and analysts "
        "with clarity, confidence and data-backed decisions."
    )

# ---------------- CONTACT ----------------
elif page == "Contact":
    st.text_input("Your Email")
    st.text_area("Message")
    st.button("Send")

# ---------------- LOGIN ----------------
elif page == "Login":
    st.text_input("Email")
    st.text_input("Password", type="password")
    st.button("Login")

# ---------------- SIGNUP ----------------
elif page == "Signup":
    st.text_input("Name")
    st.text_input("Email")
    st.text_input("Password", type="password")
    st.button("Create Account")

st.markdown("</div>", unsafe_allow_html=True)
