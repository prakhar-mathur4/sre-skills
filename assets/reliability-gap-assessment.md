# Reliability Gap Assessment: <System / service>

Use this to find what's missing on the infra and operations side, and to recommend monitoring and alerting. Based on SRE book Ch 6, 10, 21, 22, 26, 27, 32 and App E; Workbook Ch 4, 5, 18. For a brand-new service going live, also run `launch-checklist.md`.

**Assessed by:** <name>  **Date:** <YYYY-MM-DD>  **Scope:** <services, environments, regions>
**Evidence reviewed:** <architecture doc, Terraform/K8s manifests, alert rules, dashboards, runbooks, deploy pipeline, backup jobs, incident history>
**Not reviewed / no access:** <list — findings below can't cover these>

Mark each item: ✅ in place · ⚠️ partial · ❌ missing · ❓ unknown (needs verification). Only mark ✅ for something you actually saw (config, dashboard, test record), not something you were told.

## 0. Context
- What users do with the system, and the critical user journeys (e.g., login, search, checkout):
- Traffic: peak and average RPS per journey; low-traffic paths (< ~100 failures allowed per window — check with `sre_calc.py lowtraffic`):
- Existing SLOs/SLAs and contractual commitments:
- Recent incidents (last 6–12 months) and their triggers:
- Owning team(s) and on-call rotation:

## 1. Architecture and dependency map
List every component on the critical path, including third parties.

| Component | Role | Owner | Runs where (region/zone) | Instances | Critical deps | Stateful? |
|---|---|---|---|---|---|---|
| | | | | | | |

## 2. Coverage matrix (one row per component)

| Component | SLI defined | SLO + error budget | Golden signals monitored | Symptom-based paging | Runbook linked | Dashboard | Redundancy (N+2 / multi-zone) | Timeouts + retry budget | Safe deploy (canary + rollback) | Backups + tested restore | On-call owner |
|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | | |

## 3. Area checks

### 3.1 SLOs and error budgets (SRE book Ch 3–4; Workbook Ch 2, App A–B)
- [ ] SLIs measure user experience (ratio of good events / valid events), close to the user (load balancer or client, not just the server).
- [ ] SLO per critical journey, with a window (e.g., 28 days) and a target lower than "five nines" unless justified.
- [ ] Written error budget policy: what happens when the budget is spent.

### 3.2 Monitoring (SRE book Ch 6; Workbook Ch 4)
- [ ] Four golden signals per user-facing service: latency (percentiles, split success/failure), traffic, errors, saturation.
- [ ] Latency as histograms with buckets at the SLO thresholds — not averages.
- [ ] Dependency health visible (DB, cache, queue, third-party APIs): latency, errors, saturation, connection pools.
- [ ] Saturation signals with headroom: CPU throttling, memory vs limit, disk fill rate, file descriptors, queue depth/consumer lag, DB replication lag.
- [ ] Black-box (synthetic) probes for critical journeys and for low-traffic paths.
- [ ] Monitoring itself is monitored (scrape failures, missing data, meta-alert if the alerting pipeline is down).
- [ ] Logs and traces are retained long enough to debug and are linked from dashboards.

### 3.3 Alerting (SRE book Ch 6, 10; Workbook Ch 5)
- [ ] Pages are on symptoms (SLO burn), not causes (CPU high, pod restarted).
- [ ] Multiwindow, multi-burn-rate alerts (`sre_calc.py burn <slo> --window-days <n>`): page on fast burn, ticket on slow burn.
- [ ] Every page is actionable, urgent and has a runbook link; no page that's routinely ignored.
- [ ] Cause-based signals (disk 80%, cert expiring in 14 days) go to tickets, not pages — except ones that will cause an outage before a human can react.
- [ ] Low-traffic services: synthetic traffic, grouping or a longer window instead of paging on single errors.
- [ ] Alert routing tested: the page actually reaches a human (escalation, secondary).

