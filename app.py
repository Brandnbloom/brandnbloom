import streamlit as st

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

with st.container():
    st.image("assets/banner.png", caption="AI Marketing Tools for Restaurants", use_container_width=True)
    st.markdown("""
        <h1 style='text-align: center; color: #6C4F77;'>Welcome to Brand n Bloom 🌸</h1>
        <p style='text-align: center; font-size: 18px;'>Where restaurants & cafes blossom with powerful digital strategies</p>
        <hr style='border:1px solid #DABECF;'>
    """, unsafe_allow_html=True)

with st.container():
    st.header("✨ Why Choose Us?")
    st.markdown("""
    - 🌍 Global strategy for local brands  
    - 📈 AI-powered SEO & Instagram growth  
    - 🎯 Lead generation, content, website & analytics  
    """)

    st.subheader("Explore Our AI Tools")
    st.markdown("Use the sidebar to access BloomScore, DinePsych, Digital Menu, and more!")
    
    # Load logo
with st.sidebar:
    st.image("assets/logo.png.png", width=180)  # ✅ Adjust width if needed
    st.page_link("app.py", label="🏠 Home")
    st.page_link("pages/BloomInsight.py", label="📈 BloomInsight")
    st.page_link("pages/BloomScore.py", label="📊 BloomScore")
    st.page_link("pages/Consumer_Behavior.py", label="🧠 DinePsych")
    st.page_link("pages/Visual_Audit.py", label="🎨 Visual Audit")
    st.page_link("pages/Review_Reply.py", label="💬 Review Assistant")
    st.page_link("pages/Digital_Menu.py", label="📄 Digital Menu")
    st.page_link("pages/blogs.py", label="📝 Blogs")
    st.page_link("pages/contact_us.py", label="📬 Contact")
    st.page_link("pages/legal.py", label="⚖️ Terms & Privacy")
