import streamlit as st
import os

st.set_page_config(page_title="📝 Blogs - Brand n Bloom", layout="wide")
st.title("📝 Blog Vault")
st.markdown("Browse helpful guides, tips & tools for growing your hospitality brand.")

blog_dir = "blogs"

blogs = [f for f in os.listdir(blog_dir) if f.endswith(".md")]

selected = st.selectbox("📚 Choose a blog to read", blogs)

with open(os.path.join(blog_dir, selected), "r", encoding="utf-8") as f:
    st.markdown(f.read(), unsafe_allow_html=True)
