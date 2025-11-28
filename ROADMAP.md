# Vagus Roadmap

This document tracks planned engineering efforts and conceptual ideas for the future of Vagus.

## Planned Engineering (Short-Term)
- [ ] **Structured Memory Storage:** Move the memory file to a dedicated directory (`~/.vagus/sessions/`) to support named threads.
- [ ] **Session Management:** Add a `--session` flag to maintain distinct conversation contexts for different projects or sessions.

## Concepts & Exploration (Long-Term Ideas)
_These are experimental ideas that may or may not be implemented._

### User Experience
- [ ] **Interactive REPL:** A continuous "Chat Mode" loop to avoid restarting the script for every query.
- [ ] **Tmux Integration:** Ability to read/write directly to other tmux panes for context awareness.

## Cognitive Architecture
- [ ] **Temporal Context:** Implement Time-To-Live (TTL) Option for memories, so old context fades naturally over time.
- [ ] **"Amygdala" Layer:** Emotional tagging of memories to dynamically adjust their retention (TTL).
- [ ] **Hebbian Learning:** Keyword-based reinforcement to "refresh" old memories and keep them relevant.
- [ ] **Vector Embeddings:** Semantic search over the entire memory log for long-term recall beyond the immediate context window.
- [ ] **Multi-User Support:** Handling distinct user profiles within the same system.
