import os, sqlite3
from contextlib import contextmanager

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
