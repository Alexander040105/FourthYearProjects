import pandas as pd
import numpy as np
import dash
from dash import html, dcc, dash_table
import plotly.express as px
import plotly.graph_objects as go

# ── Reproduce the cleaned data from the notebook ──────────────────────────────

data = {
    "transaction_id": [1001, 1002, 1003, 1004, 1005, 1001, 1006, 1007, 1008, 1005, 1009, 1010],
    "cust_name": [
        "Juan Dela Cruz", "Maria Santos", "", "Pedro Penduko", "Ana Roces",
        "Juan Dela Cruz", "Jose Rizal", "Cardo Dalisay", "", "Ana Roces",
        "Manny Pacquiao", "Catriona Gray",
    ],
    "region": [
        "NCR", "Metro Manila", "ncr", "CALABARZON", "calabarzon",
        "NCR", "Region IV-A", "Metro Manila", "ncr", "calabarzon",
        "CALABARZON", "NCR",
    ],
    "order_date": [
        "2026-07-01", "2026/07/02", "2026-07-02", "2026/07/03", "2026-07-04",
        "2026-07-01", "2026/07/05", "2026-07-05", "2026/07/06", "2026-07-04",
        "2026-07-06", "2026/07/07",
    ],
    "amount_paid": [
        1500.50, 2400.00, 450.00, "", 3100.25, 1500.50, 1200.00, "",
        850.75, 3100.25, 5000.00, 1850.00,
    ],
    "status": [
        "Completed", "Completed", "Cancelled", "Completed", "Completed",
        "Completed", "Returned", "Completed", "Completed", "Completed",
        "Completed", "Cancelled",
    ],
}

data_df = pd.DataFrame(data)

# Clean (same logic as notebook cell 2)
data_df["amount_paid"] = data_df["amount_paid"].replace("", np.nan).astype(float)
data_df["cust_name"] = data_df["cust_name"].replace("", np.nan).astype(str)
data_df["transaction_id"] = data_df["transaction_id"].astype(int)
data_df["order_date"] = pd.to_datetime(data_df["order_date"], format="ISO8601")
data_df[["cust_name", "region", "status"]] = data_df[
    ["cust_name", "region", "status"]
].apply(lambda x: x.str.strip().str.upper())

# ── Derive chart data ─────────────────────────────────────────────────────────

# Amount by region
region_amt = (
    data_df.dropna(subset=["amount_paid"])
    .groupby("region", as_index=False)["amount_paid"]
    .sum()
    .sort_values("amount_paid", ascending=False)
)
fig_region = px.bar(
    region_amt,
    x="region",
    y="amount_paid",
    title="Total Amount Paid by Region",
    labels={"amount_paid": "Amount Paid (₱)", "region": "Region"},
    color="region",
    text_auto=".2f",
)

# Status distribution
status_counts = data_df["status"].value_counts().reset_index()
status_counts.columns = ["status", "count"]
fig_status = px.pie(
    status_counts,
    names="status",
    values="count",
    title="Order Status Distribution",
    hole=0.4,
)

# Transactions over time
daily = (
    data_df.dropna(subset=["amount_paid"])
    .groupby(data_df["order_date"].dt.date, as_index=False)["amount_paid"]
    .sum()
)
daily.columns = ["date", "amount_paid"]
fig_timeline = px.line(
    daily,
    x="date",
    y="amount_paid",
    title="Daily Revenue Trend",
    labels={"amount_paid": "Amount Paid (₱)", "date": "Order Date"},
    markers=True,
)

# Top customers
top_cust = (
    data_df.dropna(subset=["amount_paid"])
    .groupby("cust_name", as_index=False)["amount_paid"]
    .sum()
    .sort_values("amount_paid", ascending=False)
    .head(8)
)
fig_customers = px.bar(
    top_cust,
    x="amount_paid",
    y="cust_name",
    orientation="h",
    title="Top Customers by Amount Paid",
    labels={"amount_paid": "Amount Paid (₱)", "cust_name": "Customer"},
    color="amount_paid",
    color_continuous_scale="Blues",
)
fig_customers.update_yaxes(autorange="reversed")

# Data quality / null counts
null_counts = data_df.isnull().sum().reset_index()
null_counts.columns = ["column", "missing"]
fig_nulls = px.bar(
    null_counts,
    x="column",
    y="missing",
    title="Missing Values per Column",
    labels={"missing": "Missing Count", "column": "Column"},
    color="missing",
    color_continuous_scale="Reds",
    text_auto=True,
)

# Summary stats table from describe()
desc_df = data_df.describe(include="all").reset_index().rename(columns={"index": "stat"})
desc_df = desc_df.fillna("—")

# ── Helper components ────────────────────────────────────────────────────────


