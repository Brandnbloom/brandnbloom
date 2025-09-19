import streamlit as st
import requests
from .config import BACKEND_URL

st.title("Brand n Bloom - Register")

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Register"):
    if email and password:
        response = requests.post(f"{BACKEND_URL}/auth/register", json={"email": email, "password": password})
        if response.status_code == 200:
            st.success("Registered successfully! Token saved locally.")
            st.session_state["token"] = response.json()["access_token"]
        else:
            st.error(response.json().get("detail"))
    else:
        st.warning("Please enter email and password")
