# brandnbloom/ai_tools/prompts.py

CAPTION_PROMPT = """
You are a brand-savvy social media copywriter.
Write a short, catchy Instagram caption for:
{context}

Tone: friendly, GenZ, growth-minded.
Include a clear CTA.
Max 120 words.
"""

HASHTAG_PROMPT = """
Suggest 12 relevant, non-spammy hashtags for:
{context}

Audience: small business owners & creators.
Mix: high-volume + mid-tier + long-tail.
Avoid generic spam hashtags.
Return as a clean list, no numbering.
"""
