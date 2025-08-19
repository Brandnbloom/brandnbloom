import bcrypt

def hash_password(password: str) -> str:
    """
    Securely hash a password using bcrypt.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def check_password(password: str, hashed: str) -> bool:
    """
    Verify a password against a stored bcrypt hash.
    """
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
