from fastapi import APIRouter, Depends
import stripe
from sqlalchemy.orm import Session
from .models import User
from .database import get_db
from .utils.jwt_helper import decode_access_token
import os
from fastapi import Header, HTTPException

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
router = APIRouter()

def get_current_user(authorization: str = Header(...), db: Session = Depends(get_db)):
    token = authorization.split(" ")[1]
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.id==payload["user_id"]).first()
    return user

@router.post("/create-checkout-session")
def create_checkout_session(user: User = Depends(get_current_user)):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        customer_email=user.email,
        line_items=[{
            'price': os.getenv("STRIPE_PLAN_PRICE_ID"),  # e.g., monthly plan
            'quantity': 1
        }],
        mode='subscription',
        success_url="https://yourdomain.com/success",
        cancel_url="https://yourdomain.com/cancel",
    )
    return {"checkout_url": session.url}
