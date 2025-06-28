import streamlit as st
import openai
import os
from utils import can_use_tool, increment_usage, send_email_with_pdf, show_stripe_buttons

openai.api_key = os.getenv("OPENROUTER_API_KEY")

st.title("🔍 AI Competitor Snapshot")

st.markdown("""
Enter Instagram usernames or website URLs of up to *3 competing restaurants*, and let our AI compare them for:
- Content strategy
- Posting style
- Hashtag strategy
- Frequency
- Brand personality clues

You'll receive a downloadable snapshot report!
""")

# Usage limiter
if not can_use_tool("competitor_snapshot"):
    show_stripe_buttons()
    st.stop()

with st.form("snapshot_form"):
    comp1 = st.text_input("🍽️ Competitor 1 (IG handle or website)")
    comp2 = st.text_input("🍽️ Competitor 2 (optional)")
    comp3 = st.text_input("🍽️ Competitor 3 (optional)")
    email = st.text_input("📩 Your Email (for report)")
    submit = st.form_submit_button("🔎 Analyze Competitors")

if submit and comp1:
    with st.spinner("Analyzing competitive landscape..."):

        competitors = [comp for comp in [comp1, comp2, comp3] if comp.strip()]
        names = "\n".join([f"- {c}" for c in competitors])

        prompt = f"""
You are a restaurant marketing strategist.

Compare the following competitors and summarize:
- Posting frequency
- Type of content (reels, offers, behind-the-scenes, food shots, etc.)
- Hashtag usage
- Brand vibe/tone
- Any standout strengths or weaknesses

Competitors:
{names}
Use max 3 bullet points per brand. Then give 3 improvement suggestions for the user.
"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800
            )

            output = response.choices[0].message["content"]
            st.markdown("### 📊 AI Competitor Snapshot")
            st.markdown(output)

            increment_usage("competitor_snapshot")

            if email:
                send_email_with_pdf("Your Competitor Snapshot Report", email, output)

        except Exception as e:
            st.error(f"AI error: {e}")

else:
    if submit:
        st.warning("Please enter at least one competitor.")
