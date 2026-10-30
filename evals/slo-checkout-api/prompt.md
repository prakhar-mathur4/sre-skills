---
tags: [skill-creator]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

we run a checkout API (node, on EKS, prometheus + grafana, pagerduty). roughly 40M requests a month. last month we had one 25 min full outage plus a bunch of slow periods where p99 went above 2s. product keeps asking for "five nines" lol. can you help me set proper SLOs for it, an error budget policy that eng and product can agree on, and what alerts we should page on? write it up as slo.md
