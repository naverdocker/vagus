# Vagus Roadmap

This document tracks planned engineering efforts and conceptual ideas for the future of Vagus.

## Changelog
- [x] **v0.1.0:** Initial Release with Streaming & Memory.
- [x] **v0.1.1:** Architectural Refactor (Modular package structure, `pip install` support).
- [x] **v0.1.2:** Cost Observability & File Redirection Support (`--no-stream`).
- [x] **v0.1.3:** Hardening & Robustness (Structured Memory Storage, Session Management, improved error handling).

## Planned Engineering (Short-Term)
- [ ] **Vector Embeddings (RAG):** Implement semantic search over long-term history (moving beyond the 5-turn limit).


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
