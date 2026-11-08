# sql-ef-ia-agent

A GitHub Copilot custom agent for VS Code, with one skill per analysis, that finds SQL and EF Core performance problems: N+1, round trips, tracking, projections, cartesian explosion, pagination, indexes and raw SQL.

## Contents

```text
agents/
└── sql-ef-analyst.agent.md   orchestrator
skills/
├── sql-ef-diagnosis/         stage 1
├── sql-ef-round-trips/       stage 2
├── sql-ef-query-shape/       stage 3
├── sql-ef-tracking/          stage 4
├── sql-ef-indexes-plans/     stage 5
├── sql-ef-raw-sql/           stage 6
└── sql-ef-report/            stage 7 (+ references)
```

## Install

1. Copy `agents/sql-ef-analyst.agent.md` to your VS Code user agents folder.
2. Copy every folder under `skills/` to your personal skills folder (`~/.copilot/skills/`). Each folder name must match the `name` in its `SKILL.md`.
3. Open a .NET repository, select `sql-ef-analyst` and ask for a "full run", or paste an EF log or an execution plan.

Folder locations and settings were not verified against your VS Code version.

## Evidence it uses

1. Code: static patterns in LINQ and SQL.
2. EF Core logs (`Microsoft.EntityFrameworkCore.Database.Command`): commands per request and repeated statements.
3. Execution plans you paste. The agent never connects to a database.

## Safety

Read-only by default. It edits only after you approve a diff and never commits or pushes.

## Status

First version. It has not been tested on a real repository yet. The next step is validating it against the cases in https://github.com/MookieFumi/ef-core-pills.
