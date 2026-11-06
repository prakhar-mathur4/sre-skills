---
type: llm
focus: trace
weight: 1
---

The response says how to verify the fix from outside the network (e.g. openssl s_client or curl against each hostname and each load balancer, checking the full chain, the SAN list covers both names, and the new notAfter date), rather than only trusting the load balancer config or a local check
