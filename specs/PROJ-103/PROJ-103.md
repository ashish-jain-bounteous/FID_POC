# Spec: PROJ-103 - Optimize LOAD_FCT_TRADES stored procedure for faster nightly load

**Status:** AWAITING SME APPROVAL
**Verdict / severity:** FEATURE / P3   (from Triage)
**Author:** design-agent   **Date:** 2026-06-18T06:41:00Z
**Run:** `.github` guided run.

## Objective

The nightly `LOAD_FCT_TRADES` slows down as `FCT_TRADES` grows because its dedup uses a `WHERE NOT EXISTS (... FCT_TRADES ...)` anti-join that re-scans the whole fact table every run. This change makes the load faster and cheaper on Snowflake without changing what it produces. The rows loaded, key resolution, and amount calculations stay byte-for-byte identical.

## Proposed changes (ALL)

| # | File | Change | Rationale |
|---|------|--------|-----------|
| 1 | `snowflake/procs/load_fct_trades.sql` | Replace the `INSERT ... SELECT ... WHERE NOT EXISTS` anti-join with a `MERGE INTO FCT_TRADES ... ON target.TRADE_ID = source.TRADE_ID WHEN NOT MATCHED THEN INSERT`. Keep the `AND ACC.IS_CURRENT = TRUE` join (PROJ-101) and the same column projection. | MERGE dedups by key without the full-table scan, so runtime drops as the table grows. Output is unchanged. |
| 2 | `snowflake/ddl/fct_trades.sql` | Add a clustering key or enable the Search Optimization Service on `FCT_TRADES(TRADE_ID)`. | Speeds the per-key dedup lookup the MERGE relies on. |
| 3 | `control_m/CTM_LOAD_FCT_TRADES.json` | No definition change. Review the job's runtime/window after deploy and resize the warehouse if the profile warrants it. | The faster proc may let the job finish well inside its window; right-size compute for cost. |

## Impacted objects

| Object | Type | Path | Impact |
|--------|------|------|--------|
| `LOAD_FCT_TRADES` | proc | `snowflake/procs/load_fct_trades.sql` | Anti-join replaced by MERGE (change 1). |
| `FCT_TRADES` | table | `snowflake/ddl/fct_trades.sql` | Clustering / Search Optimization on `TRADE_ID` (change 2). |
| `STG_TRADES` | table | `snowflake/staging/stg_trades.sql` | Read-only source of the load; unchanged. |
| `CTM_LOAD_FCT_TRADES` | job | `control_m/CTM_LOAD_FCT_TRADES.json` | No change; post-deploy runtime/warehouse review (change 3). |

## Test plan

- Unit: same input produces the same `FCT_TRADES` rows as the pre-change proc (row count and column values match); re-running inserts zero new rows (dedup holds); a NULL `TRADE_ID` in staging is handled the same way.
- Regression: full nightly load in DEV/UAT against a production snapshot, compare `FCT_TRADES` and `VW_DAILY_POSITIONS` output before vs after (must be identical); capture the query profile to confirm the full-table scan is gone.

## Rollback plan

Change 1: redeploy the previous `INSERT ... NOT EXISTS` version of the proc. Change 2: `ALTER TABLE FCT_TRADES DROP CLUSTERING KEY` / disable Search Optimization. Change 3: no code change to revert. All are independent and non-destructive.

## Risks / open questions

| # | Risk / question | Severity | Owner |
|---|-----------------|----------|-------|
| R1 | Source-state note: `load_fct_trades.sql` already carries the MERGE optimization and a `PROJ-101, PROJ-103` header from an earlier run, so most of change 1 may already be in place. Development should reconcile against the current file, not assume the pre-MERGE baseline. | Medium | Data Eng / SME |
| R2 | Search Optimization and clustering add storage/maintenance cost. Confirm the dedup-lookup speedup is worth it for this table size. | Low | FinOps |
| R3 | Output-equivalence must be proven (R-test above) before this is treated as done; "byte-for-byte identical" is the acceptance bar. | Medium | Data Eng |

## Token budget estimate

Rough heuristic to finish PROJ-103 end to end (not a measurement):
- Remaining routed agents after design (sql-optimizer, stored-proc, code-review): 3 x ~3k-6k = ~9k-18k
- Orchestration + logging overhead: ~3k
- Already spent (triage + design): ~8k-14k
- **Estimated total to finish: ~12k-22k tokens** (evaluation excluded; add ~150k+ only if run with `--eval`)

## Approvals

- SME: __________   status: pending   date: ______
