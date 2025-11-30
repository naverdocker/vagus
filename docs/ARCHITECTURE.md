# Vagus Architecture

This document outlines the high-level architecture and data flow of Vagus.

## Core Flow

Vagus operates as a pipeline that connects user input (from arguments or stdin) to a Large Language Model (LLM), manages context via a persistent memory file, and streams the response back to the terminal.

### High-Level Diagram

```mermaid
graph TD
    User((User)) -->|Input / Args| Main[Main Controller<br/>(main.py)]
    
    subgraph "Vagus Application"
        Main -->|1. Load History| Memory[Memory System<br/>(storage.py)]
        Memory -->|Context (Last N turns)| Main
        
        Main -->|2. Send Prompt + Context| LLM[LLM Core<br/>(llm.py)]
        
        LLM -->|3. API Request| LiteLLM(LiteLLM Library)
        LiteLLM -->|Stream| ExternalAPI((External LLM API))
        ExternalAPI -->|Response Stream| LiteLLM
        
        LiteLLM -->|4. Stream Output| LLM
        LLM -->|5. Calculate Cost| Cost[Cost Utils<br/>(cost.py)]
        
        LLM -->|6. Final Text| Main
        Main -->|7. Save Interaction| Memory
    end
    
    Memory -.->|Read/Write| Disk[(~/.vagus/memory.jsonl<br/>OR<br/>~/.vagus/sessions/*)]
    Main -->|Output| User
    Cost -.->|Stderr Info| User
```

## Key Components

1.  **Main Controller (`src/vagus/main.py`):**
    *   Entry point.
    *   Parses CLI arguments (including `--session`).
    *   Orchestrates the flow: Load Memory -> Query LLM -> Save Memory.

2.  **Memory System (`src/vagus/memory/storage.py`):**
    *   Manages conversation history.
    *   **Default:** Uses `~/.vagus/memory.jsonl`.
    *   **Sessions:** Uses `~/.vagus/sessions/<name>.jsonl` if `--session` is provided.
    *   Retrieves the last `N` interactions (sliding window) to maintain context.

3.  **LLM Core (`src/vagus/core/llm.py`):**
    *   Wraps `litellm` to support multiple providers (Gemini, OpenAI, Claude).
    *   Handles streaming responses to `stdout`.

4.  **Cost Utilities (`src/vagus/utils/cost.py`):**
    *   Calculates and prints session cost to `stderr`.
