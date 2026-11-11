# Changelog

Notable changes to this skill. Versions follow [Semantic Versioning](https://semver.org/): a major version for changes that alter how the skill behaves in incompatible ways, a minor version for new templates or capabilities, a patch version for fixes.

## [Unreleased]

## [1.1.0] - 2026-11-11

### Added
- `assets/alerting-pipeline-health-checklist.md`: heartbeat (dead man's switch) alerts, an end-to-end test alert, owners for every alert route, separate failure domains, and a section on things that expire (certificates, credentials, quotas) with an emergency-reissue caution.
- Error budget policy template: a concrete "at risk" tier, exceptions (a fix is allowed but still goes through safe-change rules; a deadline is not an exception), freeze scope, freeze exit criteria and a worked example.
- Eval `clean-logs-recent-change`: an alert fires, app logs look clean, and the cause is a recent gateway config change.
- Eval `cert-expiry-alert-went-to-wrong-channel`: an expired certificate whose warning alert had no owner or page, while the monitoring-to-pager path had been silent for weeks.
- Eval `quota-cut-below-real-usage`: quota enforcement flips on, the dashboard reports zero usage, and logins fail.
- Eval `error-budget-freeze-fix-exception` (synthetic): an "at risk" error budget, a partner-dated feature, and a reliability fix, testing partial-freeze judgment.

### Changed
- `SKILL.md`: the warning marker now goes on every recommended production change, with owner, preconditions and undo; "what changed" covers config, data, policy, flag, quota and secret pushes and dormant settings, and says to inspect the effective value; "silence is not health" and expiring things need owners and pager-level alerts; budget decisions cite the policy tier.
- Gap assessment, launch checklist and canary plan: heartbeat and alert-ownership checks, an expiry inventory, and an effective-config check; the "certificate expiring in 14 days goes to tickets" rule is replaced.
- Eval `cert-expiry-alert-went-to-wrong-channel`: grader 01 reworded after the first run so mitigation must be the main plan but declaring the incident and a time-boxed look at the paging path may come first or run in parallel. Prompts for the cert and quota evals no longer state the cause.
- Evals `quota-cut-below-real-usage` (graders 02 and 07) and `error-budget-freeze-fix-exception` (grader 07) loosened after reading run traces: the responses were good but failed on ordering (read-only checks before the mitigation), a named owner when the user is the owner, and a PM-message grader that mixed several requirements (now: key numbers, a condition or fallback inside the message, no flat promise). Budget grader 07 failed 6/6 runs in both arms before the rewording, so it did not separate the skill from no skill. These were changed after seeing scores, so earlier scores for these graders are not comparable.
- `SKILL.md` rule 3: check what else the same shared-setting change touched.

### Fixed
- README: the description-length note (it is 1,017 characters, under the limit) and the eval benchmark claim, which now describes what was measured and its limits.
- `tools/check_skill.py` ignores `evals/results/`, which is also now gitignored.

## [1.0.0] - 2026-10-30

First public release.

### Added
- `SKILL.md`: responsible-SRE operating rules, work modes, topic routing to the SRE book, the Workbook and LinkedIn School of SRE.
- Templates: SLO document, error budget policy, incident state document, postmortem and postmortem review checklist, canary plan, launch checklist, capacity estimate worksheet, on-call handoff, reliability gap assessment.
- `scripts/sre_calc.py`: downtime, error budget (time and request based), multiwindow burn-rate thresholds, low-traffic check, serial/parallel availability.
- Six eval cases covering SLO design, alert review, postmortem writing, canary/config rollout, a live MySQL incident and a low-traffic SLO.
- Contribution guide, code of conduct, security policy, issue and pull request templates.
- Automated checks on every push and pull request (`tools/check_skill.py`) and calculator tests (`tests/`).

[Unreleased]: https://github.com/prakhar-mathur4/sre-skills/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/prakhar-mathur4/sre-skills/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/prakhar-mathur4/sre-skills/releases/tag/v1.0.0
