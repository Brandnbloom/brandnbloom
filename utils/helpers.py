# utils/helpers.py

import re
import unicodedata
import random
import string
from datetime import datetime, timedelta
from typing import Any, Dict


# ---------------------------------------------------------
# 1. Improved SLUGIFY (removes emojis + accents)
# ---------------------------------------------------------
def slugify(s: str) -> str:
    if not s:
        return ""
    # Remove emojis
    s = remove_emojis(s)

    # Normalize unicode (removes accents)
    s = unicodedata.normalize("NFKD", s)
    s = s.encode("ascii", "ignore").decode("ascii")

    # Convert to lowercase
    s = s.lower().strip()

    # Replace non-alphanumeric characters with "-"
    s = re.sub(r"[^a-z0-9]+", "-", s)

    # Remove leading/trailing dashes
    return s.strip("-")


# ---------------------------------------------------------
# 2. Remove emojis from any text
# ---------------------------------------------------------
def remove_emojis(s: str) -> str:
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # Emoticons
        "\U0001F300-\U0001F5FF"  # Symbols & pictographs
        "\U0001F680-\U0001F6FF"  # Transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # Flags
        "\U00002700-\U000027BF"  # Dingbats
        "\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub("", s)


# ---------------------------------------------------------
# 3. Safe filename (slugified + max length + timestamp)
# ---------------------------------------------------------
def safe_filename(name: str, extension: str = "") -> str:
    base = slugify(name)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    if extension and not extension.startswith("."):
        extension = "." + extension
    return f"{base}-{ts}{extension}"


# ---------------------------------------------------------
# 4. Random short ID (for reports, handles, etc.)
# ---------------------------------------------------------
def short_id(length: int = 8) -> str:
    chars = string.ascii_lowercase + string.digits
    return "".join(random.choice(chars) for _ in range(length))


# ---------------------------------------------------------
# 5. Email validator
# ---------------------------------------------------------
def is_valid_email(email: str) -> bool:
    if not email:
        return False
    return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email))


# ---------------------------------------------------------
# 6. Dict deep merge (right side overrides left)
# ---------------------------------------------------------
def deep_merge(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
    result = a.copy()
    for key, value in b.items():
        if (
            key in result
            and isinstance(result[key], dict)
            and isinstance(value, dict)
        ):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


# ---------------------------------------------------------
# 7. Date utilities
# ---------------------------------------------------------
def start_of_day(dt: datetime) -> datetime:
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)


def start_of_week(dt: datetime) -> datetime:
    return start_of_day(dt - timedelta(days=dt.weekday()))


def start_of_month(dt: datetime) -> datetime:
    return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def format_date(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d")


# ---------------------------------------------------------
# 8. String normalization
# ---------------------------------------------------------
def clean_text(s: str) -> str:
    """Remove duplicate spaces, trim, remove emojis."""
    s = remove_emojis(s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


# ---------------------------------------------------------
# 9. Snake_case ↔ camelCase
# ---------------------------------------------------------
def to_camel(s: str) -> str:
    parts = s.split("_")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])


def to_snake(s: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", s).lower()
