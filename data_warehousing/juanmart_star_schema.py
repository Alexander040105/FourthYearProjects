"""
JuanMart Star Schema Diagram Generator (Lab 1.3)
=================================================
Generates a PNG diagram of the JuanMart star schema using matplotlib.

Star schema layout:
  - Center: fact_sales (fact table)
  - Surrounding: dim_customer (SCD2), dim_calendar, dim_region, dim_status

Run:  python juanmart_star_schema.py
Output: juanmart_star_schema.png
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

OUTPUT_PNG = Path(__file__).parent / "juanmart_star_schema.png"


def draw_table(ax, x, y, title, columns, width=3.0, header_height=0.4, row_height=0.28, color="#1a1a2e"):
    """Draw a database table box on the matplotlib axes."""
    total_height = header_height + len(columns) * row_height

    # Table body
    body = mpatches.FancyBboxPatch(
        (x, y - total_height), width, total_height,
        boxstyle="round,pad=0.05",
        facecolor="white", edgecolor=color, linewidth=2
    )
    ax.add_patch(body)

    # Header bar
    header = mpatches.FancyBboxPatch(
        (x, y - header_height), width, header_height,
        boxstyle="round,pad=0.05",
        facecolor=color, edgecolor=color, linewidth=2
    )
    ax.add_patch(header)

    # Title text
    ax.text(x + width / 2, y - header_height / 2, title,
            ha="center", va="center", fontsize=11, fontweight="bold", color="white")

    # Column rows
    for i, (col, is_key) in enumerate(columns):
        row_y = y - header_height - (i + 0.5) * row_height
        prefix = "PK " if is_key == "PK" else "FK " if is_key == "FK" else "    "
        weight = "bold" if is_key in ("PK", "FK") else "normal"
        color_text = "#c0392b" if is_key == "PK" else "#2980b9" if is_key == "FK" else "#333"
        ax.text(x + 0.1, row_y, f"{prefix}{col}", ha="left", va="center",
                fontsize=8, fontweight=weight, color=color_text, family="monospace")

    return (x, y, width, total_height)


def draw_connection(ax, fact_center, dim_edge, color="#7f8c8d"):
    """Draw a line connecting the fact table to a dimension table."""
    ax.annotate("", xy=dim_edge, xytext=fact_center,
                arrowprops=dict(arrowstyle="-", color=color, lw=1.5))


def main():
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(-1, 17)
    ax.set_ylim(-1, 13)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_facecolor("#f5f6fa")
    fig.patch.set_facecolor("#f5f6fa")

    # Title
    ax.text(8, 12.5, "JuanMart Star Schema", ha="center", va="center",
            fontsize=18, fontweight="bold", color="#1a1a2e")
    ax.text(8, 12.0, "Data Warehouse Dimensional Model", ha="center", va="center",
            fontsize=11, color="#666")

    # ── Fact table (center) ──
    fact_cols = [
        ("transaction_id", "PK"),
        ("customer_key", "FK"),
        ("date_key", "FK"),
        ("region_key", "FK"),
        ("status_key", "FK"),
        ("amount_paid", ""),
    ]
    draw_table(ax, x=6.5, y=8.5, title="fact_sales", columns=fact_cols,
               width=3.5, color="#2c3e50")

    fact_center = (8.25, 7.0)

    # ── dim_customer (top-left, SCD2) ──
    cust_cols = [
        ("customer_key", "PK"),
        ("customer_natural_key", ""),
        ("cust_name", ""),
        ("region_name", ""),
        ("effective_date", ""),
        ("end_date", ""),
        ("is_current", ""),
    ]
    draw_table(ax, x=0.5, y=11.5, title="dim_customer (SCD2)", columns=cust_cols,
               width=3.8, color="#8e44ad")

    # ── dim_calendar (top-right) ──
    cal_cols = [
        ("date_key", "PK"),
        ("full_date", ""),
        ("year", ""),
        ("quarter", ""),
        ("month", ""),
        ("month_name", ""),
        ("day_of_week", ""),
        ("is_weekend", ""),
    ]
    draw_table(ax, x=12.5, y=11.5, title="dim_calendar", columns=cal_cols,
               width=3.5, color="#27ae60")

    # ── dim_region (bottom-left) ──
    region_cols = [
        ("region_key", "PK"),
        ("region_name", ""),
        ("region_code", ""),
        ("parent_region", ""),
    ]
    draw_table(ax, x=0.5, y=4.5, title="dim_region", columns=region_cols,
               width=3.5, color="#e67e22")

    # ── dim_status (bottom-right) ──
    status_cols = [
        ("status_key", "PK"),
        ("status_name", ""),
        ("is_revenue_recognized", ""),
    ]
    draw_table(ax, x=12.5, y=4.0, title="dim_status", columns=status_cols,
               width=3.5, color="#c0392b")

    # ── Draw connection lines ──
    # fact_sales -> dim_customer
    draw_connection(ax, (6.5, 7.5), (4.3, 9.5))
    # fact_sales -> dim_calendar
    draw_connection(ax, (10.0, 7.5), (12.5, 9.5))
    # fact_sales -> dim_region
    draw_connection(ax, (6.5, 6.5), (4.0, 3.5))
    # fact_sales -> dim_status
    draw_connection(ax, (10.0, 6.5), (12.5, 3.5))

    # ── Legend ──
    legend_y = 0.5
    ax.text(1, legend_y, "PK", fontsize=9, fontweight="bold", color="#c0392b", family="monospace")
    ax.text(1.5, legend_y, "= Primary Key", fontsize=9, color="#333")
    ax.text(4, legend_y, "FK", fontsize=9, fontweight="bold", color="#2980b9", family="monospace")
    ax.text(4.5, legend_y, "= Foreign Key", fontsize=9, color="#333")
    ax.text(8, legend_y, "SCD2 = Slowly Changing Dimension Type 2", fontsize=9, color="#666", fontstyle="italic")

    plt.tight_layout()
    plt.savefig(OUTPUT_PNG, dpi=150, bbox_inches="tight", facecolor="#f5f6fa")
    print(f"Star schema diagram saved to: {OUTPUT_PNG}")
    plt.show()


if __name__ == "__main__":
    main()
