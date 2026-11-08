---
name: sql-ef-report
description: Stage 7 of sql-ef-analyst. Build the final report with findings ranked by severity, evidence, proposed fix, trade-offs and how to measure before and after.
---

# Report

## Format

One section per finding, ordered by impact:

```text
### [High|Medium|Low] Title
Evidence: file:line or log excerpt
Confidence: Confirmed | Likely | Possible
Problem: one or two sentences
Fix: minimal change (diff or snippet)
Trade-off: what it costs or changes
Measure: commands per request, rows, bytes, plan, timing
```

## Severity

- High: injection, unbounded query on a large table, N+1 on a hot endpoint, filter in memory.
- Medium: missing projection or `AsNoTracking` on frequent reads, cartesian explosion, deep offset pagination.
- Low: micro-optimizations that need a benchmark first.

## End of report

- A table with counts per severity and per skill.
- Actions left for the user (data sizes to confirm, plans to provide, indexes to review with the DBA).
- Suggested split into commits or PRs, one concern each.
- What was not analyzed and why.

Reference material: `references/blog-posts.md`.
