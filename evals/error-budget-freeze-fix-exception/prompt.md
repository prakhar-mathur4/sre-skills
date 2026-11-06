---
tags: [skill-creator]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

need a call on releases for payments-api. SLO is 99.9% over a 28-day window that started on the 1st. on the 3rd we had a 31 minute incident (bad connection-pool setting pushed with a config change, checkout/charge requests failing the whole time). we're on day 10 of the window so 18 days left.

two things want to ship:
- the PM wants the loyalty-points feature out Thursday. there's a partner launch date with a contract penalty if we miss it.
- i have a fix for the pool setting plus a new connection-pool saturation alert, ready to ship Wednesday.

our team policy doc is attached. our CTO is in Tokyo this week (13+ hours ahead), so not easy to get live.

can we ship both? what do I tell the PM? and honestly how should freeze rules work, I don't want this to turn into a blanket ban every time we have a bad day.

Input files: error-budget-policy.md
