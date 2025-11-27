#!/usr/bin/env python3

import sys
import os
import json
from collections import deque
from google import genai
from google.genai import types

# --- CONFIGURATION ---
LOG_FILE = os.path.expanduser("~/ai/projects/ai-lab/nerve_memory.jsonl")
CONTEXT_WINDOW = 5

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY environment variable not set.", file=sys.stderr)
    sys.exit(1)
client = genai.Client(api_key=api_key)

# --- MEMORY RETRIEVAL ---
history_message = []

try:
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            for line in deque(f, maxlen=CONTEXT_WINDOW):
                if line.strip():
                    entry = json.loads(line)

                    history_message.append({
                        "role": "user",
                        "parts": [{"text": entry['input']}]
                        })

                    history_message.append({
                        "role": "model",
                        "parts": [{"text": entry['output']}]
                        })
except Exception as e:
    print(f"Warning: Memory Corrupt - {e}", file=sys.stderr)

# --- INPUT HANDLING ---
if len(sys.argv) > 1:
    user_input = " ".join(sys.argv[1:])
elif not sys.stdin.isatty():
    user_input = sys.stdin.read().strip()
else:
    print("Usage: python3 nerve.py 'prompt' OR echo 'prompt' | python3 nerve.py", file=sys.stderr)
    sys.exit(1)

# --- PROMPT ENGINEERING (Injection) ---
full_prompt = f"""
HISTORY OF CONVERSATION:
    {history_message}

CURRENT USER INPUT:
    {user_input}
"""

# --- THE SIGNAL ---
current_message = {
        "role": "user",
        "parts": [{"text": user_input}]
        }

full_conversation = history_message + [current_message]

system_instruction = "You are Nerve, a command-line AI utility. Be concise. Output plain text unless JSON is requested."

try:
    response = client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7
                ),
            contents=full_conversation
            )
    output = response.text
except Exception as e:
    print(f"Error: API request failed - {str(e)}", file=sys.stderr)
    sys.exit(1)

# --- OUTPUT & PERSISTANCE ---
print(output)

try:
    with open(LOG_FILE, "a") as f:
        json_entry = json.dumps({"input": user_input, "output": output})
        f.write(json_entry + "\n")
except Exception as e:
    print(f"Warning: Could not save memory - {e}", file=sys.stderr)
