import streamlit as st
from utils.ui import inject_css, dark_mode_toggle
from ai_tools.loyalty import points_for_amount, update_balance, recommend_reward

inject_css(); dark_mode_toggle()
st.title("🎁 Customer Loyalty AI")
balance = st.number_input("Existing points balance", value=0, step=1)
amount = st.number_input("Purchase amount", value=250.0, step=1.0)
if st.button("Apply purchase"):
    new_bal = update_balance(balance, amount)
    rec = recommend_reward(new_bal)
    st.success(f'New balance: {new_bal} points — Recommended reward: {rec}')
