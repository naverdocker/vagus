import os
import sys
import json
from collections import deque
from ..config import DEFAULT_MEMORY_FILE, SESSIONS_DIR, INTERACTION_WINDOW

def _get_memory_path(session: str | None = None) -> str:
    if session:
        os.makedirs(SESSIONS_DIR, exist_ok=True)
        return os.path.join(SESSIONS_DIR, f"{session}.jsonl")
    return DEFAULT_MEMORY_FILE

def load_memory(session: str | None = None) -> list[dict]:
    path = _get_memory_path(session)
    history: list[dict] = []
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                for line in deque(f, maxlen=INTERACTION_WINDOW):
                    if line.strip():
                        try:
                            entry = json.loads(line)
                            history.append({"role": "user", "content": entry["input"]})
                            history.append({"role": "assistant", "content": entry["output"]})
                        except json.JSONDecodeError:
                            print(f"Warning: Corrupted line in memory file '{path}', skipping.", file=sys.stderr)
        except Exception as e:
            print(f"Warning: Memory read error for '{path}' - {e}", file=sys.stderr)
    return history

def save_memory(user_input: str, assistant_output: str, session: str | None = None) -> None:
    if assistant_output:
        path = _get_memory_path(session)
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "a") as f:
                os.fchmod(f.fileno(), 0o600)
                json_entry = json.dumps({"input": user_input, "output": assistant_output})
                f.write(json_entry + "\n")
        except Exception as e:
            print(f"Warning: Memory save error for '{path}' - {e}", file=sys.stderr)

