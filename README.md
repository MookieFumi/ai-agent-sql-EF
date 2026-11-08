# ai-agent-sql-ef

A GitHub Copilot custom agent for VS Code, with one skill per analysis, that finds SQL and EF Core performance problems: N+1, round trips, tracking, projections, cartesian explosion, pagination, indexes and raw SQL.

## Contents

```text
apm.yml                        APM manifest (name, version, targets)
.apm/
├── skills/                    portable skills (Agent Skills open standard)
│   ├── sql-ef-analyst/        orchestrator
│   ├── sql-ef-diagnosis/      stage 1
│   ├── sql-ef-aspire-telemetry/ stage 1b (Aspire apps)
│   ├── sql-ef-round-trips/    stage 2
│   ├── sql-ef-query-shape/    stage 3
│   ├── sql-ef-tracking/       stage 4
│   ├── sql-ef-indexes-plans/  stage 5
│   ├── sql-ef-raw-sql/        stage 6
│   └── sql-ef-report/         stage 7 (+ references)
└── agents/
    └── sql-ef-analyst.agent.md   thin wrapper that loads the orchestrator skill
AGENTS.md                      rules for agents working on this repo
X
```

The skills hold all the logic and follow the Agent Skills open standard, so they work in any editor that supports it. The agent file only loads the `sql-ef-analyst` skill.

## Install with APM

```bash
apm install MookieFumi/ai-agent-sql-ef#v0.1.0
```

APM deploys the skills and the agent to the folders of your editor (`.github/`, `.claude/`, `.cursor/`, `.codex/`, `.gemini/`) according to `targets`. Use `--target <name>` to pick one.

Each release also attaches a zip built with `apm pack --archive`, installable with `apm install ./ai-agent-sql-ef-0.1.0.zip`.

## Install without APM

Copy every folder under `.apm/skills/` to the skills folder of your tool. Each folder name must match the `name` in its `SKILL.md`.

| Tool | Project path | Personal path |
|---|---|---|
| VS Code / GitHub Copilot | `.github/skills/` (also reads `.claude/skills/` and `.agents/skills/`) | `~/.copilot/skills/` |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Codex CLI | `.codex/skills/` | `~/.codex/skills/` |
| Cursor | `.cursor/skills/` | |
| Gemini CLI | `.gemini/skills/` | |

In VS Code enable the agent skills setting (`chat.agent.skills`). Then open a .NET repository and ask: "run sql-ef-analyst, full run", or paste an EF log or an execution plan.

## Releasing

1. Bump `version` in `apm.yml`.
2. Tag the commit with the same version prefixed by `v` and push the tag. The workflow fails if they differ.

The paths and the APM commands come from the documentation and have not been run yet. The release workflow has not run either.

## Evidence it uses

1. Code: static patterns in LINQ and SQL.
2. Aspire telemetry: structured logs and traces of a running AppHost, read with the Aspire CLI or MCP server. The agent can propose a temporary change to enable EF command logging.
3. EF Core logs (`Microsoft.EntityFrameworkCore.Database.Command`): commands per request and repeated statements.
4. Execution plans you paste. The agent never connects to a database.

## Safety

Read-only by default. It edits only after you approve a diff and never commits or pushes.

## Status

First version. It has not been tested on a real repository yet. The next step is validating it against the cases in https://github.com/MookieFumi/ef-core-pills.
