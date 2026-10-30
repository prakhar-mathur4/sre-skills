# `sre`: a Site Reliability Engineering skill for Claude

This skill makes Claude work like an experienced, careful SRE. It bases its advice on three sources:

- **Site Reliability Engineering** (Google, 2016): the principles.
- **The Site Reliability Workbook** (Google, 2018): how to put them into practice.
- **LinkedIn School of SRE**: hands-on commands for Linux, networking, MySQL and message queues.

Claude doesn't give generic advice with this skill. It applies the books' specific rules to your stack and your numbers, says which chapter each rule comes from, and does the error-budget math with a calculator.

---

## What it helps with

| You ask for… | Claude will… |
|---|---|
| **Fixing a live problem.** "p99 jumped to 4s, replica lag is growing, help!" | Stop the user impact first (roll back, pause the suspect job, shed load), then run read-only checks. Each risky command is marked ⚠️ with what it needs first, and Claude tells you how to confirm the fix worked. |
| **SLOs and error budgets** | Choose SLIs based on what users experience, set realistic targets (and push back on "five nines" with numbers), work out the budget, and write an error budget policy that product, dev and SRE can agree on. |
| **Alerting** | Set up paging when the error budget is burning too fast, with fixes for low-traffic services. Alerts that don't need someone right away become tickets. Prometheus rules included. |
| **Reviewing your setup** | Go through alert rules, runbooks, dashboards, on-call rotations, deploy processes and architectures. Findings come highest-impact first, each with a concrete fix. |
| **Finding reliability gaps** | "What's missing to make this system reliable?" Map each component against SLOs, monitoring, alerting, redundancy, overload protection, deploy safety, backups and on-call, then recommend SLIs, alert rules and dashboards (gap assessment template). |
| **Incidents and postmortems** | Run the incident with clear roles and a single live incident doc, then write a blameless postmortem (UTC timeline, trigger separated from causes, owned and typed action items) and check it against a review checklist. |
| **Releases and config changes** | Write a canary plan with a comparison group running the old version at the same time, abort criteria and a rollback plan. Config gets the same gradual, reversible rollout as code. |
| **Capacity and design** | Estimate machines, disk and network with real numbers, plan to survive two failures (N+2), and check what happens when each failure domain is lost. |
| **Overload and resilience** | Design retry limits, deadlines, load shedding, and protection against one failure spreading to other services. |
| **Data** | Plan backups that you actually test restoring, set up MySQL replication and find slow queries, design safe pipeline and queue consumers. |
| **SRE teams** | Size on-call rotations, reduce toil, set up how SRE works with dev teams, and start a new SRE team. |

You don't need to say "SRE". The skill kicks in for any reliability or production-operations question.

---

## How Claude behaves with this skill

These rules come from the books. They're what keeps the skill safe to use near production:

1. **Mitigate first, debug second.** Roll back, drain traffic or disable a feature flag before hunting for the root cause.
2. **Know the blast radius.** Before any command, Claude says what it affects, whether it can be undone, and how. It starts with read-only checks.
3. **Change safely.** Changes are gradual, observable and reversible. Code and config pushes cause about 68% of outages at Google.
4. **Confirm before acting.** If Claude has access to production, it asks before any change or destructive step.
5. **Verify, don't assume.** It checks that the user-facing signal has actually recovered, and keeps what it saw separate from what it suspects.
6. **Communicate.** Declare incidents early, assign roles, and send regular updates.
7. **Blameless always.** Look at what the system and process allowed, not at who did it.
8. **Reliability is a budget.** The goal isn't maximum reliability; it's the right target for your scale.
9. **Leave it better.** Every page leads to a fix, and every incident to action items with owners.

---

## What's inside

```
sre/
├── SKILL.md                      Instructions Claude follows (rules, modes, topic table)
├── README.md                     This file
├── LICENSE, LICENSE-docs, NOTICE
├── assets/                       Templates Claude fills in
│   ├── slo-document-template.md
│   ├── error-budget-policy-template.md
│   ├── postmortem-template.md
│   ├── postmortem-review-checklist.md
│   ├── incident-state-document-template.md
│   ├── canary-plan-template.md
│   ├── launch-checklist.md
│   ├── capacity-estimate-worksheet.md
│   ├── oncall-handoff-template.md
│   └── reliability-gap-assessment.md
├── scripts/
│   └── sre_calc.py               Calculator for availability and error budgets
└── evals/                        6 test cases used to check the skill
```

