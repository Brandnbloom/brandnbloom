import streamlit as st
import openai

st.set_page_config(page_title="DinePsych AI - Brand n Bloom", layout="wide")

st.title("🧠 DinePsych AI — Behavioral Marketing Insights")

st.markdown("Let our AI analyze your ideal customer behavior & psychology to refine your restaurant's strategy.")

# --- Input Form ---
with st.form("behavior_form"):
    restaurant_type = st.selectbox("Type of Restaurant", ["Fine Dining", "Cafe", "Quick Service", "Cloud Kitchen", "Bar"])
    audience = st.text_input("Target Audience (e.g. Gen Z, Office-goers, Parents)")
    location = st.text_input("City / Area")
    aov = st.text_input("Avg Order Value (₹)", placeholder="e.g. 700")
    peak_hours = st.text_input("Peak Hours (e.g. 12-2pm, 7-10pm)")
    common_feedback = st.text_area("Common Customer Feedback Themes (Optional)")

    submitted = st.form_submit_button("Generate Insights")

if submitted:
    with st.spinner("Analyzing customer psychology..."):
        prompt = f"""
You are a behavioral marketing strategist for restaurants.

Based on the following:

- Type of restaurant: {restaurant_type}
- Audience: {audience}
- Location: {location}
- Average order value: ₹{aov}
- Peak hours: {peak_hours}
- Feedback themes: {common_feedback}

Generate an in-depth analysis:
1. Ideal customer persona & emotional drivers
2. Marketing tone & style that appeals
3. Visual aesthetics for ads/menu
4. Instagram content suggestions
5. Promotions that would convert
"""
import os
        # Replace with your OpenAI key
        openai.api_key = os.environ("OPENAI_API_KEY")

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You're an expert in consumer psychology and restaurant marketing."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )

            output = response["choices"][0]["message"]["content"]
            st.success("✅ Insights Ready!")
            st.markdown(f"### 📋 Result:\n\n{output}")

        except Exception as e:
            st.error(f"Error: {e}")
