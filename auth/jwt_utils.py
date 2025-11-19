# auth/jwt_utils.py

import os
import time
import jwt
from typing import Optional, Dict
from jwt import ExpiredSignatureError, InvalidTokenError, DecodeError

# Never allow fallback secret in production
JWT_SECRET = os.environ.get("JWT_SECRET")
if not JWT_SECRET:
    print("⚠ WARNING: JWT_SECRET not set! Using insecure fallback for development.")
    JWT_SECRET = "insecure-local-secret"

JWT_ALGORITHM = "HS256"
JWT_ISSUER = "bloominsight.ai"  # optional but recommended


# ---------------------------------------------------
# Create JWT Token
# ---------------------------------------------------
def create_jwt(payload: Dict, exp_seconds: int = 86400) -> str:
    """
    Creates a signed JWT token.
    Adds expiration and issuer automatically.
    """
    data = payload.copy()
    data["exp"] = int(time.time()) + exp_seconds
    data["iss"] = JWT_ISSUER

    token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

    # PyJWT may return bytes in older versions
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token


# ---------------------------------------------------
# Verify JWT Token
# ---------------------------------------------------
def verify_jwt(token: str) -> Optional[Dict]:
    """
    Verifies a JWT and returns payload if valid.
    Returns None on any error.
    """
    try:
        decoded = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
            issuer=JWT_ISSUER
        )
        return decoded

    except ExpiredSignatureError:
        return None  # Token expired
    except DecodeError:
        return None  # Malformed token
    except InvalidTokenError:
        return None  # Signature mismatch, wrong issuer, etc.
    except Exception:
        return None
