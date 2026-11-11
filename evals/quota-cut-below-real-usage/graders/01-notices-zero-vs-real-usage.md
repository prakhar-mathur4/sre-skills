---
type: llm
focus: trace
weight: 1
---

The response notices that the dashboard's 0 GB usage contradicts the failing writes and the real size of the database, says the reported metric cannot be trusted, and gives a read-only way to confirm actual usage (e.g., df -h on the DB host or a database size query) before relying on any number
