# Spec: PROJ-102 — Add SETTLEMENT_DATE to FCT_TRADES and expose it in VW_DAILY_POSITIONS

**Status:** AWAITING SME APPROVAL
**Verdict / severity:** FEATURE / P3
**Author:** design-agent   **Date:** 2026-06-12T09:46:00Z

## Objective

Add a `SETTLEMENT_DATE` column to `FCT_TRADES` representing the T+2 settlement date for each trade (two trading days after `TRADE_DATE`, resolved against the `DIM_DATE` calendar using the `IS_TRADING_DAY` flag). The stored procedure `LOAD_FCT_TRADES` must derive and populate this column at load time; the view `VW_DAILY_POSITIONS` must expose it so that downstream consumers can group and filter on a settlement basis. The Control-M job definition's `impacted_objects` metadata must be updated to reflect the new column. No existing columns or behaviours are changed; this is a purely additive enhancement.

## Proposed changes (ALL)

| # | File | Change | Rationale |
|---|------|--------|-----------|
| 1 | `snowflake/ddl/fct_trades.sql` | Add column `SETTLEMENT_DATE_KEY NUMBER(38,0) NOT NULL` after `TRADE_DATE_KEY`; add FK constraint `FK_FCT_TRADES_SETTLEMENT_DATE FOREIGN KEY (SETTLEMENT_DATE_KEY) REFERENCES ANALYTICS.MART.DIM_DATE (DATE_KEY)`. | Stores the resolved T+2 trading-day settlement date as a surrogate FK into `DIM_DATE`, consistent with how `TRADE_DATE_KEY` is modelled. A surrogate key (rather than a raw DATE) keeps joins within the star schema consistent and allows settlement-day attributes (e.g. `IS_TRADING_DAY`, `MONTH_NAME`) to be resolved without extra calendar arithmetic in queries. |
| 2 | `snowflake/procs/load_fct_trades.sql` | (a) Extend the `INSERT` column list with `SETTLEMENT_DATE_KEY`. (b) In the `SELECT` projection, add a correlated subquery (or lateral join) against `DIM_DATE` to resolve the settlement date key: find the `DATE_KEY` of the second `IS_TRADING_DAY = TRUE` date strictly after `STG.TRADE_DATE`, i.e. `SELECT DATE_KEY FROM ANALYTICS.MART.DIM_DATE WHERE CALENDAR_DATE > STG.TRADE_DATE AND IS_TRADING_DAY = TRUE ORDER BY CALENDAR_DATE ASC LIMIT 1` offset by 1 (second qualifying row). See Open Question OQ-1 for the exact T+2 interpretation to confirm with the SME. | Derives settlement date at load time so the fact table is self-contained; downstream views and queries need no further calendar arithmetic. |
| 3 | `snowflake/views/vw_daily_positions.sql` | Add a second join to `DIM_DATE` aliased `SD` on `SD.DATE_KEY = FT.SETTLEMENT_DATE_KEY`; add `SD.CALENDAR_DATE AS SETTLEMENT_DATE` to the `SELECT` list; add `SD.CALENDAR_DATE` to the `GROUP BY` clause. | Exposes settlement date to downstream consumers for settlement-basis reporting, which is the stated business requirement. |
| 4 | `control_m/CTM_LOAD_FCT_TRADES.json` | Add `"ANALYTICS.MART.FCT_TRADES.SETTLEMENT_DATE_KEY"` (or a descriptive note) to the `impacted_objects` array so the job manifest reflects the full scope of columns written by the procedure. No schedule or condition changes are required. | Keeps the Control-M job metadata accurate after the proc change; the `PROJ-101_DEDUP-OK` pre-condition clean-up note already present in the file is unrelated to this ticket and is left as-is for the PROJ-101 scheduler-agent to handle. |

> **Note — no DDL `ALTER TABLE` script:** The DDL file `fct_trades.sql` is used with `CREATE OR REPLACE TABLE` semantics in this repo. Change #1 is a redefinition of that file. A corresponding **one-time migration script** (`ALTER TABLE ANALYTICS.MART.FCT_TRADES ADD COLUMN SETTLEMENT_DATE_KEY NUMBER(38,0) NOT NULL`) must be executed against the existing production table before or alongside the DDL file change. This migration script should be authored and tracked by the sql-agent / data-modelling-agent under this ticket; it is listed here as a required deliverable.

## Impacted objects

