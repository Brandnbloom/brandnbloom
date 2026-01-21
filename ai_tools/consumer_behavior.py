import streamlit as st
from typing import List


def analyze_psychology(
    awareness_level: str,
    decision_stage: str,
    motivation: List[str],
    price_sensitivity: str,
    trust_level: str,
):
    insights = []
    recommendations = []

    # Awareness analysis
    if awareness_level == "Low":
        insights.append("Users are not fully aware of the problem or your solution.")
        recommendations.append("Focus on educational content and problem-awareness messaging.")

    elif awareness_level == "Medium":
        insights.append("Users are aware but still comparing options.")
        recommendations.append("Use comparison content, case studies, and social proof.")

    else:
        insights.append("Users are highly aware and solution-ready.")
        recommendations.append("Push strong CTAs, offers, and urgency-driven campaigns.")

    # Decision stage
    if decision_stage == "Researching":
        recommendations.append("Provide blogs, guides, FAQs, and explainer videos.")

    elif decision_stage == "Considering":
        recommendations.append("Highlight differentiators, testimonials, and guarantees.")

    else:
        recommendations.append("Simplify checkout and reduce friction to convert faster.")

    # Motivation
    if "Growth" in motivation:
        insights.append("Audience is growth-oriented and future-focused.")

    if "Security" in motivation:
        insights.append("Audience seeks stability, trust, and risk reduction.")

    if "Status" in motivation:
        insights.append("Audience is influenced by premium branding and authority.")

    # Price sensitivity
    if price_sensitivity == "High":
        recommendations.append("Use bundles, discounts, and value-driven messaging.")

    elif price_sensitivity == "Medium":
        recommendations.append("Anchor pricing with value justification.")

    else:
        recommendations.append("Premium pricing is acceptable for this audience.")

    # Trust
    if trust_level == "Low":
        recommendations.append("Add reviews, testimonials, certifications, and founder story.")

    elif trust_level == "Medium":
        recommendations.append("Reinforce trust with case studies and transparent pricing.")

    else:
        recommendations.append("Leverage loyalty programs and referrals.")

    return insights, recommendations


def run():
    st.markdown("## 🧠 Consumer Behavior Analysis")
    st.markdown(
        "Understand **why** your customers think, feel, and buy — "
        "based on real behavioral psychology."
    )

    st.divider()

    # =========================
    # USER INPUTS (LIVE)
    # =========================
    awareness_level = st.selectbox(
        "Customer Awareness Level",
        ["Low", "Medium", "High"],
        help="How aware is your audience about the problem and your solution?"
    )

    decision_stage = st.selectbox(
        "Decision Stage",
        ["Researching", "Considering", "Ready to Buy"],
        help="Where is your audience in the buying journey?"
    )

    motivation = st.multiselect(
        "Primary Motivations",
        ["Growth", "Security", "Status", "Convenience", "Cost-Saving"],
        help="What emotionally drives your customers?"
    )

    price_sensitivity = st.selectbox(
        "Price Sensitivity",
        ["High", "Medium", "Low"],
        help="How sensitive is your audience to pricing?"
    )

    trust_level = st.selectbox(
        "Trust Level",
        ["Low", "Medium", "High"],
        help="How much does your audience trust your brand right now?"
    )

    st.divider()

    # =========================
    # ANALYSIS
    # =========================
    if st.button("Analyze Consumer Behavior"):
        if not motivation:
            st.warning("Please select at least one motivation.")
            return

        insights, recommendations = analyze_psychology(
            awareness_level,
            decision_stage,
            motivation,
            price_sensitivity,
            trust_level,
        )

        st.markdown("### 🔍 Key Insights")
        for i in insights:
            st.write("•", i)

        st.markdown("### ✅ Strategic Recommendations")
        for r in recommendations:
            st.write("•", r)

        st.divider()

        st.info(
            "🔗 **Next step:** Connect real data sources like Google Analytics, "
            "Instagram Insights, CRM, and Search data to unlock advanced behavior analytics."
        )
