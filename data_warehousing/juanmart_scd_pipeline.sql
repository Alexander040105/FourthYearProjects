-- ============================================================
-- JuanMart Slowly Changing Dimension Type 2 Pipeline
-- Lab 1.3 — dim_customer SCD2 Implementation
-- ============================================================
-- Tracks historical address/region changes for customers.
-- When a customer's region changes:
--   1. Expire the current record (set is_current=FALSE, end_date=new date)
--   2. Insert a new current record (effective_date=new date, is_current=TRUE)
--
-- Compatible with PostgreSQL (MERGE) / Snowflake / SQL Server.
-- ============================================================

-- ============================================================
-- SECTION 1: dim_customer Table (SCD2)
-- ============================================================

CREATE TABLE dim_customer (
    customer_key         SERIAL PRIMARY KEY,
    customer_natural_key VARCHAR(200) NOT NULL,   -- business key (e.g. customer name or ID)
    cust_name            VARCHAR(200) NOT NULL,
    region_name          VARCHAR(100) NOT NULL,
    effective_date       DATE NOT NULL,            -- when this version became active
    end_date             DATE,                     -- when this version was superseded (NULL = current)
    is_current           BOOLEAN DEFAULT TRUE,
    created_at           TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for SCD2 lookups
CREATE INDEX idx_dim_customer_natural_key ON dim_customer(customer_natural_key);
CREATE INDEX idx_dim_customer_current     ON dim_customer(customer_natural_key, is_current) WHERE is_current = TRUE;

-- ============================================================
-- SECTION 2: Staging Table for Incoming Customer Changes
-- ============================================================
-- This represents the cleaned, standardized customer data
-- arriving from the cleansing pipeline (juanmart_sanitizer.py).

CREATE TABLE stg_customer_updates (
    customer_natural_key VARCHAR(200) NOT NULL,
    cust_name            VARCHAR(200) NOT NULL,
    region_name          VARCHAR(100) NOT NULL,
    order_date           DATE NOT NULL,            -- used as effective_date for SCD2
    loaded_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- SECTION 3: SCD2 MERGE / UPSERT Logic
-- ============================================================
-- This MERGE statement handles three scenarios:
--   A) New customer → INSERT as new current record
--   B) Existing customer, same region → no change (UPDATE is a no-op)
--   C) Existing customer, region changed → expire old record, INSERT new version
-- ============================================================

-- 3.1 Expire existing current records where region has changed
-- ============================================================
UPDATE dim_customer AS dc
SET
    end_date     = stu.order_date,
    is_current   = FALSE,
    updated_at   = CURRENT_TIMESTAMP
FROM stg_customer_updates AS stu
WHERE dc.customer_natural_key = stu.customer_natural_key
  AND dc.is_current = TRUE
  AND dc.region_name <> stu.region_name;

-- 3.2 Insert new current records for:
--   - Brand new customers (not in dim_customer at all)
--   - Customers whose region just changed (old record expired above)
-- ============================================================
INSERT INTO dim_customer (
    customer_natural_key,
    cust_name,
    region_name,
    effective_date,
    end_date,
    is_current
)
SELECT
    stu.customer_natural_key,
    stu.cust_name,
    stu.region_name,
    stu.order_date,
    NULL,
    TRUE
FROM stg_customer_updates AS stu
WHERE NOT EXISTS (
    SELECT 1
    FROM dim_customer AS dc
    WHERE dc.customer_natural_key = stu.customer_natural_key
      AND dc.is_current = TRUE
      AND dc.region_name = stu.region_name
);

-- ============================================================
-- SECTION 4: Alternative Single-Statement MERGE (PostgreSQL 15+)
-- ============================================================
-- For databases that support MERGE (PostgreSQL 15+, Oracle, Snowflake,
-- SQL Server), the above two steps can be combined into a single MERGE:

/*
MERGE INTO dim_customer AS target
USING (
    SELECT
        customer_natural_key,
        cust_name,
        region_name,
        order_date
    FROM stg_customer_updates
) AS source
ON target.customer_natural_key = source.customer_natural_key
   AND target.is_current = TRUE

WHEN MATCHED AND target.region_name <> source.region_name THEN
    -- Region changed: expire the old record
    UPDATE SET
        end_date   = source.order_date,
        is_current = FALSE

WHEN NOT MATCHED THEN
    -- New customer or new version: insert new current record
    INSERT (customer_natural_key, cust_name, region_name, effective_date, end_date, is_current)
    VALUES (source.customer_natural_key, source.cust_name, source.region_name, source.order_date, NULL, TRUE);
*/

-- ============================================================
-- SECTION 5: Post-Merge Cleanup — Insert New Versions
-- ============================================================
-- After the MERGE expires old records, we still need to insert
-- the new version for changed customers. This handles that step:

INSERT INTO dim_customer (
    customer_natural_key,
    cust_name,
    region_name,
    effective_date,
    end_date,
    is_current
)
SELECT
    stu.customer_natural_key,
    stu.cust_name,
    stu.region_name,
    stu.order_date,
    NULL,
    TRUE
FROM stg_customer_updates AS stu
WHERE EXISTS (
    -- Customer exists but has no current record matching the new region
    SELECT 1
    FROM dim_customer AS dc
    WHERE dc.customer_natural_key = stu.customer_natural_key
      AND dc.is_current = FALSE
      AND dc.end_date = stu.order_date
)
AND NOT EXISTS (
    -- Don't insert if a current record with this region already exists
    SELECT 1
    FROM dim_customer AS dc
    WHERE dc.customer_natural_key = stu.customer_natural_key
      AND dc.is_current = TRUE
      AND dc.region_name = stu.region_name
);

-- ============================================================
-- SECTION 6: Verification Queries
-- ============================================================

-- 6.1 View all customer versions (history)
-- ============================================================
SELECT
    customer_key,
    customer_natural_key,
    cust_name,
    region_name,
    effective_date,
    end_date,
    is_current
FROM dim_customer
ORDER BY customer_natural_key, effective_date;

-- 6.2 View only current customer records
-- ============================================================
SELECT
    customer_key,
    customer_natural_key,
    cust_name,
    region_name,
    effective_date
FROM dim_customer
WHERE is_current = TRUE
ORDER BY customer_natural_key;

-- 6.3 Count versions per customer (detect frequent movers)
-- ============================================================
SELECT
    customer_natural_key,
    cust_name,
    COUNT(*) AS version_count,
    MIN(effective_date) AS first_seen,
    MAX(effective_date) AS last_change
FROM dim_customer
GROUP BY customer_natural_key, cust_name
HAVING COUNT(*) > 1
ORDER BY version_count DESC;

-- 6.4 Join fact_sales to SCD2 dim_customer to get
--     the region the customer lived in AT TIME OF PURCHASE
-- ============================================================
/*
SELECT
    f.transaction_id,
    f.amount_paid,
    c.cust_name,
    c.region_name AS region_at_purchase,
    f.order_date
FROM fact_sales f
JOIN dim_customer c
  ON f.customer_key = c.customer_key
  AND f.order_date >= c.effective_date
  AND (f.order_date < c.end_date OR c.end_date IS NULL)
ORDER BY f.transaction_id;
*/
