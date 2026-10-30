# <Incident title>: YYYY-MM-DD

**Status:** Active | Mitigated | Resolved
**Last updated:** HH:MM UTC by <name>

## Declaration
- **Declared by / at:** <name>, HH:MM UTC  **Severity:** <SEV>
- **Declare early:** if in doubt, declare; it's cheap to downgrade (SRE book Ch 14, Workbook Ch 9).

## Command post
- **Incident Commander:** <name> (owns overall coordination; does not hands-on debug)
- **Operations lead:** <name> (only the ops team changes production)
- **Communications lead:** <name> (stakeholder & status-page updates every N min)
- **Planning lead:** <name> (bugs, handoffs, longer-term tracking)
- **War room / channel:** <link>

## Current status summary
<2–3 lines a newcomer can read to catch up.>

## Impact
<User-visible symptoms, scope, SLO burn.>

## Mitigation first
Before root-causing, can we stop user impact? Roll back the last change, drain or shift traffic, disable a feature flag, shed load. Note any recent changes (deploys, config pushes, flags) here:
- 

## Hypotheses & what's been tried
| Hypothesis | Test / action | Result | Owner |
|---|---|---|---|

## Next steps / exit criteria
- [ ]

## Timeline (UTC, most recent first)
- HH:MM —

## Stakeholder updates
| Time (UTC) | Audience | Channel | Summary |
|---|---|---|---|

## Handoff log
- HH:MM — IC role handed from <A> to <B>; B confirmed.

## After the incident
- [ ] All-clear declared and communicated.
- [ ] Temporary mitigations (flags, extra capacity, disabled retries) listed with owners to revert.
- [ ] Postmortem owner assigned (use `postmortem-template.md` + `postmortem-review-checklist.md`).
