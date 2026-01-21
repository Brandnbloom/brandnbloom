import streamlit as st
import random

def generate_mock_profile(handle: str):
    """Generate a fake social media profile with stats."""
    followers = random.randint(100, 50000)
    following = random.randint(50, 2000)
    posts = random.randint(10, 1000)
    engagement_rate = round(random.uniform(0.01, 0.2), 3)  # 1%–20%
    bio = f"This is a mock profile for {handle}"
    profile_picture = "https://via.placeholder.com/150"

    return {
        "username": handle,
        "followers": followers,
        "following": following,
        "posts": posts,
        "engagement_rate": engagement_rate,
        "bio": bio,
        "profile_picture": profile_picture
    }

def run():
    st.markdown("## 👤 Profile Mock")
    st.markdown(
        "Simulate a social media profile to test tools like BloomScore, "
        "Consumer Behavior, and analytics."
    )

    handle = st.text_input("Enter profile handle", "brandnbloom")

    if st.button("Generate Mock Profile"):
        profile = generate_mock_profile(handle)

        st.image(profile["profile_picture"], width=150)
        st.markdown(f"**Username:** {profile['username']}")
        st.markdown(f"**Followers:** {profile['followers']}")
        st.markdown(f"**Following:** {profile['following']}")
        st.markdown(f"**Posts:** {profile['posts']}")
        st.markdown(f"**Engagement Rate:** {profile['engagement_rate']*100:.2f}%")
        st.markdown(f"**Bio:** {profile['bio']}")
