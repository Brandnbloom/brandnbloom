import streamlit as st

def require_login():
    if "user" not in st.session_state:
        st.warning("Please log in to access this page.")
        st.stop()

def set_user(user_row):
    st.session_state["user"] = dict(user_row) if user_row else None

def get_user():
    return st.session_state.get("user")
