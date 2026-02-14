import streamlit as st
import openai
import os
from utils import can_use_tool, increment_usage, send_email_with_pdf

# API setup
openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"  # Only if using OpenRouter

st.title("💬 Review Reply Assistant – Batch Mode")

st.markdown("""
Respond to **one or many customer reviews** with empathy and professionalism.  
Paste multiple reviews separated by `---` and get a ready-to-use reply for each.
""")

# Usage control
if not can_use_tool("review_reply_assistant"):
    st.error("⚠️ You've reached the usage limit for this tool.")
    st.stop()

with st.form("review_reply_form"):
    review_input = st.text_area("📝 Customer Review(s)", placeholder="""
Example (multiple reviews):
"Food was amazing but service was a bit slow."
---
"Loved the ambience, but the pasta was bland."
""", height=250)
    tone = st.selectbox("🎭 Tone of Response", ["Grateful", "Apologetic", "Witty", "Professional", "Friendly"])
    email = st.text_input("📩 Your Email (for PDF copy, optional)")
    submit = st.form_submit_button("✍️ Generate Reply")

if submit and review_input.strip():
    with st.spinner("Generating AI-powered reply..."):
        reviews = [r.strip() for r in review_input.split("---") if r.strip()]

        all_replies = []
        for idx, review in enumerate(reviews, start=1):
            prompt = f"""
You are a restaurant manager writing a {tone.lower()} reply to this customer review:
"{review}"

Be respectful, brand-positive, and professional. Keep it short and sweet.
"""
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=200
                )

                if response and response.choices:
                    reply = response.choices[0].message["content"].strip()
                else:
                    reply = "⚠️ Could not generate a reply."

                all_replies.append(f"**Review {idx}:** {review}\n**Reply:** {reply}\n")

            except Exception as e:
                all_replies.append(f"**Review {idx}:** {review}\n**Error:** {e}\n")

        # Display replies
        st.markdown("### ✅ Suggested Replies")
        for reply_block in all_replies:
            st.markdown(reply_block)
            st.markdown("---")

        increment_usage("review_reply_assistant")

        if email:
            send_email_with_pdf("Your Review Replies", email, "\n\n".join(all_replies))

else:
    if submit:
        st.warning("Please paste at least one review to generate a reply.")

st.info("""
🧠 *Note:* The insights provided by this tool are generated using AI and public data. 
While helpful, they may not reflect 100% accuracy or real-time changes. 
Always consult professionals before making critical decisions.
""")
