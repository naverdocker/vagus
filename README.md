# Vagus

> **The neural interface for your terminal.**

Vagus is a CLI-based AI utility that connects your terminal workflows directly to Large Language Models.

## Features

- **Gemini API Integration:** Built on `gemini-2.0-flash` for high-speed inference.
- **Persistent Memory:** Automatically stores conversation history in a local JSONL file (`~/.vagus/memory.jsonl`).
- **Context Injection:** Injects the last 5 conversation turns into every prompt to maintain continuity.
- **Universal Input:** Supports standard piping (`echo "logs" | vagus`) or command-line arguments.
- **Smart Retrieval:** Uses efficient `deque` loading to handle memory without parsing the entire history file.
- **Secure Configuration:** Zero config files; relies on `GEMINI_API_KEY` environment variables for security.

## Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/vagus.git](https://github.com/YOUR_USERNAME/vagus.git)
   cd vagus
