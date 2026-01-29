import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_insight(summary):

    prompt = f"""
    You are a marketing data analyst.

    Explain this data simply with business recommendations:

    {summary}

    Give 3 bullet points.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user","content":prompt}],
        temperature=0.4
    )

    return response.choices[0].message.content
