import streamlit as st
from db.models import get_user_by_email
from auth.security import verify_password
from auth.session import set_user

st.title("🔐 Login")

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login"):
    row = get_user_by_email(email)
    if row and verify_password(password, row["password_hash"]):
        set_user(row)
        st.success("Logged in! Use the sidebar to access the Dashboard.")
    else:
        st.error("Invalid credentials")
