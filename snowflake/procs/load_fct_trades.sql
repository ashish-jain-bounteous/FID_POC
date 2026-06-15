-- Object: LOAD_FCT_TRADES
-- Owner: data-engineering
-- Ticket: PROJ-101
-- Description: Nightly load of FCT_TRADES from staging. Resolves dimension keys
--              and inserts new trades. Scheduled by Control-M job CTM_LOAD_FCT_TRADES.
--              PROJ-101: DIM_ACCOUNT join now filters IS_CURRENT = TRUE to prevent
--              SCD-2 fan-out duplicates; dedup guard uses NULL-safe NOT EXISTS.

CREATE OR REPLACE PROCEDURE ANALYTICS.MART.LOAD_FCT_TRADES()
RETURNS STRING
LANGUAGE SQL
AS
$$
DECLARE
    ROWS_INSERTED NUMBER DEFAULT 0;
BEGIN
    INSERT INTO ANALYTICS.MART.FCT_TRADES (
        TRADE_KEY,
        TRADE_ID,
        ACCOUNT_KEY,
        SECURITY_KEY,
        TRADE_DATE_KEY,
        SIDE,
        QUANTITY,
        PRICE,
        GROSS_AMOUNT,
        FEE_AMOUNT,
        NET_AMOUNT,
        LOAD_TIMESTAMP
    )
    SELECT
        ANALYTICS.MART.SEQ_FCT_TRADES.NEXTVAL,
        STG.TRADE_ID,
        ACC.ACCOUNT_KEY,
        SEC.SECURITY_KEY,
        DT.DATE_KEY,
        STG.SIDE,
        STG.QUANTITY,
        STG.PRICE,
        STG.QUANTITY * STG.PRICE                         AS GROSS_AMOUNT,
        STG.FEE_AMOUNT,
        (STG.QUANTITY * STG.PRICE) - STG.FEE_AMOUNT      AS NET_AMOUNT,
        CURRENT_TIMESTAMP()
    FROM ANALYTICS.STAGE.STG_TRADES STG
    JOIN ANALYTICS.MART.DIM_ACCOUNT  ACC ON ACC.ACCOUNT_ID = STG.ACCOUNT_ID
                                        AND ACC.IS_CURRENT = TRUE
    JOIN ANALYTICS.MART.DIM_SECURITY SEC ON SEC.SYMBOL     = STG.SYMBOL
    JOIN ANALYTICS.MART.DIM_DATE     DT  ON DT.CALENDAR_DATE = STG.TRADE_DATE
    WHERE NOT EXISTS (
        SELECT 1 FROM ANALYTICS.MART.FCT_TRADES FT2
        WHERE FT2.TRADE_ID = STG.TRADE_ID
    );

    ROWS_INSERTED := SQLROWCOUNT;
    RETURN 'LOAD_FCT_TRADES complete. Rows inserted: ' || ROWS_INSERTED;
END;
$$;
