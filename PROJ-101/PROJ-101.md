# Spec: PROJ-101 — FCT_TRADES shows duplicate trades for some accounts after nightly load

**Status:** APPROVED BY SME (2026-06-10T11:36:05Z) — approved as-is
**Verdict / severity:** ISSUE / P2   (from Triage)
**Author:** design-agent   **Date:** 2026-06-10T00:00:00Z

---

## Objective

The nightly stored procedure `LOAD_FCT_TRADES` joins the SCD-2 dimension
`DIM_ACCOUNT` on `ACCOUNT_ID` alone, without filtering to the current row
(`IS_CURRENT = TRUE`). When an account has more than one active history row in
`DIM_ACCOUNT` (i.e. a bad SCD-2 load left multiple rows with `IS_CURRENT = TRUE`
for the same `ACCOUNT_ID`), the join fans out and inserts one duplicate
`FCT_TRADES` row per extra dimension row for every affected trade. The existing
`TRADE_ID NOT IN (...)` guard only prevents re-processing staging rows on
subsequent runs; it does not prevent the fan-out during the original run, and it
does not self-heal rows that are already in `FCT_TRADES`. Downstream,
`VW_DAILY_POSITIONS` aggregates `NET_QUANTITY` and `NET_AMOUNT` directly from
`FCT_TRADES`, so every duplicated trade is double- (or triple-) counted in
reported positions.

This fix (a) corrects the join predicate so future loads can never fan out, (b)
adds a stricter dedup guard as a second line of defence, and (c) purges the
already-corrupted duplicate rows from `FCT_TRADES` in a controlled one-time
remediation step. No new columns or behaviour are added; this is a pure
correctness fix.

---

## Proposed changes (ALL)

| # | File | Change | Rationale |
|---|------|--------|-----------|
| 1 | `snowflake/procs/load_fct_trades.sql` | Add `AND ACC.IS_CURRENT = TRUE` to the `DIM_ACCOUNT` join predicate (line 45). The join line changes from `JOIN ANALYTICS.MART.DIM_ACCOUNT ACC ON ACC.ACCOUNT_ID = STG.ACCOUNT_ID` to `JOIN ANALYTICS.MART.DIM_ACCOUNT ACC ON ACC.ACCOUNT_ID = STG.ACCOUNT_ID AND ACC.IS_CURRENT = TRUE`. | **Root-cause fix.** Without this predicate the join matches every historical version of an account and fans out one staging row into N fact rows, one per DIM_ACCOUNT version. Adding `IS_CURRENT = TRUE` pins each staging trade to exactly one current dimension row, eliminating the fan-out. |
| 2 | `snowflake/procs/load_fct_trades.sql` | Strengthen the existing dedup guard. Replace `WHERE STG.TRADE_ID NOT IN (SELECT TRADE_ID FROM ANALYTICS.MART.FCT_TRADES)` with `WHERE NOT EXISTS (SELECT 1 FROM ANALYTICS.MART.FCT_TRADES FT2 WHERE FT2.TRADE_ID = STG.TRADE_ID)`. Also update the procedure header comment block: change `-- Ticket: SEED-0001` to `-- Ticket: PROJ-101` and remove the `-- NOTE (PROJ-101):` known-defect comment. | The `NOT IN` form returns `NULL`-unsafe results if any `TRADE_ID` in `FCT_TRADES` is `NULL` (Snowflake evaluates `x NOT IN (... NULL ...)` as `NULL`, silently dropping rows). `NOT EXISTS` is always safe. Removing the defect note keeps the header accurate once the fix is applied. Updating the ticket reference attributes the change to the correct ticket. |
| 3 | `snowflake/ddl/fct_trades.sql` | Add a `UNIQUE` constraint on `TRADE_ID`: `CONSTRAINT UQ_FCT_TRADES_TRADE_ID UNIQUE (TRADE_ID)`. | **Second line of defence.** A unique constraint on the natural key means the database itself rejects a duplicate insert, so even if the join predicate were regressed in a future change the load would fail loudly rather than silently corrupting data. Snowflake enforces `UNIQUE` constraints via `NOVALIDATE` by default on large tables; an explicit constraint documents the intent and enables enforcement on new inserts. |
| 4 | One-time data remediation script *(new file)*: `snowflake/remediation/PROJ-101_dedup_fct_trades.sql` | Create a new, run-once remediation script that identifies and deletes the duplicate rows already present in `FCT_TRADES`. The script: (a) identifies duplicate `TRADE_ID` values using a `ROW_NUMBER()` window function partitioned by `TRADE_ID` ordered by `LOAD_TIMESTAMP ASC` (keeping the earliest insert, i.e. `ROW_NUMBER() = 1`), (b) deletes every row where `ROW_NUMBER() > 1`, (c) records a row count of deleted rows, (d) is wrapped in an explicit `BEGIN TRANSACTION` / `COMMIT` block with a `ROLLBACK` safety net. The file must include the standard header block (`-- Object:`, `-- Owner: data-engineering`, `-- Ticket: PROJ-101`, `-- Description:`). | The `IS_CURRENT` fix prevents future duplicates but does not remove the corrupted rows already inserted by prior nightly runs. Until they are deleted, `VW_DAILY_POSITIONS` continues to double-count. The `ROW_NUMBER` approach is deterministic and idempotent: running it twice produces the same result. |
| 5 | `control_m/CTM_LOAD_FCT_TRADES.json` | Add `"PROJ-101_DEDUP-OK"` as a one-time `in_condition` (pre-condition) for the next scheduled run after the fix is deployed, to enforce that the remediation script runs and completes successfully before the corrected procedure processes the following night's trades. Remove this condition after the first clean run. | Ensures the remediation and the procedure fix are deployed and executed in the correct order. The job will not run (and thus cannot re-insert staging rows already partially duplicated) until the dedup remediation signals completion. This is an operational sequencing control, not a permanent change to the job definition. |

