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
