---
name: sql-ef-round-trips
description: Stage 2 of sql-ef-analyst. Detect N+1 queries, queries inside loops, SaveChanges inside loops and repeated statements per request, in code and in EF Core logs.
---

# Round trips

## Purpose

Fewer round trips to the database. Fix these before tuning individual queries.

## Detect in code

- A query (`ToList`, `Find`, `FirstOrDefault`, `Any`, `Count`) inside `foreach`, `for`, `while` or a LINQ `Select` lambda.
- Navigation properties read inside a loop when lazy loading is on (`UseLazyLoadingProxies`, virtual navigations).
- `SaveChanges` or `SaveChangesAsync` inside a loop.
- `Count() > 0` or `Any()` followed by another query for the same data.
- Repository methods called once per item of a list (`GetByIdAsync` in a loop).

## Detect in logs

Enable `Microsoft.EntityFrameworkCore.Database.Command` at Information. Group the log lines of one request by SQL text with parameters removed. Flag:

- The same statement repeated more than 3 times in one request (N+1 signature).
- More than about 10 commands for a single endpoint.
- Many `UPDATE` or `INSERT` statements in a row from a loop.

## Fixes

| Problem | Fix | Trade-off |
|---|---|---|
| N+1 on related data | `Include`, or better a `Select` projection | Include can cause cartesian explosion, see `sql-ef-query-shape` |
| Lookups by id in a loop | One query with `Where(x => ids.Contains(x.Id))` | Very large lists need chunks |
| `SaveChanges` in a loop | One `SaveChanges` after the loop | Different failure behavior: all or nothing |
| Bulk change of many rows | `ExecuteUpdate` or `ExecuteDelete` | Skips the change tracker, interceptors on entities, and concurrency tokens |

## Measure

Report commands per request before and after. Row counts and command counts are deterministic; timings are not, so quote orders of magnitude.

Read `references/blog-posts.md` of the report skill for the long explanations.
