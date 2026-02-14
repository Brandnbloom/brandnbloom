# Simple consumer behavior questionnaire engine.
# Stores questions and computes simple persona & recommendations.
QUESTIONS = [
    {"id":"q1","q":"Who is your primary customer? (Age, gender, occupation)","type":"text"},
    {"id":"q2","q":"What problem does your product/service solve?","type":"text"},
    {"id":"q3","q":"Preferred platform for discovery? (Instagram/Facebook/Google)","type":"choice","choices":["Instagram","Facebook","Google","Offline"]},
    {"id":"q4","q":"Price sensitivity? (Low/Medium/High)","type":"choice","choices":["Low","Medium","High"]},
    {"id":"q5","q":"Frequency of purchase? (One-time/Monthly/Weekly)","type":"choice","choices":["One-time","Monthly","Weekly"]},
]

def run_questionnaire(answers: dict) -> dict:
    # answers: {q1: val, q2: val, ...}
    persona = {}
    # Infer channel focus
    channel = answers.get("q3","Instagram")
    if channel == "Instagram":
        persona["channel_focus"] = "Visual-first; prioritize Reels & Stories"
    elif channel == "Google":
        persona["channel_focus"] = "SEO & long-form content"
    else:
        persona["channel_focus"] = "Community & local outreach"
    # Price strategy
    ps = answers.get("q4","Medium")
    persona["price_strategy"] = "Premium positioning" if ps=="Low" else "Value pricing" if ps=="High" else "Competitive pricing"
    # Purchase frequency
    freq = answers.get("q5","One-time")
    persona["retention_recos"] = ["Loyalty program", "Email nurture sequence"] if freq in ["Monthly","Weekly"] else ["Offer follow-ups & referral discounts"]
    # Custom recos
    persona["quick_recos"] = [
        "Run 2 Reels/week focusing on customer pain points",
        "Use user-generated content (UGC) to build trust"
    ]
    return {"persona": persona, "summary": f"Detected channel: {channel}; price sensitivity: {ps}; frequency: {freq}"}