---

## Impacted objects

The following objects are confirmed impacted (source: Triage block in
`tickets/PROJ-101.json`, cross-referenced against source files):

| Object | Type | Path | Impact |
|--------|------|------|--------|
| `ANALYTICS.MART.LOAD_FCT_TRADES` | Stored procedure | `snowflake/procs/load_fct_trades.sql` | **Root-cause object.** Join predicate and dedup guard are changed (Changes 1 and 2). |
| `ANALYTICS.MART.FCT_TRADES` | Table | `snowflake/ddl/fct_trades.sql` | Receives the `UNIQUE` constraint (Change 3). Existing duplicate rows are removed by the remediation script (Change 4). |
| `ANALYTICS.MART.DIM_ACCOUNT` | Table | `snowflake/ddl/dim_account.sql` | No DDL change. The `IS_CURRENT` column already exists; this spec only changes how it is used in the join. Read-only reference. |
| `ANALYTICS.MART.VW_DAILY_POSITIONS` | View | `snowflake/views/vw_daily_positions.sql` | No DDL change. Downstream consumer of `FCT_TRADES`. Aggregation correctness is restored automatically once duplicate fact rows are removed (Change 4). |
| `CTM_LOAD_FCT_TRADES` | Control-M job | `control_m/CTM_LOAD_FCT_TRADES.json` | One-time sequencing condition added (Change 5). |
| `PROJ-101_dedup_fct_trades.sql` *(new)* | Remediation script | `snowflake/remediation/PROJ-101_dedup_fct_trades.sql` | New one-time script (Change 4). |

**Secondary / monitoring objects (no change required):**
- `ANALYTICS.MART.DIM_SECURITY` — joined in `LOAD_FCT_TRADES` but not involved in the fan-out; no change.
- `ANALYTICS.MART.DIM_DATE` — same as `DIM_SECURITY`.
- `ANALYTICS.STAGE.STG_TRADES` — source of the load; no change.

---

## Test plan

### Unit tests

