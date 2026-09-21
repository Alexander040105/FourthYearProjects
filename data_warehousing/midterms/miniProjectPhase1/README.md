# Mini Project Phase 1 — Group 8: Retail Grocery Inventory & POS Warehouse

**Business scenario:** A supermarket chain needs to monitor daily store sales,
stock turnover rates, and inventory reorder thresholds across multiple branches.

**Pipeline:** process the messy POS extract → clean currency symbols, dates, and
headers → load a star-schema SQLite warehouse → store derived supplier audit
logs in MongoDB → run monthly sales variance queries using SQL CTEs.

## Files

| File | Purpose |
|---|---|
| `Grocery_Inventory_and_Sales_Dataset.csv` | Raw extract (990 rows × 16 cols) |
| `grocery_etl.py` | Full ETL pipeline: extract → cleanse → SQLite + MongoDB load → analytics |
| `monthly_variance.sql` | CTE-based analytics (monthly variance, reorder pressure, stockout list) |
| `miniProjectPhase1.ipynb` | Narrated walkthrough notebook (executed) |
| `cleaned_grocery_inventory.csv` | Cleaned output dataset |
| `quarantined_rows.csv` | Rows that failed validation (with reason) — currently empty |
| `grocery_warehouse.db` | SQLite warehouse (star schema + views) |
| `supplier_audit_logs.json` | Local export of the MongoDB audit documents |
| `mongo_verification.json` | Sample document + collection count proof |
| `pipeline_summary.txt` | Full run report |

## Data quality issues found & fixed

| Issue | Evidence | Fix |
|---|---|---|
| Currency symbols in price | `Unit_Price` = `"$4.50 "` on all 990 rows | strip `$`, commas, whitespace → `REAL` |
| Misspelled header | `Catagory` | renamed → `category` |
| Missing category | 1 null | imputed `'Uncategorized'` + `MISSING_CATEGORY` audit event |
| Mixed-width dates | `M/D/YYYY`, `MM/DD/YYYY`, etc. | parsed → ISO `YYYY-MM-DD` |
| Unvalidated IDs | `XX-XXX-XXXX` pattern assumed | regex-validated; failures would be quarantined |

## Warehouse model

The raw `product_id` / `supplier_id` are record-level (unique per row), so the
business entities become dimension keys:

```
 dim_product              dim_supplier             dim_store
 (name + category, 124)   (name, 350)              (location, 990)
        \                       |                       /
         \                      |                      /
                    fact_inventory (990 rows)
   measures: stock_quantity, reorder_level, reorder_quantity,
   unit_price, sales_volume, inventory_turnover_rate,
   date_received, last_order_date, expiration_date, status
```

Views supporting the expected outcome:

- **`v_reorder_recommendations`** — every item at/below reorder level with
  `suggested_order_qty` and a CRITICAL/HIGH replenishment priority →
  automated replenishment queue.
- **`v_stockout_risk`** — `days_of_cover` (on-hand ÷ daily sales velocity)
  tiered CRITICAL (<7d) / HIGH (<15d) / WATCH (<30d) / LOW → stockout
  prevention watchlist.

## MongoDB — `supplier_audit_logs`

One document per supplier entity (350 docs), keyed on `supplier_name`, with an
embedded `audit_events` array derived deterministically from the data:

| Event type | Severity | Trigger |
|---|---|---|
| `REORDER_TRIGGERED` | HIGH | `stock_quantity ≤ reorder_level` |
| `STOCKOUT_RISK` | CRITICAL | on-hand < half of sales volume |
| `EXPIRED_BEFORE_LAST_ORDER` | MEDIUM | `expiration_date < last_order_date` (data anomaly) |
| `BACKORDERED` | HIGH | `status = 'Backordered'` |
| `DISCONTINUED_WITH_STOCK` | LOW | discontinued but stock remains |
| `MISSING_CATEGORY` | LOW | category was null in source |

## How to run

From the repo root, using the project `.venv`:

```powershell
cd data_warehousing\midterms\miniProjectPhase1
..\..\..\.venv\Scripts\python.exe grocery_etl.py                # full run (needs MONGODB_URI)
..\..\..\.venv\Scripts\python.exe grocery_etl.py --dry-run      # offline run via mongomock
..\..\..\.venv\Scripts\python.exe grocery_etl.py --skip-mongo   # SQLite only
..\..\..\.venv\Scripts\python.exe grocery_etl.py --full-refresh # rebuild targets
```

MongoDB connection is read from `MONGODB_URI` / `MONGODB_DATABASE` in the first
`.env` found in this folder, then `data_warehousing/.env`. Re-runs are
idempotent (`row_hash` UNIQUE in SQLite, `_id = supplier_name` upserts in
MongoDB).

## Headline results

- 990/990 rows cleaned, 0 quarantined; all prices normalized to numeric.
- Monthly sales variance (CTE + `LAG()`) covers 13 months, 2024-02 → 2025-02.
- 298 items flagged for replenishment; 27 items at CRITICAL stockout risk.
- 350 supplier audit documents capturing 1,839 events.
