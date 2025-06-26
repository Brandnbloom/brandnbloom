import streamlit as st

st.title("📝 Review Reply Assistant")

st.markdown("Generate responses for Google reviews.")

review = st.text_area("Paste the review here:")
tone = st.selectbox("Select a tone", ["Grateful", "Apologetic", "Witty"])

if st.button("Generate Reply"):
    if review:
        st.success(f"Here’s a {tone.lower()} reply to that review:")
        st.write(f"Dear customer, thank you for your feedback...")
    else:
        st.warning("Please paste a review first.")
