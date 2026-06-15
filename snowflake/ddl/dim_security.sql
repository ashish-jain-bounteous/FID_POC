-- Object: DIM_SECURITY
-- Owner: data-engineering
-- Ticket: SEED-0001
-- Description: Security / instrument dimension for the trades star schema.

CREATE OR REPLACE TABLE ANALYTICS.MART.DIM_SECURITY (
    SECURITY_KEY       NUMBER(38,0)  NOT NULL,   -- surrogate key
    SYMBOL             VARCHAR(20)   NOT NULL,    -- natural/business key (ticker)
    SECURITY_NAME      VARCHAR(200),
    ASSET_CLASS        VARCHAR(40),               -- EQUITY, BOND, ETF, MMF, ...
    EXCHANGE           VARCHAR(40),
    CURRENCY_CODE      VARCHAR(3),
    SECTOR             VARCHAR(80),
    EFFECTIVE_FROM     TIMESTAMP_NTZ NOT NULL,
    EFFECTIVE_TO       TIMESTAMP_NTZ,
    IS_CURRENT         BOOLEAN       NOT NULL DEFAULT TRUE,
    CONSTRAINT PK_DIM_SECURITY PRIMARY KEY (SECURITY_KEY)
);
