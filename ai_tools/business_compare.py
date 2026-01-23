import streamlit as st
from services.insights_store import save_insight
from services.caption_engine import generate_caption

def run():
    st.markdown("### ⚖️ Business Compare")

    user_id = st.session_state.get("user_id", "guest")

    brand_a = st.text_input("Brand A")
    brand_b = st.text_input("Brand B")

    focus = st.selectbox(
        "Comparison focus",
        ["Content Strategy", "Brand Positioning", "Engagement Style"]
    )

    if st.button("Compare Brands"):
        if not brand_a or not brand_b:
            st.warning("Please enter both brands.")
            return

        # Deterministic insight logic
        insights = {
            "brand_a": brand_a,
            "brand_b": brand_b,
            "focus": focus,
            "winner": brand_a if len(brand_a) > len(brand_b) else brand_b,
            "key_difference": f"{focus} execution style differs significantly"
        }

        # 1️⃣ Save insight
        save_insight(
            user_id=user_id,
            tool="Business Compare",
            data=insights
        )

        # 2️⃣ Generate AI caption
        caption_prompt = generate_caption(
            insight=insights,
            tone="analytical",
            platform="LinkedIn"
        )

        st.success("Comparison saved to Dashboard ✅")

        st.markdown("#### ✨ AI Caption Suggestion")
        st.text_area("Caption", caption_prompt, height=200)


