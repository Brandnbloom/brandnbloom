import streamlit as st
import openai
import os
from utils import can_use_tool, increment_usage, send_email_with_pdf
# show_stripe_buttons removed temporarily

openai.api_key = os.getenv("OPENROUTER_API_KEY")

st.title("💬 Review Reply Assistant")

st.markdown("""
Respond to customer reviews with empathy and professionalism.  
Just paste the review, select tone, and get a ready-to-use response.
""")

# Usage control
if not can_use_tool("review_reply_assistant"):
    show_stripe_buttons()
    st.stop()

with st.form("review_reply_form"):
    review = st.text_area("📝 Customer Review", placeholder="e.g., 'Food was amazing but service was a bit slow.'")
    tone = st.selectbox("🎭 Tone of Response", ["Grateful", "Apologetic", "Witty", "Professional", "Friendly"])
    email = st.text_input("📩 Your Email (for PDF copy, optional)")
    submit = st.form_submit_button("✍️ Generate Reply")

if submit and review:
    with st.spinner("Generating AI-powered reply..."):
        prompt = f"""
You are a restaurant manager writing a {tone.lower()} reply to this review:
"{review}"

Be respectful, brand-positive, and professional. Keep it short and sweet.
"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200
            )
            reply = response.choices[0].message["content"]

            st.markdown("### ✅ Suggested Reply")
            st.success(reply)
            st.code(reply)

            increment_usage("review_reply_assistant")

            if email:
                send_email_with_pdf("Your Review Reply", email, reply)

        except Exception as e:
            st.error(f"AI Error: {e}")
else:
    if submit:
        st.warning("Please paste a review to generate a reply.")

st.info("""
🧠 *Note:* The insights provided by this tool are generated using AI and public data. While helpful, they may not reflect 100% accuracy or real-time changes. Always consult professionals before making critical decisions.
""")
