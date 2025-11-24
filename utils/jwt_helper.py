# utils/jwt_helper.py

from datetime import datetime, timedelta
from jose import jwt, JWTError, ExpiredSignatureError
import os
from dotenv import load_dotenv

load_dotenv()

# Environment variables
SECRET_KEY = os.getenv("JWT_SECRET", "fallback_dev_secret")
REFRESH_SECRET_KEY = os.getenv("REFRESH_JWT_SECRET", "fallback_refresh_secret")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24       # 1 day
REFRESH_TOKEN_EXPIRE_DAYS = 7               # 7 days


# ---------------------------------------------------------
# Create Access Token
# ---------------------------------------------------------
def create_access_token(data: dict, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ---------------------------------------------------------
# Create Refresh Token
# ---------------------------------------------------------
def create_refresh_token(data: dict, expires_days: int = REFRESH_TOKEN_EXPIRE_DAYS) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=expires_days)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)


# ---------------------------------------------------------
# Decode Access Token (returns payload or raises)
# ---------------------------------------------------------
def decode_access_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        # Token expired
        return None
    except JWTError:
        # Invalid token
        return None


# ---------------------------------------------------------
# Decode Refresh Token
# ---------------------------------------------------------
def decode_refresh_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        return None
    except JWTError:
        return None


# ---------------------------------------------------------
# Utility: Verify token (returns bool)
# ---------------------------------------------------------
def is_token_valid(token: str) -> bool:
    return decode_access_token(token) is not None
