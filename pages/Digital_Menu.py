import streamlit as st
from utils import can_use_tool, increment_usage, send_email_with_pdf
# show_stripe_buttons removed temporarily

st.title("📄 Digital Menu Creator")

if can_use_tool("DigitalMenu"):
    with st.form("menu_form"):
        restaurant = st.text_input("Restaurant Name")
        email = st.text_input("📧 Your Email")
        dishes = st.text_area("🧾 Enter dishes and prices (one per line e.g., Pasta - ₹250)")

        submitted = st.form_submit_button("Generate Menu")

        if submitted and dishes:
            increment_usage("DigitalMenu")
            menu = f"{restaurant} Menu\n\n{dishes}"
            st.code(menu)
            send_email_with_pdf("Your Digital Menu", email, menu)
