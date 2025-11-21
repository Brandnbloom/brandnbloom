import streamlit as st
import requests
from .config import BACKEND_URL

st.title("Social Media Tools")

# ---------------- Check Login ----------------
if "token" not in st.session_state:
    st.warning("Please login first.")
    st.stop()

headers = {"Authorization": f"Bearer {st.session_state['token']}"}

# ---------------- Schedule Post ----------------
st.subheader("📅 Schedule a Post")

platform = st.selectbox("Platform", ["Instagram", "LinkedIn", "Facebook", "Twitter"])
content = st.text_area("Post Content")
schedule_time = st.text_input("Schedule Time (YYYY-MM-DD HH:MM)")

if st.button("Schedule Post"):
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/social/schedule",
            json={"platform": platform, "content": content, "schedule_time": schedule_time},
            headers=headers,
            timeout=20
        )
        if response.status_code == 200:
            st.success("Post scheduled successfully!")
            st.json(response.json())
        else:
            st.error(response.json().get("detail", "Error scheduling post."))
    except Exception as e:
        st.error(f"Connection error: {e}")

# ---------------- View Posts ----------------
st.subheader("📌 Your Scheduled Posts")

if st.button("View My Posts"):
    try:
        response = requests.get(
            f"{BACKEND_URL}/api/social/posts",
            headers=headers,
            timeout=20
        )
        if response.status_code == 200:
            st.json(response.json())
        else:
            st.error("Error fetching posts.")
    except Exception as e:
        st.error(f"Connection error: {e}")

# ---------------- Engagement Metrics ----------------
st.subheader("📈 Engagement Metrics")

if st.button("View Engagements"):
    try:
        response = requests.get(
            f"{BACKEND_URL}/api/social/engagements",
            headers=headers,
            timeout=20
        )
        if response.status_code == 200:
            engagements = response.json()
            if len(engagements) == 0:
                st.info("No engagements yet.")
            else:
                for idx, item in enumerate(engagements):
                    st.write(
                        f"{idx}: {item['platform']} — {item['comment']} "
                        f"(Status: {item['status']})"
                    )
        else:
            st.error("Error fetching engagements.")
    except Exception as e:
        st.error(f"Connection error: {e}")

# ---------------- Reply to Comment ----------------
st.subheader("💬 Reply to Comment")

comment_id = st.number_input("Comment ID", min_value=0, step=1)
reply_text = st.text_input("Reply Text")

if st.button("Reply"):
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/social/reply",
            json={"comment_id": comment_id, "reply": reply_text},
            headers=headers,
            timeout=20
        )
        if response.status_code == 200:
            st.success("Replied successfully!")
            st.json(response.json())
        else:
            st.error(response.json().get("detail", "Error replying to comment."))
    except Exception as e:
        st.error(f"Connection error: {e}")
