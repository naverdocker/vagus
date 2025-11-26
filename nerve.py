#!/usr/bin/env python3

import sys
import os
import json
from google import genai

# --- CONFIGURATION ---
LOG_FILE = os.path.expanduser("~/ai/projects/ai-lab/nerve_memory.jsonl")
CONTEXT_WINDOW = 5

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY environment variable not set.")
    sys.exit(1)
client = genai.Client(api_key=api_key)

# --- MEMORY RETRIEVAL ---
history_context = ""
try:
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            # Read all lines and take the last CONTEXT_WINDOW lines
            all_lines = f.readlines()
            last_lines = all_lines[-CONTEXT_WINDOW:]
            for line in last_lines:
                if line.strip():
                    entry = json.loads(line)
                    history_context += f"User: {entry['input']}\nAI: {entry['output']}\n"
except Exception as e:
    print(f"[Warning: Memory Corrupt] {e}")


# --- INPUT HANDLING ---
if len(sys.argv) > 1:
    user_input = " ".join(sys.argv[1:])
elif not sys.stdin.isatty():
    user_input = sys.stdin.read().strip()
else:
    print("Usage: python3 nerve.py 'prompt' OR echo 'prompt' | python3 nerve.py")
    sys.exit(1)

# --- PROMPT ENGINEERING (Injection) ---
full_prompt = f"""
HISTORY OF CONVERSATION:
    {history_context}

CURRENT USER INPUT:
    {user_input}
"""

# --- THE SIGNAL ---
try:
    response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=full_prompt
            )
    output = response.text
except Exception as e:
    output = f"[Error]: {str(e)}"

# --- OUTPUT & PERSISTANCE ---
print(output)

try:
    with open(LOG_FILE, "a") as f:
        json_entry = json.dumps({"input": user_input, "output": output})
        f.write(json_entry + "\n")
except Exception as e:
    print(f"[Warning: Could not save memory] {e}")

