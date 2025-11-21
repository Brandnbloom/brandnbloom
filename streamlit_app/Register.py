import streamlit as st
import requests
from .config import BACKEND_URL

st.title("Brand n Bloom - Register")

# --- If user is already logged in ---
if "token" in st.session_state:
    st.success("You are already logged in!")
    st.markdown("Go to your **Dashboard** from the sidebar.")
    st.stop()

# --- Registration Form ---
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Register"):
    if not email or not password:
        st.warning("Please enter both email and password.")
        st.stop()

    try:
        response = requests.post(
            f"{BACKEND_URL}/auth/register",
            json={"email": email, "password": password},
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            st.session_state["token"] = data["access_token"]
            st.success("🎉 Registration successful! You are now logged in.")
            st.experimental_rerun()  # Auto-redirect
        else:
            error_msg = response.json().get("detail", "Registration failed.")
            st.error(error_msg)

    except Exception as e:
        st.error(f"Unable to connect to server: {e}")
