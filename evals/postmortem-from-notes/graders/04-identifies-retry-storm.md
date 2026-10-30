---
type: llm
focus: trace
weight: 1
---

postmortem.md identifies retry amplification (5x orders-api retries without backoff × 3x mobile retries) and DB connection exhaustion as contributing causes
