# Contributing

Thanks for helping make this skill better. Corrections from people who run production systems are the most valuable contributions here: if the skill gave advice that would hurt in the real world, we want to know.

## Ways to help

- **Report bad advice.** Open a ["Bad SRE advice" issue](../../issues/new/choose) with the prompt, what the agent said, and what a good SRE would have done.
- **Report a bug** in the calculator, templates or install steps.
- **Suggest a topic or template** (e.g., a new runbook template, a Kubernetes card, Datadog examples).
- **Send a pull request** with a fix or addition.
- **Ask questions** in [Discussions](../../discussions), not issues.

## Ground rules (please read)

1. **Never paste text from the SRE books.** *Site Reliability Engineering* and *The Site Reliability Workbook* are copyrighted ("All rights reserved"). Summarise ideas in your own words and cite the chapter, e.g. `(Workbook Ch 5)`. PRs containing copied passages will be closed.
2. **Credit other sources.** Material adapted from CC BY sources (like LinkedIn School of SRE) needs attribution in the file and in [NOTICE](NOTICE). Don't add material whose license doesn't allow reuse.
3. **Keep it safe near production.** Anything that changes a system must say what it affects, whether it can be undone, and how. Mark risky commands with ⚠️ and start with read-only checks. Don't weaken the "Operating as a responsible SRE" rules in `SKILL.md`.
4. **Be specific and verifiable.** Real numbers, real thresholds, real commands. Check any math with `scripts/sre_calc.py`.
5. **Stay tool-neutral.** The skill works in Claude Code, Codex, Cursor, Copilot, Antigravity and Gemini CLI. Don't add instructions that only make sense for one agent.
6. **Keep `SKILL.md` lean.** Its description must stay under 1,024 characters. Put detail in `assets/` templates rather than growing `SKILL.md`.

## Making a change

```bash
git clone https://github.com/prakhar-mathur4/sre-skills.git
cd sre-skills
git checkout -b my-change

# ...edit...

pip install pyyaml
python3 tools/check_skill.py              # structure, links, frontmatter, private files
python3 -m unittest discover -s tests     # calculator tests
```

Then open a pull request. The same checks run automatically on every PR.

### What to include

| If you change… | Also… |
|---|---|
| `scripts/sre_calc.py` | Add or update a test in `tests/test_sre_calc.py`, with the expected value worked out by hand. |
| A template in `assets/` | Make sure `SKILL.md`'s templates table and the README still match. |
| Behaviour in `SKILL.md` | Add or update a case in `evals/` that shows the new behaviour, and describe in the PR how you tested it with an agent. |
| Anything user-facing | Add a line to `CHANGELOG.md` under "Unreleased". |

### Testing behaviour with an agent

Install your branch as a skill (see the README's Installing section), then try the relevant prompts from `evals/`. With Claude Code you can run the cases directly:

```bash
claude plugin eval . --allow-tools Write,Edit,Bash --scaffold
```

## Pull request tips

- One topic per PR; small PRs get reviewed faster.
- Explain *why*, with a source citation or real-world experience.
- PRs are squash-merged, so the PR title becomes the commit message. Make it clear.

## License of contributions

By contributing, you agree that your contributions are licensed under the project's licenses: code under [MIT](LICENSE), content under [CC BY 4.0](LICENSE-docs).

## Code of Conduct

This project follows our [Code of Conduct](CODE_OF_CONDUCT.md). Be kind; we're all on call sometimes.
