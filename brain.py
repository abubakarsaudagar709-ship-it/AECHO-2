"""
AECHO - Brain Module
Handles memory (facts), identity (owner/creator), and normal conversation logic.
"""

import json
import os

MEMORY_FILE = "memory.json"

# Creator is permanent and hardcoded - never changes regardless of owner
CREATOR_NAME = "Abubakar Saudagar"

# Default memory structure used when no memory.json exists yet
DEFAULT_MEMORY = {
    "owner": None,          # current owner's name, set on first run
    "creator": CREATOR_NAME,
    "password": None,       # owner's permanent password, set on first run
    "temp_password": None,  # used only during ownership transfer
    "failed_attempts": 0,
    "facts": {}              # general learned facts, e.g. {"favorite_color": "black"}
}


def load_memory():
    """Load memory.json, or create it with defaults if missing."""
    if not os.path.exists(MEMORY_FILE):
        save_memory(DEFAULT_MEMORY)
        return DEFAULT_MEMORY.copy()

    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def save_memory(memory):
    """Write memory dict to memory.json."""
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


def is_first_run(memory):
    """True if no owner has been set yet."""
    return memory.get("owner") is None


def set_owner(memory, name, password):
    """Set the owner for the first time (first boot only)."""
    memory["owner"] = name
    memory["password"] = password
    memory["failed_attempts"] = 0
    save_memory(memory)


def verify_password(memory, entered_password):
    """
    Check entered password against stored owner password.
    Returns True/False. Locks AECHO after 3 failed attempts.
    """
    if entered_password == memory.get("password"):
        memory["failed_attempts"] = 0
        save_memory(memory)
        return True

    memory["failed_attempts"] = memory.get("failed_attempts", 0) + 1
    save_memory(memory)
    return False


def is_locked(memory):
    """True if AECHO has locked itself after 3+ failed attempts."""
    return memory.get("failed_attempts", 0) >= 3


def start_ownership_transfer(memory, temp_password):
    """Owner sets a temporary password to allow a new person to claim ownership."""
    memory["temp_password"] = temp_password
    save_memory(memory)


def complete_ownership_transfer(memory, entered_temp_password, new_owner_name):
    """
    If entered temp password matches, transfer ownership to new person.
    Returns True if transfer succeeded.
    """
    if entered_temp_password and entered_temp_password == memory.get("temp_password"):
        memory["owner"] = new_owner_name
        memory["temp_password"] = None
        memory["failed_attempts"] = 0
        save_memory(memory)
        return True
    return False


def remember_fact(memory, key, value):
    """Store a general fact learned from conversation."""
    memory["facts"][key] = value
    save_memory(memory)


def recall_fact(memory, key):
    """Retrieve a previously stored fact, or None if not known."""
    return memory.get("facts", {}).get(key)


def get_identity_response(memory, asked_by_name=None):
    """
    Handles 'who are you' / identity-related questions.
    Creator is always fixed; owner is dynamic from memory.
    """
    owner = memory.get("owner", "Unknown")
    return (
        f"I am AECHO, Abubakar's Enhanced Cognitive Handling Operator. "
        f"I was created by {CREATOR_NAME}. "
        f"My current owner is {owner}."
    )


def process_input(memory, user_text):
    """
    Main conversation entry point - normal convo logic.
    Checks for identity questions first, then falls back to generic response.
    More triggers will be added here feature by feature.
    """
    text_lower = user_text.lower()

    identity_triggers = ["who are you", "kaun ho tum", "tum kaun ho"]
    if any(trigger in text_lower for trigger in identity_triggers):
        return get_identity_response(memory)

    # Placeholder fallback - will expand with more logic each feature
    return "I heard you, but I don't have a response for that yet."
