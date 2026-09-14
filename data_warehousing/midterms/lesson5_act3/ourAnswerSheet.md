Part 1:

1. Slice — filtering the cube to a single region (North) for the fiscal year 2025.

2. Drill-down — moving from annual regional totals into monthly store-level detail within the North region.

3. Dice — selecting a multi-dimensional sub-cube across product (Electronics, Apparel), customer segment (Corporate), region (East, West), and time (Q1).

4. Roll-up — aggregating daily line-item data up to monthly district totals.

5. Pivot — rotating the report axes by swapping Store Locations (rows) with Product Categories (columns).

Part 2:

1.
WITH MonthlyStoreRevenue AS (
    SELECT
        store_id,
        strftime('%Y-%m', invoice_date) AS month_key,
        SUM(quantity * unit_price) AS total_revenue
    FROM fact_sales
    GROUP BY store_id, strftime('%Y-%m', invoice_date)
)
SELECT * FROM MonthlyStoreRevenue;

2.
WITH MonthlyStoreRevenue AS (
    SELECT
        store_id,
        strftime('%Y-%m', invoice_date) AS month_key,
        SUM(quantity * unit_price) AS total_revenue
    FROM fact_sales
    GROUP BY store_id, strftime('%Y-%m', invoice_date)
)
SELECT
    store_id,
    month_key,
    total_revenue,
    LAG(total_revenue, 1) OVER (
        PARTITION BY store_id
        ORDER BY month_key
    ) AS prev_month_revenue,
    total_revenue - LAG(total_revenue, 1) OVER (
        PARTITION BY store_id
        ORDER BY month_key
    ) AS mom_variance
FROM MonthlyStoreRevenue;

3. Using a window function with PARTITION BY is preferred over a self-join because it computes the result in a single pass over the sorted data, without creating duplicate aggregate tables or matching conditions. Self-joins require two monthly aggregate tables to be joined on store_id and a shifted month, which is more complex, slower, and can fail when months are missing or stores have different date ranges. Window functions also keep row-level context within each partition and are generally more efficient because they avoid join overhead.

Part 3:

```javascript
db.sales_documents.aggregate([
    {
        "$match": {
            "status": "completed"
        }
    },
    {
        "$group": {
            "_id": "$product_category",
            "total_units_sold": {
                "$sum": "$quantity"
            },
            "total_revenue": {
                "$sum": {
                    "$multiply": ["$quantity", "$unit_price"]
                }
            }
        }
    },
    {
        "$sort": {
            "total_revenue": -1
        }
    },
    {
        "$limit": 3
    }
]);
```
