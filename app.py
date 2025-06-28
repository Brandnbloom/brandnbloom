
import streamlit as st

st.set_page_config(page_title="Brand n Bloom", layout="wide")

# 🌸 Banner
st.image("assets/banner.png", use_column_width=True)
st.markdown(
    "<div style='text-align:center; font-size:24px; color:#725B53; margin-top:-20px;'>"
    "Where branding blooms into a beautiful story 🌸"
    "</div>",
    unsafe_allow_html=True
)

# 🌸 Sidebar Navigation
with st.sidebar:
    st.image("assets/logo.png", width=150)
    st.page_link("app.py", label="🏠 Home")
    st.page_link("pages/BloomScore.py", label="📊 BloomScore")
    st.page_link("pages/Consumer_Behavior.py", label="🧠 DinePsych")
    st.page_link("pages/Visual_Audit.py", label="🎨 Visual Audit")
    st.page_link("pages/Review_Reply.py", label="💬 Review Assistant")
    st.page_link("pages/Digital_Menu.py", label="📄 Digital Menu")
    st.page_link("pages/BloomInsight.py", label="📈 BloomInsight")
    st.page_link("pages/blogs.py", label="📝 Blogs")
    st.page_link("pages/contact_us.py", label="📬 Contact")
    st.page_link("pages/legal.py", label="⚖️ Terms & Privacy")