| Object | Type | Schema | Impact |
|--------|------|--------|--------|
| `FCT_TRADES` | Table | `ANALYTICS.MART` | New column `SETTLEMENT_DATE_KEY`; new FK constraint |
| `LOAD_FCT_TRADES` | Stored Procedure | `ANALYTICS.MART` | Extended `INSERT`/`SELECT` to derive and populate `SETTLEMENT_DATE_KEY` |
| `VW_DAILY_POSITIONS` | View | `ANALYTICS.MART` | New join to `DIM_DATE` (settlement alias); new `SETTLEMENT_DATE` output column and `GROUP BY` term |
| `DIM_DATE` | Table (read-only) | `ANALYTICS.MART` | Referenced by the new T+2 subquery in `LOAD_FCT_TRADES` and by the new join in `VW_DAILY_POSITIONS`; no DDL changes |
| `CTM_LOAD_FCT_TRADES` | Control-M Job | `DWH_NIGHTLY` | `impacted_objects` metadata updated; no schedule or condition changes |
| Migration script (new) | One-time SQL | — | `ALTER TABLE` to add column to existing production table |

## Test plan

### Unit tests

- **UT-1 Standard T+2 (no weekend/holiday boundary):** Stage a trade with `TRADE_DATE = 2026-06-10` (Wednesday). Verify `SETTLEMENT_DATE_KEY` resolves to `DIM_DATE.DATE_KEY` for `2026-06-12` (Friday — two trading days forward, assuming both Thursday and Friday are `IS_TRADING_DAY = TRUE`).
- **UT-2 T+2 crosses a weekend:** Stage a trade with `TRADE_DATE = 2026-06-12` (Friday). Verify settlement resolves to the second trading day after Friday, skipping Saturday and Sunday — expected `2026-06-16` (Tuesday), assuming Monday is a trading day.
- **UT-3 T+2 crosses a market holiday:** Seed `DIM_DATE` with a holiday (`IS_TRADING_DAY = FALSE`) on the first candidate day after trade date. Verify the procedure skips that day and resolves to the correct second trading day.
- **UT-4 Missing DIM_DATE coverage:** Stage a trade whose T+2 settlement date does not exist in `DIM_DATE` (calendar not yet populated far enough). Verify the procedure raises a descriptive error or returns a zero row-count with an appropriate message rather than inserting a NULL FK or silently dropping the row. The exact error-handling behaviour is an open question (see OQ-2).
- **UT-5 VW_DAILY_POSITIONS settlement column:** After a successful load, query `VW_DAILY_POSITIONS` and confirm `SETTLEMENT_DATE` is populated, non-null, and equals the `CALENDAR_DATE` corresponding to `FCT_TRADES.SETTLEMENT_DATE_KEY` for each row.
- **UT-6 No duplicate or fan-out rows in view:** Confirm that adding the second `DIM_DATE` join in `VW_DAILY_POSITIONS` does not increase row count relative to the pre-change baseline (i.e. the join is 1:1, not 1:many).
- **UT-7 Existing column regression — TRADE_DATE unaffected:** Verify that `TRADE_DATE` and all pre-existing columns in `VW_DAILY_POSITIONS` return identical values before and after the change.
- **UT-8 FCT_TRADES NOT NULL constraint:** Attempt to insert a row into `FCT_TRADES` with `SETTLEMENT_DATE_KEY = NULL`; confirm the constraint is enforced.
- **UT-9 FK constraint enforcement:** Attempt to insert a row with a `SETTLEMENT_DATE_KEY` value not present in `DIM_DATE`; confirm the FK constraint rejects the row.

### Regression tests

- Re-run the full `LOAD_FCT_TRADES` procedure against the existing staging data fixture used in PROJ-101 regression; confirm row counts are unchanged and no existing columns are modified.
- Re-run any existing `VW_DAILY_POSITIONS` regression queries; confirm all pre-existing output columns (`ACCOUNT_ID`, `ACCOUNT_NAME`, `SYMBOL`, `SECURITY_NAME`, `TRADE_DATE`, `BUY_QUANTITY`, `SELL_QUANTITY`, `NET_QUANTITY`, `NET_AMOUNT`) return identical values.
- Update the regression catalog to add `SETTLEMENT_DATE` as a tracked output column of `VW_DAILY_POSITIONS`.
- Confirm the Control-M job `CTM_LOAD_FCT_TRADES` still passes its validation / dry-run check after the JSON metadata update.

## Rollback plan

