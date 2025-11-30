import os

VAGUS_DIR = os.path.expanduser("~/.vagus")
SESSIONS_DIR = os.path.join(VAGUS_DIR, "sessions")
DEFAULT_MEMORY_FILE = os.path.join(VAGUS_DIR, "memory.jsonl")

DEFAULT_MODEL = "gemini/gemini-2.0-flash"
DEFAULT_TEMP = 0.7

# Number of interactions (user + AI turns) to keep in memory.
INTERACTION_WINDOW = 5