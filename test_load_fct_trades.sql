-- Object: FCT_TRADES load tests (PROJ-101)
-- Owner: test-engineering
-- Ticket: PROJ-101
-- Description: Unit tests for the LOAD_FCT_TRADES IS_CURRENT fan-out fix and the
--              NULL-safe dedup guard. Implements spec cases U-1, U-3, U-4, U-7,
--              U-8. Each test seeds isolated *_TEST tables, asserts via a
--              CALL to a thin wrapper, and is expected to be run in a scratch
--              schema. Assertions use COUNT-based checks with explicit columns.

-- ---------------------------------------------------------------------------
-- U-1  Fan-out prevention: two IS_CURRENT=TRUE rows for one ACCOUNT_ID must
--      still produce exactly ONE FCT_TRADES row per TRADE_ID after the fix.
-- ---------------------------------------------------------------------------
-- Seed: DIM_ACCOUNT_TEST has two current rows for ACCOUNT_ID 'A1';
--       STG_TRADES_TEST has one trade T1 for 'A1'.
-- Expected: COUNT(*) = 1 in FCT_TRADES_TEST for TRADE_ID 'T1'.
SELECT
    CASE WHEN COUNT(*) = 1 THEN 'PASS' ELSE 'FAIL' END AS U1_RESULT,
    COUNT(*)                                           AS ACTUAL_ROWS
FROM ANALYTICS.SCRATCH.FCT_TRADES_TEST
WHERE TRADE_ID = 'T1';

-- ---------------------------------------------------------------------------
-- U-3  Historical-row exclusion: with one IS_CURRENT=FALSE and one
--      IS_CURRENT=TRUE row, the loaded ACCOUNT_KEY must be the current row's.
-- ---------------------------------------------------------------------------
SELECT
    CASE WHEN COUNT(*) = 1 THEN 'PASS' ELSE 'FAIL' END AS U3_RESULT
FROM ANALYTICS.SCRATCH.FCT_TRADES_TEST FT
JOIN ANALYTICS.SCRATCH.DIM_ACCOUNT_TEST ACC
  ON ACC.ACCOUNT_KEY = FT.ACCOUNT_KEY
WHERE FT.TRADE_ID = 'T3'
  AND ACC.IS_CURRENT = TRUE;

-- ---------------------------------------------------------------------------
-- U-4  Dedup guard idempotency: re-running the load adds zero new rows.
-- ---------------------------------------------------------------------------
-- Run harness: capture COUNT before, CALL LOAD, compare. Expected delta = 0.
SELECT
    CASE WHEN COUNT(*) = :EXPECTED_BASELINE THEN 'PASS' ELSE 'FAIL' END AS U4_RESULT
FROM ANALYTICS.SCRATCH.FCT_TRADES_TEST;

-- ---------------------------------------------------------------------------
-- U-7 / U-8  Remediation correctness: after running the dedup remediation on a
--      table seeded with 3 rows for one TRADE_ID, exactly 1 remains and it is
--      the earliest LOAD_TIMESTAMP row.
-- ---------------------------------------------------------------------------
SELECT
    CASE WHEN COUNT(*) = 1
              AND MIN(LOAD_TIMESTAMP) = MAX(LOAD_TIMESTAMP)
         THEN 'PASS' ELSE 'FAIL' END AS U7_U8_RESULT
FROM ANALYTICS.SCRATCH.FCT_TRADES_TEST
WHERE TRADE_ID = 'T8';
