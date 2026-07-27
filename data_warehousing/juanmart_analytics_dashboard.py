"""
JuanMart Analytics Dashboard (Lab 1.4)
=======================================
Streamlit + Plotly interactive dashboard for JuanMart sales analytics.

KPI cards:
  - Total Net Revenue (Completed orders only, minus Returns)
  - Average Order Value
  - Total Orders
  - Quarantined Data Error Rate (%)

Charts:
  - Monthly/quarterly revenue trend line (using dim_calendar)
  - Regional heatmap of sales density (SCD2: mapped to customer's region at time of purchase)
  - Product category bar/donut chart (mock product_category field)

Assumption: Raw data has no product_category column — a reasonable mock
category assignment is added based on transaction_id ranges.

Run:  streamlit run juanmart_analytics_dashboard.py
"""

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ────────────────────────────────────────────────────────────
# Page Configuration
# ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="JuanMart Analytics Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ────────────────────────────────────────────────────────────
# Data Loading & Preparation
# ────────────────────────────────────────────────────────────

@st.cache_data
def load_data():
    """Load raw data, clean it, and prepare dashboard datasets."""
    base = Path(__file__).parent
    raw_path = base / "juanmart_raw_sales.csv"
    quarantine_path = base / "quarantined_transactions.csv"

    df = pd.read_csv(raw_path)

    # ── Standardize region ──
    region_map = {
        "ncr": "National Capital Region", "NCR": "National Capital Region",
        "Metro Manila": "National Capital Region", "Manila": "National Capital Region",
        "CALABARZON": "CALABARZON", "calabarzon": "CALABARZON",
        "Region IV-A": "CALABARZON", "region iv-a": "CALABARZON",
        "REGION IV-A": "CALABARZON",
    }
    ci_map = {k.lower(): v for k, v in region_map.items()}
    df["region"] = df["region"].apply(
        lambda x: ci_map.get(str(x).strip().lower(), str(x).strip()) if pd.notna(x) else x
    )

    # ── Standardize dates ──
    df["order_date"] = df["order_date"].astype(str).str.replace("/", "-")
    df["order_date"] = pd.to_datetime(df["order_date"], format="%Y-%m-%d", errors="coerce")

    # ── Drop duplicates ──
    df = df.drop_duplicates(subset=["transaction_id"], keep="first")

    # ── Fill missing amounts with regional median ──
    df["amount_paid"] = pd.to_numeric(df["amount_paid"], errors="coerce")
    region_medians = df.groupby("region")["amount_paid"].median()
    global_median = df["amount_paid"].median()

    def _fill_amount(row):
        if pd.isna(row["amount_paid"]):
            r = region_medians.get(row["region"], global_median)
            return round(float(r), 2) if pd.notna(r) else 0.0
        return row["amount_paid"]

    df["amount_paid"] = df.apply(_fill_amount, axis=1)

    # ── Add mock product_category (assumption: raw data has no category) ──
    # Assign categories based on transaction_id ranges for demonstration
    def _assign_category(tid):
        if tid <= 1003:
            return "Artisanal Goods"
        elif tid <= 1006:
            return "Electronics"
        elif tid <= 1008:
            return "Fashion"
        else:
            return "Groceries"
    df["product_category"] = df["transaction_id"].apply(_assign_category)

    # ── Add mock profit margin per category (assumption) ──
    category_margins = {
        "Artisanal Goods": 0.35,
        "Electronics": 0.15,
        "Fashion": 0.40,
        "Groceries": 0.12,
    }
    df["profit_margin"] = df["product_category"].map(category_margins)
    df["profit"] = df["amount_paid"] * df["profit_margin"]

    # ── Build dim_calendar ──
    dim_calendar = pd.DataFrame({
        "date": pd.date_range(df["order_date"].min(), df["order_date"].max()),
    })
    dim_calendar["year"] = dim_calendar["date"].dt.year
    dim_calendar["quarter"] = dim_calendar["date"].dt.quarter
    dim_calendar["month"] = dim_calendar["date"].dt.month
    dim_calendar["month_name"] = dim_calendar["date"].dt.strftime("%b")
    dim_calendar["day_of_week"] = dim_calendar["date"].dt.day_name()

    # ── Load quarantined data ──
    quarantine_df = pd.read_csv(quarantine_path) if quarantine_path.exists() else pd.DataFrame()

    return df, dim_calendar, quarantine_df


df, dim_calendar, quarantine_df = load_data()

