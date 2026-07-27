-- ============================================================
-- JuanMart Schema Audit & 3NF Normalization Proposal
-- Lab 1.1 — Diagnostic SQL Script
-- ============================================================
-- This script assumes a staging table `stg_juanmart_raw_sales`
-- has been loaded from juanmart_raw_sales.csv.
-- Compatible with PostgreSQL / Snowflake / BigQuery (ANSI SQL).
-- ============================================================

-- ============================================================
-- SECTION 1: Diagnostic Queries
-- ============================================================

-- 1.1 Detect duplicate transaction_id rows
-- ============================================================
SELECT
    transaction_id,
    COUNT(*) AS occurrence_count
FROM stg_juanmart_raw_sales
GROUP BY transaction_id
HAVING COUNT(*) > 1
ORDER BY transaction_id;

-- 1.2 Show the full duplicate rows for manual review
-- ============================================================
SELECT *
FROM stg_juanmart_raw_sales
WHERE transaction_id IN (
    SELECT transaction_id
    FROM stg_juanmart_raw_sales
    GROUP BY transaction_id
    HAVING COUNT(*) > 1
)
ORDER BY transaction_id;

-- 1.3 Detect NULL amount_paid values
-- ============================================================
SELECT
    transaction_id,
    cust_name,
    region,
    order_date,
    amount_paid,
    status
FROM stg_juanmart_raw_sales
WHERE amount_paid IS NULL
   OR TRIM(CAST(amount_paid AS VARCHAR)) = ''
ORDER BY transaction_id;

-- 1.4 Detect NULL or empty cust_name values
-- ============================================================
SELECT
    transaction_id,
    cust_name,
    region,
    order_date,
    amount_paid,
    status
FROM stg_juanmart_raw_sales
WHERE cust_name IS NULL
   OR TRIM(CAST(cust_name AS VARCHAR)) = ''
ORDER BY transaction_id;

-- 1.5 Detect non-standard region values
--   Valid standardized regions are:
--     'National Capital Region', 'CALABARZON'
--   Any other value is non-standard and needs cleansing.
-- ============================================================
SELECT
    region AS raw_region_value,
    COUNT(*) AS row_count
FROM stg_juanmart_raw_sales
GROUP BY region
ORDER BY region;

-- Full list of rows with non-standard regions
SELECT *
FROM stg_juanmart_raw_sales
WHERE region NOT IN (
    'National Capital Region',
    'CALABARZON'
)
ORDER BY transaction_id;

-- 1.6 Detect mixed date formats (non-ISO dates)
--   ISO 8601 format: YYYY-MM-DD
--   Non-standard: YYYY/MM/DD or any other format
-- ============================================================
SELECT
    transaction_id,
    order_date,
    CASE
        WHEN order_date ~ '^\d{4}-\d{2}-\d{2}$' THEN 'YYYY-MM-DD (ISO)'
        WHEN order_date ~ '^\d{4}/\d{2}/\d{2}$' THEN 'YYYY/MM/DD (non-ISO)'
        ELSE 'UNKNOWN'
    END AS date_format
FROM stg_juanmart_raw_sales
ORDER BY transaction_id;

-- 1.7 Overall data quality summary
-- ============================================================
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT transaction_id) AS distinct_transaction_ids,
    COUNT(*) - COUNT(DISTINCT transaction_id) AS duplicate_row_count,
    SUM(CASE WHEN cust_name IS NULL OR TRIM(CAST(cust_name AS VARCHAR)) = '' THEN 1 ELSE 0 END) AS null_cust_name_count,
    SUM(CASE WHEN amount_paid IS NULL OR TRIM(CAST(amount_paid AS VARCHAR)) = '' THEN 1 ELSE 0 END) AS null_amount_paid_count,
    COUNT(DISTINCT region) AS distinct_region_values,
    SUM(CASE WHEN order_date NOT LIKE '%-%' THEN 1 ELSE 0 END) AS non_iso_date_count
FROM stg_juanmart_raw_sales;


-- ============================================================
-- SECTION 2: 3NF Normalization Proposal
-- ============================================================
-- The raw flat table violates 3NF because:
--   - region is embedded in the sales row (transitive dependency)
--   - status is a repeating descriptive attribute
--   - customer details are denormalized into the sales row
--
-- Normalized entities:
--   dim_customer  — customer master (SCD2-ready)
--   dim_region    — region reference lookup
--   dim_status    — order status reference lookup
--   stg_sales_order — transactional fact staging (normalized)
-- ============================================================

-- 2.1 Region dimension table
-- ============================================================
CREATE TABLE dim_region (
    region_key       SERIAL PRIMARY KEY,
    region_name      VARCHAR(100) NOT NULL UNIQUE,
    region_code      VARCHAR(20),
    parent_region    VARCHAR(100),
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Seed with standardized values
INSERT INTO dim_region (region_name, region_code) VALUES
    ('National Capital Region', 'NCR'),
    ('CALABARZON', 'CALABARZON');

-- 2.2 Status dimension table
-- ============================================================
CREATE TABLE dim_status (
    status_key       SERIAL PRIMARY KEY,
    status_name      VARCHAR(50) NOT NULL UNIQUE,
    is_revenue_recognized BOOLEAN DEFAULT FALSE,
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Seed with known statuses
INSERT INTO dim_status (status_name, is_revenue_recognized) VALUES
    ('Completed', TRUE),
    ('Cancelled', FALSE),
    ('Returned', FALSE);

-- 2.3 Customer dimension table (SCD2-ready)
-- ============================================================
CREATE TABLE dim_customer (
    customer_key     SERIAL PRIMARY KEY,
    customer_natural_key VARCHAR(200),   -- natural key: cust_name (ideally a customer_id)
    cust_name        VARCHAR(200) NOT NULL,
    region_key       INTEGER REFERENCES dim_region(region_key),
    effective_date   DATE NOT NULL,
    end_date         DATE,
    is_current       BOOLEAN DEFAULT TRUE,
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2.4 Calendar dimension table
-- ============================================================
CREATE TABLE dim_calendar (
    date_key         SERIAL PRIMARY KEY,
    full_date        DATE NOT NULL UNIQUE,
    year             INTEGER NOT NULL,
    quarter          INTEGER NOT NULL,
    month            INTEGER NOT NULL,
    month_name       VARCHAR(20),
    day_of_week      VARCHAR(20),
    is_weekend       BOOLEAN
);

-- 2.5 Normalized sales order staging table (fact grain)
-- ============================================================
CREATE TABLE stg_sales_order (
    transaction_id   INTEGER NOT NULL,
    customer_key     INTEGER REFERENCES dim_customer(customer_key),
    region_key       INTEGER REFERENCES dim_region(region_key),
    status_key       INTEGER REFERENCES dim_status(status_key),
    order_date       DATE NOT NULL,
    amount_paid      NUMERIC(12, 2),
    loaded_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (transaction_id)
);

-- 2.6 View: Denormalized audit view (joins all dims back for verification)
-- ============================================================
CREATE OR REPLACE VIEW v_sales_audit AS
SELECT
    s.transaction_id,
    c.cust_name,
    r.region_name,
    s.order_date,
    s.amount_paid,
    st.status_name
FROM stg_sales_order s
JOIN dim_customer  c  ON s.customer_key = c.customer_key
JOIN dim_region    r  ON s.region_key   = r.region_key
JOIN dim_status    st ON s.status_key   = st.status_key
ORDER BY s.transaction_id;
