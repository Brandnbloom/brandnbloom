import streamlit as st
import json

st.set_page_config(page_title="🔒 Admin - Usage Dashboard")

st.title("🔒 Admin Dashboard – Brand n Bloom")

try:
    with open("usage.json", "r") as f:
        data = json.load(f)

    st.write(f"📊 Total Users: {len(data)}")

    for email, count in data.items():
        st.markdown(f"- **{email}** → {count} uses")

except Exception as e:
    st.error(f"Could not load usage data: {e}")
