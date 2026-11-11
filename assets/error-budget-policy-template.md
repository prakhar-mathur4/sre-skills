# Error Budget Policy: <Service name>

| Status | Author | Date | Reviewers | Approvers (product, dev, SRE) | Approval date | Revisit date |
|---|---|---|---|---|---|---|
| Draft | | YYYY-MM-DD | | | | YYYY-MM-DD (≤ 1 year) |

Structure follows the Site Reliability Workbook, Appendix B and Ch 2.

## Service overview
<What the service does, release cadence (backend / clients / config), which releases this policy covers.>

## Goals
- Protect users from repeated SLO misses.
- Give an incentive to balance reliability with feature work.

## Non-goals
This policy is not a punishment for missing SLOs. Halting change is undesirable; the policy gives the team permission to focus on reliability when the data says reliability matters more than features.

## SLOs covered
<Link to the SLO document. Window length and type, e.g., 28 days, fixed.>

State whether the window is **fixed** (resets on a set date) or **rolling** (always the last N days). Everything below depends on it. A rolling window recovers continuously as old bad minutes age out, so "days left in the window" only makes sense for a fixed window.

## SLO miss policy
- **At or above SLO:** releases (including config and data changes) proceed per the normal release process.
- **Budget at risk** (more than **X%** of the window's budget used; example: X = 50%): the numbers are for your team to choose, not universal. Pick X from your own incident history, and consider also treating a sustained burn rate above 1x as at risk (`python3 scripts/sre_calc.py burn <slo> --window-days <N>` shows the rates that matter). In this tier:
  - risky changes need an extra reviewer and a canary;
  - reliability work is scheduled this sprint, not "when there's time";
  - feature launches need an explicit rollback plan and an on-call engineer who has been told about the launch;
  - any deadline-driven launch needs a written risk acceptance from the named escalation owner (see Escalation policy).
- **Budget exhausted over the preceding window:** freeze (see Freeze scope) until the service is back within SLO. Only the exceptions below may proceed.
- **The team must work on reliability** if:
  - the miss came from this service's own code or process (bug, bad rollout, manual mistake);
  - a postmortem shows a hard dependency that could be made soft (e.g., a fallback or cache);
  - miscategorised errors hid budget burn that would have caused a miss.
- **The team may continue feature work** if:
  - the outage was caused by a company-wide infrastructure/network problem;
  - the outage was caused by another team's service that has itself frozen releases;
  - the budget was consumed by out-of-scope traffic (load tests, pen tests);
  - miscategorised errors consumed budget with no user impact.

## Exceptions
- **May proceed during a freeze:** P0 fixes, security fixes, and reliability fixes that reduce the burn.
- **A fix is not exempt from safe-change rules.** Each one still goes through the normal process: canary or staged rollout, a rollback plan, and SRE approval. Rushed fixes are a common cause of the next outage.
- **A business or partner deadline is not an exception.** Take it to the escalation owner with the current burn numbers (budget used, budget left, burn rate); do not decide it inside the team.

## Freeze scope
A freeze covers feature launches and risky changes. It never blocks fixes, rollbacks or security patches: a freeze that blocks fixes only makes outages longer.

## Freeze exit criteria
The freeze ends when **all** of these hold:
- burn rate has been below **1x** for **N** days (example: N = 3);
- budget is back above **Z%** (example: Z = 50% remaining, or back below the at-risk threshold).

Only <role, e.g., SRE lead or service owner> may call the end of the freeze. Review the freeze status weekly, at the reporting meeting below.

## Outage policy
- A single incident consuming **> 20% of the error budget over the window** (the 20% is a placeholder; set your own) requires a blameless postmortem with at least one P0 action item addressing the root cause.
- A single **class** of outage consuming > 20% of budget over a quarter requires a P0 item in next quarter's planning.

## Escalation policy
Disagreements about the budget calculation or required actions escalate to <role, e.g., VP Eng / CTO>, who decides.

## Reporting
- Weekly: budget status per SLO, shared with <channel/meeting>.
- Quarterly: SLO performance review; revisit SLO targets and this policy.

## Background (for readers new to error budgets)
The error budget is 1 − SLO. If the SLO is 99.9% over 4 weeks, up to 0.1% of valid requests may fail in that window. Spending the budget on releases and experiments is fine; running out means users are seeing more failures than we agreed is acceptable.

## Worked example (illustrative, not a real service)
Assumptions: SLO 99.9% over a fixed 28-day window that started on the 1st. One incident causes 31 minutes of full unavailability.

```bash
python3 scripts/sre_calc.py budget 99.9 --days 28 --bad-minutes 31
# allowed downtime 40.3 min, budget consumed 76.9%, remaining 9.3 min
```

- **Tier:** at risk (77% is above the example X = 50%), but not exhausted, so the hard halt does not apply.
- **The fix** ships, behind a canary, with a rollback plan.
- **A partner-dated feature** goes to the escalation owner with these numbers, or ships behind a flag with staged exposure and written abort criteria.
- **The decision** is recorded in the release ticket.
- **Postmortem:** the incident used more than 20% of the budget, so a blameless postmortem with a P0 action item is required.
