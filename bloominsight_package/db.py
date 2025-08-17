import sqlite3
import json
import os
from datetime import datetime

class Database:
    def __init__(self, path="data/bloominsight.db"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self._init()

    def _init(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS profiles
                     (id TEXT PRIMARY KEY, username TEXT, data TEXT, last_seen TIMESTAMP)''')
        c.execute('''CREATE TABLE IF NOT EXISTS snapshots
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, fetched_at TIMESTAMP, profile_json TEXT, posts_json TEXT)''')
        self.conn.commit()

    def insert_profile_snapshot(self, username, profile, posts):
        c = self.conn.cursor()
        c.execute("INSERT INTO snapshots (username,fetched_at,profile_json,posts_json) VALUES (?,?,?,?)",
                  (username, datetime.utcnow().isoformat(), json.dumps(profile), json.dumps(posts)))
        self.conn.commit()

    def get_history(self, username, limit=100):
        c = self.conn.cursor()
        c.execute("SELECT fetched_at, profile_json, posts_json FROM snapshots WHERE username=? ORDER BY fetched_at DESC LIMIT ?", (username, limit))
        rows = c.fetchall()
        return rows
