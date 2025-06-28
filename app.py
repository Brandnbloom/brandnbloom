import streamlit as st

st.set_page_config(page_title="Brand n Bloom", page_icon="🌸", layout="wide")

with st.container():
    st.image("assets/banner.png", use_column_width=True)
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