import streamlit as st
from utils.ui import inject_css, dark_mode_toggle
from ai_tools.menu_pricing import suggest_prices

inject_css(); dark_mode_toggle()
st.title("🍽️ Menu Pricing Optimization")
cost = st.number_input("Cost to make (₹)", value=100.0, step=1.0)
margin = st.slider("Desired margin (%)", 10, 80, 40)
comp = st.number_input("Competitor price (optional)", value=0.0)
if st.button("Suggest"):
    comp_val = comp if comp>0 else None
    res = suggest_prices(cost, margin, comp_val)
    st.json(res)
