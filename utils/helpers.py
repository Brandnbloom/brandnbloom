# utils/helpers.py
import re
def slugify(s: str):
    return re.sub(r'[^a-z0-9]+','-', s.lower()).strip('-')
