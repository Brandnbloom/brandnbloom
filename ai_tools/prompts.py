import streamlit as st
import pandas as pd

sample_data = pd.DataFrame({
    "customer_id": [1,2,3],
    "recency": [10, 20, 5],
    "frequency": [3, 1, 5],
    "monetary": [200, 150, 500],
    "churn": [0, 1, 0]
})

st.download_button(
    "📥 Download Sample Data",
    data=sample_data.to_csv(index=False),
    file_name="sample_data.csv",
    mime="text/csv"
)

PROMPTS = {
    "Social Media Caption": [
        "Write a catchy Instagram caption for {brand} promoting {product}.",
        "Create 3 engaging Twitter posts for {brand} about {topic}.",
    ],
    "Email Marketing": [
        "Draft a high-conversion email for {brand} announcing {product}.",
        "Write a follow-up email for leads interested in {service}.",
    ],
    "Ad Copy": [
        "Create a short ad copy for {brand} targeting {audience}.",
        "Generate Google ad headlines for {product}.",
    ],
    "Content Ideas": [
        "List 5 blog post ideas for {brand} in the niche of {topic}.",
        "Suggest 3 YouTube video ideas for {brand} about {product}.",
    ],
}

def run():
    st.markdown("## 📝 AI Prompt Generator")
    st.markdown(
        "Select a category, fill in the fields, and generate marketing prompts."
    )

    category = st.selectbox("Choose category", list(PROMPTS.keys()))
    st.markdown(f"### Example Prompts for {category}")
    for i, prompt in enumerate(PROMPTS[category]):
        st.code(f"{i+1}. {prompt}")

    # Dynamic inputs for placeholders
    placeholders = {}
    for placeholder in ["brand", "product", "topic", "service", "audience"]:
        placeholders[placeholder] = st.text_input(f"Enter {placeholder} (optional)")

    if st.button("Generate Prompts"):
        results = []
        for template in PROMPTS[category]:
            prompt_text = template
            for key, val in placeholders.items():
                if val.strip():
                    prompt_text = prompt_text.replace(f"{{{key}}}", val)
            results.append(prompt_text)

        st.markdown("### ✅ Generated Prompts")
        for p in results:
            st.code(p)
