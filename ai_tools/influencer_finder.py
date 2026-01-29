import streamlit as st
from services.insights_store import save_insight
from services.caption_engine import generate_caption
import pandas as pd

sample_data = pd.DataFrame({
    "customer_id": [1,2,3],
    "recency": [10, 20, 5],
    "frequency": [3, 1, 5],
    "monetary": [200, 150, 500],
    "churn": [0, 1, 0]
})

st.download_button(
    "📥 Download Sample Data",
    data=sample_data.to_csv(index=False),
    file_name="sample_data.csv",
    mime="text/csv"
)

def run():
    st.markdown("### 🤝 Influencer Finder")

    user_id = st.session_state.get("user_id", "guest")

    niche = st.selectbox(
        "Brand niche",
        ["Fashion", "Beauty", "Fitness", "Tech", "Parenting", "Education"]
    )

    platform = st.selectbox(
        "Platform",
        ["Instagram", "LinkedIn", "YouTube"]
    )

    goal = st.selectbox(
        "Collaboration goal",
        ["Brand Awareness", "Sales", "UGC Content", "Trust Building"]
    )

    creator_size = st.selectbox(
        "Creator size",
        ["Nano (1k–10k)", "Micro (10k–50k)", "Mid (50k–200k)"]
    )

    if st.button("Find Influencers"):
        alignment_score = 70

        if creator_size.startswith("Nano"):
            alignment_score += 10
        if goal == "Trust Building":
            alignment_score += 10

        insights = {
            "niche": niche,
            "platform": platform,
            "creator_size": creator_size,
            "collaboration_goal": goal,
            "alignment_score": min(alignment_score, 95),
            "recommended_creator_type": "authentic storytellers"
        }

        # 1️⃣ Save insight
        save_insight(
            user_id=user_id,
            tool="Influencer Finder",
            data=insights
        )

        # 2️⃣ Generate outreach caption
        caption_prompt = generate_caption(
            insight=insights,
            tone="professional",
            platform=platform
        )

        st.success("Influencer strategy saved to Dashboard ✅")

          # ---------------- Check usage ----------------
    from streamlit_app import check_usage
    if not check_usage("Influencer finder"):
        st.stop()  # Stop the tool if free limit reached

    # ---------------- Tool logic ----------------
    uploaded_file = st.file_uploader("Upload Customer Data", type=['csv'])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("Data loaded successfully!")
        # Your influencer finder logic here...


        st.markdown("#### ✨ Outreach Message (DM / Email)")
        st.text_area("Message", caption_prompt, height=220)

