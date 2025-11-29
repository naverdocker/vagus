# Vagus
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/naverdocker/vagus?sort=semver)](https://github.com/naverdocker/vagus/releases)

> **The neural interface for your terminal.**

Vagus is a CLI-based AI utility that connects your terminal workflows directly to Large Language Models.


## Features

- **Multi-Model Support:** Uses litellm to route requests to Gemini, GPT-4, Claude or other local LLMs via the --model flag.

- **Streaming Response:** Instant, token-by-token output directly to the terminal.

- **Universal Input:** Seamlessly handles piped context and arguments simultaneously (cat logs | vagus "Fix this").

- **Persistent Memory:** Local JSONL-based persistence in ~/.vagus/.

- **Context Injection:** Automatically recalls the last 5 turns of conversation.


## Installation

### For Developers (Source)
Clone the repository:
   ```bash
   git clone https://github.com/naverdocker/vagus.git
   cd vagus
   ```

Install in Editable Mode:
   ```bash
   pip install -e .
   ```

### For Users (Direct Install)
Install Vagus directly from GitHub without cloning:
   ```bash
   pip install git+https://github.com/naverdocker/vagus.git
   ```

## Configuration
Set your API key (depending on the model used):
   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   # OR
   export OPENAI_API_KEY="your_api_key_here"
   ```


## Usage

### Interactive Mode:
Ask a quick question.
   ```bash
   vagus "How do I reverse a list in Python?"
   ```

### Pipeline Mode:
Pipe content from other tools directly into Vagus.
   ```bash
   # Debug a log file
   cat /var/log/syslog | vagus "Find the root cause of the error"
   # Explain a script
   cat deploy.sh | vagus "Explain what this script does"
   ```

### Switch Models:
Use different models supported by LiteLLM.
   ```bash
   vagus -m "gpt-4o" "Refactor this code"
   vagus -m "anthropic/claude-3-opus" "Write a poem"
   ```

## Roadmap
   See [ROADMAP.md](ROADMAP.md) for future plans and upcoming features.
