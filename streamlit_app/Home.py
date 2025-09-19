import streamlit as st
from streamlit_app import Register, Login, Dashboard, SEOTools

menu = ["Home", "Register", "Login", "Dashboard", "SEO Tools", "Social Tools", "Ads Tools"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Ads Tools":
    AdsTools

if choice == "Social Tools":
    SocialTools

if choice == "Home":
    st.subheader("Welcome to Brand n Bloom SaaS")
elif choice == "Register":
    Register
elif choice == "Login":
    Login
elif choice == "Dashboard":
    Dashboard
elif choice == "SEO Tools":
    SEOTools
