import streamlit as st
import requests
from .config import BACKEND_URL

st.title("Social Media Tools")

if "token" not in st.session_state:
    st.warning("Please login first.")
    st.stop()

# ---------------- Schedule Post ----------------
st.subheader("Schedule a Post")
platform = st.selectbox("Platform", ["Instagram", "LinkedIn", "Facebook", "Twitter"])
content = st.text_area("Content")
schedule_time = st.text_input("Schedule Time (YYYY-MM-DD HH:MM)")

if st.button("Schedule Post"):
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    response = requests.post(f"{BACKEND_URL}/tools/schedule-post",
                             params={"platform": platform, "content": content, "schedule_time": schedule_time},
                             headers=headers)
    if response.status_code == 200:
        st.success("Post scheduled successfully!")
        st.json(response.json())
    else:
        st.error("Error scheduling post.")

if st.button("View My Posts"):
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    response = requests.get(f"{BACKEND_URL}/tools/posts", headers=headers)
    if response.status_code == 200:
        st.json(response.json())
    else:
        st.error("Error fetching posts.")

# ---------------- Engagement Metrics ----------------
st.subheader("Engagements")
if st.button("View Engagements"):
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    response = requests.get(f"{BACKEND_URL}/tools/engagements", headers=headers)
    if response.status_code == 200:
        engagements = response.json()
        for idx, comment in enumerate(engagements):
            st.write(f"{idx}: {comment['platform']} - {comment['comment']} (Status: {comment['status']})")
    else:
        st.error("Error fetching engagements.")

# Reply to comment
st.subheader("Reply to Comment")
comment_id = st.number_input("Comment ID", min_value=0, step=1)
reply_text = st.text_input("Reply Text")

if st.button("Reply"):
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    response = requests.post(f"{BACKEND_URL}/tools/reply-comment",
                             params={"platform": "Any", "comment_id": comment_id, "reply": reply_text},
                             headers=headers)
    if response.status_code == 200:
        st.success("Replied successfully!")
        st.json(response.json())
    else:
        st.error("Error replying to comment.")
