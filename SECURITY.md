# Security Policy

## Reporting a problem

Please **don't open a public issue** for security problems. Report them privately through GitHub: [Report a vulnerability](https://github.com/prakhar-mathur4/sre-skills/security/advisories/new).

You can expect an acknowledgement within a few days and an update once the issue has been assessed.

## What counts

This repository is instructions and templates for AI agents that may run commands on production systems, so "security" includes unsafe guidance, not just code bugs:

- A template, card or instruction that leads an agent to run a **destructive or irreversible command** without warning, confirmation or a rollback plan.
- Content that could be used for **prompt injection**, e.g. text in a template or eval file that tells an agent to ignore its user, exfiltrate data or skip confirmations.
- **Secrets, credentials or personal data** accidentally committed to the repo.
- A bug in `scripts/sre_calc.py` that produces **dangerously wrong numbers**, e.g. alert thresholds that would never fire.

Ordinary bad advice (a threshold that's too noisy, a missing best practice) is welcome as a normal ["Bad SRE advice" issue](https://github.com/prakhar-mathur4/sre-skills/issues/new/choose).

## Supported versions

Only the latest release and the `main` branch receive fixes.

## Using this skill safely

- Give agents the least access they need; start with read-only credentials.
- Keep your tool's permission prompts on for commands that change production.
- Review alert rules and config changes before applying them, and roll them out the way the skill recommends (non-paging channel first, canary, rollback ready).
