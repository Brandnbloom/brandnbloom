import streamlit as st

FREE_LIMIT = 3

def can_use_tool():
    if "usage_count" not in st.session_state:
        st.session_state.usage_count = 0

    return st.session_state.usage_count < FREE_LIMIT


def increment_usage():
    st.session_state.usage_count += 1


def usage_banner():
    remaining = FREE_LIMIT - st.session_state.get("usage_count", 0)

    if remaining > 0:
        st.info(f"🟢 Free uses left: {remaining}")
    else:
        st.error("🚫 Free limit reached. Please upgrade to continue.")