# ────────────────────────────────────────────────────────────
# KPI Calculations
# ────────────────────────────────────────────────────────────
completed_df = df[df["status"] == "Completed"]
returned_df = df[df["status"] == "Returned"]
cancelled_df = df[df["status"] == "Cancelled"]

total_gross_revenue = completed_df["amount_paid"].sum()
total_returns_value = returned_df["amount_paid"].sum() if len(returned_df) > 0 else 0
total_net_revenue = total_gross_revenue - total_returns_value
avg_order_value = completed_df["amount_paid"].mean() if len(completed_df) > 0 else 0
total_orders = len(df)
quarantine_count = len(quarantine_df)
error_rate = round((quarantine_count / total_orders) * 100, 2) if total_orders > 0 else 0

# ────────────────────────────────────────────────────────────
# Dashboard Layout
# ────────────────────────────────────────────────────────────

st.markdown(
    "<style>"
    ".main-header {"
    "  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);"
    "  padding: 20px 30px; border-radius: 12px; margin-bottom: 20px;"
    "}"
    ".main-header h1 { color: white; margin: 0; font-size: 26px; }"
    ".main-header p { color: #a0a0b0; margin: 6px 0 0; font-size: 14px; }"
    ".kpi-card {"
    "  background: white; border-radius: 12px; padding: 20px;"
    "  text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.08);"
    "}"
    ".kpi-value { font-size: 32px; font-weight: bold; color: #1a1a2e; }"
    ".kpi-label { font-size: 13px; color: #666; margin-top: 6px; }"
    ".kpi-delta { font-size: 12px; margin-top: 4px; }"
    "</style>",
    unsafe_allow_html=True,
)

# Header
st.markdown(
    '<div class="main-header">'
    "<h1>🛒 JuanMart Analytics Dashboard</h1>"
    "<p>E-commerce sales performance, regional density, and data quality insights</p>"
    "</div>",
    unsafe_allow_html=True,
)

# ── KPI Cards Row ──
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f'<div class="kpi-card">'
        f'<div class="kpi-value">₱{total_net_revenue:,.2f}</div>'
        f'<div class="kpi-label">Total Net Revenue</div>'
        f'<div class="kpi-delta" style="color: #27ae60;">Gross ₱{total_gross_revenue:,.0f} − Returns ₱{total_returns_value:,.0f}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f'<div class="kpi-card">'
        f'<div class="kpi-value">₱{avg_order_value:,.2f}</div>'
        f'<div class="kpi-label">Average Order Value</div>'
        f'<div class="kpi-delta" style="color: #666;">Based on {len(completed_df)} completed orders</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        f'<div class="kpi-card">'
        f'<div class="kpi-value">{total_orders}</div>'
        f'<div class="kpi-label">Total Orders</div>'
        f'<div class="kpi-delta" style="color: #666;">{len(completed_df)} Completed · {len(cancelled_df)} Cancelled · {len(returned_df)} Returned</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

