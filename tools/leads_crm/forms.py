# tools/leads_crm/forms.py

import streamlit as st
from .crm_db import create_lead

def show_forms_ui():
    st.title("Lead Form Builder & Quick Capture")

    st.write("Quickly capture leads from clients, forms, chats, and inquiries.")

    with st.form("lead_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone (optional)")
        source = st.selectbox(
            "Source",
            ["Landing Page", "Instagram", "Facebook Ads", "Google Ads", "Manual Entry"]
        )

        submit_btn = st.form_submit_button("Save Lead")

        if submit_btn:
            try:
                if not name.strip() or not email.strip():
                    st.warning("Name and Email are required.")
                    return

                lead = create_lead({
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "source": source
                })

                st.success(f"Lead saved successfully! Lead ID: {lead.id}")

            except Exception as e:
                st.error(f"Error: {str(e)}")

