import streamlit as st
from services.insights_store import save_insight
from services.caption_engine import generate_caption

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

        st.markdown("#### ✨ Outreach Message (DM / Email)")
        st.text_area("Message", caption_prompt, height=220)

