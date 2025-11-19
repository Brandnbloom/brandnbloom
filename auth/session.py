import streamlit as st
from typing import Optional, Dict, Any

def set_user(user_row):
    st.session_state["user"] = dict(user_row) if user_row else None

def get_user() -> Optional[Dict[str, Any]]:
    return st.session_state.get("user")

def is_logged_in() -> bool:
    return "user" in st.session_state

def require_login():
    if not is_logged_in():
        st.warning("Please log in to access this page.")
        st.stop()

def logout():
    st.session_state.pop("user", None)

def require_role(role: str):
    user = get_user()
    if not user or user.get("role") != role:
        st.error("Access denied.")
        st.stop()
