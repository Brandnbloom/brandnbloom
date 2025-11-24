import streamlit as st
from .scheduler import schedule_post
import datetime

def show_calendar():
    st.title("📅 Social Media Content Calendar")

    st.subheader("Create & Schedule Posts")

    platform = st.selectbox("Select Platform:", ["instagram", "linkedin", "tiktok"])

    content = st.text_area("Write Your Post Content:", height=150)

    # Character counter
    st.caption(f"Characters: {len(content)}")

    media = st.file_uploader("Upload image/video (optional):", type=["png", "jpg", "jpeg", "mp4"])

    hashtags = st.text_input("Add hashtags (optional):", placeholder="#marketing #business")

    first_comment = st.text_area("First Comment (optional – esp. for Instagram):", height=80)

    # Combine content + hashtags
    full_content = content
    if hashtags.strip():
        full_content += "\n\n" + hashtags

    # User selects date AND time
    date = st.date_input("Select Post Date:", min_value=datetime.date.today())
    time = st.time_input("Select Post Time:", datetime.time(hour=10, minute=0))

    schedule_datetime = datetime.datetime.combine(date, time).isoformat()

    repeat = st.selectbox("Repeat:", ["No repeat", "Daily", "Weekly"])

    # LIVE preview
    st.subheader("Post Preview")
    st.write("### ✨ Your Post")
    st.write(full_content if full_content.strip() else "*No content yet*")

    if first_comment.strip():
        st.write("**First Comment:**")
        st.caption(first_comment)

    if media:
        st.image(media, use_column_width=True)

    # VALIDATION
    if st.button("📌 Schedule Post"):
        if not content.strip():
            st.error("Post content cannot be empty!")
            return
        
        payload = {
            "platform": platform,
            "content": full_content,
            "media": media.name if media else None,
            "first_comment": first_comment.strip(),
            "repeat": repeat,
        }

        try:
            job_id = schedule_post(platform, full_content, schedule_datetime, payload)
            st.success(f"✅ Post Scheduled Successfully! Job ID: {job_id}")
        except Exception as e:
            st.error(f"❌ Failed to schedule: {str(e)}")

    st.markdown("---")
    st.subheader("📜 Scheduled Posts (coming soon)")
    st.info("This section will display all upcoming scheduled posts once scheduler DB integration is added.")
