---
type: llm
focus: trace
weight: 1
---

The response marks load balancer changes with a warning marker (⚠️) and states the blast radius (both load balancers serve all traffic, so change one at a time) and how to roll back (e.g. keep the old certificate and config, validate config before reload, how to revert)
