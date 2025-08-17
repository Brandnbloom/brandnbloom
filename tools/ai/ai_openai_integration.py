# Simple OpenAI integration for caption suggestions.
# Requires OPENAI_API_KEY in env.
import os
try:
    import openai
except Exception:
    openai = None

def suggest_caption(prompt, max_tokens=60):
    if not openai:
        return {'error':'openai library not installed'}
    key = os.environ.get('OPENAI_API_KEY')
    if not key:
        return {'error':'OPENAI_API_KEY not set'}
    openai.api_key = key
    resp = openai.ChatCompletion.create(
        model='gpt-4o-mini',  # placeholder; use available model
        messages=[{'role':'user','content': prompt}],
        max_tokens=max_tokens,
        temperature=0.7
    )
    text = resp['choices'][0]['message']['content']
    return {'caption': text}
