-- Object: DIM_ACCOUNT
-- Owner: data-engineering
-- Ticket: SEED-0001
-- Description: Account / customer dimension for the trades star schema.

CREATE OR REPLACE TABLE ANALYTICS.MART.DIM_ACCOUNT (
    ACCOUNT_KEY        NUMBER(38,0)  NOT NULL,   -- surrogate key
    ACCOUNT_ID         VARCHAR(20)   NOT NULL,   -- natural/business key
    ACCOUNT_NAME       VARCHAR(200),
    ACCOUNT_TYPE       VARCHAR(40),              -- BROKERAGE, RETIREMENT, ...
    CUSTOMER_SEGMENT   VARCHAR(40),
    OPEN_DATE          DATE,
    STATUS             VARCHAR(20),
    EFFECTIVE_FROM     TIMESTAMP_NTZ NOT NULL,
    EFFECTIVE_TO       TIMESTAMP_NTZ,
    IS_CURRENT         BOOLEAN       NOT NULL DEFAULT TRUE,
    CONSTRAINT PK_DIM_ACCOUNT PRIMARY KEY (ACCOUNT_KEY)
);
