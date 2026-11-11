---
tags: [skill-creator]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

getting paged for payments-api, HighErrorRate firing since ~14:00. 5xx rate is 4.2% at the gateway (normally under 0.2%). weird thing is the app logs look totally clean, no stack traces, no ERROR lines. sample from one pod:

```
2026-11-02T14:12:07Z INFO  request completed method=POST path=/v1/charges status=200 duration_ms=212
2026-11-02T14:12:07Z INFO  request completed method=GET path=/v1/charges/ch_9f2 status=200 duration_ms=38
2026-11-02T14:12:08Z INFO  request completed method=POST path=/v1/charges status=200 duration_ms=461
2026-11-02T14:12:08Z INFO  upstream call ledger-service ok duration_ms=402
2026-11-02T14:12:09Z INFO  request completed method=POST path=/v1/refunds status=200 duration_ms=517
2026-11-02T14:12:09Z INFO  request completed method=GET path=/healthz status=200 duration_ms=1
```

pasting today's #deploys channel too in case it helps:

```
11:02 deploy-bot: ledger-service v4.18.0 -> prod (ci)
13:58 deploy-bot: api-gateway route config applied: payments.timeout 3000ms -> 300ms (platform-config #812)
14:05 deploy-bot: web-frontend v2.91.1 -> prod (ci)
```

since the app logs are clean could this just be a monitoring glitch? i have kubectl access. which logs should i dig into first?