| # | Test case | Method | Expected result |
|---|-----------|--------|-----------------|
| U-1 | **IS_CURRENT fan-out prevention** | Seed `DIM_ACCOUNT` with two rows for the same `ACCOUNT_ID` both having `IS_CURRENT = TRUE` (simulating a bad SCD-2 load). Seed `STG_TRADES` with one trade for that `ACCOUNT_ID`. Call `LOAD_FCT_TRADES`. | Exactly one row inserted into `FCT_TRADES` for that `TRADE_ID`. Prior to the fix this test produces two rows; after the fix it produces one. |
| U-2 | **Normal single-IS_CURRENT row** | Seed `DIM_ACCOUNT` with one row (`IS_CURRENT = TRUE`) for an `ACCOUNT_ID`. Seed one matching staging trade. Call `LOAD_FCT_TRADES`. | Exactly one row inserted. `ACCOUNT_KEY` matches the current `DIM_ACCOUNT` row. |
| U-3 | **Historical-row exclusion** | Seed `DIM_ACCOUNT` with two rows for one `ACCOUNT_ID`: one `IS_CURRENT = FALSE` (historical), one `IS_CURRENT = TRUE` (current). Seed one staging trade. Call `LOAD_FCT_TRADES`. | Exactly one row inserted; `ACCOUNT_KEY` matches the `IS_CURRENT = TRUE` row only. |
| U-4 | **Dedup guard — no-duplicate on re-run** | After U-2, run `LOAD_FCT_TRADES` again without adding new staging rows. | Zero new rows inserted. |
| U-5 | **NULL-safe dedup guard** | Insert a row into `FCT_TRADES` with `TRADE_ID = NULL` (if the DDL allows it; otherwise confirm constraint prevents it). Seed a staging trade. Call `LOAD_FCT_TRADES`. | Staging trade is still inserted correctly; the `NOT EXISTS` guard does not silently drop valid rows due to `NULL` comparison. |
| U-6 | **UNIQUE constraint enforcement** | Attempt a direct `INSERT` into `FCT_TRADES` of a row with a `TRADE_ID` that already exists. | Statement fails with a constraint violation error (confirms Change 3 is enforced). |
| U-7 | **Remediation script idempotency** | Run `PROJ-101_dedup_fct_trades.sql` twice against a table that contains known duplicate `TRADE_ID` rows. | First run removes duplicates; second run deletes zero rows and completes without error. |
| U-8 | **Remediation script row selection** | Seed `FCT_TRADES` with three rows for the same `TRADE_ID` (different `TRADE_KEY`, `LOAD_TIMESTAMP` staggered). Run the remediation script. | Two rows deleted; the row with the earliest `LOAD_TIMESTAMP` is retained. |

### Regression tests

| # | Test case | Scope |
|---|-----------|-------|
| R-1 | Re-run the full nightly load end-to-end in the DEV or UAT environment against a snapshot of production `STG_TRADES` and dimension data. Verify row counts in `FCT_TRADES` match the expected unique trade count (no fan-out). | `LOAD_FCT_TRADES`, `FCT_TRADES` |
| R-2 | Compare `VW_DAILY_POSITIONS` output (NET_QUANTITY, NET_AMOUNT) between pre-fix (duplicated data) and post-fix + post-remediation snapshots for a sample of affected accounts. Confirm positions halve (or reduce) to correct values. | `VW_DAILY_POSITIONS`, `FCT_TRADES` |
| R-3 | Verify that `DIM_ACCOUNT` joins in the procedure still resolve correctly for all accounts that have only one `IS_CURRENT = TRUE` row (no regression for the common case). | `LOAD_FCT_TRADES`, `DIM_ACCOUNT` |
| R-4 | Confirm the Control-M job sequencing change (Change 5) does not block normal scheduling after the one-time condition is cleared. | `CTM_LOAD_FCT_TRADES` |
| R-5 | Run the existing regression catalog (if any) for the `TRADES_MART` pipeline and confirm no new failures are introduced. | All mart objects |

---

## Rollback plan

Each change can be rolled back independently in reverse order of deployment.

| # | Change | Rollback action |
|---|--------|-----------------|
| 5 | Control-M sequencing condition | Remove the `PROJ-101_DEDUP-OK` `in_condition` from `CTM_LOAD_FCT_TRADES.json` and redeploy the job definition. The job reverts to its original pre-conditions. |
| 4 | Remediation script | The script is run-once and destructive (it deletes rows). To roll back: restore `FCT_TRADES` from the pre-remediation snapshot (taken as part of the Change 4 deployment runbook). The script itself is simply not re-executed. Ensure the pre-remediation snapshot backup is created before executing the script. |
| 3 | UNIQUE constraint on `FCT_TRADES` | Execute `ALTER TABLE ANALYTICS.MART.FCT_TRADES DROP CONSTRAINT UQ_FCT_TRADES_TRADE_ID;`. No data change. |
| 2 | NOT EXISTS dedup guard | Revert `load_fct_trades.sql` to use the original `WHERE STG.TRADE_ID NOT IN (SELECT TRADE_ID FROM ANALYTICS.MART.FCT_TRADES)` clause. Re-execute `CREATE OR REPLACE PROCEDURE` to redeploy. |
| 1 | IS_CURRENT join predicate | Remove `AND ACC.IS_CURRENT = TRUE` from the `DIM_ACCOUNT` join in `load_fct_trades.sql`. Re-execute `CREATE OR REPLACE PROCEDURE` to redeploy. Note: rolling back Change 1 re-exposes the root-cause defect. |

