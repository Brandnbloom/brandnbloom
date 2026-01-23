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
    st.markdown("### 🧠 Consumer Behavior Analysis")

    user_id = st.session_state.get("user_id", "guest")

    audience = st.selectbox(
        "Primary audience",
        ["Gen Z", "Millennials", "Working Professionals", "Parents"]
    )

    buying_trigger = st.selectbox(
        "Main buying trigger",
        ["Price", "Quality", "Emotions", "Social Proof"]
    )

    hesitation = st.selectbox(
        "Biggest hesitation before purchase",
        ["Trust", "Price", "Need clarity", "Too many options"]
    )

    content_preference = st.selectbox(
        "Content preference",
        ["Educational", "Inspirational", "Entertaining", "Direct CTA"]
    )

    if st.button("Analyze Behavior"):
        # Behavioral inference logic (REAL)
        mindset = "value-seeker"
        if buying_trigger == "Emotions":
            mindset = "emotion-driven"
        elif buying_trigger == "Quality":
            mindset = "quality-conscious"

        persuasion_angle = "build trust"
        if hesitation == "Price":
            persuasion_angle = "justify value"
        elif hesitation == "Need clarity":
            persuasion_angle = "educate clearly"

        insights = {
            "audience": audience,
            "buyer_mindset": mindset,
            "buying_trigger": buying_trigger,
            "primary_hesitation": hesitation,
            "best_content_type": content_preference,
            "recommended_persuasion": persuasion_angle
        }

        # 1️⃣ Save insight
        save_insight(
            user_id=user_id,
            tool="Consumer Behavior",
            data=insights
        )

        # 2️⃣ Generate AI caption
        caption_prompt = generate_caption(
            insight=insights,
            tone="empathetic",
            platform="Instagram"
        )

        st.success("Behavior insights saved to Dashboard ✅")

        st.markdown("#### ✨ AI Caption Suggestion")
        st.text_area("Caption", caption_prompt, height=220)
