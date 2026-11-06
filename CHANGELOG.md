# Changelog

Notable changes to this skill. Versions follow [Semantic Versioning](https://semver.org/): a major version for changes that alter how the skill behaves in incompatible ways, a minor version for new templates or capabilities, a patch version for fixes.

## [Unreleased]

### Added
- Eval `clean-logs-recent-change`: an alert fires, app logs look clean, and the cause is a recent gateway config change.
- Eval `cert-expiry-alert-went-to-wrong-channel`: an expired certificate whose warning alert had no owner or page, while the monitoring-to-pager path had been silent for weeks.
- Eval `quota-cut-below-real-usage`: quota enforcement flips on, the dashboard reports zero usage, and logins fail.
- Eval `error-budget-freeze-fix-exception` (synthetic): an "at risk" error budget, a partner-dated feature, and a reliability fix, testing partial-freeze judgment.

## [1.0.0] - 2026-10-30

First public release.

### Added
- `SKILL.md`: responsible-SRE operating rules, work modes, topic routing to the SRE book, the Workbook and LinkedIn School of SRE.
- Templates: SLO document, error budget policy, incident state document, postmortem and postmortem review checklist, canary plan, launch checklist, capacity estimate worksheet, on-call handoff, reliability gap assessment.
- `scripts/sre_calc.py`: downtime, error budget (time and request based), multiwindow burn-rate thresholds, low-traffic check, serial/parallel availability.
- Six eval cases covering SLO design, alert review, postmortem writing, canary/config rollout, a live MySQL incident and a low-traffic SLO.
- Contribution guide, code of conduct, security policy, issue and pull request templates.
- Automated checks on every push and pull request (`tools/check_skill.py`) and calculator tests (`tests/`).

[Unreleased]: https://github.com/prakhar-mathur4/sre-skills/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/prakhar-mathur4/sre-skills/releases/tag/v1.0.0
