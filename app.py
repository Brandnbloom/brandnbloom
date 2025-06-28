import streamlit as st
from PIL import Image
import base64

# ✅ SEO & Page Setup
st.set_page_config(
    page_title="Brand n Bloom – AI Tools for Restaurant Marketing",
    page_icon="🌸",
    layout="wide"
)

# ✅ Inject SEO meta tags
st.markdown("""
    <meta name="description" content="Brand n Bloom is an AI-powered marketing agency for restaurants and hospitality businesses. Try our tools for SEO, Instagram audits, and more.">
    <meta name="keywords" content="Restaurant Marketing, AI Tools, Instagram Audit, SEO for Cafe, Digital Menu, Hospitality Growth">
    <meta name="author" content="Brand n Bloom">
    <meta property="og:title" content="Brand n Bloom – AI Tools for Restaurants" />
    <meta property="og:description" content="Grow your restaurant online with AI-powered tools like BloomScore, DinePsych & more." />
    <meta property="og:image" content="https://brand-n-bloom.com/assets/banner.png" />
    <meta property="og:url" content="https://www.brand-n-bloom.com/" />
""", unsafe_allow_html=True)


# -------------------
# Custom Navbar Styling
# -------------------
custom_css = """
<style>
/* Banner */
.banner {
    width: 100%;
    padding: 2rem;
    background-color: #FAF3F0;
    text-align: center;
    border-radius: 15px;
    margin-top: 1rem;
}

/* Logo + Title */
.logo-title {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.logo-title img {
    width: 60px;
    height: 60px;
    border-radius: 10px;
}

/* Menu */
.menu {
    margin-top: 2rem;
    background-color: #FFF0F5;
    padding: 1rem;
    border-radius: 10px;
}

.menu a {
    text-decoration: none;
    color: #3B3B3B;
    font-weight: bold;
    padding: 0.5rem 1rem;
    display: inline-block;
    transition: background-color 0.2s ease-in-out;
}
.menu a:hover {
    background-color: #FADADD;
    border-radius: 5px;
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# -------------------
# Logo & Title
# -------------------
col1, col2 = st.columns([0.1, 0.9])

with col1:
    st.image("assets/logo.png", width=70)  # <-- Use your actual logo path

with col2:
    st.markdown("<h1 style='margin-bottom: 0;'>Brand n Bloom</h1>", unsafe_allow_html=True)
    st.caption("Where local brands blossom globally 💫")

# -------------------
# Banner
# -------------------
st.markdown("""
<div class='banner'>
    <h2>Grow your hospitality brand with our AI-powered marketing tools 🚀</h2>
    <p>Tools for Instagram, website audit, reviews, digital menu, and more — all tailored for restaurants.</p>
</div>
""", unsafe_allow_html=True)

# -------------------
# Menu (Internal Navigation)
# -------------------
st.markdown("""
<div class='menu'>
    <a href="/bloomscore" target="_self">🌺 BloomScore</a>
    <a href="/consumer_behavior" target="_self">🧠 DinePsych</a>
    <a href="/review_reply_assistant" target="_self">💬 Review Assistant</a>
    <a href="/visual_brand_audit" target="_self">🎨 Visual Brand Audit</a>
    <a href="/competitor_snapshot" target="_self">📊 Competitor Tool</a>
    <a href="/digital_menu_creator" target="_self">📋 Menu Creator</a>
    <a href="/about_us" target="_self">👤 About Us</a>
    <a href="/services" target="_self">🛠️ Services</a>
    <a href="/manifesto" target="_self">📜 Manifesto</a>
</div>
""", unsafe_allow_html=True)

# -------------------
# Optional CTA or Image
# -------------------
st.markdown("### 👇 Get started with your favorite tool below!")
