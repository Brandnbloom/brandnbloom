from fastapi import FastAPI
from app.auth import router as auth_router
from app.billing import router as billing_router
from app.database import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Brand n Bloom API")

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(billing_router, prefix="/billing", tags=["Billing"])
