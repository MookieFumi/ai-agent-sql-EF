---
name: sql-ef-raw-sql
description: Stage 6 of sql-ef-analyst. Review hand-written SQL (FromSql, ExecuteSql, Dapper, .sql files) for injection, SELECT star, bad parameters and missing limits.
---

# Raw SQL

## Detect

- String concatenation or interpolation with `FromSqlRaw` / `ExecuteSqlRaw` (injection). `FromSqlInterpolated` and `FromSql` parameterize, `Raw` variants do not.
- `SELECT *` in a query consumed by a few columns.
- Missing `WHERE`, `LIMIT` or `TOP` on large tables.
- Parameters typed wrongly (string for a numeric column, unicode vs ansi), which breaks index use.
- Dynamic `ORDER BY` built from user input (use an allowlist).
- Dapper calls inside loops (same N+1 problem as EF).
- `IN` lists built by concatenating values.
- Multiple statements that could be one set-based statement.

## Fixes

Parameterize, project only needed columns, add limits, compare with the equivalent LINQ query when one exists, and mention when raw SQL is the right tool (window functions, hints, bulk operations).

Security findings (injection) are always High severity.
