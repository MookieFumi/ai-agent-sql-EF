---
name: sql-ef-indexes-plans
description: Stage 5 of sql-ef-analyst. Read a pasted execution plan (SQL Server, PostgreSQL EXPLAIN, SQLite) and the EF model to find missing, unused or unusable indexes, and propose an index migration.
---

# Indexes and plans

## Inputs

An execution plan pasted by the user (never connect to the database), plus the generated SQL and the EF model configuration. Ask which database and its version.

## What to look for in a plan

| Signal | Meaning | Action |
|---|---|---|
| Full table scan, `Seq Scan`, `Table Scan` on a large table with a selective filter | Missing or unusable index | Propose an index on the filter columns |
| Index scan instead of seek | Predicate not sargable | Rewrite the predicate (no function on the column, no leading wildcard `LIKE '%x'`) |
| Sort operator over many rows | `ORDER BY` without a supporting index | Index matching the sort, include it in the keyset predicate |
| Key lookup / heap fetch for every row | Index lacks columns | Covering index with `INCLUDE` |
| Estimated rows far from actual rows | Stale statistics | Update statistics, ask the DBA |
| Implicit conversion warning | Parameter type does not match the column type | Align the .NET type and the column type (for example `string` unicode vs varchar) |

## In the EF model

- Foreign keys: EF creates an index by convention, check it exists in migrations.
- Filters used in `Where` / `OrderBy` with no `HasIndex`.
- Composite indexes: equality columns first, then range or sort column.
- Redundant indexes (a prefix of another index).

## Rules

- Every index costs writes and storage. State the trade-off and the table write rate if known.
- Provide the index as an EF `HasIndex` configuration plus a migration, never raw DDL applied by hand.
- Explain that plans differ between providers; say which one you read.
- Without a plan, mark index findings as Possible.
