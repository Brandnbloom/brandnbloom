import bcrypt

def hash_password(password: str, rounds: int = 12) -> str:
    """Return a bcrypt hashed password."""
    salt = bcrypt.gensalt(rounds=rounds)
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def verify_password(password: str, hashed: str) -> bool:
    """Verify a plaintext password against its hashed form."""
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
