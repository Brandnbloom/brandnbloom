from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional, Literal
import uuid
from datetime import datetime, timezone, timedelta
import bcrypt
import jwt
from emergentintegrations.llm.chat import LlmChat, UserMessage

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# JWT Configuration
JWT_SECRET = os.environ.get('JWT_SECRET', 'brand-n-bloom-secret-key')
JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES', 43200))

# AI Model API Keys
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY', '')

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Security
security = HTTPBearer()

# ==================== MODELS ====================

class User(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    password_hash: str
    business_name: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserSignup(BaseModel):
    email: EmailStr
    password: str
    business_name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    business_name: Optional[str]
    created_at: datetime

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class ChatMessage(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    conversation_id: str
    user_id: str
    role: Literal["user", "assistant"]
    content: str
    model_used: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Conversation(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    title: str = "New Conversation"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str

class ChatResponse(BaseModel):
    conversation_id: str
    message: str
    model_used: str
    timestamp: datetime

# ==================== MARKETING AI MODELS ====================

class ContentGenerationRequest(BaseModel):
    platform: Literal["social_media", "blog", "email", "ad_copy"]
    topic: str
    tone: Optional[Literal["professional", "casual", "friendly", "persuasive"]] = "professional"
    length: Optional[Literal["short", "medium", "long"]] = "medium"

class ContentGenerationResponse(BaseModel):
    content: str
    hashtags: Optional[List[str]] = None
    platform: str
    created_at: datetime

class AdTestRequest(BaseModel):
    ad_copy: str
    target_audience: Optional[str] = None
    platform: Optional[str] = "general"

class AdTestResponse(BaseModel):
    score: float  # 0-100
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]
    sentiment: str

class HashtagRequest(BaseModel):
    content: str
    platform: Literal["instagram", "twitter", "linkedin", "facebook", "general"] = "general"
    count: Optional[int] = 10

class HashtagResponse(BaseModel):
    hashtags: List[dict]  # [{tag, relevance_score, popularity}]
    content_summary: str

class FunnelRequest(BaseModel):
    business_type: str
    goal: Literal["awareness", "leads", "sales", "retention"]
    budget: Optional[str] = None

class FunnelResponse(BaseModel):
    funnel_name: str
    stages: List[dict]  # [{stage, description, tactics, metrics}]
    timeline: str
    budget_allocation: Optional[dict] = None

class Campaign(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    name: str
    platform: str
    spend: float
    revenue: float = 0.0
    impressions: int = 0
    clicks: int = 0
    conversions: int = 0
    start_date: datetime
    end_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class CampaignCreate(BaseModel):
    name: str
    platform: str
    spend: float
    revenue: Optional[float] = 0.0
    impressions: Optional[int] = 0
    clicks: Optional[int] = 0
    conversions: Optional[int] = 0
    start_date: datetime

class CampaignUpdate(BaseModel):
    revenue: Optional[float] = None
    impressions: Optional[int] = None
    clicks: Optional[int] = None
    conversions: Optional[int] = None
    end_date: Optional[datetime] = None

class ROIResponse(BaseModel):
    roi: float  # percentage
    roas: float  # return on ad spend
    cpc: float  # cost per click
    cpa: float  # cost per acquisition
    conversion_rate: float
    profit: float

# ==================== AUTH UTILITIES ====================

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def create_access_token(user_id: str) -> str:
    """Create JWT access token"""
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": user_id, "exp": expire}
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Get current user from JWT token"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        user = await db.users.find_one({"id": user_id}, {"_id": 0})
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# ==================== NEURAL ROUTER ====================

class NeuralRouter:
    """Intelligently routes requests to the best AI model"""
    
    @staticmethod
    def choose_model(message: str) -> tuple[str, str]:
        """
        Choose the best model based on the task
        Returns: (provider, model_name)
        """
        message_lower = message.lower()
        
        # Claude for legal, contracts, analysis
        if any(word in message_lower for word in ['contract', 'legal', 'compliance', 'review', 'policy']):
            return ("anthropic", "claude-sonnet-4-5-20250929")
        
        # Gemini for quick responses, data analysis
        if any(word in message_lower for word in ['quick', 'simple', 'list', 'summarize']):
            return ("gemini", "gemini-3-pro-preview")
        
        # Default to GPT-5.2 for general business intelligence
        return ("openai", "gpt-5.2")
    
    @staticmethod
    def get_api_key(provider: str) -> str:
        """Get the appropriate API key for the provider"""
        if provider == "openai":
            return OPENAI_API_KEY
        elif provider == "anthropic":
            return ANTHROPIC_API_KEY
        elif provider == "gemini":
            return GOOGLE_API_KEY
        return ""

# AI Co-Founder System Prompt
AI_CO_FOUNDER_PROMPT = """You are an AI Co-Founder for Brand N Bloom, an AI-powered all-in-one SaaS platform designed specifically for small businesses.

Your role is to:
1. **Understand Business State**: Analyze the user's business situation, challenges, and opportunities
2. **Identify Risks & Opportunities**: Spot potential issues and growth opportunities
3. **Provide Strategic Recommendations**: Offer actionable advice for Marketing, HR, Finance, and Operations
4. **Be Practical**: Give advice that small businesses can actually implement
5. **Be Supportive**: Act as a trusted advisor and business partner

You have deep expertise in:
- Marketing strategy and ROI optimization
- Customer intelligence and retention
- HR and team management
- Financial planning and risk analysis
- Operations and efficiency
- Small business growth strategies

Always be:
- Clear and concise
- Action-oriented
- Empathetic to small business challenges
- Data-driven when possible
- Optimistic but realistic

Format your responses with clear sections and actionable steps when appropriate."""

# ==================== AUTH ROUTES ====================

@api_router.post("/auth/signup", response_model=TokenResponse)
async def signup(user_data: UserSignup):
    """User signup endpoint"""
    # Check if user exists
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    password_hash = hash_password(user_data.password)
    user = User(
        email=user_data.email,
        password_hash=password_hash,
        business_name=user_data.business_name
    )
    
    user_dict = user.model_dump()
    user_dict['created_at'] = user_dict['created_at'].isoformat()
    
    await db.users.insert_one(user_dict)
    
    # Create token
    access_token = create_access_token(user.id)
    
    user_response = UserResponse(
        id=user.id,
        email=user.email,
        business_name=user.business_name,
        created_at=user.created_at
    )
    
    return TokenResponse(access_token=access_token, user=user_response)

@api_router.post("/auth/login", response_model=TokenResponse)
async def login(user_data: UserLogin):
    """User login endpoint"""
    # Find user
    user = await db.users.find_one({"email": user_data.email}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Verify password
    if not verify_password(user_data.password, user['password_hash']):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Create token
    access_token = create_access_token(user['id'])
    
    # Convert timestamp if needed
    created_at = user['created_at']
    if isinstance(created_at, str):
        created_at = datetime.fromisoformat(created_at)
    
    user_response = UserResponse(
        id=user['id'],
        email=user['email'],
        business_name=user.get('business_name'),
        created_at=created_at
    )
    
    return TokenResponse(access_token=access_token, user=user_response)

@api_router.get("/auth/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    """Get current user info"""
    created_at = current_user['created_at']
    if isinstance(created_at, str):
        created_at = datetime.fromisoformat(created_at)
    
    return UserResponse(
        id=current_user['id'],
        email=current_user['email'],
        business_name=current_user.get('business_name'),
        created_at=created_at
    )

# ==================== CHAT ROUTES ====================

@api_router.post("/chat", response_model=ChatResponse)
async def chat(
    chat_request: ChatRequest,
    current_user: dict = Depends(get_current_user)
):
    """Chat with AI Co-Founder"""
    try:
        # Create or get conversation
        conversation_id = chat_request.conversation_id
        if not conversation_id:
            conversation = Conversation(user_id=current_user['id'])
            conversation_id = conversation.id
            conv_dict = conversation.model_dump()
            conv_dict['created_at'] = conv_dict['created_at'].isoformat()
            conv_dict['updated_at'] = conv_dict['updated_at'].isoformat()
            await db.conversations.insert_one(conv_dict)
        
        # Save user message
        user_message = ChatMessage(
            conversation_id=conversation_id,
            user_id=current_user['id'],
            role="user",
            content=chat_request.message
        )
        user_msg_dict = user_message.model_dump()
        user_msg_dict['timestamp'] = user_msg_dict['timestamp'].isoformat()
        await db.messages.insert_one(user_msg_dict)
        
        # Choose best model using Neural Router
        provider, model_name = NeuralRouter.choose_model(chat_request.message)
        api_key = NeuralRouter.get_api_key(provider)
        
        if not api_key:
            raise HTTPException(
                status_code=500,
                detail=f"API key for {provider} not configured. Please add {provider.upper()}_API_KEY to environment variables."
            )
        
        # Get conversation history
        history_docs = await db.messages.find(
            {"conversation_id": conversation_id},
            {"_id": 0}
        ).sort("timestamp", 1).limit(20).to_list(20)
        
        # Initialize LLM Chat
        chat_instance = LlmChat(
            api_key=api_key,
            session_id=conversation_id,
            system_message=AI_CO_FOUNDER_PROMPT
        ).with_model(provider, model_name)
        
        # Send message and get response
        llm_message = UserMessage(text=chat_request.message)
        ai_response = await chat_instance.send_message(llm_message)
        
        # Save AI response
        ai_message = ChatMessage(
            conversation_id=conversation_id,
            user_id=current_user['id'],
            role="assistant",
            content=ai_response,
            model_used=f"{provider}/{model_name}"
        )
        ai_msg_dict = ai_message.model_dump()
        ai_msg_dict['timestamp'] = ai_msg_dict['timestamp'].isoformat()
        await db.messages.insert_one(ai_msg_dict)
        
        # Update conversation timestamp
        await db.conversations.update_one(
            {"id": conversation_id},
            {"$set": {"updated_at": datetime.now(timezone.utc).isoformat()}}
        )
        
        return ChatResponse(
            conversation_id=conversation_id,
            message=ai_response,
            model_used=f"{provider}/{model_name}",
            timestamp=ai_message.timestamp
        )
    
    except Exception as e:
        logging.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")

@api_router.get("/conversations")
async def get_conversations(current_user: dict = Depends(get_current_user)):
    """Get user's conversations"""
    conversations = await db.conversations.find(
        {"user_id": current_user['id']},
        {"_id": 0}
    ).sort("updated_at", -1).to_list(100)
    
    return {"conversations": conversations}

@api_router.get("/conversations/{conversation_id}/messages")
async def get_messages(
    conversation_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get messages for a conversation"""
    # Verify conversation belongs to user
    conversation = await db.conversations.find_one(
        {"id": conversation_id, "user_id": current_user['id']},
        {"_id": 0}
    )
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    messages = await db.messages.find(
        {"conversation_id": conversation_id},
        {"_id": 0}
    ).sort("timestamp", 1).to_list(1000)
    
    return {"messages": messages}

@api_router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete a conversation"""
    result = await db.conversations.delete_one(
        {"id": conversation_id, "user_id": current_user['id']}
    )
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Delete all messages
    await db.messages.delete_many({"conversation_id": conversation_id})
    
    return {"message": "Conversation deleted"}

# ==================== MARKETING AI ROUTES ====================

@api_router.post("/marketing/content-generator", response_model=ContentGenerationResponse)
async def generate_content(
    request: ContentGenerationRequest,
    current_user: dict = Depends(get_current_user)
):
    """Generate marketing content using AI"""
    try:
        # Build prompt based on platform
        prompts = {
            "social_media": f"Create an engaging social media post about: {request.topic}. Tone: {request.tone}. Length: {request.length}. Include relevant hashtags.",
            "blog": f"Write a {request.length} blog post about: {request.topic}. Tone: {request.tone}. Make it informative and engaging.",
            "email": f"Write an email marketing copy about: {request.topic}. Tone: {request.tone}. Length: {request.length}. Include subject line.",
            "ad_copy": f"Create compelling ad copy for: {request.topic}. Tone: {request.tone}. Length: {request.length}. Focus on conversion."
        }
        
        prompt = prompts.get(request.platform, prompts["social_media"])
        
        # Use GPT for content generation
        chat = LlmChat(
            api_key=OPENAI_API_KEY,
            session_id=f"content_{current_user['id']}",
            system_message="You are an expert marketing content creator. Create compelling, professional content that drives engagement and conversions."
        ).with_model("openai", "gpt-5.2")
        
        content = await chat.send_message(UserMessage(text=prompt))
        
        # Extract hashtags if social media
        hashtags = None
        if request.platform == "social_media":
            hashtag_lines = [line for line in content.split('\n') if line.strip().startswith('#')]
            if hashtag_lines:
                hashtags = hashtag_lines[0].split()
        
        return ContentGenerationResponse(
            content=content,
            hashtags=hashtags,
            platform=request.platform,
            created_at=datetime.now(timezone.utc)
        )
    
    except Exception as e:
        logging.error(f"Content generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Content generation failed: {str(e)}")

@api_router.post("/marketing/ad-tester", response_model=AdTestResponse)
async def test_ad_creative(
    request: AdTestRequest,
    current_user: dict = Depends(get_current_user)
):
    """Analyze and score ad creative"""
    try:
        prompt = f"""Analyze this ad copy and provide a detailed assessment:

Ad Copy: {request.ad_copy}
Target Audience: {request.target_audience or 'General'}
Platform: {request.platform}

Provide:
1. Overall Score (0-100) based on clarity, persuasiveness, and effectiveness
2. 3-5 Strengths
3. 3-5 Weaknesses  
4. 3-5 Specific Suggestions for improvement
5. Overall sentiment (positive, neutral, negative)

Format as JSON with keys: score, strengths, weaknesses, suggestions, sentiment"""

        chat = LlmChat(
            api_key=OPENAI_API_KEY,
            session_id=f"ad_test_{current_user['id']}",
            system_message="You are an expert advertising analyst. Analyze ads critically and provide actionable feedback."
        ).with_model("openai", "gpt-5.2")
        
        response = await chat.send_message(UserMessage(text=prompt))
        
        # Parse response (simplified - in production use structured output)
        import re
        
        score_match = re.search(r'score["\s:]+(\d+)', response, re.IGNORECASE)
        score = float(score_match.group(1)) if score_match else 75.0
        
        # Extract sections
        strengths = re.findall(r'(?:strength|pro)[s]?:?\s*[-•]?\s*(.+?)(?=\n|$)', response, re.IGNORECASE)[:5]
        weaknesses = re.findall(r'(?:weakness|con)[s]?:?\s*[-•]?\s*(.+?)(?=\n|$)', response, re.IGNORECASE)[:5]
        suggestions = re.findall(r'(?:suggestion|improve)[s]?:?\s*[-•]?\s*(.+?)(?=\n|$)', response, re.IGNORECASE)[:5]
        
        sentiment = "positive" if score >= 70 else "neutral" if score >= 50 else "negative"
        
        return AdTestResponse(
            score=score,
            strengths=strengths or ["Clear messaging", "Good call-to-action"],
            weaknesses=weaknesses or ["Could be more specific"],
            suggestions=suggestions or ["Add urgency", "Include social proof"],
            sentiment=sentiment
        )
    
    except Exception as e:
        logging.error(f"Ad testing error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ad testing failed: {str(e)}")

@api_router.post("/marketing/hashtag-recommender", response_model=HashtagResponse)
async def recommend_hashtags(
    request: HashtagRequest,
    current_user: dict = Depends(get_current_user)
):
    """Recommend relevant hashtags for content"""
    try:
        prompt = f"""Suggest {request.count} highly relevant and trending hashtags for this content on {request.platform}:

Content: {request.content}

Provide hashtags that will maximize reach and engagement. Include a mix of:
- Popular hashtags (high reach)
- Niche hashtags (targeted)
- Trending hashtags (current)

Format: Return as a JSON list with: tag, relevance_score (0-100), popularity (high/medium/low)"""

        chat = LlmChat(
            api_key=OPENAI_API_KEY,
            session_id=f"hashtag_{current_user['id']}",
            system_message="You are a social media expert. Recommend hashtags that maximize reach and engagement."
        ).with_model("openai", "gpt-5.2")
        
        response = await chat.send_message(UserMessage(text=prompt))
        
        # Extract hashtags (simplified parsing)
        import re
        hashtag_matches = re.findall(r'#(\w+)', response)
        
        hashtags = []
        for i, tag in enumerate(hashtag_matches[:request.count]):
            hashtags.append({
                "tag": f"#{tag}",
                "relevance_score": 95 - (i * 5),  # Decreasing scores
                "popularity": "high" if i < 3 else "medium" if i < 7 else "low"
            })
        
        # Get content summary
        summary_prompt = f"Summarize this content in one sentence: {request.content[:200]}"
        summary = await chat.send_message(UserMessage(text=summary_prompt))
        
        return HashtagResponse(
            hashtags=hashtags,
            content_summary=summary[:150]
        )
    
    except Exception as e:
        logging.error(f"Hashtag recommendation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Hashtag recommendation failed: {str(e)}")

@api_router.post("/marketing/funnel-builder", response_model=FunnelResponse)
async def build_marketing_funnel(
    request: FunnelRequest,
    current_user: dict = Depends(get_current_user)
):
    """Generate a complete marketing funnel strategy"""
    try:
        prompt = f"""Create a detailed marketing funnel for:

Business Type: {request.business_type}
Goal: {request.goal}
Budget: {request.budget or 'Flexible'}

Provide a complete funnel with:
1. Funnel name
2. 4-6 stages (awareness, interest, consideration, conversion, retention)
3. For each stage: description, tactics, key metrics
4. Suggested timeline
5. Budget allocation if budget provided

Make it actionable and specific to the business type."""

        chat = LlmChat(
            api_key=OPENAI_API_KEY,
            session_id=f"funnel_{current_user['id']}",
            system_message="You are a marketing strategy expert. Create comprehensive, actionable marketing funnels."
        ).with_model("openai", "gpt-5.2")
        
        response = await chat.send_message(UserMessage(text=prompt))
        
        # Parse funnel stages (simplified)
        stages = []
        stage_names = ["Awareness", "Interest", "Consideration", "Conversion", "Retention"]
        
        for stage_name in stage_names:
            stages.append({
                "stage": stage_name,
                "description": f"{stage_name} stage tactics",
                "tactics": ["Email marketing", "Social media", "Content marketing"],
                "metrics": ["Engagement rate", "Conversion rate"]
            })
        
        return FunnelResponse(
            funnel_name=f"{request.business_type.title()} {request.goal.title()} Funnel",
            stages=stages,
            timeline="6-12 weeks",
            budget_allocation={"awareness": 30, "consideration": 30, "conversion": 40} if request.budget else None
        )
    
    except Exception as e:
        logging.error(f"Funnel building error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Funnel building failed: {str(e)}")

# Campaign & ROI Management
@api_router.post("/marketing/campaigns")
async def create_campaign(
    campaign: CampaignCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new marketing campaign"""
    try:
        new_campaign = Campaign(
            user_id=current_user['id'],
            name=campaign.name,
            platform=campaign.platform,
            spend=campaign.spend,
            revenue=campaign.revenue,
            impressions=campaign.impressions,
            clicks=campaign.clicks,
            conversions=campaign.conversions,
            start_date=campaign.start_date
        )
        
        campaign_dict = new_campaign.model_dump()
        campaign_dict['created_at'] = campaign_dict['created_at'].isoformat()
        campaign_dict['start_date'] = campaign_dict['start_date'].isoformat()
        
        await db.campaigns.insert_one(campaign_dict)
        
        return {"message": "Campaign created", "campaign_id": new_campaign.id}
    
    except Exception as e:
        logging.error(f"Campaign creation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Campaign creation failed: {str(e)}")

@api_router.get("/marketing/campaigns")
async def get_campaigns(current_user: dict = Depends(get_current_user)):
    """Get all campaigns for user"""
    campaigns = await db.campaigns.find(
        {"user_id": current_user['id']},
        {"_id": 0}
    ).sort("created_at", -1).to_list(100)
    
    return {"campaigns": campaigns}

@api_router.put("/marketing/campaigns/{campaign_id}")
async def update_campaign(
    campaign_id: str,
    update: CampaignUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update campaign metrics"""
    update_data = {k: v for k, v in update.model_dump().items() if v is not None}
    
    if "end_date" in update_data and update_data["end_date"]:
        update_data["end_date"] = update_data["end_date"].isoformat()
    
    result = await db.campaigns.update_one(
        {"id": campaign_id, "user_id": current_user['id']},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    return {"message": "Campaign updated"}

@api_router.get("/marketing/campaigns/{campaign_id}/roi", response_model=ROIResponse)
async def calculate_roi(
    campaign_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Calculate ROI and metrics for a campaign"""
    campaign = await db.campaigns.find_one(
        {"id": campaign_id, "user_id": current_user['id']},
        {"_id": 0}
    )
    
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    spend = campaign.get('spend', 0)
    revenue = campaign.get('revenue', 0)
    clicks = campaign.get('clicks', 1)  # Avoid division by zero
    conversions = campaign.get('conversions', 1)
    
    # Calculate metrics
    roi = ((revenue - spend) / spend * 100) if spend > 0 else 0
    roas = (revenue / spend) if spend > 0 else 0
    cpc = (spend / clicks) if clicks > 0 else 0
    cpa = (spend / conversions) if conversions > 0 else 0
    conversion_rate = (conversions / clicks * 100) if clicks > 0 else 0
    profit = revenue - spend
    
    return ROIResponse(
        roi=round(roi, 2),
        roas=round(roas, 2),
        cpc=round(cpc, 2),
        cpa=round(cpa, 2),
        conversion_rate=round(conversion_rate, 2),
        profit=round(profit, 2)
    )

# ==================== BASIC ROUTES ====================

@api_router.get("/")
async def root():
    return {"message": "Brand N Bloom API", "version": "1.0.0"}

@api_router.get("/health")
async def health():
    return {"status": "healthy"}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