### 3.4 Redundancy and failure domains (SRE book Ch 22, 23, 26; Workbook Ch 12)
- [ ] No single point of failure: every component survives losing one instance, one zone; decide explicitly on one region.
- [ ] N+2 capacity at peak (one planned + one unplanned loss).
- [ ] Stateful systems: replication, automatic or rehearsed failover, quorum sized for failure domains.
- [ ] Dependencies on shared services (DNS, auth, config, secrets) have a plan for when they're slow or down.

### 3.5 Overload and cascading failure (SRE book Ch 21, 22; Workbook Ch 11)
- [ ] Every outbound call has a deadline/timeout, propagated downstream.
- [ ] Retries: limited per request (~3), with exponential backoff and jitter, retry budget per client (< ~10%), at one layer only.
- [ ] Load shedding / rate limiting at the edge; graceful degradation for non-critical features.
- [ ] Autoscaling has limits and doesn't exhaust a shared dependency (DB connections).
- [ ] Health checks don't take down healthy instances (liveness doesn't depend on dependencies).
- [ ] Load tested to find the breaking point; capacity plan covers 12–24 months of growth.

### 3.6 Change safety (SRE book Ch 8; Workbook Ch 14, 16, App C)
- [ ] Deploys are progressive (canary with a concurrent control group), with automatic halt or rollback.
- [ ] Config and feature-flag changes get the same gradual, reversible rollout as code.
- [ ] Rollback is one step, tested, and takes minutes.
- [ ] Irreversible changes (schema/data migrations) are staged and backward-compatible.
- [ ] Infra-as-code is reviewed and has drift detection; no manual production changes without a record.

### 3.7 Data integrity (SRE book Ch 26; Workbook Ch 13)
- [ ] Backups for every stateful store, with defined RPO/RTO.
- [ ] Restores are tested on a schedule and timed (an untested backup isn't a backup).
- [ ] Protection against deletion and corruption (soft delete, point-in-time recovery, offsite/immutable copies).
- [ ] Pipelines/queues: idempotent consumers, dead-letter queue monitored, data freshness SLO.

### 3.8 Operations and people (SRE book Ch 11, 14, 15, 29; Workbook Ch 8, 9, 10)
- [ ] On-call rotation is sustainable (enough people; pager load reviewed).
- [ ] Incident process: declared roles (IC, ops, comms), a single incident doc, stakeholder updates.
- [ ] Blameless postmortems with owned, tracked action items — and they get done.
- [ ] Runbooks are current and tested in drills (DiRT / game days, failover tests).
- [ ] Toil is measured and capped (~50%).

## 4. Findings (highest user impact first)

| # | Gap | Area | Risk (what breaks, for whom, how likely) | Evidence | Fix (for this stack) | Effort | Priority | Source |
|---|---|---|---|---|---|---|---|---|
| 1 | | | | | | S/M/L | P0/P1/P2 | |

## 5. Recommended monitoring and alerting

### SLIs and SLOs
| Journey | SLI (good / valid) | Measured at | SLO | Window |
|---|---|---|---|---|
| | | | | |

### Alerts
| Alert | Condition (exact rule or query) | Severity (page / ticket) | Why it matters | Runbook |
|---|---|---|---|---|
| <journey> fast burn | burn rate > <x> over <long> AND <short> | page | | |
| <journey> slow burn | burn rate > <y> over <long> AND <short> | ticket | | |
| | | | | |

Include the rules themselves in the user's format (Prometheus, Datadog, New Relic…), with metric names marked as assumptions to verify.

### Dashboards
- Service overview: SLO status and remaining budget, golden signals, deploy markers.
- Dependencies: per-dependency latency, errors, saturation.
- Capacity: utilisation vs N+2 headroom, growth trend.

## 6. Plan
- **Quick wins (this week):**
- **Next 1–3 months:**
- **Longer-term / needs design:**

## 7. Rollout of the recommendations
- New alerts run in a non-paging channel for ~1 week; compare against real incidents before switching to paging.
- Remove or demote old noisy alerts only after the replacements are live.
- Any infra change follows the canary/rollback rules above.

## 8. Assumptions and open questions
| Assumption / question | How to verify | Owner |
|---|---|---|
| | | |
