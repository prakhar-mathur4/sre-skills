# Error Budget Policy: payments-api

| Status | Owner | Date | Revisit date |
|---|---|---|---|
| Approved | Payments platform team (eng, product, SRE) | 2026-03-02 | 2027-03-02 |

## Scope
Covers every production change to payments-api: code releases, config pushes and data migrations. SLO: 99.9% of valid requests succeed, measured over a 28-day window that starts on the 1st of the month (day 10 is the 10th).

## Purpose
This policy helps us decide how much risk to take with releases. It is a decision tool for the team. It is not a penalty for having a bad incident.

## Tiers

1. **Healthy** (under 50% of budget used): normal release process.
2. **At risk** (50% or more of budget used, but not yet exhausted): risky changes need an extra reviewer and a canary rollout. Reliability bugs go to the top of the sprint. Feature launches need an explicit rollback plan and an on-call who knows about them.
3. **Exhausted** (100% of budget used): halt all releases except P0 incident fixes and security fixes until the service is back within SLO.

## Postmortems
Any single incident that uses more than 20% of the window's budget needs a written blameless postmortem, with at least one P0 action item aimed at the root cause.

## Escalation
If people disagree about the budget math, which tier applies, or whether a change may ship, the CTO decides. The decision and the reasoning are recorded in the release ticket.

## Reporting
Budget status is posted in #payments-eng every Monday.
