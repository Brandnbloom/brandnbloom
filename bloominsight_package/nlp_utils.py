from textblob import TextBlob
import re

def summarize_caption(caption, max_len=140):
    if not caption:
        return ""
    tb = TextBlob(caption)
    s = str(tb.sentences[0]) if tb.sentences else caption[:max_len]
    return s[:max_len]

def suggest_hashtags(caption, top_n=5):
    # naive hashtag extractor and suggestion from caption keywords
    words = re.findall(r'\w+', caption.lower())
    stop = set(['the','and','for','with','this','that','from','are','into','your','you'])
    keywords = [w for w in words if w not in stop and len(w)>3]
    suggestions = []
    for k in keywords[:top_n]:
        suggestions.append(f"#{k}")
    return suggestions
