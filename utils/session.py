import streamlit as st
import uuid

def get_user_id():
    """
    Returns a persistent user ID for the session.
    """
    if "user_id" not in st.session_state:
        st.session_state.user_id = str(uuid.uuid4())
    return st.session_state.user_id

