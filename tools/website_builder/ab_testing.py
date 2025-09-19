import random
from tools.analytics.events_store import EventStore

class ABTest:
    def __init__(self, name, variants):
        self.name = name
        self.variants = variants  # list of variant IDs

    def assign_variant(self, user_id):
        # Simple deterministic assignment: hash mod n
        return random.choice(self.variants)

def log_exposure(test_name, user_id, variant):
    EventStore.log_event({
        "type": "ab_exposure",
        "test": test_name,
        "user_id": user_id,
        "variant": variant
    })

def log_conversion(test_name, user_id, variant, value=1):
    EventStore.log_event({
        "type": "ab_conversion",
        "test": test_name,
        "user_id": user_id,
        "variant": variant,
        "value": value
    })
