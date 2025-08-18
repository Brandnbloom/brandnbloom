from db.database import get_cursor

def create_user(email, name, password_hash):
    with get_cursor() as cur:
        cur.execute("INSERT INTO users(email, name, password_hash) VALUES(?,?,?)", (email, name, password_hash))
        return cur.lastrowid

def get_user_by_email(email):
    with get_cursor() as cur:
        cur.execute("SELECT * FROM users WHERE email = ?", (email,))
        return cur.fetchone()

def log_kpis(ig_handle, followers, likes, reach, impressions, er):
    with get_cursor() as cur:
        cur.execute('''INSERT INTO kpi_logs(ig_handle, followers, likes, reach, impressions, engagement_rate)
                       VALUES(?,?,?,?,?,?)''', (ig_handle, followers, likes, reach, impressions, er))
        return cur.lastrowid

def get_kpis(ig_handle, limit=50):
    with get_cursor() as cur:
        cur.execute("SELECT * FROM kpi_logs WHERE ig_handle=? ORDER BY timestamp DESC LIMIT ?", (ig_handle, limit))
        return cur.fetchall()

def save_report(user_id, ig_handle, pdf_path):
    with get_cursor() as cur:
        cur.execute("INSERT INTO reports(user_id, ig_handle, pdf_path) VALUES(?,?,?)", (user_id, ig_handle, pdf_path))
        return cur.lastrowid
