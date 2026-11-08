---
name: sql-ef-query-shape
description: Stage 3 of sql-ef-analyst. Detect queries with the wrong shape in EF Core: entities instead of projections, ToList before Where, cartesian explosion, unbounded lists, unstable pagination and client evaluation.
---

# Query shape

## Detect in code

| Pattern | Problem | Fix |
|---|---|---|
| Read-only endpoint returns entities or maps them after `ToList` | Loads every column, including large ones | `Select` into a DTO before `ToList` |
| `.ToList()` or `.AsEnumerable()` followed by `.Where`, `.OrderBy`, `.Skip`, `.Take`, `.Count` | Filtering happens in memory after loading the table | Move the operator before the materialization |
| Two or more collection `Include` on the same query | Cartesian explosion: rows multiply | `AsSplitQuery`, or a projection, or separate queries |
| List query without `Take` | Fine with 200 rows, breaks with millions | Add a limit and pagination |
| `Skip`/`Take` with deep pages | The database still walks the skipped rows | Keyset pagination |
| `OrderBy` on a non-unique column with paging | Rows repeat or disappear between pages | Add a unique tie-breaker such as the id |
| `Count() > 0` | Can count more than needed | `Any()`. Report as Low: in many cases the plan is the same, so ask for the plan before calling it a defect |
| Custom C# method inside a `Where` or `Select` | Client evaluation or runtime exception | Translate to expressions or move after the query |
| `Contains` with a huge list | Huge parameter list, plan cache pollution | Chunk, or use a temp table or join |

## Detect in generated SQL

`SELECT` with every column when the endpoint shows three, `JOIN` fanout visible as repeated parent columns, missing `LIMIT`/`TOP`, no `WHERE` for a filter written in LINQ.

## Rules

- Before reporting a cartesian explosion, check the options applied to the same query (`AsSplitQuery`, `AsSingleQuery`, a global `UseQuerySplittingBehavior`). A toggled option means the finding is Possible.
- `AsSplitQuery` adds round trips and the data can change between statements. Measure both shapes and mention the trade-off.
- Do not change a query shape if the table is small and will stay small. Say so.

## Measure

Compare columns selected, rows returned, bytes and memory allocated.