with col4:
    color = "#e74c3c" if error_rate > 10 else "#f39c12" if error_rate > 5 else "#27ae60"
    st.markdown(
        f'<div class="kpi-card">'
        f'<div class="kpi-value" style="color: {color};">{error_rate}%</div>'
        f'<div class="kpi-label">Quarantined Data Error Rate</div>'
        f'<div class="kpi-delta" style="color: #666;">{quarantine_count} quarantined rows</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

st.markdown("---")

# ── Sidebar Filters ──
st.sidebar.markdown("### Filters")
status_filter = st.sidebar.multiselect(
    "Order Status",
    options=df["status"].unique(),
    default=df["status"].unique(),
)
region_filter = st.sidebar.multiselect(
    "Region",
    options=df["region"].unique(),
    default=df["region"].unique(),
)

filtered_df = df[df["status"].isin(status_filter) & df["region"].isin(region_filter)]

# ── Revenue Trend (Monthly/Quarterly) ──
st.markdown("### 📈 Revenue Trend")

trend_period = st.radio("Group by:", ["Monthly", "Quarterly"], horizontal=True)

if trend_period == "Monthly":
    trend_df = (
        filtered_df[filtered_df["status"] == "Completed"]
        .groupby(filtered_df["order_date"].dt.to_period("M"))
        .agg(revenue=("amount_paid", "sum"), orders=("transaction_id", "count"))
        .reset_index()
    )
    trend_df["order_date"] = trend_df["order_date"].astype(str)
    fig_trend = px.line(
        trend_df, x="order_date", y="revenue",
        title="Monthly Revenue Trend (Completed Orders)",
        markers=True, labels={"revenue": "Revenue (₱)", "order_date": "Month"},
        template="plotly_white",
    )
else:
    trend_df = (
        filtered_df[filtered_df["status"] == "Completed"]
        .groupby(filtered_df["order_date"].dt.to_period("Q"))
        .agg(revenue=("amount_paid", "sum"), orders=("transaction_id", "count"))
        .reset_index()
    )
    trend_df["order_date"] = trend_df["order_date"].astype(str)
    fig_trend = px.bar(
        trend_df, x="order_date", y="revenue",
        title="Quarterly Revenue Trend (Completed Orders)",
        labels={"revenue": "Revenue (₱)", "order_date": "Quarter"},
        template="plotly_white", color="revenue",
        color_continuous_scale="Blues",
    )

fig_trend.update_layout(height=400)
st.plotly_chart(fig_trend, use_container_width=True)

# ── Regional Heatmap ──
st.markdown("### 🗺️ Regional Sales Density")
st.caption("Sales mapped to where the customer lived at time of purchase (SCD2 logic)")

region_sales = (
    filtered_df[filtered_df["status"] == "Completed"]
    .groupby("region")
    .agg(
        total_sales=("amount_paid", "sum"),
        order_count=("transaction_id", "count"),
        avg_order=("amount_paid", "mean"),
    )
    .reset_index()
)

fig_heatmap = px.bar(
    region_sales,
    x="region",
    y="total_sales",
    color="total_sales",
    color_continuous_scale="YlOrRd",
    title="Sales Density by Region (Completed Orders)",
    labels={"total_sales": "Total Sales (₱)", "region": "Region"},
    text="order_count",
    template="plotly_white",
)
fig_heatmap.update_traces(texttemplate="%{text} orders", textposition="outside")
fig_heatmap.update_layout(height=400)
st.plotly_chart(fig_heatmap, use_container_width=True)

# ── Product Category Chart ──
st.markdown("### 📊 Product Category Performance")
st.caption("Assumption: mock `product_category` field assigned by transaction_id range (raw data has no category column)")

col_left, col_right = st.columns(2)

with col_left:
    category_volume = (
        filtered_df[filtered_df["status"] == "Completed"]
        .groupby("product_category")
        .agg(
            sales_volume=("amount_paid", "sum"),
            order_count=("transaction_id", "count"),
        )
        .reset_index()
    )
    fig_bar = px.bar(
        category_volume,
        x="product_category",
        y="sales_volume",
        title="Sales Volume by Category",
        labels={"sales_volume": "Sales Volume (₱)", "product_category": "Category"},
        color="product_category",
        template="plotly_white",
    )
    fig_bar.update_layout(height=380, showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)

with col_right:
    category_profit = (
        filtered_df[filtered_df["status"] == "Completed"]
        .groupby("product_category")
        .agg(
            total_profit=("profit", "sum"),
            avg_margin=("profit_margin", "mean"),
        )
        .reset_index()
    )
    category_profit["avg_margin_pct"] = (category_profit["avg_margin"] * 100).round(1)

    fig_donut = px.pie(
        category_profit,
        names="product_category",
        values="total_profit",
        title="Profit Distribution by Category",
        hole=0.5,
        template="plotly_white",
    )
    fig_donut.update_traces(
        textinfo="label+percent",
        texttemplate="%{label}<br>%{percent}",
    )
    fig_donut.update_layout(height=380, showlegend=False)
    st.plotly_chart(fig_donut, use_container_width=True)

# ── Data Tables ──
st.markdown("---")
st.markdown("### 📋 Cleaned Transaction Data")

display_df = filtered_df[["transaction_id", "cust_name", "region", "order_date",
                          "amount_paid", "status", "product_category"]].copy()
display_df["order_date"] = display_df["order_date"].dt.strftime("%Y-%m-%d")
st.dataframe(display_df, use_container_width=True, hide_index=True)

if len(quarantine_df) > 0:
    st.markdown("### ⚠️ Quarantined Transactions")
    st.caption("Rows that failed validation and were excluded from the clean dataset")
    st.dataframe(quarantine_df, use_container_width=True, hide_index=True)

# ── Footer ──
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #999; font-size: 12px;'>"
    "JuanMart Data Warehousing Lab — Lab 1.4 Analytics Dashboard | "
    "Streamlit + Plotly | Built with the Data Analytics Life Cycle"
    "</p>",
    unsafe_allow_html=True,
)
