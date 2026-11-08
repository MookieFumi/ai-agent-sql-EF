---
name: sql-ef-diagnosis
description: Stage 1 of sql-ef-analyst. Read-only inventory of a .NET repository's data access (provider, EF Core version, DbContexts, query sites, logging) and recommendation of which analysis stages to run.
---

# Diagnosis

## Purpose

Know what evidence exists before analyzing. This stage writes nothing.

## Steps

1. Find projects that reference `Microsoft.EntityFrameworkCore*`, `Dapper`, `Npgsql`, `Microsoft.Data.SqlClient` or `Microsoft.Data.Sqlite`. Record the EF Core version and the provider.
2. List every `DbContext`, its `OnModelCreating` or `IEntityTypeConfiguration<>` classes, and the `UseXxx` provider call. Note `UseLazyLoadingProxies`, `UseQueryTrackingBehavior`, `AddDbContextPool` and `EnableSensitiveDataLogging`.
3. Count query sites: `.ToList`, `.ToListAsync`, `.FirstOrDefault*`, `.Single*`, `.Any*`, `.Count*`, `.SaveChanges*`, `FromSql*`, `ExecuteSql*`, `ExecuteUpdate*`, `ExecuteDelete*`.
4. Check whether SQL logging is available: `LogTo`, `ILogger` category `Microsoft.EntityFrameworkCore.Database.Command`, OpenTelemetry. Say how to enable it if missing.
5. Detect an Aspire AppHost and service defaults. If present, recommend `sql-ef-aspire-telemetry` as the way to get logs and traces.
6. Look for a pasted log or execution plan from the user, and for existing indexes in migrations.
7. Ask the user: approximate table sizes, the endpoints or jobs they care about, and which database they use in production.

## Output

A short table: evidence available (code, log, plan), risks seen at a glance, and the recommended stages. Ask which stages to run.
