# On-call Handoff: <rotation> — <from date> → <to date>

**Outgoing:** <name>  **Incoming:** <name>

## Shift summary
- Pages: <count> (target ≤ 2 per 12h shift — SRE book Ch 11)
- Tickets / interrupts: <count>
- Incidents declared: <list with links>
- Error budget status: <per SLO, % consumed>

## Ongoing issues the incoming person must know
| Issue | Status | Next step | Link |
|---|---|---|---|

## Pages this shift
| Time (UTC) | Alert | Actionable? | Action taken | Follow-up (fix alert / bug / postmortem) |
|---|---|---|---|---|

## Changes in flight
<Deploys, migrations, config pushes, maintenance windows in the next shift.>

## Pager load review (Workbook Ch 8)
- Actionable pages / total pages: <x / y>
- Pages from **production bugs** (existing vs. newly introduced): 
- Pages from **alerting** (thresholds too tight, new alerts, dependency SLO misalignment): 
- Pages from **human processes** (manual prod changes, missed follow-ups): 
- Point fixes vs. systemic fixes still needed:

## Toil & alert hygiene
- Non-actionable or noisy alerts to tune or delete:
- Repeated manual tasks worth automating:

## Notes
