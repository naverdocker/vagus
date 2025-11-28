# Vagus
![GitHub release (latest by date)](https://img.shields.io/github/v/release/naverdocker/vagus)

> **The neural interface for your terminal.**

Vagus is a CLI-based AI utility that connects your terminal workflows directly to Large Language Models.


## Features

- **Multi-Model Support:** Uses litellm to route requests to Gemini, GPT-4, Claude or other local LLMs via the --model flag.

- **Streaming Response:** Instant, token-by-token output directly to the terminal.

- **Universal Input:** Seamlessly handles piped context and arguments simultaneously (cat logs | vagus "Fix this").

- **Persistent Memory:** Local JSONL-based persistence in ~/.vagus/.

- **Context Injection:** Automatically recalls the last 5 turns of conversation.


## Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/naverdocker/vagus.git](https://github.com/YOUR_USERNAME/vagus.git)
   cd vagus
   ```

2. Installation dependencies
   ```bash
   pip install litellm
   ```

3. Set your API key (depending on the model used):
   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   # OR
   export OPENAI_API_KEY="your_api_key_here"
   ```


## Usage

### Interactive Mode:Ask a quick question.
    ```bash
    python3 vagus.py "How do I reverse a list in Python?"
    ```

### Pipeline Mode: Pipe content from other tools directly into Vagus.
    ```bash
    # Debug a log file
    cat /var/log/syslog | python3 vagus.py "Find the root cause of the error"
    # Explain a script
    cat deploy.sh | python3 vagus.py "Explain what this script does"
    ```

### Switch Models:Use different models supported by LiteLLM.
    ```bash
    python3 vagus.py -m "gpt-4o" "Refactor this code"
    python3 vagus.py -m "anthropic/claude-3-opus" "Write a poem"
    ```

## Roadmap
    See [ROADMAP.md](roadmap.md) for future plans and upcoming features.
