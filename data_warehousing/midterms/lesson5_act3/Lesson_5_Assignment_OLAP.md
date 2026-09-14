# Data Warehousing – Lesson 5: OLAP Operations & Advanced Analytical Querying

**Prepared by:** Prof. Rob Malitao
**Date:** September 8, 2026
**Due Date:** September 15, 2026

> **Note:** You may refer to your database schema, field names, and table structures from the Lesson 4 Laboratory Activity (e.g., `fact_sales` and `sales_documents`) when formulating your SQL queries and MongoDB aggregation pipelines for Parts 2 and 3.

## Assignment Objective

This assignment evaluates students' theoretical comprehension and practical design capabilities regarding:
- Multidimensional OLAP cube operations
- Advanced relational window functions (SQLite focus)
- Document-oriented aggregation pipelines (MongoDB focus)

---

## Part 1: Multi-Dimensional OLAP Operations Case Analysis

RetailPulse Inc. maintains a data warehouse cube measuring total sales volume across four dimensions:

- **Time** (Year, Quarter, Month, Day)
- **Geography** (Region, Store, City)
- **Product** (Category, Sub-category, SKU)
- **Customer Segment** (Retail, Corporate, Wholesale)

For each of the following business intelligence requests, identify which core OLAP operation (**Roll-up**, **Drill-down**, **Slice**, **Dice**, or **Pivot**) is being described, and briefly justify your answer:

1. **Request A:** Management requests a report displaying total sales exclusively for the North region, filtering out all other regions for the entire fiscal year of 2025.
2. **Request B:** An executive looks at annual regional sales totals, then clicks on the North region to view monthly breakdowns for each individual store within that territory.
3. **Request C:** The marketing team needs to view a sub-cube containing only Electronics and Apparel categories sold to Corporate customers across the East and West regions during Q1.
4. **Request D:** A financial analyst summarizes daily transaction line items into monthly district aggregates to speed up executive review meetings.
5. **Request E:** A dashboard view reorganizes a report by swapping the row headers (Store Locations) and column headers (Product Categories) to analyze product performance across branches from a new directional perspective.

---

## Part 2: Advanced Relational SQL Query Formulation (SQLite)

Using your knowledge of Common Table Expressions (CTEs) and Window Functions, answer the following query design problems based on a standard relational table `fact_sales` with columns:

`transaction_id`, `store_id`, `product_id`, `quantity`, `unit_price`, `invoice_date`

1. Write a modular SQLite query utilizing a CTE named `MonthlyStoreRevenue` that calculates total revenue per store per month.
2. Extend your query using a Window Function (`LAG()`) to compute the month-over-month (MoM) revenue variance for each store location, ensuring row granularity is preserved.
3. Explain why using a window function with `PARTITION BY store_id` is computationally and structurally superior to writing a self-join across two separate monthly aggregate tables.

---

## Part 3: MongoDB Aggregation Pipeline Design

A retail document collection `sales_documents` contains semi-structured sales records with fields:

`transaction_id`, `customer_id`, `product_category`, `quantity`, `unit_price`, `status`

Write a JSON array representing a MongoDB aggregation pipeline (`db.sales_documents.aggregate([...])`) that accomplishes the following business logic sequentially:

1. Filters records where `status` equals `"completed"`.
2. Groups the filtered documents by `product_category`, calculating the total units sold (`$sum`) and total revenue (`$sum` of product multiplied by price).
3. Sorts the resulting categories in descending order of total revenue.
4. Limits the output to the top 3 highest-earning product categories.

---

## Assignment Evaluation Rubric

| Criteria | Excellent (4) | Proficient (2-3) | Developing (1) |
|---|---|---|---|
| **OLAP Cube Operations Accuracy** | Correctly identifies and justifies all five multidimensional OLAP operations with precise business context. | Identifies most operations with minor confusion between slice/dice or roll-up/drill-down. | Fails to correctly map business scenarios to OLAP operations. |
| **Advanced SQL & CTE Logic** | Formulates syntactically sound SQLite queries using proper CTE structuring, partitioning, and offset functions. | Writes functional queries with minor syntax errors or suboptimal window frame definitions. | Relies on invalid query syntax or fails to implement window functions/CTEs. |
| **MongoDB Aggregation Pipeline Design** | Accurately constructs pipeline stage objects (`$match`, `$group`, `$sort`, `$limit`) using correct MongoDB operator syntax. | Constructs a working pipeline with minor operator placement or syntax omissions. | Pipeline fails logical validation or uses incorrect MongoDB stage syntax. |
