#!/usr/bin/env python3
"""Validate the skills, the agent wrapper and the APM manifest of this repository."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / ".apm" / "skills"
AGENTS = ROOT / ".apm" / "agents"
NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
FORBIDDEN_IN_SKILLS = ["vscode/askQuestions"]

errors = []


def fail(message):
    errors.append(message)


def read_front_matter(path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        fail(f"{path.relative_to(ROOT)}: missing YAML front matter")
        return {}, text
    fields = {}
    for line in match.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    return fields, text


def check_skills():
    folders = sorted(p for p in SKILLS.iterdir() if p.is_dir())
    if not folders:
        fail(".apm/skills has no skills")
    for folder in folders:
        skill_file = folder / "SKILL.md"
        relative = skill_file.relative_to(ROOT)
        if not skill_file.exists():
            fail(f"{folder.relative_to(ROOT)}: missing SKILL.md")
            continue
        fields, text = read_front_matter(skill_file)
        name = fields.get("name", "")
        description = fields.get("description", "")
        if name != folder.name:
            fail(f"{relative}: name '{name}' must equal the folder name '{folder.name}'")
        if not NAME_PATTERN.match(name) or len(name) > 64:
            fail(f"{relative}: name must be lowercase letters, numbers and single hyphens, max 64 characters")
        if not description:
            fail(f"{relative}: description is required")
        if len(description) > 1024:
            fail(f"{relative}: description is longer than 1024 characters")
        if name.startswith(('"', "'")) or description.startswith(('"', "'")):
            fail(f"{relative}: name and description must be unquoted")
        if text.count("\n") > 500:
            fail(f"{relative}: SKILL.md is longer than 500 lines, move detail to references/")
        for forbidden in FORBIDDEN_IN_SKILLS:
            if forbidden in text:
                fail(f"{relative}: editor-specific tool name '{forbidden}' is not allowed in skills")
        for link in re.findall(r"`(references/[^`]+)`", text):
            if not (folder / link).exists():
                fail(f"{relative}: referenced file '{link}' does not exist")


def check_agents():
    agents = sorted(AGENTS.glob("*.agent.md"))
    if not agents:
        fail(".apm/agents has no *.agent.md file")
    existing = {p.name for p in SKILLS.iterdir() if p.is_dir()}
    for agent in agents:
        fields, text = read_front_matter(agent)
        if not fields.get("name") or not fields.get("description"):
            fail(f"{agent.relative_to(ROOT)}: name and description are required")
        for skill in re.findall(r"`(sql-ef-[a-z0-9-]+)`", text):
            if skill not in existing:
                fail(f"{agent.relative_to(ROOT)}: references unknown skill '{skill}'")


def check_manifest():
    manifest = ROOT / "apm.yml"
    if not manifest.exists():
        fail("apm.yml is missing")
        return
    text = manifest.read_text(encoding="utf-8")
    for key in ("name", "version"):
        if not re.search(rf"^{key}:\s*\S+", text, re.MULTILINE):
            fail(f"apm.yml: '{key}' is required")


def check_orchestrator_lists_every_skill():
    orchestrator = SKILLS / "sql-ef-analyst" / "SKILL.md"
    if not orchestrator.exists():
        fail("skill sql-ef-analyst is missing")
        return
    text = orchestrator.read_text(encoding="utf-8")
    for folder in SKILLS.iterdir():
        if folder.is_dir() and folder.name != "sql-ef-analyst" and f"`{folder.name}`" not in text:
            fail(f"sql-ef-analyst does not list the skill '{folder.name}'")


check_skills()
check_agents()
check_manifest()
check_orchestrator_lists_every_skill()

if errors:
    print("Validation failed:")
    for error in errors:
        print(f"  - {error}")
    sys.exit(1)

print("Validation passed.")