Claude reads only what it needs: `SKILL.md` first, then the template or calculator the task calls for. It cites the books by chapter, so you can look up the source; both books are free to read online at [sre.google/books](https://sre.google/books/).

**Optional local `references/` folder.** The skill can also use a `references/` folder (a one-page `principles.md`, short School of SRE troubleshooting cards, and chapter text of the books). It is not in this repo because it includes copyrighted book text. If you build your own from books you own, put it at `sre/references/` and the skill will read it; `.gitignore` keeps it out of commits.

---

## The calculator

You can use it directly. It needs only Python 3.

```bash
cd sre
python3 scripts/sre_calc.py downtime 99.95
#   allowed downtime per hour/day/week/month/quarter/year

python3 scripts/sre_calc.py budget 99.9 --days 28 --bad-minutes 25
#   how much of the error budget an outage used

python3 scripts/sre_calc.py requests 99.9 --total 4.2e7 --failed 31000
#   the same, counted in requests

python3 scripts/sre_calc.py burn 99.9 --window-days 28
#   burn-rate thresholds for pages and tickets (Workbook Ch 5)

python3 scripts/sre_calc.py lowtraffic 99.9 --rps 0.003
#   is this service too quiet for burn-rate paging?

python3 scripts/sre_calc.py compose --serial 99.95 99.9 --parallel 99.5 99.5
#   combined availability of services in a chain and redundant copies
```

---

## Installing

The skill follows the open **Agent Skills** format: a folder with a `SKILL.md` and its supporting files. Any tool that reads that format can use it, including Claude Code, OpenAI Codex, Cursor, Google Antigravity, GitHub Copilot and Gemini CLI. Nothing in it is specific to Claude. The calculator only needs `python3`.

### Where each tool looks

| Tool | One project | All your projects | Call it directly |
|---|---|---|---|
| **Claude Code** | `<project>/.claude/skills/sre/` | `~/.claude/skills/sre/` | `/sre` or "use the sre skill" |
| **OpenAI Codex** | `<project>/.agents/skills/sre/` | `~/.codex/skills/sre/` ¹ | `$sre` |
| **Cursor** | `<project>/.cursor/skills/sre/` or `<project>/.agents/skills/sre/` | — | mention the skill in chat |
| **Google Antigravity** | `<project>/.agent/skills/sre/` | `~/.gemini/antigravity/skills/sre/` | mention the skill in chat |
| **GitHub Copilot** | `<project>/.github/skills/sre/` | `~/.copilot/skills/sre/` | mention the skill in chat |
| **Gemini CLI** | `<project>/.gemini/skills/sre/` | — | mention the skill in chat |

¹ Codex reads `$CODEX_HOME/skills` (which defaults to `~/.codex/skills`). Tools change these paths from time to time, so check the tool's current docs if the skill doesn't show up.

### Option A: one shared copy, linked into each tool (recommended)

Keep the skill in one place and link it into each tool, so one update reaches all of them:

First get the skill:

```bash
git clone https://github.com/<your-username>/<repo>.git ~/sre-skill
```

Then link it:

```bash
SKILL=~/sre-skill

# Claude Code
mkdir -p ~/.claude/skills && ln -s "$SKILL" ~/.claude/skills/sre

# OpenAI Codex
mkdir -p ~/.codex/skills && ln -s "$SKILL" ~/.codex/skills/sre

# Google Antigravity
mkdir -p ~/.gemini/antigravity/skills && ln -s "$SKILL" ~/.gemini/antigravity/skills/sre

# GitHub Copilot
mkdir -p ~/.copilot/skills && ln -s "$SKILL" ~/.copilot/skills/sre
```

Cursor and Gemini CLI read skills from inside each project. Link the skill into each project where you want it:

```bash
cd /path/to/your/project
mkdir -p .cursor/skills && ln -s ~/sre-skill .cursor/skills/sre   # Cursor
mkdir -p .gemini/skills && ln -s ~/sre-skill .gemini/skills/sre   # Gemini CLI
```

### Option B: copy it

If a tool doesn't follow symlinks, copy the folder instead (you'll need to re-copy after updates):

