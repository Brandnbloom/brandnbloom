import hashlib
import json
import sqlite3
from datetime import datetime
from tools.analytics.events_store import EventStore

DB = "abtest.db"


# -------------------------------------------------------
# Database Setup
# -------------------------------------------------------
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS tests (
            name TEXT PRIMARY KEY,
            variants TEXT,
            traffic_split TEXT,
            status TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()


# -------------------------------------------------------
# A/B Test Class
# -------------------------------------------------------
class ABTest:
    def __init__(self, name, variants, traffic_split=None):
        """
        variants = ["A", "B", "C"]
        traffic_split example: {"A": 0.5, "B": 0.3, "C": 0.2}
        """
        self.name = name
        self.variants = variants

        if traffic_split:
            assert abs(sum(traffic_split.values()) - 1) < 0.0001, "Traffic split must sum to 1"
            self.traffic_split = traffic_split
        else:
            # default equal split
            n = len(variants)
            self.traffic_split = {v: 1/n for v in variants}

        self.save_test()

    # ------------------------------------------
    # Save Test Metadata Persistently
    # ------------------------------------------
    def save_test(self):
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("""
            INSERT OR REPLACE INTO tests 
            (name, variants, traffic_split, status, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            self.name,
            json.dumps(self.variants),
            json.dumps(self.traffic_split),
            "active",
            datetime.utcnow().isoformat()
        ))
        conn.commit()
        conn.close()

    # ------------------------------------------
    # Deterministic Variant Assignment
    # ------------------------------------------
    def assign_variant(self, user_id):
        """
        Deterministic assignment using hashing ensures:
        - Same user always gets same variant
        - Distribution based on traffic splits
        """

        if not user_id:
            return self.variants[0]  # fallback

        # Generate stable hash between 0 and 1
        bucket = int(hashlib.sha256(str(user_id).encode()).hexdigest(), 16) % 1000000
        ratio = bucket / 1000000.0

        cumulative = 0
        for var, split in self.traffic_split.items():
            cumulative += split
            if ratio <= cumulative:
                return var

        # fallback (should never happen)
        return list(self.variants)[-1]


# -------------------------------------------------------
# Event Logging
# -------------------------------------------------------
def log_exposure(test_name, user_id, variant):
    EventStore.log_event({
        "type": "ab_exposure",
        "test": test_name,
        "user_id": user_id,
        "variant": variant,
        "timestamp": datetime.utcnow().isoformat()
    })


def log_conversion(test_name, user_id, variant, value=1):
    EventStore.log_event({
        "type": "ab_conversion",
        "test": test_name,
        "user_id": user_id,
        "variant": variant,
        "value": value,
        "timestamp": datetime.utcnow().isoformat()
    })


# -------------------------------------------------------
# Test Management
# -------------------------------------------------------
def get_test(name):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT variants, traffic_split, status FROM tests WHERE name=?", (name,))
    row = c.fetchone()
    conn.close()

    if not row:
        return None

    variants = json.loads(row[0])
    traffic_split = json.loads(row[1])
    return ABTest(name, variants, traffic_split)


def pause_test(name):
    conn = sqlite3.connect(DB)
    conn.execute("UPDATE tests SET status='paused' WHERE name=?", (name,))
    conn.commit()
    conn.close()


def resume_test(name):
    conn = sqlite3.connect(DB)
    conn.execute("UPDATE tests SET status='active' WHERE name=?", (name,))
    conn.commit()
    conn.close()


# -------------------------------------------------------
# Reporting (Conversion Rates, Counts)
# -------------------------------------------------------
def get_test_results(test_name):
    """
    Aggregates exposure and conversion counts by variant.
    """
    events = EventStore.query_events(10000)

    exposures = {}
    conversions = {}

    for e in events:
        data = json.loads(e.payload)

        if data.get("test") != test_name:
            continue

        variant = data.get("variant")

        if data["type"] == "ab_exposure":
            exposures[variant] = exposures.get(variant, 0) + 1

        if data["type"] == "ab_conversion":
            conversions[variant] = conversions.get(variant, 0) + data.get("value", 1)

    # Build final result
    result = {}
    for v in exposures:
        exp = exposures.get(v, 0)
        conv = conversions.get(v, 0)
        rate = (conv / exp) if exp > 0 else 0
        result[v] = {
            "exposures": exp,
            "conversions": conv,
            "conversion_rate": round(rate, 4)
        }

    return result
