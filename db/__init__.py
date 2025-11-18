# db.py
from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", os.getenv("DATABASE_URL", "sqlite:///./bnb.db"))
engine = create_engine(DATABASE_URL, echo=False)

from .models import *   # ✅ import at module level

def init_db():
    ...
  # create all models
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)

