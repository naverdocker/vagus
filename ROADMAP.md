# Vagus Roadmap

This document tracks planned engineering efforts and conceptual ideas for the future of Vagus.

## Changelog
- [x] **v0.1.0:** Initial Release with Streaming & Memory.
- [x] **v0.1.1:** Architectural Refactor (Modular package structure, `pip install` support).
- [x] **v0.1.2:** Cost Observability & File Redirection Support (`--no-stream`).
- [x] **v0.1.3:** Hardening & Robustness (Structured Memory Storage, Session Management, improved error handling).
- [x] **v0.2.0:** RAG Implementation (PDF Chat, Vector Store, Optional Dependencies).
- [x] **v0.2.1:** Maintenance & Optimization (Smart RAG Caching, ID Safety, Dependency Pinning).

## Planned Engineering (Short-Term)
- [ ] **Model Shortcuts:** Configurable aliases (e.g., `-m1` -> `gpt-4o`, `-m2` -> `groq/...`) for quick switching.
- [ ] **Docker Support:** Containerize Vagus for isolated testing and "run anywhere" usage.
- [ ] **Remote Embeddings:** Support OpenAI/Gemini embedding APIs to reduce local dependency weight.
- [ ] **CI/CD Pipeline:** Add GitHub Actions for automated linting, testing, and release builds.
- [ ] **Unit Test Suite:** Replace manual tests with a robust `pytest` suite.
- [ ] **Vector Search over History:** Extend RAG to index long-term conversation history (moving beyond the 5-turn limit).

## Concepts & Exploration (Long-Term Ideas)
_These are experimental ideas that may or may not be implemented._

### User Experience
- [ ] **Interactive REPL:** A continuous "Chat Mode" loop to avoid restarting the script for every query.
- [ ] **Tmux Integration:** Ability to read/write directly to other tmux panes for context awareness.

### Cognitive Architecture
- [ ] **Temporal Context:** Implement Time-To-Live (TTL) Option for memories, so old context fades naturally over time.
- [ ] **"Amygdala" Layer:** Emotional tagging of memories to dynamically adjust their retention (TTL).
- [ ] **Hebbian Learning:** Keyword-based reinforcement to "refresh" old memories and keep them relevant.
- [ ] **Multi-User Support:** Handling distinct user profiles within the same system.
