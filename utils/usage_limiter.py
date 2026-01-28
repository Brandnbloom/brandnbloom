import streamlit as st

FREE_LIMIT = 3

def init_usage():
    """
    Initialize usage counter.
    """
    if "tool_usage_count" not in st.session_state:
        st.session_state.tool_usage_count = 0


def can_use_tool():
    """
    Check if user can still use tools.
    """
    init_usage()
    return st.session_state.tool_usage_count < FREE_LIMIT


def increment_usage():
    """
    Increase usage count after a tool is run.
    """
    init_usage()
    st.session_state.tool_usage_count += 1


def show_limit_message():
    """
    Show upgrade message.
    """
    st.warning("🚫 Free limit reached (3 tools used). Upgrade to continue.")
    st.stop()
