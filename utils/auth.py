# utils/auth.py

from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
import jwt
import os
import logging

from .database import get_db
from .models import User
from .jwt_helper import create_access_token, create_refresh_token, decode_token

router = APIRouter()
logger = logging.getLogger("auth")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWT_SECRET = os.getenv("JWT_SECRET", "supersecretjwt")
JWT_REFRESH_SECRET = os.getenv("JWT_REFRESH_SECRET", "superrefreshsecret")

security = HTTPBearer()
# ------------------------------------------------------------

# Pydantic Schemas
# ------------------------------------------------------------
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_id: int
    email: EmailStr

# ------------------------------------------------------------
# Registration
# ------------------------------------------------------------
@router.post("/register", response_model=TokenResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(user.password)

    new_user = User(
        email=user.email,
        hashed_password=hashed_password,
        role="user"  # default role; optional
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token({"user_id": new_user.id})
    refresh_token = create_refresh_token({"user_id": new_user.id})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user_id=new_user.id,
        email=new_user.email
    )

# ------------------------------------------------------------
# Login
# ------------------------------------------------------------
@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token({"user_id": db_user.id})
    refresh_token = create_refresh_token({"user_id": db_user.id})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user_id=db_user.id,
        email=db_user.email
    )

# ------------------------------------------------------------
# Refresh Token Endpoint
# ------------------------------------------------------------
class RefreshRequest(BaseModel):
    refresh_token: str


@router.post("/refresh")
def refresh_token(data: RefreshRequest):
    try:
        payload = jwt.decode(
            data.refresh_token,
            JWT_REFRESH_SECRET,
            algorithms=["HS256"]
        )
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user_id = payload.get("user_id")
    new_access_token = create_access_token({"user_id": user_id})

    return {"access_token": new_access_token, "token_type": "bearer"}

# ------------------------------------------------------------
# Auth Dependency
# ------------------------------------------------------------
def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials

    try:
        payload = decode_token(token)
        return payload   # contains user_id, expiry, etc.

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )

# ------------------------------------------------------------
# Optional Role Check
# ------------------------------------------------------------
def require_admin(user=Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return user
