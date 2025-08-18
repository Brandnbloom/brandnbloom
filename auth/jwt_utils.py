import os, time, jwt
JWT_SECRET = os.environ.get("JWT_SECRET", "change-me")

def create_jwt(payload: dict, exp_seconds: int = 86400):
    data = payload.copy()
    data["exp"] = int(time.time()) + exp_seconds
    return jwt.encode(data, JWT_SECRET, algorithm="HS256")

def verify_jwt(token: str):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except Exception:
        return None
