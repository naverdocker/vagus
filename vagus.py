#!/usr/bin/env python3

import sys
import os
import json
import argparse
from collections import deque
try:
    from litellm import completion
except ImportError:
    print("Error: 'litellm' module not found. Run: pip install litellm", file=sys.stderr)
    sys.exit(1)

# --- CONFIGURATION DEFAULTS ---
DEFAULT_MODEL = "gemini/gemini-2.0-flash"
DEFAULT_TEMP = 0.7
MEMORY_FILE = os.path.expanduser("~/.vagus/memory.jsonl")
CONTEXT_WINDOW = 5


# --- ARGUMENT PARSING ---
parser = argparse.ArgumentParser(description="Vagus: The Neural Interface")
parser.add_argument("prompt", nargs="*", help="The user prompt")
parser.add_argument("-m", "--model", type=str, default=DEFAULT_MODEL, help="Model (e.g. gpt-4o, claude-3-5-sonnet)")
parser.add_argument("-t", "--temp", type=float, default=DEFAULT_TEMP, help="Creativity (0.0 - 2.0)")
parser.add_argument("--json", action="store_true", help="Force JSON output")
args = parser.parse_args()


# --- INPUT HANDLING ---
user_input_parts = []

if args.prompt:
    user_input_parts.append(" ".join(args.prompt))

if not sys.stdin.isatty():
    piped_data = sys.stdin.read().strip()
    if piped_data:
        user_input_parts.append(f"\n[Context Data]:\n{piped_data}")

if not user_input_parts:
    print("Usage: vagus 'prompt' | vagus -m gpt-40 'prompt'", file=sys.stderr)
    sys.exit(1)

final_user_input = "\n".join(user_input_parts)

# --- MEMORY RETRIEVAL ---
history_messages = []
if os.path.exists(MEMORY_FILE):
    try:
        with open(MEMORY_FILE, "r") as f:
            for line in deque(f, maxlen=CONTEXT_WINDOW):
                if line.strip():
                    entry = json.loads(line)
                    history_messages.append({"role": "user", "content": entry['input']})
                    history_messages.append({"role": "assistant", "content": entry['output']})
    except Exception as e:
        print(f"Warning: Memory read error - {e}", file=sys.stderr)

# --- THE SIGNAL ---
messages = history_messages + [{"role": "user", "content": final_user_input}]

sys_content = "You are Vagus, a digital regulatory system. Be concise."
if args.json:
    sys_content += " Output ONLY valid JSON."

messages.insert(0, {"role": "system", "content": sys_content})

# --- STREAMING OUTPUT ---
full_response_text = ""
try:
    response = completion(
            model=args.model,
            messages=messages,
            temperature=args.temp,
            stream=True
            )

    for chunk in response:
        if chunk.choices and chunk.choices[0].delta.content:
            delta = chunk.choices[0].delta.content
            print(delta, end="", flush=True)
            full_response_text += delta

    print()

except Exception as e:
    print(f"\nError: Signal blocked - {str(e)}", file=sys.stderr)
    sys.exit()

# --- MEMORY STORAGE ---
if full_response_text:
    try:
        os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
        with open(MEMORY_FILE, "a") as f:
            json_entry = json.dumps({"input": final_user_input, "output": full_response_text})
            f.write(json_entry + "\n")
    except Exception as e:
        print(f"Warning: Memory storage failed - {e}", file=sys.stderr)
