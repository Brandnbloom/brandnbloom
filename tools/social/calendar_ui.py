import streamlit as st
from .scheduler import schedule_post

def show_calendar():
    st.title("Content Calendar")
    platform = st.selectbox("Platform", ["instagram","linkedin","tiktok"])
    content = st.text_area("Post content")
    post_time = st.date_input("Post Date")
    if st.button("Schedule"):
        job = schedule_post(platform, content, post_time.isoformat(), {})
        st.success(f"Scheduled! Job id: {job}")
