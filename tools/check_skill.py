#!/usr/bin/env python3
"""Repository checks for the sre skill. Run from the repo root:

    python3 tools/check_skill.py

Checks:
  - SKILL.md frontmatter is valid YAML with a valid name and a description <= 1024 chars
  - every assets/ and scripts/ file that SKILL.md or README.md mentions exists
  - relative links in README.md point to files that exist
  - each eval case has prompt.md, case.yaml (valid YAML) and at least one grader
  - nothing that must stay private is tracked: references/, PDFs, workspaces
"""
import pathlib
import re
import subprocess
import sys

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")

ROOT = pathlib.Path(__file__).resolve().parent.parent
errors = []


def err(msg):
    errors.append(msg)


def check_frontmatter():
    text = (ROOT / "SKILL.md").read_text()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return err("SKILL.md: missing YAML frontmatter")
    try:
        meta = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        return err(f"SKILL.md: frontmatter is not valid YAML: {e}")
    name = meta.get("name", "")
    desc = meta.get("description", "")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) or len(name) > 64:
        err(f"SKILL.md: name {name!r} must be lowercase letters, digits and hyphens, <= 64 chars")
    if not desc:
        err("SKILL.md: description is empty")
    elif len(desc) > 1024:
        err(f"SKILL.md: description is {len(desc)} chars; the Agent Skills limit is 1024")
    if re.search(r"<[^>]+>", desc):
        err("SKILL.md: description must not contain XML/HTML tags")


def check_mentioned_files():
    for doc in ("SKILL.md", "README.md"):
        text = (ROOT / doc).read_text()
        for rel in sorted(set(re.findall(r"\b((?:assets|scripts)/[\w.-]+\.(?:md|py))", text))):
            if not (ROOT / rel).exists():
                err(f"{doc}: mentions {rel}, which doesn't exist")
        # Bare template names in tables, e.g. `canary-plan-template.md`
        if doc == "SKILL.md":
            for name in sorted(set(re.findall(r"`([\w-]+-(?:template|checklist|worksheet|assessment)\.md)`", text))):
                if not (ROOT / "assets" / name).exists():
                    err(f"SKILL.md: mentions template {name}, which isn't in assets/")


def check_readme_links():
    text = (ROOT / "README.md").read_text()
    for target in re.findall(r"\]\(([^)#\s]+)\)", text):
        if re.match(r"[a-z]+:", target):
            continue
        if not (ROOT / target).exists():
            err(f"README.md: link to {target}, which doesn't exist")


def check_evals():
    cases = [p for p in (ROOT / "evals").iterdir() if p.is_dir()]
    if not cases:
        err("evals/: no test cases")
    for case in cases:
        for f in ("prompt.md", "case.yaml"):
            if not (case / f).exists():
                err(f"{case.relative_to(ROOT)}: missing {f}")
        if (case / "case.yaml").exists():
            try:
                yaml.safe_load((case / "case.yaml").read_text())
            except yaml.YAMLError as e:
                err(f"{case.relative_to(ROOT)}/case.yaml: invalid YAML: {e}")
        graders = case / "graders"
        if not graders.is_dir() or not any(graders.iterdir()):
            err(f"{case.relative_to(ROOT)}: no graders")


def check_private_files():
    try:
        tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.split()
    except (OSError, subprocess.CalledProcessError):
        return  # not a git checkout; skip
    for f in tracked:
        if f.startswith("references/") or f.lower().endswith(".pdf") or "-workspace/" in f:
            err(f"{f}: must not be committed (copyrighted or local-only material)")


check_frontmatter()
check_mentioned_files()
check_readme_links()
check_evals()
check_private_files()

if errors:
    print("Skill checks failed:")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
print("All skill checks passed.")
