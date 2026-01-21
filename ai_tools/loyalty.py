import streamlit as st

# -------------------------------------------------
# LOYALTY ENGINE
# -------------------------------------------------
TIERS = ["Bronze", "Silver", "Gold", "Platinum"]


def calculate_points(actions: dict) -> int:
    """
    actions: dict containing number of actions, e.g.
    {'purchase': 5, 'referral': 2, 'review': 3}
    """
    points = 0
    points += actions.get("purchase", 0) * 10
    points += actions.get("referral", 0) * 20
    points += actions.get("review", 0) * 5
    return points


def determine_tier(total_points: int) -> str:
    if total_points >= 200:
        return "Platinum"
    elif total_points >= 100:
        return "Gold"
    elif total_points >= 50:
        return "Silver"
    return "Bronze"


# -------------------------------------------------
# STREAMLIT UI
# -------------------------------------------------
def run():
    st.markdown("## 🎁 Loyalty Program Designer")
    st.markdown(
        "Design loyalty programs and calculate user points & tiers in real time."
    )

    st.divider()

    st.markdown("### Define User Actions")
    purchases = st.number_input("Number of purchases", min_value=0, value=0)
    referrals = st.number_input("Number of referrals", min_value=0, value=0)
    reviews = st.number_input("Number of reviews", min_value=0, value=0)

    if st.button("Calculate Loyalty"):
        actions = {
            "purchase": purchases,
            "referral": referrals,
            "review": reviews,
        }

        total_points = calculate_points(actions)
        tier = determine_tier(total_points)

        st.divider()
        st.markdown(f"### 🏆 Total Points: {total_points}")
        st.markdown(f"### 🌟 Current Tier: {tier}")

        # Optional suggestions
        st.markdown("### Tips to Level Up:")
        if tier != "Platinum":
            st.markdown(f"- Make {TIERS[TIERS.index(tier)+1]} tier by earning more points!")
