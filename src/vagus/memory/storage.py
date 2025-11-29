import os
import sys
import json
from collections import deque
from ..config import MEMORY_FILE, CONTEXT_WINDOW

def load_memory():
    """Retrieve the last N turns of conversation."""
    history_messages = []
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                for line in deque(f, maxlen=CONTEXT_WINDOW):
                    if line.strip():
                        entry = json.loads(line)
                        history_messages.append({"role": "user", "content": entry["input"]})
                        history_messages.append({"role": "assistant", "content": entry["output"]})
        except Exception as e:
            print(f"Warning: Memory read error - {e}", file=sys.stderr)
    return history_messages

def save_memory(user_input, assistant_output):
    """Appends the new interaction to JSONL file."""
    if assistant_output:
        try:
            os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
            with open(MEMORY_FILE, "a") as f:
                json_entry = json.dumps({"input": user_input, "output": assistant_output})
                f.write(json_entry + "\n")
        except Exception as e:
            print(f"Warning: Memory storage failed - {e}", file=sys.stderr)

