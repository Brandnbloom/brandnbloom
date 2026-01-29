import sqlite3
from hashlib import sha256

DB_FILE = "data/users.db"

# Initialize DB
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             email TEXT UNIQUE,
             password TEXT,
             usage TEXT,
             subscribed INTEGER DEFAULT 0
             )''')

0 = free user

1 = paid user


Function to update subscription:

def activate_subscription(email):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE users SET subscribed=1 WHERE email=?", (email,))
    conn.commit()
    conn.close()

When a user logs in, load subscription status:

def get_subscription(email):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT subscribed FROM users WHERE email=?", (email,))
    res = c.fetchone()
    conn.close()
    return res[0] == 1 if res else False

# Add user
def add_user(email, password):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    hashed_pw = sha256(password.encode()).hexdigest()
    try:
        c.execute("INSERT INTO users (email, password, usage) VALUES (?, ?, ?)", (email, hashed_pw, "{}"))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

# Authenticate user
def authenticate_user(email, password):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    hashed_pw = sha256(password.encode()).hexdigest()
    c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, hashed_pw))
    user = c.fetchone()
    conn.close()
    return user

# Get usage
def get_usage(email):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT usage FROM users WHERE email=?", (email,))
    res = c.fetchone()
    conn.close()
    if res and res[0]:
        import json
        return json.loads(res[0])
    return {}

# Update usage
def update_usage(email, usage_dict):
    import json
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE users SET usage=? WHERE email=?", (json.dumps(usage_dict), email))
    conn.commit()
    conn.close()

