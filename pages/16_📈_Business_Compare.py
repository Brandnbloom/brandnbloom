import streamlit as st
from utils.ui import inject_css, dark_mode_toggle
from ai_tools.business_compare import compare_handles

inject_css(); dark_mode_toggle()
st.title("📈 Business Comparison")
handles = st.text_area("Handles (comma separated)", "brandnbloom_demo,competitor1").split(",")
if st.button("Compare"):
    res = compare_handles([h.strip() for h in handles if h.strip()])
    st.json(res)
