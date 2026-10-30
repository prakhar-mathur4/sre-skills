# Postmortem Review Checklist

Run every postmortem draft through this before calling it done. Based on the Site Reliability Workbook Ch 10 ("bad" vs "good" postmortem) and SRE book Ch 15.

## Blamelessness
- [ ] No individual is blamed. People appear by role, or are named only for factual actions in the timeline, framed neutrally.
- [ ] Phrases like "X should have…" are rewritten as system/process gaps ("nothing in the process required…").
- [ ] Human error, where present, is treated as a symptom: what allowed the error, and what would have caught it?

## Context and impact
- [ ] A reader with no prior context can understand the system involved (brief architecture, links).
- [ ] Impact is quantified: duration, users or requests affected, revenue or orders, data loss, SLO and error budget consumed.
- [ ] Inconsistencies in the source data are flagged as open questions, not silently resolved.

## Timeline
- [ ] Timeline is in UTC, with the source timezone noted.
- [ ] It covers trigger, detection, escalation, key decisions, mitigation, recovery and all-clear.
- [ ] Key intervals are stated: time to detect, time to mitigate, time to resolve.

## Causes
- [ ] The trigger is separated from the root causes and contributing factors.
- [ ] Causes go past the first "why" (5 Whys), into process, tooling and design gaps.
- [ ] Anything that made the incident worse during response (e.g., a mitigation that backfired) is analysed.
- [ ] Detection is evaluated: did monitoring catch it, and how fast? Were alerts symptom-based?

## Action items
- [ ] Every item is specific and verifiable. "Improve", "investigate" or "look into" only appear with a concrete outcome.
- [ ] Every item has an owner, a priority (not all the same priority) and a tracking link or bug.
- [ ] Items are typed: prevent / mitigate / detect / process.
- [ ] The set is **mostly preventive**, not only mitigative, and addresses the root causes, not just the trigger.
- [ ] There's at least one item per major contributing factor.
- [ ] Temporary mitigations still in place (flags, extra capacity) have an item to resolve them.

## Lessons
- [ ] Covers what went well, what went wrong, and where we got lucky.

## Process
- [ ] Reviewed by someone outside the incident.
- [ ] Shared widely: postmortems are for the org to learn from.
- [ ] Action item follow-up date set.
