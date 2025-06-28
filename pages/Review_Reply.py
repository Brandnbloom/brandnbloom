import streamlit as st
import openai
import os
from utils import can_use_tool, increment_usage, send_email_with_pdf, show_stripe_buttons

openai.api_key = os.getenv("OPENROUTER_API_KEY")

st.title("💬 Review Reply Assistant")

st.markdown("""
Tired of replying to every review manually?  
Let AI generate human-like responses in your brand’s voice — be it grateful, apologetic, or witty.  
""")

# Usage control
if not can_use_tool("review_reply_assistant"):
    show_stripe_buttons()
    st.stop()

# Form
with st.form("review_form"):
    customer_review = st.text_area("🗣️ Customer Review", placeholder="Paste a real customer review here")
    tone = st.selectbox("🎭 Tone of Response", ["Grateful", "Apologetic", "Professional", "Witty"])
    email = st.text_input("📩 Email to receive reply as PDF (optional)")
    submit = st.form_submit_button("🪄 Generate Reply")

if submit and customer_review:
    with st.spinner("Generating reply..."):
        prompt = f"""
A customer has left the following review:
"{customer_review}"

Write a response in a {tone.lower()} tone.
Be professional, kind, and representative of a restaurant brand.
Do not exceed 4 lines.
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            reply = response.choices[0].message["content"]
            st.success("✅ Suggested Reply")
            st.markdown(f"> {reply}")

            increment_usage("review_reply_assistant")

            if email:
                send_email_with_pdf("Your Review Reply", email, reply)

        except Exception as e:
            st.error(f"AI Error: {e}")
else:
    if submit:
        st.warning("Please paste a review to proceed.")
