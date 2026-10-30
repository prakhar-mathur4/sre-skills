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
<Link to the SLO document. Window: e.g., 4-week rolling.>

## SLO miss policy
- **At or above SLO:** releases (including config and data changes) proceed per the normal release process.
- **Budget at risk** (e.g., > 50% consumed with > half the window left): <e.g., extra review for risky changes, canary required for every change, reliability bugs prioritised in sprint>.
- **Budget exhausted over the preceding window:** halt all changes and releases other than P0 issues and security fixes until the service is back within SLO.
- **The team must work on reliability** if:
  - the miss came from this service's own code or process (bug, bad rollout, manual mistake);
  - a postmortem shows a hard dependency that could be made soft (e.g., a fallback or cache);
  - miscategorised errors hid budget burn that would have caused a miss.
- **The team may continue feature work** if:
  - the outage was caused by a company-wide infrastructure/network problem;
  - the outage was caused by another team's service that has itself frozen releases;
  - the budget was consumed by out-of-scope traffic (load tests, pen tests);
  - miscategorised errors consumed budget with no user impact.

## Outage policy
- A single incident consuming **> 20% of the error budget over the window** requires a postmortem with at least one P0 action item addressing the root cause.
- A single **class** of outage consuming > 20% of budget over a quarter requires a P0 item in next quarter's planning.

## Escalation policy
Disagreements about the budget calculation or required actions escalate to <role, e.g., VP Eng / CTO>, who decides.

## Reporting
- Weekly: budget status per SLO, shared with <channel/meeting>.
- Quarterly: SLO performance review; revisit SLO targets and this policy.

## Background (for readers new to error budgets)
The error budget is 1 − SLO. If the SLO is 99.9% over 4 weeks, up to 0.1% of valid requests may fail in that window. Spending the budget on releases and experiments is fine; running out means users are seeing more failures than we agreed is acceptable.
