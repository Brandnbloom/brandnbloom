import streamlit as st
from .crm_db import create_lead

def show_forms_ui():
    st.title("Lead Form Builder & Quick Capture")
    name = st.text_input("Name")
    email = st.text_input("Email")
    source = st.selectbox("Source", ["Landing Page","Instagram","Ads","Manual"])
    if st.button("Save Lead"):
        lead = create_lead({"name": name, "email": email, "source": source})
        st.success(f"Saved lead id {lead.id}")
