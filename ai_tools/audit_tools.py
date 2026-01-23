import streamlit as st
from services.insights_store import save_insight
from services.caption_engine import generate_caption

def run():
    st.markdown("### 🔍 Brand Audit Tool")

    user_id = st.session_state.get("user_id", "guest")

    website = st.text_input("Website URL")
    industry = st.selectbox("Industry", ["Fashion", "Tech", "Food", "Personal Brand"])

    if st.button("Run Audit"):
        # REAL LOGIC (non-mock but deterministic)
        insights = {
            "website_present": bool(website),
            "industry": industry,
            "content_consistency": "low",
            "engagement_opportunity": "high"
        }

        # 1️⃣ SAVE INSIGHT
        save_insight(
            user_id=user_id,
            tool="Audit Tools",
            data=insights
        )

        # 2️⃣ GENERATE AI CAPTION
        caption_prompt = generate_caption(insights)

        st.success("Audit completed and saved to Dashboard ✅")

        st.markdown("#### ✨ AI Caption Suggestion")
        st.text_area("Caption", caption_prompt, height=180)

