import streamlit as st, json, pathlib
from utils.ui import inject_css, dark_mode_toggle

inject_css(); dark_mode_toggle()
st.title("💰 Pricing")

data = json.loads(pathlib.Path("branding.json").read_text(encoding="utf-8"))
cols = st.columns(3, gap="large")
for idx, plan in enumerate(data.get("pricing", [])):
    with cols[idx]:
        st.markdown(f"#### {plan['plan']}")
        st.markdown(f"**{plan['price']}**")
        st.write("---")
        for f in plan["features"]:
            st.write("✅", f)
        st.write("")
        st.button("Choose", key=f"plan_{plan['plan']}")
