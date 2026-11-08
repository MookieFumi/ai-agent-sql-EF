# Testing guide

Goal: confirm the skills load and produce the expected findings in a real editor, using the known cases of https://github.com/MookieFumi/ef-core-pills. About 15 minutes.

## 1. Prepare

Install the package with APM (https://github.com/microsoft/apm), `pip install apm-cli`:

```bash
git clone https://github.com/MookieFumi/ef-core-pills
cd ef-core-pills
apm init            # only if the project has no apm.yml yet
apm install MookieFumi/ai-agent-sql-ef
```

`apm install` takes no prompts for this package: it deploys to the targets listed in the `apm.yml` of the project (or the ones it detects, such as `.github/` or `.claude/`). To force one editor: `apm install MookieFumi/ai-agent-sql-ef --target claude` (or `copilot`). Until the first tag exists this installs `main`; afterwards use `#v0.1.0`.

Check where it put the files and write it down (it feeds the fixes):

```bash
git status --short
```

Fallback if APM fails or you do not want it: copy `.apm/skills/*` by hand into `.github/skills/` (VS Code) or `.claude/skills/` (Claude Code), keeping each folder name, and `.apm/agents/sql-ef-analyst.agent.md` into `.github/agents/`.

VS Code: enable the agent skills setting (`chat.agent.skills`), open Copilot Chat in agent mode and check that the skills appear in the tools picker. Claude Code: run `/skills` or start a new session and check that the `sql-ef-*` skills are listed. The logic lives in the skills, so they are enough in both editors; the agent file is only an optional shortcut for VS Code.

## 2. Prompts to run

Run them in a new chat each, in this order.

1. `Run sql-ef-analyst, full run, on this repository. Report only, do not change any file.`
2. `Use sql-ef-round-trips on src/EfCorePills/Pills/NPlusOne.`
3. `Use sql-ef-query-shape on src/EfCorePills/Pills.`
4. `Analyze this EF log with sql-ef-round-trips:` followed by a pasted log (run the demo with `dotnet run --project src/EfCorePills` and paste the first part of the output).

## 3. Expected results

See `docs/validation/ef-core-pills.md`. In short, the agent should report:

- `CountAsync` inside a loop (NPlusOne).
- The whole entity returned instead of a projection (Projection).
- Tracking on a read-only query (Tracking).
- `ToListAsync()` followed by `Where` (InMemoryFilter).
- Two collection `Include` (CartesianExplosion), as Possible because the demo toggles `AsSplitQuery`.
- `SaveChangesAsync` in a loop (BulkUpdate).
- `Count() > 0` as Low (AnyVsCount).
- No finding for the keyset pagination or for the fixed versions.

## 4. What to record

Write these down; they feed the blog post and the fixes:

- Editor, version, plan (for example Copilot Free) and method used to install.
- Did the skills load by themselves, or did you have to name them?
- Did the agent ask questions, and were they useful?
- Findings: which expected ones appeared, which are missing, and which are false positives.
- Did it edit any file without asking? (It must not.)
- A short quote of the best finding and the worst one.
- Anything confusing in the README or in the install steps.

Send the notes (or screenshots without secrets) and they will be turned into fixes and into the real case for the post.
