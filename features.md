# Nerve Features

## Current Features
- **Gemini API Integration:** Utilizes the `gemini-2.0-flash` model for generating responses.
- **Persistent Conversation Memory:** Stores chat history locally in a JSON Lines (`.jsonl`) file (`nerve_memory.jsonl`).
- **Contextual Awareness:** Automatically injects the last 5 conversation turns into the prompt to maintain context.
- **Flexible Input:** Supports input via command-line arguments (`python3 nerve.py "query"`) or piping (`echo "query" | python3 nerve.py`).
- **Secure Configuration:** Uses environment variables (`GEMINI_API_KEY`) for API key management.
- **Efficient Memory Retrieval:** Uses `deque` to efficiently read only the relevant tail of the memory log.
- **Robust Error Handling:** Gracefully handles missing API keys, API request failures, and corrupted memory files.

## Past Features
*(None yet - this is the initial release)*

## Future Feature Options (Roadmap)
### Short-Term
- **Temporal Context:** Implement time-based forgetting (TTL) instead of just line-count limits.
- **Interactive Mode:** A continuous REPL (Read-Eval-Print Loop) mode to avoid restarting the script for every query.
- **Markdown Rendering:** formatting the output in the terminal for better readability.

### Long-Term
- **Dynamic Persistence ("Amygdala"):** Emotional tagging of memories to adjust their retention (TTL).
- **Hebbian Learning:** Keyword-based reinforcement to "refresh" old memories and keep them relevant.
- **Vector Embeddings:** Semantic search over the entire memory log for long-term recall beyond the immediate context window.
- **Multi-User/Session Support:** Handling distinct conversation streams or user profiles.
