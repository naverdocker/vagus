#!/usr/bin/env python3

import sys
import os
from google import genai

LOG_FILE = os.path.expanduser("~/ai/projects/ai-lab/nerve_memory.txt")
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

if len(sys.argv) > 1:
    user_input = " ".join(sys.argv[1:])
elif not sys.stdin.isatty():
    user_input = sys.stdin.read().strip()
else:
    print("Usage: python3 nerve.py 'prompt' OR echo 'prompt' | python3 nerve.py")
    sys.exit(1)

try:
    response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=user_input
            )
    output = response.text
except Exception as e:
    output = f"[Error]: {str(e)}"

print(output)

with open(LOG_FILE, "a") as f:
    f.write(f"\n--- ENTRY ---[INPUT]: {user_input}\n[OUTPUT]: {output}\n")

