import streamlit as st

st.set_page_config(page_title="Brand n Bloom", layout="wide")

# 🌸 Banner
st.image("assets/banner.png", use_container_width=True)

# 🌟 Introduction
st.markdown("""
<style>
    .main-title {
        font-size: 32px;
        font-weight: 600;
        color: #3c3c3c;
    }
    .subtext {
        font-size: 18px;
        color: #666;
    }
</style>

<div class="main-title">Welcome to Brand n Bloom 🌸</div>
<div class="subtext">
    Unleash the power of branding with AI. Our tools empower restaurants and brands to analyze, grow, and bloom creatively.
</div>
""", unsafe_allow_html=True)

# 🌿 Sidebar Navigation
with st.sidebar:
    st.image("assets/logo.png", width=150)
    st.markdown("### Navigate")
    
    st.page_link("app.py", label="🏠 Home", icon="🏠")
    st.page_link("pages/BloomScore.py", label="📊 BloomScore")
    st.page_link("pages/Consumer_Behavior.py", label="🧠 DinePsych")
    st.page_link("pages/Visual_Audit.py", label="🎨 Visual Audit")
    st.page_link("pages/Review_Reply.py", label="💬 Review Assistant")
    st.page_link("pages/Digital_Menu.py", label="📄 Digital Menu")
    st.page_link("pages/BloomInsight.py", label="📈 BloomInsight")

    st.markdown("### 📚 Info")
    st.page_link("pages/about_us.py", label="👥 About Us")
    st.page_link("pages/about_ceo.py", label="👩‍💼 About CEO")
    st.page_link("pages/our_services.py", label="🛠️ Products & Services")
    st.page_link("pages/manifesto.py", label="📜 Manifesto")

    st.markdown("### 📝 More")
    st.page_link("pages/blogs.py", label="📝 Blogs")
    st.page_link("pages/contact_us.py", label="📬 Contact")
    st.page_link("pages/legal.py", label="⚖️ Terms & Privacy")
