import streamlit as st
import openai
import os
from PIL import Image
import io
from utils import can_use_tool, increment_usage, send_email_with_pdf
# show_stripe_buttons removed temporarily

openai.api_key = os.getenv("OPENROUTER_API_KEY")

st.title("🎨 Visual Brand Audit")

st.markdown("""
Upload your brand’s Instagram feed or website screenshots, and let our AI review the *aesthetic consistency, tone, color palette*, and how “on-brand” your visuals feel.

Perfect for designers, restaurateurs, and marketers who care about their visual voice.
""")

# Usage control
if not can_use_tool("visual_brand_audit"):
    show_stripe_buttons()
    st.stop()

# Form
with st.form("audit_form"):
    uploaded_files = st.file_uploader("📷 Upload screenshots (max 3)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    email = st.text_input("📩 Email to receive full visual report (optional)")
    submit = st.form_submit_button("🪄 Analyze Visuals")

if submit and uploaded_files:
    with st.spinner("Analyzing visual style..."):
        descriptions = []
        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file)
            buf = io.BytesIO()
            image.save(buf, format="PNG")
            byte_data = buf.getvalue()
            base64_image = base64.b64encode(byte_data).decode("utf-8")

            # Send image description to GPT
            prompt = f"""
You are a brand designer AI. Analyze this image for:
- Brand tone (fun, modern, luxurious, minimal, etc.)
- Color psychology
- Visual consistency (fonts, spacing, grid, etc.)
- Moodboard feel
Be short (max 4 bullet points).
"""
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4-vision-preview",
                    messages=[
                        {"role": "system", "content": "You analyze visuals and brand moodboards."},
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                            ]
                        }
                    ],
                    max_tokens=300
                )
                result = response.choices[0].message["content"]
                descriptions.append(result)

            except Exception as e:
                st.error(f"AI error: {e}")
                continue

        final_output = "\n\n---\n\n".join(descriptions)
        st.markdown("### 🖌️ AI Visual Review:")
        st.markdown(final_output)

        increment_usage("visual_brand_audit")

        if email:
            send_email_with_pdf("Your Visual Brand Audit", email, final_output)
else:
    if submit:
        st.warning("Please upload at least 1 image.")

st.info("""
🧠 *Note:* The insights provided by this tool are generated using AI and public data. While helpful, they may not reflect 100% accuracy or real-time changes. Always consult professionals before making critical decisions.
""")
