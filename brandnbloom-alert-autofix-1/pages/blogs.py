import streamlit as st

st.set_page_config(page_title="📝 Blogs", layout="wide")

st.title("📝 Our Latest Blogs")

# Example blog list
blogs = [
    {
        "title": "🌼 How to Build a Blooming Brand Identity",
        "summary": "Discover simple branding techniques that help small businesses bloom in crowded markets.",
        "url": "https://yourblog.com/brand-identity"
    },
    {
        "title": "📊 Why Data-Driven Design Wins Every Time",
        "summary": "We discuss the psychology and numbers behind color, font, and UX choices that convert.",
        "url": "https://yourblog.com/data-design"
    },
    {
        "title": "🧠 AI Tools for Restaurants: The BloomStack Suite",
        "summary": "Explore how restaurants are using AI tools like BloomScore, DinePsych, and Review Reply.",
        "url": "https://yourblog.com/ai-tools-restaurants"
    }
]

for blog in blogs:
    with st.container():
        st.markdown(f"### [{blog['title']}]({blog['url']})")
        st.markdown(f"<div style='color: #666;'>{blog['summary']}</div>", unsafe_allow_html=True)
        st.markdown("---")
