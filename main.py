from fastapi import FastAPI
from app.auth import router as auth_router
from app.billing import router as billing_router
from app.seo import router as seo_router
from app.social import router as social_router
from app.ads import router as ads_router
from app.database import Base, engine
from db.db import init_db

# -----------------------------
# FastAPI App Initialization
# -----------------------------
app = FastAPI(title="Brand n Bloom API", description="Marketing Automation & Brand Insights API")

# -----------------------------
# Routers / Endpoints
# -----------------------------
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(billing_router, prefix="/billing", tags=["Billing"])
app.include_router(seo_router, prefix="/tools", tags=["SEO Tools"])
app.include_router(social_router, prefix="/tools", tags=["Social Media Tools"])
app.include_router(ads_router, prefix="/tools", tags=["Ads & Marketing Tools"])

# -----------------------------
# Startup Events
# -----------------------------
@app.on_event("startup")
def on_startup():
    init_db()
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized and tables created.")

# -----------------------------
# Root endpoint
# -----------------------------
@app.get("/", tags=["Root"])
def home():
    return {"message": "API is working!"}
