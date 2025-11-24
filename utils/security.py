# utils/security.py

import os
import secrets
import hashlib
import time
from typing import Optional, Dict
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext

# ------------------------------------------------------------
# Setup
# ------------------------------------------------------------

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("JWT_SECRET", "supersecretjwt")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day


# ------------------------------------------------------------
# Password Hashing
# ------------------------------------------------------------

def hash_password(password: str) -> str:
    """Hashes a plain password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies whether a password matches its hash."""
    return pwd_context.verify(plain_password, hashed_password)


# ------------------------------------------------------------
# JWT Handling
# ------------------------------------------------------------

def create_jwt_token(data: dict, expires_minutes: Optional[int] = None) -> str:
    """Creates a JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=expires_minutes or ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_jwt_token(token: str) -> Optional[dict]:
    """Verifies + decodes a JWT token."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None


# ------------------------------------------------------------
# Token Blacklist (Optional)
# ------------------------------------------------------------

# {token: expiry_timestamp}
TOKEN_BLACKLIST: Dict[str, float] = {}


def blacklist_token(token: str, ttl_minutes: int = 1440):
    """Blacklist a token after logout."""
    TOKEN_BLACKLIST[token] = time.time() + ttl_minutes * 60


def is_token_blacklisted(token: str) -> bool:
    """Check if token is blacklisted."""
    expiry = TOKEN_BLACKLIST.get(token)
    if not expiry:
        return False
    if time.time() > expiry:
        del TOKEN_BLACKLIST[token]
        return False
    return True


# ------------------------------------------------------------
# API Key Generator
# ------------------------------------------------------------

def generate_api_key() -> str:
    """Generates a secure random API key."""
    return secrets.token_hex(32)


# ------------------------------------------------------------
# CSRF Token Generator
# ------------------------------------------------------------

def generate_csrf_token() -> str:
    """Creates a CSRF token using SHA256."""
    raw = secrets.token_urlsafe(32)
    return hashlib.sha256(raw.encode()).hexdigest()


# ------------------------------------------------------------
# Simple Rate Limit Helper
# ------------------------------------------------------------

RATE_LIMIT_STORE: Dict[str, list] = {}  # {ip: [timestamps]}

def is_rate_limited(key: str, limit: int = 10, seconds: int = 60) -> bool:
    """
    Basic rate limiting:
      limit = number of requests
      seconds = per time window
    """
    now = time.time()
    if key not in RATE_LIMIT_STORE:
        RATE_LIMIT_STORE[key] = []

    # Remove old requests
    RATE_LIMIT_STORE[key] = [
        ts for ts in RATE_LIMIT_STORE[key] if now - ts < seconds
    ]

    # Check limit
    if len(RATE_LIMIT_STORE[key]) >= limit:
        return True

    # Record new request
    RATE_LIMIT_STORE[key].append(now)
    return False
