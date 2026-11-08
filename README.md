# ai-agent-sql-ef

A GitHub Copilot custom agent for VS Code, with one skill per analysis, that finds SQL and EF Core performance problems: N+1, round trips, tracking, projections, cartesian explosion, pagination, indexes and raw SQL.

## Contents

```text
skills/                        portable (Agent Skills open standard)
├── sql-ef-analyst/            orchestrator
├── sql-ef-diagnosis/          stage 1
├── sql-ef-round-trips/        stage 2
├── sql-ef-query-shape/        stage 3
├── sql-ef-tracking/           stage 4
├── sql-ef-indexes-plans/      stage 5
├── sql-ef-raw-sql/            stage 6
└── sql-ef-report/             stage 7 (+ references)
agents/
├── vscode/sql-ef-analyst.agent.md   thin wrapper for VS Code custom agents
└── claude/sql-ef-analyst.md         thin wrapper for Claude Code subagents
AGENTS.md                      rules for agents working on this repo
```

The skills hold all the logic and work in any editor that supports Agent Skills. The agent files only load the `sql-ef-analyst` skill, so they are optional.

## Install

Copy every folder under `skills/` to the skills folder of your tool. Each folder name must match the `name` in its `SKILL.md`.

| Tool | Project path | Personal path |
|---|---|---|
| VS Code / GitHub Copilot | `.github/skills/` (also reads `.claude/skills/` and `.agents/skills/`) | `~/.copilot/skills/` |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Codex CLI | `.codex/skills/` | `~/.codex/skills/` |
| Cursor | `.cursor/skills/` | |
| Gemini CLI | `.gemini/skills/` | |

Optional agent wrappers: copy `agents/vscode/sql-ef-analyst.agent.md` to your VS Code agents folder, or `agents/claude/sql-ef-analyst.md` to `.claude/agents/`.

Then open a .NET repository and ask: "run sql-ef-analyst, full run", or paste an EF log or an execution plan. In VS Code enable the agent skills setting (`chat.agent.skills`).

Paths come from Microsoft Learn documentation and were not tested with each tool.

## Evidence it uses

1. Code: static patterns in LINQ and SQL.
2. EF Core logs (`Microsoft.EntityFrameworkCore.Database.Command`): commands per request and repeated statements.
3. Execution plans you paste. The agent never connects to a database.

## Safety

Read-only by default. It edits only after you approve a diff and never commits or pushes.

## Status

First version. It has not been tested on a real repository yet. The next step is validating it against the cases in https://github.com/MookieFumi/ef-core-pills.
