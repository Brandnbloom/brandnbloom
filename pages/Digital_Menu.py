import streamlit as st
import openai
import os
from utils import can_use_tool, increment_usage, send_email_with_pdf
# show_stripe_buttons removed temporarily

openai.api_key = os.getenv("OPENROUTER_API_KEY")

st.title("🍽️ Digital Menu Creator")

st.markdown("""
Build a modern restaurant menu with the help of AI.  
Just enter dish names, categories, and our AI will craft a clean, classy menu for print or digital use.
""")

# Usage control
if not can_use_tool("digital_menu_creator"):
    show_stripe_buttons()
    st.stop()

# Form
with st.form("menu_form"):
    st.write("✏️ Enter dishes and their categories below:")
    user_input = st.text_area("Menu Input", placeholder="""
Example:
Starters:
- Veg Spring Rolls
- Chicken Tikka

Main Course:
- Butter Chicken
- Paneer Tikka Masala

Desserts:
- Gulab Jamun
- Chocolate Mousse
    """, height=300)

    email = st.text_input("📩 Email for downloadable PDF (optional)")
    submit = st.form_submit_button("🎨 Generate Menu")

if submit and user_input.strip():
    with st.spinner("Creating your AI-powered menu..."):
        prompt = f"""
You are a modern menu designer. Create a clean, well-structured restaurant menu based on the input below.
Use bold dish names, short 1-line descriptions (if missing), and professional formatting.
Input:\n{user_input}
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            ai_menu = response.choices[0].message["content"]

            st.markdown("### 📋 Your AI-Generated Menu")
            st.markdown(ai_menu)

            increment_usage("digital_menu_creator")

            if email:
                send_email_with_pdf("Your Restaurant Menu", email, ai_menu)

        except Exception as e:
            st.error(f"AI Error: {e}")
else:
    if submit:
        st.warning("Please enter dish data to proceed.")

st.info("""
🧠 *Note:* The insights provided by this tool are generated using AI and public data. While helpful, they may not reflect 100% accuracy or real-time changes. Always consult professionals before making critical decisions.
""")
