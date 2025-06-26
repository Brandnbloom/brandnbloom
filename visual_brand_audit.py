import streamlit as st

st.title("🎨 Visual Brand Audit")

st.markdown("Upload your brand's screenshot to get feedback.")

uploaded_file = st.file_uploader("Upload Instagram or website screenshot")

if uploaded_file:
    st.image(uploaded_file, use_column_width=True)
    st.success("Here’s what we see:")
    st.write("🟢 Consistent brand tone\n🔴 Low contrast in visuals\n🟡 Improve color harmony")
