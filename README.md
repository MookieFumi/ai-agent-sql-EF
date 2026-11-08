# ai-agent-sql-ef

`ai-agent-sql-ef` is an AI agent, with one skill per analysis, that finds SQL and EF Core performance problems: N+1, round trips, tracking, projections, cartesian explosion, pagination, indexes and raw SQL. It works in any editor that supports Agent Skills (VS Code with GitHub Copilot, Claude Code, Cursor, Codex, Gemini CLI).

Repository naming: each agent lives in its own repository named `ai-agent-<topic>`, so this one is the `sql-ef` agent. Its skills are prefixed `sql-ef-` to avoid clashes when several agents are installed together.

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

Each release also attaches a zip built with.

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

See `docs/testing-guide.md` to try it against `ef-core-pills`.

## Pipelines

- `ci.yml` runs on every pull request and on `main`. Job `build` runs `scripts/validate.py` (skill names match their folders, front matter is valid, no editor-specific tool names, the agent only references existing skills). Job `pack` installs the package with APM into an empty project (`scripts/smoke-install.sh`, which fails unless every skill is deployed), builds the zip with `scripts/build-package.py` and uploads it as an artifact.
- `release.yml` runs when a `v*` tag is pushed: validates, smoke tests the APM install, builds the zip and creates the GitHub Release with it. It can also be started by hand from the Actions tab (`Run workflow`); a manual run never creates a Release, it only validates, smoke tests, builds and uploads the zip as an artifact, so you can test it safely.

Run the validation locally with `python3 scripts/validate.py`.

## Versioning and releasing

The version lives in one place: `version` in `apm.yml`. It follows semantic versioning (`MAJOR.MINOR.PATCH`):

- PATCH: fix a rule or a typo in a skill, no change in behavior.
- MINOR: add a skill or a rule, or extend what a skill detects.
- MAJOR: rename or remove a skill, or change how the agent behaves in a way that breaks how people use it.

To release:

1. In a pull request, bump `version` in `apm.yml` (for example `0.1.0` to `0.2.0`). The README install examples and `docs/` do not hardcode it except the examples below, update them if you want.
2. Merge the pull request (squash).
3. Tag the merge commit with the same version prefixed by `v` and push the tag:

   ```bash
   git checkout main && git pull
   git tag v0.2.0
   git push origin v0.2.0
   ```

4. The `release` workflow checks that the tag matches `apm.yml`, validates, smoke tests the APM install, builds `ai-agent-sql-ef-<version>.zip` and creates the GitHub Release with that zip. If the tag and the manifest differ, it fails and nothing is published.

Consumers install a version with the tag: `apm install MookieFumi/ai-agent-sql-ef#v0.2.0`, and update with `apm update`. A tag is immutable by convention; to fix a bad release publish a new patch version instead of moving the tag.

To test the release pipeline without publishing, run `release` by hand from the Actions tab: it never creates a Release.
