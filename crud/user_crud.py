# crud/user_crud.py

from sqlmodel import select
from db.db import get_session
from models.models import User
from utils.security import hash_password, verify_password


def create_user(email: str, name: str, password: str):
    """
    Create a new user and store hashed password.
    """
    with get_session() as session:
        # Check if email already exists
        stmt = select(User).where(User.email == email)
        existing = session.exec(stmt).first()
        if existing:
            raise ValueError("Email already registered.")

        user = User(
            email=email,
            name=name,
            hashed_password=hash_password(password)
        )
        
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def get_user_by_email(email: str):
    """
    Fetch a user by email.
    """
    with get_session() as session:
        stmt = select(User).where(User.email == email)
        return session.exec(stmt).first()


def authenticate_user(email: str, password: str):
    """
    Verify a user's credentials.
    Returns user object if valid, otherwise None.
    """
    user = get_user_by_email(email)
    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user