1. **`VW_DAILY_POSITIONS`** — `CREATE OR REPLACE VIEW` with the prior definition (remove the `SD` join, remove `SETTLEMENT_DATE` from `SELECT` and `GROUP BY`). This is safe at any time and has no data impact; re-running the original view DDL is sufficient.
2. **`LOAD_FCT_TRADES`** — `CREATE OR REPLACE PROCEDURE` with the prior definition (remove `SETTLEMENT_DATE_KEY` from `INSERT` and `SELECT`). Must be done before or simultaneously with step 3 to avoid insert failures caused by a NOT NULL column still present on the table.
3. **`FCT_TRADES` column** — Execute `ALTER TABLE ANALYTICS.MART.FCT_TRADES DROP COLUMN SETTLEMENT_DATE_KEY`. This is a destructive DDL operation; all settled-date data loaded since the feature went live will be lost. A table backup or zero-copy clone should be taken immediately before the production deployment to enable point-in-time recovery if needed.
4. **`fct_trades.sql` DDL file** — Revert to the pre-PROJ-102 version in source control.
5. **`load_fct_trades.sql` proc file** — Revert to the pre-PROJ-102 version in source control.
6. **`vw_daily_positions.sql` view file** — Revert to the pre-PROJ-102 version in source control.
7. **`CTM_LOAD_FCT_TRADES.json`** — Revert the `impacted_objects` array to its pre-PROJ-102 state in source control; redeploy the job definition.

Rollback order: step 1 (view) → step 2 (proc) → step 3 (table column drop). Steps 4–7 are source-control reversions and can proceed in any order after the live objects are reverted.

## Risks / open questions

- **OQ-1 (CRITICAL — blocks implementation): Calendar T+2 vs. trading-day T+2.** The ticket states "T+2 from trade date" but does not specify whether T+2 means two *calendar* days (`DATEADD(DAY, 2, TRADE_DATE)`) or two *trading days* (second `IS_TRADING_DAY = TRUE` date after `TRADE_DATE` in `DIM_DATE`). These differ on Fridays, pre-holiday dates, and holiday-adjacent dates. The `DIM_DATE.IS_TRADING_DAY` column exists and is available, but its use must be mandated by the SME. **SME must confirm the exact T+2 convention before the sql-agent/stored-proc-agent implements change #2.**

- **OQ-2: Behaviour when DIM_DATE does not contain the settlement date.** If the DIM_DATE calendar has not been populated far enough forward (e.g. a trade loaded near the end of the calendar table), the T+2 subquery returns no row. Should the procedure (a) fail the entire batch, (b) skip only the affected rows and log a warning, or (c) default to `DATEADD(DAY, 2, TRADE_DATE)` calendar days as a fallback? The NOT NULL constraint on `SETTLEMENT_DATE_KEY` means option (c) would require a separate DIM_DATE row to exist for the fallback date. SME to decide.

- **OQ-3: NOT NULL vs. NULLABLE for SETTLEMENT_DATE_KEY.** Defining the column `NOT NULL` is the cleanest model but means the loader will reject any trade whose settlement date cannot be resolved (see OQ-2). If business continuity requires trades to load even when settlement cannot be resolved, the column should be `NULL`-able (with a downstream alert). SME to confirm.

- **OQ-4: Impact on downstream consumers of VW_DAILY_POSITIONS.** Adding `SETTLEMENT_DATE` to the `GROUP BY` changes the granularity of the view — rows that previously grouped by `(ACCOUNT_ID, SYMBOL, TRADE_DATE)` will now also group by `SETTLEMENT_DATE`. Because `SETTLEMENT_DATE` is deterministically derived from `TRADE_DATE`, each `TRADE_DATE` maps to exactly one `SETTLEMENT_DATE`, so the group key is extended but not multiplied. This must be verified by the impact-analysis-agent and confirmed with downstream report owners before deployment.

- **OQ-5: `VW_DAILY_POSITIONS` join to DIM_DATE on IS_CURRENT.** The current view joins `DIM_DATE` without an `IS_CURRENT` filter (DIM_DATE is not an SCD-2 table, so this is correct). Confirm that DIM_DATE has no duplicate `DATE_KEY` rows that could cause fan-out on the new settlement join.

- **OQ-6: PROJ-101_DEDUP-OK pre-condition in CTM job.** The Control-M job already contains a one-time pre-condition from PROJ-101. The scheduler-agent should confirm whether that condition has been retired before this feature is deployed, to avoid blocking the PROJ-102 load run on a condition that may no longer be emitted.

- **R-1: Production migration script risk.** Adding a NOT NULL column to a large production table with `ALTER TABLE` can be a long-running or locking operation depending on Snowflake's internal handling. The sql-agent should evaluate whether a phased approach (add as NULLABLE, backfill, then add NOT NULL constraint) is safer.

## Approvals

- SME: __________   status: pending   date: ______
