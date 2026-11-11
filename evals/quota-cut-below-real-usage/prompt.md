---
tags: [skill-creator]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

help, auth-service started throwing "storage quota exceeded" on writes about 10 minutes ago and roughly 60% of logins are failing. the capacity alert on the auth-db volume fired at 03:43 and paged me at 03:48. the quota dashboard for auth-db says usage 0 GB, limit 2 GB. I have admin on the quota service and kubectl. what do I do right now?
