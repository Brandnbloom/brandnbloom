import streamlit as st

st.title("📝 Review Reply Assistant")
st.markdown("Generate human-like responses to Google reviews.")

review = st.text_area("📩 Paste your customer's review below:")
tone = st.selectbox("🎭 Choose the tone of your reply:", ["Grateful", "Apologetic", "Witty", "Professional"])

if st.button("Generate Reply"):
    if review:
        st.success("✅ Here's your suggested reply:")
        if tone == "Grateful":
            st.write(f"Thank you so much for your kind words! We're thrilled you enjoyed your experience. Looking forward to welcoming you again!")
        elif tone == "Apologetic":
            st.write(f"We’re truly sorry to hear about your experience. Your feedback helps us improve. We'd love a chance to make it right.")
        elif tone == "Witty":
            st.write(f"Oh no, we dropped the (bread)ball! 🥖 We’ll work harder to rise next time – thanks for the heads-up!")
        elif tone == "Professional":
            st.write(f"Thank you for your valuable feedback. We take every review seriously and are committed to constant improvement.")
    else:
        st.warning("Please paste a review first.")
