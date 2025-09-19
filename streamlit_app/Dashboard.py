import streamlit as st
import requests
from .config import BACKEND_URL

st.title("Brand n Bloom Dashboard")

if "token" not in st.session_state:
    st.warning("Please login first.")
    st.stop()

st.write("Welcome to your dashboard!")

if st.button("Upgrade Plan / Checkout"):
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    response = requests.post(f"{BACKEND_URL}/billing/create-checkout-session", headers=headers)
    if response.status_code == 200:
        checkout_url = response.json()["checkout_url"]
        st.markdown(f"[Click here to pay]({checkout_url})")
    else:
        st.error("Error creating checkout session.")
