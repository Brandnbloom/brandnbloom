# billing.py
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
import stripe
import os

from .models import User
from .database import get_db
from .utils.jwt_helper import decode_access_token

# Stripe setup
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
router = APIRouter()

# Dependency to get current logged-in user
def get_current_user(authorization: str = Header(...), db: Session = Depends(get_db)) -> User:
    try:
        token = authorization.split(" ")[1]
    except IndexError:
        raise HTTPException(status_code=401, detail="Authorization header malformed")

    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == payload["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Create Stripe checkout session
@router.post("/create-checkout-session")
def create_checkout_session(user: User = Depends(get_current_user)):
    price_id = os.getenv("STRIPE_PLAN_PRICE_ID")
    if not price_id:
        raise HTTPException(status_code=500, detail="Stripe price ID not configured")

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            customer_email=user.email,
            line_items=[{
                "price": price_id,
                "quantity": 1
            }],
            mode="subscription",
            success_url="https://yourdomain.com/success",
            cancel_url="https://yourdomain.com/cancel",
        )
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=502, detail=f"Stripe error: {str(e)}")

    return {"checkout_url": session.url}
