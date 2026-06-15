-- Object: DIM_DATE
-- Owner: data-engineering
-- Ticket: SEED-0001
-- Description: Calendar / date dimension for the trades star schema.

CREATE OR REPLACE TABLE ANALYTICS.MART.DIM_DATE (
    DATE_KEY           NUMBER(38,0)  NOT NULL,   -- YYYYMMDD surrogate
    CALENDAR_DATE      DATE          NOT NULL,
    DAY_OF_WEEK        VARCHAR(10),
    DAY_OF_MONTH       NUMBER(2,0),
    MONTH_NUMBER       NUMBER(2,0),
    MONTH_NAME         VARCHAR(10),
    QUARTER_NUMBER     NUMBER(1,0),
    YEAR_NUMBER        NUMBER(4,0),
    IS_TRADING_DAY     BOOLEAN       NOT NULL DEFAULT TRUE,
    CONSTRAINT PK_DIM_DATE PRIMARY KEY (DATE_KEY)
);
