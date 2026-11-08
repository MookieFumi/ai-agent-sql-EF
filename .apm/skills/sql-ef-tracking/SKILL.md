---
name: sql-ef-tracking
description: Stage 4 of sql-ef-analyst. Detect unnecessary change tracking, identity resolution trade-offs, DbContext lifetime and thread-safety problems, pooling and compiled-query opportunities.
---

# Tracking and context

## Detect in code

- Read-only queries without `AsNoTracking`, or without `AsNoTrackingWithIdentityResolution` when the graph needs shared instances.
- No global decision: check `UseQueryTrackingBehavior` in the context registration, and say if it is safe to change. Changing it globally breaks code that edits what it reads, so ask.
- `Find` or `FirstOrDefault` used only to read, on a hot path.
- A `DbContext` stored in a singleton or a static field, or used from `Task.WhenAll` / `Parallel.ForEach` (not thread-safe). Fix with one context per unit of work, via `IDbContextFactory<T>`.
- A long-lived context that tracks thousands of entities across operations.
- `AddDbContext` on a high-throughput service: evaluate `AddDbContextPool` (watch state kept in the context between uses).
- Compiled queries (`EF.CompileAsyncQuery`) only for proven hot paths. They remove the expression-tree work per call, not the database time.

## Rules

- Tracking cost grows with the number of entities, so quantify it: entities tracked and memory allocated.
- AsNoTracking changes identity: two rows pointing to the same parent produce two parent instances. Tell the user.
- Never recommend pooling or compiled queries without a benchmark.
