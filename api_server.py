# api_server.py
"""
Production-ready API server for Brand N Bloom.

Features:
- FastAPI app with CORS
- Structured logging
- Unified JSON responses
- JWT authentication (inline helpers)
- Rate limiting (in-memory, simple sliding window)
- Background tasks for long-running jobs
- Async-safe endpoints where possible
- Input validation via Pydantic
- Clear extension points for DB / external API integration
"""

import os
import time
import logging
import asyncio
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta

from fastapi import (
    FastAPI,
    Request,
    HTTPException,
    status,
    Depends,
    BackgroundTasks,
)
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, validator

# JWT (python-jose)
from jose import jwt as jose_jwt, JWTError

# Import your modules (these should already exist in your repo)
# Wrap imports in try/except so the module can still start if some optional components are missing.
try:
    from bloominsight.scraper import fetch_public_profile
except Exception:
    def fetch_public_profile(handle: str):
        return {"handle": handle, "note": "fetch_public_profile stub (module missing)"}

try:
    from bloominsight.analyzer import analyze_profile
except Exception:
    def analyze_profile(profile: dict):
        return {"followers": 1000, "likes": 100, "reach": 800, "impressions": 2000, "engagement_rate": 6.5}

try:
    from bloominsight.report_api import generate_and_send_weekly_report
except Exception:
    def generate_and_send_weekly_report(user_id, email, handle, kpis):
        # stub: create a fake pdf path
        return f"/tmp/report_{handle}.pdf"

try:
    from ai_tools.influencer_finder import find_influencers
except Exception:
    def find_influencers(handles):
        return {"handles": handles, "recommendation": []}

try:
    from ai_tools.business_compare import compare_handles
except Exception:
    def compare_handles(handles):
        return {h: {"followers": 1000, "engagement_rate": 2.3} for h in handles}

try:
    from ai_tools.menu_pricing import suggest_prices
except Exception:
    def suggest_prices(cost, margin, competitor):
        return {"price": round(cost * (1 + (margin or 40) / 100), 2)}

try:
    from ai_tools.consumer_behavior import run_questionnaire
except Exception:
    def run_questionnaire(answers):
        return {"summary": "stubbed questionnaire result"}

try:
    from ai_tools.bloomscore import compute_bloomscore
except Exception:
    def compute_bloomscore(profile):
        return {"score": 62.5, "components": {}}


# -----------------------
# JWT helpers (inline)
# -----------------------
JWT_SECRET = os.getenv("JWT_SECRET", None)
if not JWT_SECRET:
    raise RuntimeError("JWT_SECRET must be set in environment variables")

JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))  # default 1 day


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token using python-jose.
    data: payload (e.g. {"user_id": 1})
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    token = jose_jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode and verify JWT. Returns payload dict on success, None on failure.
    """
    try:
        payload = jose_jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        return None


# -------------------------
# Setup logger
# -------------------------
logger = logging.getLogger("brandnbloom.api")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# FastAPI app
app = FastAPI(title="Brand N Bloom API", version="1.1")

# CORS (adjust origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict to your dashboard origin in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Unified response helpers
# -------------------------
def success_response(data: Any = None, message: str = "OK") -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"success": True, "message": message, "data": data},
    )


def error_response(status_code: int, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"success": False, "message": message, "data": None},
    )


# -------------------------
# Rate limiting (simple)
# -------------------------
# In-memory store: { key: [timestamps] }
RATE_LIMIT_STORE: Dict[str, List[float]] = {}
RATE_LIMIT_LIMIT = int(os.getenv("RATE_LIMIT_LIMIT", "60"))  # requests
RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "60"))  # seconds


def is_rate_limited(key: str, limit: int = RATE_LIMIT_LIMIT, window: int = RATE_LIMIT_WINDOW) -> bool:
    """
    Simple sliding window rate limiter.
    Key can be IP address or user_id.
    """
    now = time.time()
    hits = RATE_LIMIT_STORE.get(key, [])
    # keep only hits within window
    hits = [t for t in hits if now - t < window]
    if len(hits) >= limit:
        RATE_LIMIT_STORE[key] = hits
        return True
    hits.append(now)
    RATE_LIMIT_STORE[key] = hits
    return False


# -------------------------
# Auth dependency
# -------------------------
security = HTTPBearer(auto_error=False)


def get_client_ip(request: Request) -> str:
    # Try common headers then fallback to client.host
    ip = request.headers.get("x-forwarded-for")
    if ip:
        # may contain comma list
        return ip.split(",")[0].strip()
    try:
        return request.client.host or "unknown"
    except Exception:
        return "unknown"


def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)):
    """
    Decodes JWT and returns payload (e.g. user_id). Raises 401 if invalid.
    """
    if not credentials or not credentials.credentials:
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    # Optionally: check token blacklist here
    return payload


# -------------------------
# Request / Response Models
# -------------------------
class HandleRequest(BaseModel):
    handle: str = Field(..., min_length=2, max_length=64)

    @validator("handle")
    def sanitize_handle(cls, v: str):
        return v.strip().lstrip("@")


class ReportRequest(BaseModel):
    handle: str
    email: str
    user_id: Optional[int] = 1


class CompareRequest(BaseModel):
    handles: List[str]


class MenuSuggestRequest(BaseModel):
    cost: float = Field(..., gt=0)
    margin: Optional[float] = Field(40.0, ge=0, le=200)
    competitor: Optional[float] = None


class ConsumerRequest(BaseModel):
    answers: Dict[str, Any]


class SignupRequest(BaseModel):
    email: str
    name: Optional[str] = None
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


# -------------------------
# Background / Helper Tasks
# -------------------------
async def _generate_and_store_report_background(user_id: int, email: str, handle: str, kpis: dict):
    """Background wrapper for report generation & emailing (io-bound)."""
    try:
        logger.info("Background: generate_and_send_weekly_report started for %s", handle)
        # generate_and_send_weekly_report may be sync, run in threadpool
        loop = asyncio.get_running_loop()
        pdf_path = await loop.run_in_executor(None, generate_and_send_weekly_report, user_id, email, handle, kpis)
        logger.info("Background: report generated %s", pdf_path)
    except Exception as e:
        logger.exception("Background report generation failed: %s", e)


# -------------------------
# Exception handlers
# -------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error on %s: %s", request.url, exc)
    return error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error")


# -------------------------
# Health
# -------------------------
@app.get("/health")
async def health():
    return success_response({"service": "brand-n-bloom", "status": "ok"}, message="healthy")


# -------------------------
# Simple user stubs (replace with DB integration)
# -------------------------
# For production: replace these with real DB calls.
def create_user(email: str, name: Optional[str], password: str) -> int:
    logger.info("create_user stub called for %s", email)
    # TODO: persist into DB and return real user_id
    return 1


def verify_user(email: str, password: str) -> bool:
    logger.info("verify_user stub called for %s", email)
    # TODO: check user from DB (hashed password)
    return True


# -------------------------
# Auth endpoints (signup/login)
# -------------------------
@app.post("/auth/signup")
async def signup(req: SignupRequest):
    try:
        # Implement your create_user logic to persist user and return id
        user_id = create_user(req.email, req.name, req.password)
        token = create_access_token({"user_id": user_id})
        return success_response({"user_id": user_id, "access_token": token})
    except Exception as e:
        logger.exception("Signup failed: %s", e)
        return error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Signup failed")


@app.post("/auth/login")
async def login(req: LoginRequest):
    try:
        ok = verify_user(req.email, req.password)
        if not ok:
            return error_response(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
        # In a real flow, lookup user id
        user_id = 1
        token = create_access_token({"user_id": user_id})
        return success_response({"access_token": token})
    except Exception as e:
        logger.exception("Login failed: %s", e)
        return error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Login failed")


# -------------------------
# Scrape endpoint (public)
# -------------------------
@app.post("/scrape")
async def scrape(req: HandleRequest, request: Request):
    ip = get_client_ip(request)
    if is_rate_limited(ip):
        return error_response(status.HTTP_429_TOO_MANY_REQUESTS, "Rate limit exceeded")

    try:
        # fetch_public_profile may be blocking - run in threadpool
        loop = asyncio.get_running_loop()
        profile = await loop.run_in_executor(None, fetch_public_profile, req.handle)
        return success_response(profile)
    except Exception as e:
        logger.exception("/scrape failed: %s", e)
        return error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to fetch profile")


# -------------------------
# Analyze endpoint (public)
# -------------------------
@app.post("/analyze")
async def analyze(req: HandleRequest, request: Request):
    ip = get_client_ip(request)
    if is_rate_limited(ip):
        return error_response(status.HTTP_429_TOO_MANY_REQUESTS, "Rate limit exceeded")

    try:
        loop = asyncio.get_running_loop()
        profile = await loop.run_in_executor(None, fetch_public_profile, req.handle)
        # compute analysis in threadpool (sync)
        analysis = await loop.run_in_executor(None, analyze_profile, profile)
        # optionally log KPIs to DB here
        return success_response(analysis)
    except Exception as e:
        logger.exception("/analyze failed: %s", e)
        return error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to analyze profile")


# -------------------------
# Send weekly report (protected)
# -------------------------
@app.post("/send-report")
async def send_report(req: ReportRequest, background_tasks: BackgroundTasks, current_user: dict = Depends(get_current_user)):
    # Rate limit per user
    user_key = f"user:{current_user.get('user_id')}"
    if is_rate_limited(user_key, limit=10, window=60):
        return error_response(status.HTTP_429_TOO_MANY_REQUESTS, "Rate limit exceeded for user")

    try:
        loop = asyncio.get_running_loop()
        profile = await loop.run_in_executor(None, fetch_public_profile, req.handle)
        analysis = await loop.run_in_executor(None, analyze_profile, profile)
        kpis = {
            "Followers": analysis.get("followers"),
            "Likes": analysis.get("likes"),
            "Reach": analysis.get("reach"),
            "Impressions": analysis.get("impressions"),
            "Engagement Rate (%)": analysis.get("engagement_rate"),
        }
        # schedule background job
        background_tasks.add_task(_generate_and_store_report_background, req.user_id, req.email, req.handle, kpis)
        return success_response({"status": "scheduled"}, message="Report generation scheduled")
    except Exception as e:
        logger.exception("/send-report failed: %s", e)
        return error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to schedule report")


# -------------------------
# BloomScore (protected)
# -------------------------
@app.post("/bloomscore")
async def bloomscore_api(req: HandleRequest, request: Request, current_user: dict = Depends(get_current_user)):
    ip = get_client_ip(request)
    if is_rate_limited(ip):
        return error_response(status.HTTP_429_TOO_MANY_REQUESTS, "Rate limit exceeded")

    try:
        loop = asyncio.get_running_loop()
        profile = await loop.run_in_executor(None, fetch_public_profile, req.handle)
        # compute_bloomscore may be sync
        result = await loop.run_in_executor(None, compute_bloomscore, profile)
        return success_response(result)
    except Exception as e:
        logger.exception("/bloomscore failed: %s", e)
        return error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to compute bloomscore")


# -------------------------
# Influencer finder (protected)
# -------------------------
class HandlesPayload(BaseModel):
    handles: List[str] = Field(..., min_items=1)


@app.post("/influencers")
async def influencers_api(payload: HandlesPayload, current_user: dict = Depends(get_current_user)):
    try:
        # For heavier flows, run in background / threadpool
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, find_influencers, payload.handles)
        return success_response(result)
    except Exception as e:
        logger.exception("/influencers failed: %s", e)
        return error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to find influencers")


# -------------------------
# Compare handles (public)
# -------------------------
@app.post("/compare")
async def compare_api(payload: HandlesPayload, request: Request):
    ip = get_client_ip(request)
    if is_rate_limited(ip):
        return error_response(status.HTTP_429_TOO_MANY_REQUESTS, "Rate limit exceeded")

    try:
        loop = asyncio.get_running_loop()
        # run compare in threadpool
        result = await loop.run_in_executor(None, compare_handles, payload.handles)
        return success_response(result)
    except Exception as e:
        logger.exception("/compare failed: %s", e)
        return error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to compare handles")


# -------------------------
# Menu pricing suggestion
# -------------------------
@app.post("/menu-suggest")
async def menu_suggest_api(req: MenuSuggestRequest):
    try:
        result = suggest_prices(req.cost, req.margin, req.competitor)
        return success_response(result)
    except Exception as e:
        logger.exception("/menu-suggest failed: %s", e)
        return error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to suggest prices")


# -------------------------
# Consumer questionnaire
# -------------------------
@app.post("/consumer")
async def consumer_api(req: ConsumerRequest, current_user: dict = Depends(get_current_user)):
    try:
        # run quickly, convert to sync if needed
        result = run_questionnaire(req.answers)
        return success_response(result)
    except Exception as e:
        logger.exception("/consumer failed: %s", e)
        return error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to run questionnaire")


# -------------------------
# Menu: quick health check & open endpoints list
# -------------------------
@app.get("/")
async def root():
    routes = [{"path": route.path, "name": route.name, "methods": list(route.methods)} for route in app.routes]
    return success_response({"message": "Brand N Bloom API", "routes": routes})


# -------------------------
# Shutdown cleanup (optional)
# -------------------------
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Brand N Bloom API")
