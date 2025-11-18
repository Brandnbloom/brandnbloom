from fastapi import APIRouter, HTTPException
from crud.user_crud import create_user, authenticate_user
from utils.security import create_token

router = APIRouter(prefix="/auth")


@router.post("/register")
def register(email: str, name: str, password: str):
    user = create_user(email, name, password)
    return {"message": "User created", "id": user.id}


@router.post("/login")
def login(email: str, password: str):
    user = authenticate_user(email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"user_id": user.id, "email": user.email})
    return {"access_token": token}