def kpi_card(title, value):
    return html.Div(
        style={
            "flex": 1,
            "background": "white",
            "borderRadius": "12px",
            "padding": "20px",
            "textAlign": "center",
        },
        children=[
            html.Div(
                str(value),
                style={"fontSize": "28px", "fontWeight": "bold", "color": "#1a1a2e"},
            ),
            html.Div(
                title,
                style={"fontSize": "13px", "color": "#666", "marginTop": "6px"},
            ),
        ],
    )


def chart_card(_id, figure, flex=1):
    return html.Div(
        id=_id,
        style={
            "flex": flex,
            "background": "white",
            "borderRadius": "12px",
            "padding": "20px",
        },
        children=[dcc.Graph(figure=figure, style={"height": "360px"})],
    )


# ── Dash app ──────────────────────────────────────────────────────────────────

app = dash.Dash(__name__)
app.title = "Sales Data Profiling Dashboard"

app.layout = html.Div(
    style={
        "fontFamily": "Segoe UI, Arial, sans-serif",
        "backgroundColor": "#f5f6fa",
        "minHeight": "100vh",
        "padding": "0",
    },
    children=[
        # Header
        html.Header(
            style={
                "backgroundColor": "#1a1a2e",
                "color": "white",
                "padding": "24px 40px",
                "marginBottom": "24px",
            },
            children=[
                html.H1(
                    "JuanMart Sales — Data Profiling Dashboard",
                    style={"margin": 0, "fontSize": "26px"},
                ),
                html.P(
                    "Exploratory view of raw sales transactions, data quality, and revenue breakdowns.",
                    style={"margin": "6px 0 0", "color": "#a0a0b0"},
                ),
            ],
        ),
        html.Div(
            style={"maxWidth": "1200px", "margin": "0 auto", "padding": "0 24px 48px"},
            children=[
                # KPI cards
                html.Div(
                    style={"display": "flex", "gap": "16px", "marginBottom": "32px"},
                    children=[
                        kpi_card("Total Transactions", len(data_df)),
                        kpi_card(
                            "Total Revenue",
                            f"₱{data_df['amount_paid'].sum():,.2f}",
                        ),
                        kpi_card(
                            "Avg Order Value",
                            f"₱{data_df['amount_paid'].mean():,.2f}",
                        ),
                        kpi_card(
                            "Missing Values",
                            int(data_df.isnull().sum().sum()),
                        ),
                    ],
                ),
                # Charts row 1
                html.Div(
                    style={"display": "flex", "gap": "24px", "marginBottom": "24px"},
                    children=[
                        chart_card("region", fig_region, flex=1),
                        chart_card("status", fig_status, flex=1),
                    ],
                ),
                # Charts row 2
                html.Div(
                    style={"display": "flex", "gap": "24px", "marginBottom": "24px"},
                    children=[
                        chart_card("timeline", fig_timeline, flex=1),
                        chart_card("customers", fig_customers, flex=1),
                    ],
                ),
                # Null chart + describe table
                html.Div(
                    style={"display": "flex", "gap": "24px", "marginBottom": "24px"},
                    children=[
                        chart_card("nulls", fig_nulls, flex=1),
                        html.Div(
                            style={"flex": 1, "background": "white", "borderRadius": "12px", "padding": "20px"},
                            children=[
                                html.H3("Summary Statistics", style={"marginTop": 0}),
                                dash_table.DataTable(
                                    data=desc_df.to_dict("records"),
                                    columns=[{"name": c, "id": c} for c in desc_df.columns],
                                    style_table={"overflowX": "auto"},
                                    style_cell={
                                        "textAlign": "center",
                                        "padding": "8px",
                                        "fontSize": "13px",
                                    },
                                    style_header={
                                        "backgroundColor": "#1a1a2e",
                                        "color": "white",
                                        "fontWeight": "bold",
                                    },
                                ),
                            ],
                        ),
                    ],
                ),
                # Raw data table
                html.Div(
                    style={"background": "white", "borderRadius": "12px", "padding": "20px"},
                    children=[
                        html.H3("Cleaned Transaction Data", style={"marginTop": 0}),
                        dash_table.DataTable(
                            data=data_df.assign(
                                order_date=data_df["order_date"].dt.strftime("%Y-%m-%d")
                            ).to_dict("records"),
                            columns=[
                                {"name": c, "id": c} for c in data_df.columns
                            ],
                            style_table={"overflowX": "auto"},
                            style_cell={
                                "textAlign": "center",
                                "padding": "8px",
                                "fontSize": "13px",
                            },
                            style_header={
                                "backgroundColor": "#1a1a2e",
                                "color": "white",
                                "fontWeight": "bold",
                            },
                            page_size=15,
                        ),
                    ],
                ),
            ],
        ),
    ],
)


if __name__ == "__main__":
    app.run(debug=True, port=8050)