**Pre-deployment requirement:** before executing Change 4 (the remediation DELETE),
take and validate a backup snapshot of `ANALYTICS.MART.FCT_TRADES` (e.g. via
`CREATE TABLE ANALYTICS.MART.FCT_TRADES_BACKUP_PROJ101 AS SELECT * FROM ANALYTICS.MART.FCT_TRADES`).
This snapshot is the rollback artefact for Change 4.

---

## Risks / open questions

| # | Risk / question | Severity | Owner |
|---|-----------------|----------|-------|
| R1 | **DIM_ACCOUNT data quality root cause.** The fan-out only occurs when `DIM_ACCOUNT` contains multiple `IS_CURRENT = TRUE` rows for the same `ACCOUNT_ID`. This is itself a data quality defect in the SCD-2 load process. This spec fixes the symptom in `LOAD_FCT_TRADES` but does not fix the upstream SCD-2 load. The SCD-2 loader should be investigated and fixed separately to prevent `IS_CURRENT` from being set incorrectly. Until that is done, the `IS_CURRENT = TRUE` guard in `LOAD_FCT_TRADES` will pick **one** of the multiple current rows (Snowflake does not guarantee which without an explicit `ORDER BY`); this may resolve to a non-deterministic `ACCOUNT_KEY`. SME should confirm whether a deterministic tie-breaker (e.g. `QUALIFY ROW_NUMBER() OVER (PARTITION BY ACCOUNT_ID ORDER BY EFFECTIVE_FROM DESC) = 1`) is needed in the join. | High | Data Engineering / SME |
| R2 | **Scale of existing duplicates.** The number of duplicate rows already in `FCT_TRADES` is unknown. Before running the remediation script, engineering should run a diagnostic query (`SELECT TRADE_ID, COUNT(*) FROM ANALYTICS.MART.FCT_TRADES GROUP BY TRADE_ID HAVING COUNT(*) > 1`) to assess scope and impact. If the count is very large (e.g. millions of rows), the DELETE may require chunking to avoid long-running transactions and table lock contention. | Medium | Data Engineering |
| R3 | **UNIQUE constraint backfill.** The `UNIQUE` constraint (Change 3) cannot be added while duplicates remain in `FCT_TRADES`. Change 4 (remediation DELETE) must complete and be validated before Change 3 is applied. The deployment order is: Change 1 → Change 2 → Change 4 → Change 3 → Change 5. | Medium | Data Engineering |
| R4 | **VW_DAILY_POSITIONS consumers.** `VW_DAILY_POSITIONS` is a view; once `FCT_TRADES` is cleaned up the view will automatically return correct values. However, any downstream reports or dashboards that cached or extracted position data during the affected period will contain stale incorrect numbers. A communication to downstream consumers (risk/reporting teams) may be needed. | Low–Medium | Data Product Owner |
| R5 | **Control-M one-time condition lifecycle.** The `PROJ-101_DEDUP-OK` condition (Change 5) must be removed from the job definition after the first clean post-fix run. If it is not removed it will block all future nightly runs. A follow-up ticket or deployment checklist item should track this removal. | Low | Scheduler / Data Engineering |
| R6 | **DIM_SECURITY also SCD-2.** `DIM_SECURITY` has the same `IS_CURRENT` / `EFFECTIVE_FROM` / `EFFECTIVE_TO` columns as `DIM_ACCOUNT`, indicating it is also an SCD-2 dimension. The join in `LOAD_FCT_TRADES` to `DIM_SECURITY` (`JOIN ANALYTICS.MART.DIM_SECURITY SEC ON SEC.SYMBOL = STG.SYMBOL`) also lacks `AND SEC.IS_CURRENT = TRUE`. This is out of scope for PROJ-101 but should be raised as a separate defect ticket to be addressed before a bad SCD-2 load on `DIM_SECURITY` causes the same class of fan-out. | Low (future risk) | Data Engineering |

---

## Approvals

- SME: SME   status: approved   date: 2026-06-10T11:36:05Z   notes: approved as-is via Jarvis gate
