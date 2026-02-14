import streamlit as st
from db.models import get_user_by_email, create_user
from auth.security import hash_password

st.title("🆕 Signup")

name = st.text_input("Full Name")
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Create account"):
    if get_user_by_email(email):
        st.error("Email already registered.")
    else:
        uid = create_user(email, name, hash_password(password))
        st.success("Account created! Go to Login.")
