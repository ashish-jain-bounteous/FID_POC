-- Object: FCT_TRADES (one-time dedup remediation)
-- Owner: data-engineering
-- Ticket: PROJ-101
-- Description: Run-once remediation that removes duplicate TRADE_ID rows already
--              present in ANALYTICS.MART.FCT_TRADES (inserted by prior nightly
--              runs before the IS_CURRENT join fix). Keeps the earliest row per
--              TRADE_ID by LOAD_TIMESTAMP. Idempotent: a second run deletes zero
--              rows. Must run AFTER the proc fix (Changes 1-2) and BEFORE adding
--              the UNIQUE constraint (Change 3).
--
-- PRE-DEPLOYMENT REQUIREMENT (manual runbook step, not executed here):
--   Take a validated backup snapshot first, e.g.
--   CREATE TABLE ANALYTICS.MART.FCT_TRADES_BACKUP_PROJ101 AS
--     SELECT TRADE_KEY, TRADE_ID, ACCOUNT_KEY, SECURITY_KEY, TRADE_DATE_KEY,
--            SIDE, QUANTITY, PRICE, GROSS_AMOUNT, FEE_AMOUNT, NET_AMOUNT, LOAD_TIMESTAMP
--     FROM ANALYTICS.MART.FCT_TRADES;

BEGIN TRANSACTION;

-- Delete all but the earliest-loaded row per TRADE_ID.
DELETE FROM ANALYTICS.MART.FCT_TRADES
WHERE TRADE_KEY IN (
    SELECT TRADE_KEY
    FROM (
        SELECT
            TRADE_KEY,
            ROW_NUMBER() OVER (
                PARTITION BY TRADE_ID
                ORDER BY LOAD_TIMESTAMP ASC, TRADE_KEY ASC
            ) AS RN
        FROM ANALYTICS.MART.FCT_TRADES
    ) RANKED
    WHERE RANKED.RN > 1
);

COMMIT;

-- Verification (expect zero rows after remediation):
--   SELECT TRADE_ID, COUNT(*) AS DUP_COUNT
--   FROM ANALYTICS.MART.FCT_TRADES
--   GROUP BY TRADE_ID
--   HAVING COUNT(*) > 1;
