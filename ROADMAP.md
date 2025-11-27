# Vagus Roadmap

## Short-Term
- [ ] **Flexible Input Combination:** Enable simultaneous piping of content *and* passing of arguments (e.g., `cat file | vagus --temp 0.5 "Fix this"`).
- [ ] **Structured Memory Storage:** Move the memory file to a dedicated directory (`~/.vagus/sessions/`) to support named threads.
- [ ] **Session Management:** Add a `--session` flag to maintain distinct conversation contexts for different projects.

## Mid-Term
- [ ] **Interactive REPL:** A continuous "Chat Mode" loop to avoid restarting the script for every query.
- [ ] **Temporal Context:** Implement Time-To-Live (TTL) for memories, so old context fades naturally over time.

## Long-Term
- [ ] **"Amygdala" Layer:** Emotional tagging of memories to dynamically adjust their retention (TTL).
- [ ] **Hebbian Learning:** Keyword-based reinforcement to "refresh" old memories and keep them relevant.
- [ ] **Vector Embeddings:** Semantic search over the entire memory log for long-term recall beyond the immediate context window.
- **Multi-User Support:** Handling distinct user profiles within the same system.
