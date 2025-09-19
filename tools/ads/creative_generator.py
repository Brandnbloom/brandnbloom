import streamlit as st
from utils.ai_client import generate_text

def show_creative_ui():
    st.title("Ad Creative Generator")
    ad_type = st.selectbox("Platform", ["Google Search", "Facebook", "LinkedIn", "Instagram"])
    product = st.text_area("Describe product or offer", value="Organic face oil for oily skin")
    tone = st.selectbox("Tone", ["Professional","Playful","Emotional","Direct"])
    if st.button("Generate creatives"):
        prompt = f"Write 10 {ad_type} ad headlines, 6 short descriptions, 6 CTAs, and 3 image prompt ideas for this product. Tone: {tone}. Product: {product}"
        out = generate_text(prompt, max_tokens=500)
        st.code(out)
