# SLO: <Service name>

| Status | Author | Date | Reviewers | Approvers (product, dev, SRE) | Approval date | Revisit date |
|---|---|---|---|---|---|---|
| Draft | | YYYY-MM-DD | | | | YYYY-MM-DD |

Structure follows the Site Reliability Workbook, Appendix A and Ch 2.

## Service overview
<What the service does, who its users are, the critical user journeys, and the architecture components in the request path.>

## SLIs and SLOs
Express every SLI as good events / valid events (so it reads 0–100%). Choose ≤ 5 SLI types.

| Category | SLI specification (good / valid) | SLI implementation (where measured) | SLO | Window |
|---|---|---|---|---|
| Availability | Proportion of valid requests served without a 5xx (or timeout) | Load balancer / ingress logs or metrics | 99.9% | 4-week rolling |
| Latency | Proportion of successful requests served faster than 300 ms | LB histogram, bucket `le=0.3` | 90% | 4-week rolling |
| Latency (tail) | Proportion of successful requests served faster than 1 s | LB histogram, bucket `le=1` | 99% | 4-week rolling |
| Freshness / correctness / coverage (pipelines) | | | | |
| Durability (storage) | | | | |

Notes:
- **Valid** excludes: <e.g., health checks, 4xx caused by client input, load-test traffic>.
- Implementation caveats: <e.g., LB logs miss requests that never reached the LB; client-side probes would catch DNS failures>.

## Rationale
<Why these targets. Where they came from (historical performance over the last N weeks), user expectations, dependency limits (your SLO can't exceed critical dependencies), cost of the next nine. Use `scripts/sre_calc.py`.>

## Error budget
| SLO | Budget per window | In requests (at current traffic) | In full-outage minutes |
|---|---|---|---|

Policy: see `<link to error budget policy>` (use `error-budget-policy-template.md`).

## Alerting
Multiwindow, multi-burn-rate alerts (Workbook Ch 5):

| Severity | Burn rate | Long / short window | Budget consumed when it fires |
|---|---|---|---|
| Page | 14.4 | 1 h / 5 m | 2% |
| Page | 6 | 6 h / 30 m | 5% |
| Ticket | 1 | 3 d / 6 h | 10% |

<If traffic is low, check `sre_calc.py lowtraffic` and see Workbook Ch 5 options.>

## Clarifications and caveats
<Known gaps, planned SLI improvements, dependencies whose SLOs we rely on.>
