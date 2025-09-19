from fastapi import FastAPI
from app.auth import router as auth_router
from app.billing import router as billing_router
from app.database import Base, engine
from app.seo import router as seo_router

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Brand n Bloom API")

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(billing_router, prefix="/billing", tags=["Billing"])
app.include_router(seo_router, prefix="/tools", tags=["SEO Tools"])
