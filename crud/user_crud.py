from sqlmodel import select
from db.db import get_session
from models.models import User
from utils.security import hash_password, verify_password


def create_user(email: str, name: str, password: str):
    with get_session() as session:
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
    with get_session() as session:
        stmt = select(User).where(User.email == email)
        return session.exec(stmt).first()


def authenticate_user(email: str, password: str):
    user = get_user_by_email(email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
