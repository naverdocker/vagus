#!/usr/bin/env python3

import sys
import os
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

if len(sys.argv) > 2:
    print("Usage: python3 nerve.py \"your thoughts here\"")
    sys.exit(1)

user_thought = sys.argv[1]

response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=user_thought
        )

print(response.text)



