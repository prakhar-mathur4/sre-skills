# <Service/Incident title> Postmortem (incident #<id>)

**Date:** YYYY-MM-DD
**Authors:** <names>
**Status:** Draft | In review | Complete, action items in progress | Closed
**Severity:** <SEV level>

## Summary
<One or two sentences: what broke, for how long, who noticed.>

## Impact
<Effect on users, revenue, SLOs, error budget consumed. Quantify: requests failed, users affected, duration, data lost.>

## Root causes and contributing factors
<The circumstances that allowed this to happen. Use "5 Whys" to go past the first answer. Describe systems and processes, not individuals — this is blameless.>

## Trigger
<Binary push, config push, user behaviour change, pipeline, provider change, performance decay, capacity, hardware (the trigger categories in Workbook App C).>
<The specific event that set it off (deploy, traffic spike, config push, dependency failure).>

## Detection
<How it was detected (alert name, customer report), and time-to-detect. Did monitoring work as intended?>

## Resolution
<What was done to mitigate and then fully fix.>

## Action items
| Action item (specific, verifiable) | Type (prevent / mitigate / detect / process) | Priority | Owner | Tracking | Status |
|---|---|---|---|---|---|
| | | P0 | | | TODO |

Mostly **preventive** items, at least one per major contributing factor, with different priorities. Include reverting any temporary mitigations still in place. (Workbook Ch 10)

## Lessons learned
### What went well
-
### What went wrong
-
### Where we got lucky
-

## Timeline (all times UTC; note the source timezone if converted)
| Time | Event |
|---|---|
| HH:MM | |

## Supporting information
<Links to dashboards, graphs, incident state doc, chat logs.>
