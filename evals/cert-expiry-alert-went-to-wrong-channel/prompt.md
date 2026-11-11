---
tags: [skill-creator]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

everything is on fire. since 17:56 UTC browsers show "your connection is not private" on app.shop.example and api.shop.example, the mobile app is throwing SSL errors, support has 140 tickets in 25 min. both hostnames share one cert on our two load balancers (lb-eu-1, lb-eu-2). i checked and the cert's notAfter was today 17:56.

the person who bought it from the commercial CA did it by hand last year and has since moved teams. we're moving to Let's Encrypt via cert-manager but nobody has issued one from it yet, this would be the first. i can ssh to both load balancers.

also, our probe rules are in the attached file. i also noticed the pager app has no events from our monitoring since 1 Jul 09:12 (today is 30 Jul), but figured that's just a quiet month.

what do i do right now, and what should we change afterwards?

Input files: probe-rules.yaml
