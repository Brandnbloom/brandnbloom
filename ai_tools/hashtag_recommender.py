import streamlit as st
from services.insights_store import save_insight
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

BASE_HASHTAGS = {
    "Branding": ["#branding", "#brandstrategy", "#brandidentity"],
    "Marketing": ["#digitalmarketing", "#growthmarketing", "#contentmarketing"],
    "Personal Brand": ["#personalbrand", "#creatorlife", "#buildinpublic"],
}

PLATFORM_TAGS = {
    "Instagram": ["#reels", "#instagrowth", "#explorepage"],
    "LinkedIn": ["#linkedincreators", "#founders", "#b2bmarketing"],
}

def run():
    st.markdown("### 🔖 Hashtag Strategy Generator")

    user_id = st.session_state.get("user_id", "guest")

    topic = st.text_input("Content topic")
    niche = st.selectbox("Niche", list(BASE_HASHTAGS.keys()))
    platform = st.selectbox("Platform", ["Instagram", "LinkedIn"])

    if st.button("Generate Hashtags"):
        if not topic:
            st.warning("Please enter a topic.")
            return

        core = [f"#{topic.replace(' ', '')}", f"#{topic.replace(' ', '')}tips"]
        growth = BASE_HASHTAGS[niche]
        discovery = PLATFORM_TAGS[platform]

        hashtags = {
            "core": core,
            "growth": growth,
            "discovery": discovery
        }

        # 1️⃣ Save insight
        save_insight(
            user_id=user_id,
            tool="Hashtag Recommender",
            data=hashtags
        )

        st.success("Hashtag strategy saved to Dashboard ✅")

        st.markdown("#### 🎯 Recommended Hashtags")
        st.code(" ".join(core + growth + discovery))
