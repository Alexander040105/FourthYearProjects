# Group Analytical Summary Report

## Retail Grocery Inventory & Point-of-Sale (POS) Warehouse

**Group 8** — Members: *[list member names here]*
Course: Data Warehousing · Mini Project Phase 1–2 · *[date]*

---

## 1. Business scenario

A supermarket chain needs to monitor daily store sales, stock turnover
rates, and inventory reorder thresholds across multiple branches. The
goal: a warehouse model that supports **automated inventory
replenishment** and **stockout prevention**.

We built an end-to-end pipeline over the Kaggle *Grocery Store Sales and
Inventory* dataset (990 rows × 16 columns): messy POS/inventory records
are cleansed, loaded into a star-schema SQLite warehouse, mirrored by
supplier audit logs in MongoDB Atlas, and analyzed with SQL CTEs and
OLAP operations.

## 2. Architecture

```
Grocery_Inventory_and_Sales_Dataset.csv  (messy extract, 990 rows)
            │
            ▼  etl_pipeline.py  ── Extract / Transform ──────────────┐
            │   • strip $ and whitespace from Unit_Price (990 rows)  │
            │   • fix misspelled 'Catagory' header                   │
            │   • impute 1 missing category → 'Uncategorized'        │
            │   • parse mixed-width M/D/YYYY dates → ISO             │
            │   • validate IDs (XX-XXX-XXXX regex), negative values  │
            │   • quarantine unrecoverable rows (0 failed)           │
            │   • row_hash (SHA-256) → idempotent re-runs            │
            ▼                                                        ▼
   warehouse.db (SQLite star schema)                    MongoDB Atlas
   ├─ dim_product   (124)                                supplier_audit_logs
   ├─ dim_supplier  (350)                                (350 docs, 1,839 events)
   ├─ dim_store     (990)
   └─ fact_inventory(990)
        ├─ v_reorder_recommendations  (298 flagged)
        └─ v_stockout_risk            (days_of_cover tiers)
            │
            ▼  monthly_variance.sql + olap_analysis.py
   milestone1_log.txt · olap_output.txt
```

## 3. Data quality issues found and fixed

| Issue | Evidence | Fix |
|---|---|---|
| Currency symbols in price | `Unit_Price = "$4.50 "` on all 990 rows | strip `$`, commas, whitespace → `REAL` |
| Misspelled header | `Catagory` | renamed → `category` |
| Missing category | 1 null | imputed `'Uncategorized'` + `MISSING_CATEGORY` audit event |
| Mixed-width dates | `M/D/YYYY`, `MM/DD/YYYY` variants | parsed → ISO `YYYY-MM-DD` |
| Unvalidated IDs | `XX-XXX-XXXX` format assumed | regex-validated; failures quarantined |
| Negative quantities | rule-based | quarantine rule armed (0 triggered) |

**Result: 990/990 rows cleansed, 0 quarantined.**

## 4. Warehouse design

The source `product_id`/`supplier_id` are record-level (unique per row),
so they are kept on the fact as **degenerate dimensions** while the true
business entities — product (name + category), supplier (name), and
location — become conformed dimensions with surrogate keys:

| Table | Rows | Grain |
|---|---|---|
| `dim_product` | 124 | product name + category |
| `dim_supplier` | 350 | supplier name |
| `dim_store` | 990 | warehouse location |
| `fact_inventory` | 990 | one inventory/sales record |

Measures: `stock_quantity`, `reorder_level`, `reorder_quantity`,
`unit_price`, `sales_volume`, `inventory_turnover_rate`, three dates,
`status`. `row_hash` (UNIQUE) makes re-runs idempotent.

**Outcome views** (this is where the business requirements live):

- **`v_reorder_recommendations`** — every item at/below reorder level
  with `suggested_order_qty` and CRITICAL/HIGH priority → **automated
  replenishment queue** (298 items flagged).
- **`v_stockout_risk`** — `days_of_cover = on-hand × 30 ÷ monthly sales
  velocity`, tiered CRITICAL <7d / HIGH <15d / WATCH <30d / LOW →
  **stockout prevention watchlist**.

## 5. Supplier audit logs (MongoDB)

`supplier_audit_logs` holds one document per supplier entity (350 docs),
keyed `_id = supplier_name` for idempotent upserts, each embedding a
deterministic `audit_events` array:

| Event | Severity | Trigger |
|---|---|---|
| `REORDER_TRIGGERED` | HIGH | stock ≤ reorder level |
| `STOCKOUT_RISK` | CRITICAL | on-hand < half of sales volume |
| `EXPIRED_BEFORE_LAST_ORDER` | MEDIUM | expiry precedes last order (data anomaly) |
| `BACKORDERED` | HIGH | status = Backordered |
| `DISCONTINUED_WITH_STOCK` | LOW | discontinued but stock remains |
| `MISSING_CATEGORY` | LOW | category null in source |

**1,839 events** across 350 documents — MongoDB was chosen because audit
events are variable-shape, append-oriented data that doesn't fit a rigid
relational row.

## 6. OLAP findings (`olap_analysis.py`)

Sales window: **13 months, 2024-02 → 2025-02** · total revenue
**≈ $344,269**.

- **Roll-up:** 2024 calendar-year revenue $294,055 / 48,973 units.
- **Variance (CTE + `LAG()`):** strongest growth +63.9% (2024-03) and
  +56.5% (2024-04); sharpest contraction **−41.3% in 2024-09** —
  a clear seasonal dip worth a demand-planning note.
- **Drill-down / slice:** **Fruits & Vegetables is the #1 category
  ($89,479, 26% of revenue)** — but 38% of its items are
  Discontinued/Backordered, so a third of category revenue is at risk.
- **Dice:** in the Active × (Dairy+Beverages) × H2-2024 sub-cube,
  **Wikido leads** at $2,700.
- **Rank:** top supplier **Youfeed** ($6,613); the top 10 suppliers
  account for $45,479 of supplier-attributed revenue.
- **ABC / Pareto:** tier **A** = Fruits & Vegetables, Beverages, Seafood,
  Dairy — four categories = **78.7%** of revenue; B = Grains & Pulses,
  Oils & Fats; C = Bakery, Uncategorized.
- **Stockout posture:** CRITICAL **27** · HIGH **108** · WATCH **221** ·
  LOW **301**. The 10 most urgent items cover <5 days of sales — e.g.
  Egg (Chicken) at 3.0 days of cover.

## 7. Recommendations

1. **Feed `v_reorder_recommendations` into purchasing daily** — 298
   items are already at/below reorder level; the `suggested_order_qty`
   column is directly actionable.
2. **Put the 27 CRITICAL items on immediate expedite** — under ~5 days
   of cover, any supplier delay becomes a shelf stockout.
3. **Watch perishables hardest:** Fruits & Vegetables is both the
   revenue leader and heavily flagged — prioritize its reorder cycle.
4. **Protect tier-A supply lines** — the four A-tier categories carry
   ~79% of revenue; their supplier SLAs deserve the strictest terms.

## 8. Assumptions and limitations

- The dataset has no true POS transaction timestamp; **`last_order_date`
  is used as the sales month** for all revenue/variance analysis.
- `sales_volume` is treated as monthly velocity for `days_of_cover`.
- `dim_store` is 1:1 with fact rows — locations are unique free-text
  addresses in the source (no store hierarchy exists to conform to).
- 0 quarantined rows reflects this dataset; the quarantine rules are
  armed and produce `quarantined_rows.csv` when violations occur.

## 9. Appendix — execution evidence

| Screenshot | Shows |
|---|---|
| 1 | `python etl_pipeline.py` console run (extract → load → analytics) |
| 2 | `warehouse.db` schema in DBeaver (4 tables + 2 views) |
| 3 | `v_reorder_recommendations` / `v_stockout_risk` query results |
| 4 | MongoDB Compass — `supplier_audit_logs` documents |
| 5 | `python olap_analysis.py` console / `olap_output.txt` |

### Deliverable map

| Required file | In this repo |
|---|---|
| `etl_pipeline.py` | ✅ `etl_pipeline.py` |
| `warehouse.db` | ✅ `warehouse.db` |
| `milestone1_log.txt` | ✅ `milestone1_log.txt` |
| `olap_analysis.py` | ✅ `olap_analysis.py` |
| `olap_output.txt` | ✅ `olap_output.txt` |
| `Group_X_Report.pdf` | ✅ this document → `Group_8_Report.pdf` |
