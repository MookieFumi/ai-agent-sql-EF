# Agent instructions

This repository ships the `sql-ef-analyst` skill set. The skills in `.apm/skills/` follow the Agent Skills open standard, so they are the portable part. The files under `.apm/agents/` are thin wrappers for editors that have a custom agent format.

- Do not put editor-specific tool names in `.apm/skills/**/SKILL.md`. Say "ask the user" instead of naming a question tool.
- Skill `name` must be lowercase with hyphens and match its folder.
- All files, names and comments are in English.
- Never commit generated output or user execution plans.
