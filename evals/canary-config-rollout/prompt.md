---
tags: [skill-creator]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

we need to ship two things friday ~4pm: bump our node orders-service from v2.2 to v2.3 (20 pods on EKS, argo rollouts available but we never set it up) and change the nginx ingress config to lower the rate limit from 500 to 200 req/s per client because of some abuse. can you write the rollout plan? save as rollout-plan.md
