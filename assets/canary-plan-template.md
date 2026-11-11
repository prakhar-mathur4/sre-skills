# Canary Plan: <Change / release>

Based on Site Reliability Workbook Ch 16 (Canarying Releases) and Ch 14 (safe config changes). Applies to binaries **and** config changes — config pushes are the #2 outage trigger (Workbook App C).

**Change:** <what is changing; binary version / config diff link>
**Owner:** <name>  **Date/time window:** <avoid Fridays, holidays, peak traffic>
**Risk level:** low / medium / high — <why>

## Populations
- **Canary:** <e.g., 1 pod of 20 / 1% of traffic / one region / internal users>
- **Control:** <a concurrent, same-size slice on the old version — not "before vs after">
- Representative? <traffic mix, regions, client types covered>

## Stages
| Stage | Population | Minimum duration | Metrics judged | Promote if | Abort if |
|---|---|---|---|---|---|
| 1 | 1% | 30 min | crashes, 5xx ratio, error logs | canary ≤ control + X | any crash loop; 5xx ratio > 2× control |
| 2 | 10% | 2 h | + latency p50/p99, saturation | | |
| 3 | 50% | 4 h | + business metrics (checkout rate) | | |
| 4 | 100% | — | SLO burn rate | | |

Pick durations that fit release velocity (daily releases can't have week-long canaries) and the traffic rate (higher QPS → shorter time to a representative sample). Avoid overlapping canaries.

## Config and blast-radius checks (before stage 1)
- [ ] Diff the **rendered/effective config** in the running canary against control, not just the source diff. Redact secrets before pasting. Defaults, templates and overrides can make the live value differ from what was reviewed.
- [ ] Ask: **what does this change activate later or elsewhere?** Examples: a topology, policy, quota or data push that replicates globally; a dormant setting this change switches on; a shared config read by other services.
- **Abort if:** the effective diff contains anything not in the reviewed change, or the answer to "later or elsewhere" is unknown or reaches beyond the canary population.

## Metrics (≤ ~12, ranked by how well they show user-visible problems)
1. Error ratio (SLI) — canary vs control
2. Latency percentiles (SLI) — canary vs control
3. Crash/restart count
4. <Dependency error rates>
5. <Business metric>

Each must be **attributable** to the change (compare canary vs control at the same time) and have a defined acceptable range.

## Rollback
- **How:** <exact command / pipeline step / flag flip>
- **Time to roll back:** <minutes>; tested? <date>
- **Automatic rollback trigger:** <condition> — or at minimum automatic halt of progression.
- **Irreversible parts:** <schema/data migrations, external side effects> → how they are staged.

## Monitoring & communication
- Dashboard: <link showing canary vs control side by side>
- Who watches each stage: <name>
- Announce in: <channel>; incident process if aborted with user impact.

## Error budget check
Current budget remaining: <x%>. If the budget is exhausted, only P0/security changes proceed (see error budget policy).
