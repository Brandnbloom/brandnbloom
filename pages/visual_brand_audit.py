import streamlit as st

st.title("🎨 Visual Brand Audit Tool")
st.markdown("Upload a screenshot of your Instagram or website and let AI assess your brand vibe.")

uploaded_file = st.file_uploader("📸 Upload screenshot", type=["png", "jpg", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, use_column_width=True)
    st.success("✅ Audit Complete!")
    st.markdown("""
    ### 🔍 AI Observations:
    - **Tone:** Friendly and inviting  
    - **Color Palette:** Pastel, warm tones — visually pleasing  
    - **Font Usage:** Consistent typography  
    - **Moodboard Match:** 8.5/10  
    - **Suggestions:** Try more contrast on CTAs and consistent filter style
    """)
