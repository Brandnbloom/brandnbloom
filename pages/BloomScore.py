import streamlit as st
import openai
import os
from utils import can_use_tool, increment_usage, send_email_with_pdf, show_stripe_buttons

openai.api_key = os.getenv("OPENROUTER_API_KEY")

st.title("🌸 BloomScore – Brand Health Checker")

st.markdown("""
Enter your Instagram and Website to get an AI-powered report on your brand’s current health — design, engagement, SEO, storytelling, and more.
""")

# Usage control
if not can_use_tool("bloomscore"):
    show_stripe_buttons()
    st.stop()

# Form
with st.form("bloomscore_form"):
    insta = st.text_input("📷 Instagram handle or URL", placeholder="e.g. https://instagram.com/yourbrand")
    website = st.text_input("🌐 Website URL", placeholder="e.g. https://yourbrand.com")
    email = st.text_input("📩 Email (to receive PDF report)")
    submit = st.form_submit_button("🚀 Analyze My Brand")

if submit and (insta or website):
    with st.spinner("Analyzing..."):
        prompt = f"""
You are a brand marketing strategist. Analyze the following brand based on their Instagram and website. 
URL: {website}
Instagram: {insta}

Evaluate:
1. Visual Branding & Tone Consistency
2. Engagement Quality
3. Website speed/design/responsiveness
4. SEO presence (based on public site info)
5. Content gaps and recommendations

Give the analysis in short bullet points (under 100 words per point).
Then give a final 'BloomScore' (out of 100) and a 1-line summary.
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            result = response.choices[0].message["content"]

            st.success("✅ Brand Report Generated!")
            st.markdown(result)

            increment_usage("bloomscore")

            if email:
                send_email_with_pdf("Your BloomScore Report", email, result)

        except Exception as e:
            st.error(f"AI Error: {e}")
else:
    if submit:
        st.warning("Please enter at least one valid input.")
