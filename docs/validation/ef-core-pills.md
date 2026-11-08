# Validation against ef-core-pills

Source: https://github.com/MookieFumi/ef-core-pills (shallow clone of `main`, 2026-11-08).

## How this was done

The static rules of the skills were applied by hand to the demo code, and the log rule to the recorded `results.txt` of the demo. The agent was **not** run inside an editor, so this validates the rules, not the agent loop (skill loading, questions, diffs).

Each pill contains both the bad version and the fix on purpose, so a finding in a pill is expected.

## Static pass

| Pill | Bad pattern in the demo | Skill and rule | Result |
|---|---|---|---|
| NPlusOne | `CountAsync` inside `foreach` over orders | `sql-ef-round-trips`: query inside a loop | Found |
| Projection | `Orders.AsNoTracking()...ToListAsync()` returns the whole entity | `sql-ef-query-shape`: entity instead of projection | Found |
| Tracking | `ToListAsync()` without `AsNoTracking` on 50,000 shipments | `sql-ef-tracking`: read-only query with tracking | Found |
| Tracking | `Include(Customer)` with `AsNoTracking` duplicates customers | `sql-ef-tracking`: identity resolution trade-off | Found (as a trade-off note) |
| InMemoryFilter | `ToListAsync()` then `.Where(...)` | `sql-ef-query-shape`: `ToList` before `Where`; also list without `Take` | Found |
| CartesianExplosion | Two collection `Include` with `AsSingleQuery` | `sql-ef-query-shape`: two collection `Include` | Found |
| BulkUpdate | `SaveChangesAsync` inside `foreach` | `sql-ef-round-trips`: `SaveChanges` in a loop | Found |
| BulkUpdate | `ids.Contains(...)` with 2,000 ids | `sql-ef-query-shape`: `Contains` with a huge list | Found, Low |
| AnyVsCount | `CountAsync(filter) > 0` | `sql-ef-query-shape`: `Count() > 0` | Found, but must be Low (see below) |
| Pagination | `Skip`/`Take` with deep pages | `sql-ef-query-shape`: deep offset pagination | Found; the unique tie-breaker (`ThenBy(Id)`) was correctly not flagged |

## Log pass

`results.txt` reports `commands=301` for the one-query-per-order version against `commands=2` for `Include`. The `sql-ef-round-trips` log rule (the same statement repeated more than 3 times per request) flags the 301 case and not the other two.

## Gaps found

1. **Any vs Count:** the demo shows no difference in three of four cases. The rule must report it as Low and ask for the plan, never as a defect. Fixed in `sql-ef-query-shape`.
2. **Toggled fixes:** the demo selects `AsSplitQuery` or `AsSingleQuery` at runtime. A static scan sees two collection `Include` and cannot tell which branch runs. The skill now tells the agent to check the options applied to the same query before reporting.
3. **Helper queries:** `FindLastRowOfPreviousPageAsync` uses `Skip` as a helper of the keyset demo. Without context it looks like deep offset pagination. Reported as Possible only, which is the intended behavior.
4. **Not covered by any rule:** nothing in this repo exercises raw SQL, `DbContext` thread safety, indexes or plans, so those skills are still unvalidated.

## Not validated

- Running the agent in VS Code, Claude Code or any other editor.
- Reading telemetry from a running Aspire AppHost.
- Execution plans.