```bash
cp -R ~/sre-skill ~/.claude/skills/sre
```

### Check it's installed

1. Restart the tool, or start a new session or chat.
2. Ask an SRE question, e.g. *"Our API does 10M requests a month. Help me pick an SLO and error budget."*
3. The answer should cite chapters like *(Workbook Ch 2)* and use `scripts/sre_calc.py` for the numbers. If it doesn't, call the skill directly (see the table above).

### Keep it out of shared repos

If you install it inside a project, keep the skill folder out of that project's commits (especially if you added a local `references/` folder):

```bash
# in the project root
echo ".claude/skills/sre/"  >> .gitignore
echo ".agents/skills/sre/"  >> .gitignore
echo ".cursor/skills/sre/"  >> .gitignore
echo ".agent/skills/sre/"   >> .gitignore
echo ".github/skills/sre/"  >> .gitignore
echo ".gemini/skills/sre/"  >> .gitignore
```

The global folders in your home directory (Option A) avoid this problem entirely.

### Differences between tools

- **When it triggers:** each tool decides from the skill's `description` whether to load it, so it may kick in more or less often outside Claude Code. Calling it directly always works.
- **Description length:** the Agent Skills format limits `description` to 1,024 characters. This skill's description is currently longer, and some tools may cut it off or reject the skill. If a tool won't load it, shorten the `description` in `SKILL.md` to under 1,024 characters.
- **Asking before production changes:** the skill tells the agent to ask before any change to production, but whether a command actually runs without asking depends on each tool's own permission settings. Keep those on "ask" when the agent has production access.

---

## Example prompts

- "Our checkout API does 40M requests a month and product wants five nines. Help me set SLOs and an error budget policy."
- "Here's our Prometheus rules file; on-call gets 30 pages a week. What's wrong with it?"
- "Turn these Slack incident notes into a postmortem."
- "We're shipping v2.3 and a rate-limit config change Friday at 4pm. Write the rollout plan."
- "orders-api p99 is 4s and MySQL replica lag is 900s and climbing. What do I do right now?"
- "Our internal admin API gets 200 requests a day. Should it have the same SLO and paging as the public API?"
- "Here's our Terraform, K8s manifests and Prometheus rules for the payments service. What's missing to make it reliable? Suggest SLOs, alerts and dashboards."
- "How many engineers do we need for a sustainable 24/7 on-call?"
- "Estimate the servers and storage for ingesting 2 TB of logs a day with 30-day retention."

---

## Testing

The `evals/` folder has 6 realistic test cases: SLO design, an alert review, a postmortem, a canary rollout, a live MySQL incident, and a low-traffic SLO. Each one has pass/fail checks. They were run with and without the skill, and the results are in `../sre-workspace/`.

With Claude Code you can rerun them yourself:
```bash
cd sre && claude plugin eval . --allow-tools Write,Edit,Bash --scaffold
```

---

## Notes and limits

- **The Google books are from 2016 and 2018** and describe Google's own tools (Borg, Borgmon, Chubby). Claude translates them to Kubernetes, Prometheus, Datadog, PagerDuty and so on, and treats the Workbook as newer where the two books differ.
- **Corrections to the sources.** The Workbook's low-traffic example says a "1,000x" burn rate where the arithmetic gives 100x. School of SRE has an error in TIME_WAIT timing, one in an XtraBackup restore step, and a wrong definition of differential backups. The skill uses the corrected figures.
- **Claude's advice is still advice.** Check metric names, labels and thresholds against your own system before shipping. Test new alert rules (e.g. with `promtool test rules`) and run them in a non-paging channel first.

---

## Licensing

- **Code** (`scripts/`): [MIT](LICENSE).
- **Content** (`SKILL.md`, `README.md`, `assets/`, `evals/`): [CC BY 4.0](LICENSE-docs). Reuse it freely with credit.
- **Sources.** The skill cites *Site Reliability Engineering* (© Google, 2016) and *The Site Reliability Workbook* (© Google LLC, 2018), both published by O'Reilly Media, and draws on [LinkedIn School of SRE](https://linkedin.github.io/school-of-sre/) (CC BY 4.0). No book text is included. See [NOTICE](NOTICE) for full attribution. This project isn't affiliated with or endorsed by Google, O'Reilly or LinkedIn.
