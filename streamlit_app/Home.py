import streamlit as st
from streamlit_app import Register, Login, Dashboard

st.title("Brand n Bloom SaaS")

menu = ["Home", "Register", "Login", "Dashboard"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Home":
    st.subheader("Welcome to Brand n Bloom SaaS")
    st.write("Manage your SEO, Ads, Social & more from one platform.")
elif choice == "Register":
    Register
elif choice == "Login":
    Login
elif choice == "Dashboard":
    Dashboard
