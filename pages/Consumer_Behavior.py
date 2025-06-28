import streamlit as st
from utils import can_use_tool, increment_usage, send_email_with_pdf, show_stripe_buttons
st.title("🧠 DinePsych – Consumer Behavior Insights")

if can_use_tool("DinePsych"):
    with st.form("dinepsych_form"):
        cuisine = st.selectbox("Cuisine Type", ["Indian", "Italian", "Chinese", "Mexican"])
        avg_bill = st.slider("Average Bill Size (in ₹)", 100, 3000)
        meal_time = st.selectbox("Peak Meal Time", ["Breakfast", "Lunch", "Dinner"])
        email = st.text_input("Your Email")

        submitted = st.form_submit_button("Generate Insight")

        if submitted:
            increment_usage("DinePsych")

            # Simulated insight
            insight = f'''
            🍽️ Based on your inputs:
            - Cuisine: {cuisine}
            - Avg Bill: ₹{avg_bill}
            - Peak Time: {meal_time}

            🧠 Behavioral Insight:
            - Customers prefer shared platters.
            - Loyalty increases with ambient music & personalized service.
            '''

            st.code(insight)
            send_email_with_pdf("Your DinePsych Report", email, insight)
