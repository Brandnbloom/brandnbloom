import os, sqlite3
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv 
import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")  # Postgres URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DB_PATH = os.environ.get("DATABASE_URL", "sqlite:///bnb.sqlite3")
# Normalize path for sqlite
if DB_PATH.startswith("sqlite:///"):
    DB_FILE = DB_PATH.replace("sqlite:///", "")
else:
    DB_FILE = "bnb.sqlite3"

os.makedirs(os.path.dirname(DB_FILE) or ".", exist_ok=True)

def connect():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

@contextmanager
def get_cursor():
    conn = connect()
    try:
        cur = conn.cursor()
        yield cur
        conn.commit()
    finally:
        conn.close()
