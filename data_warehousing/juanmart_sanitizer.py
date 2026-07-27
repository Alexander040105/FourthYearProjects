"""
JuanMart Data Cleansing Pipeline (Lab 1.2)
============================================
Also known as: 1.2_data_cleansing.py

This script reads the raw juanmart_raw_sales.csv, applies a series of
cleansing transformations, and writes:
  - cleaned_juanmart_sales.parquet  (cleaned dataset)
  - quarantined_transactions.csv    (rows that failed validation)

Run:  python juanmart_sanitizer.py
"""

import pandas as pd
import numpy as np
import re
from pathlib import Path

# ────────────────────────────────────────────────────────────
# Configuration
# ────────────────────────────────────────────────────────────
RAW_CSV = Path(__file__).parent / "juanmart_raw_sales.csv"
CLEANED_PARQUET = Path(__file__).parent / "cleaned_juanmart_sales.parquet"
QUARANTINE_CSV = Path(__file__).parent / "quarantined_transactions.csv"

REGION_MAP = {
    "ncr": "National Capital Region",
    "NCR": "National Capital Region",
    "Metro Manila": "National Capital Region",
    "Manila": "National Capital Region",
    "CALABARZON": "CALABARZON",
    "calabarzon": "CALABARZON",
    "Region IV-A": "CALABARZON",
    "region iv-a": "CALABARZON",
    "REGION IV-A": "CALABARZON",
}

REQUIRED_FIELDS = ["cust_name"]


# ────────────────────────────────────────────────────────────
# Cleansing Functions
# ────────────────────────────────────────────────────────────

def standardize_region(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize the 'region' column using a mapping dict.
    Collapses all variants of NCR -> 'National Capital Region'
    and all variants of CALABARZON -> 'CALABARZON'.
    Uses case-insensitive lookup so that any casing variant is mapped.
    """
    df = df.copy()

    ci_map = {}
    for k, v in REGION_MAP.items():
        ci_map[k.lower()] = v

    def _map_region(val):
        if pd.isna(val):
            return val
        key = str(val).strip().lower()
        return ci_map.get(key, str(val).strip())

    df["region"] = df["region"].apply(_map_region)
    return df


def standardize_dates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert mixed date formats (YYYY-MM-DD and YYYY/MM/DD)
    into a uniform YYYY-MM-DD string, then parse to datetime.
    """
    df = df.copy()

    def _normalize_date(val):
        if pd.isna(val):
            return val
        s = str(val).strip()
        if re.match(r"^\d{4}/\d{2}/\d{2}$", s):
            s = s.replace("/", "-")
        return s

    df["order_date"] = df["order_date"].apply(_normalize_date)
    df["order_date"] = pd.to_datetime(df["order_date"], format="%Y-%m-%d", errors="coerce")
    return df


def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove exact duplicate rows based on transaction_id.
    Keeps the first occurrence, drops subsequent duplicates.
    The count is derived programmatically.
    """
    before = len(df)
    df = df.drop_duplicates(subset=["transaction_id"], keep="first")
    after = len(df)
    removed = before - after
    print(f"  [drop_duplicates] Removed {removed} duplicate row(s) ({before} -> {after})")
    return df


def fill_missing_amounts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fill missing 'amount_paid' with the median amount for that row's
    region (computed AFTER region standardization).
    Falls back to global median if a region has no non-null amounts.
    """
    df = df.copy()
    df["amount_paid"] = pd.to_numeric(df["amount_paid"], errors="coerce")

    region_medians = df.groupby("region")["amount_paid"].median()
    global_median = df["amount_paid"].median()

    def _fill(row):
        if pd.isna(row["amount_paid"]):
            regional = region_medians.get(row["region"], global_median)
            if pd.isna(regional):
                regional = global_median
            return round(float(regional), 2)
        return row["amount_paid"]

    missing_before = int(df["amount_paid"].isna().sum())
    df["amount_paid"] = df.apply(_fill, axis=1)
    missing_after = int(df["amount_paid"].isna().sum())
    print(f"  [fill_missing_amounts] Filled {missing_before - missing_after} missing amount(s) with regional median")
    return df


def quarantine_bad_rows(df: pd.DataFrame) -> tuple:
    """
    Split out rows still missing a required field (e.g. cust_name)
    after cleaning into a separate quarantine DataFrame.
    Returns: (clean_df, quarantine_df)
    """
    df = df.copy()

    bad_mask = pd.Series(False, index=df.index)
    reasons = pd.Series("", index=df.index)

    for field in REQUIRED_FIELDS:
        field_mask = df[field].isna() | (df[field].astype(str).str.strip() == "")
        bad_mask |= field_mask
        reasons.loc[field_mask & (reasons == "")] = f"missing {field}"
        reasons.loc[field_mask & (reasons != "")] = reasons + f", missing {field}"

    quarantine = df[bad_mask].copy()
    quarantine["quarantine_reason"] = reasons[bad_mask]

    clean = df[~bad_mask].copy()

    print(f"  [quarantine_bad_rows] Quarantined {len(quarantine)} row(s), {len(clean)} row(s) remain clean")
    return clean, quarantine


# ────────────────────────────────────────────────────────────
# Pipeline
# ────────────────────────────────────────────────────────────

def load_raw(path: Path = RAW_CSV) -> pd.DataFrame:
    """Load the raw CSV into a DataFrame."""
    df = pd.read_csv(path)
    print(f"Loaded {len(df)} rows from {path.name}")
    return df


def run_pipeline(df: pd.DataFrame) -> tuple:
    """
    Execute the full cleansing pipeline in order:
      1. Standardize region naming
      2. Standardize date formats
      3. Drop duplicates
      4. Fill missing amounts (using standardized region medians)
      5. Quarantine rows with missing required fields
    """
    print("\n=== Running Cleansing Pipeline ===")

    print("Step 1: Standardize regions")
    df = standardize_region(df)

    print("Step 2: Standardize dates")
    df = standardize_dates(df)

    print("Step 3: Drop duplicates")
    df = drop_duplicates(df)

    print("Step 4: Fill missing amounts with regional median")
    df = fill_missing_amounts(df)

    print("Step 5: Quarantine rows with missing required fields")
    clean_df, quarantine_df = quarantine_bad_rows(df)

    print(f"\nPipeline complete: {len(clean_df)} clean rows, {len(quarantine_df)} quarantined rows")
    return clean_df, quarantine_df


def main():
    """Main entry point — runs the full pipeline and writes outputs."""
    df = load_raw()
    clean_df, quarantine_df = run_pipeline(df)

    # Write cleaned data to Parquet
    clean_df.to_parquet(CLEANED_PARQUET, index=False)
    print(f"\nWrote cleaned data to {CLEANED_PARQUET.name}")

    # Write quarantined rows to CSV
    if len(quarantine_df) > 0:
        quarantine_df.to_csv(QUARANTINE_CSV, index=False)
        print(f"Wrote {len(quarantine_df)} quarantined rows to {QUARANTINE_CSV.name}")
    else:
        print("No quarantined rows to write.")

    # Print final cleaned table preview
    print("\n=== Cleaned Data Preview ===")
    print(clean_df.to_string(index=False))

    print("\n=== Quarantined Data Preview ===")
    if len(quarantine_df) > 0:
        print(quarantine_df.to_string(index=False))
    else:
        print("(none)")


if __name__ == "__main__":
    main()
