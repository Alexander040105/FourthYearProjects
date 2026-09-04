#!/usr/bin/env python3
"""
multi_target_etl.py
RetailPulse Inc. - Incremental Multi-Target ETL Pipeline

Extracts raw CSV transaction data and semi-structured JSON feedback logs from a
local landing zone, cleans and reshapes them, then loads the structured stream
into a SQLite warehouse (fact_sales, dim_store) and the flexible stream into a
MongoDB Atlas collection (sales_documents, feedback_logs).

The pipeline is incremental by default:
- File-level watermarking skips files that have already been fully loaded.
- Changed or partially-processed files are rescanned.
- Target-side duplicate detection (row_hash UNIQUE, _id=row_hash, log_id)
  ensures re-runs are idempotent.
- A --full-refresh flag rebuilds everything from scratch.
"""

import argparse
import hashlib
import json
import logging
import os
import sqlite3
import sys
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import numpy as np
import pandas as pd

try:
    from pymongo import MongoClient
    from pymongo.errors import BulkWriteError, PyMongoError

    PYMONGO_AVAILABLE = True
except ImportError:  # pragma: no cover
    MongoClient = BulkWriteError = PyMongoError = None
    PYMONGO_AVAILABLE = False


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
LANDING_ZONE = SCRIPT_DIR / "landing_zone"
CSV_PATH = LANDING_ZONE / "warehouse_messy_data.csv"
JSON_PATH = LANDING_ZONE / "feedback_logs.json"
DB_PATH = SCRIPT_DIR / "retail_warehouse.db"
ENV_PATH = SCRIPT_DIR / ".env"
SUMMARY_PATH = SCRIPT_DIR / "pipeline_summary.txt"


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stdout)
logger = logging.getLogger("multi_target_etl")


# ---------------------------------------------------------------------------
# Environment loader
# ---------------------------------------------------------------------------
def load_env(path: Path = ENV_PATH) -> None:
    """Load KEY=VALUE pairs from a .env file into os.environ."""
    if not path.exists():
        return

    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()

            # Strip surrounding quotes
            if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
                value = value[1:-1]

            if key and os.environ.get(key) is None:
                os.environ[key] = value


# ---------------------------------------------------------------------------
# Watermark / state manager
# ---------------------------------------------------------------------------
class StateManager:
    """Persist incremental pipeline state inside the SQLite warehouse.

    Tracks:
    - which source files have been fully processed by each target
    - which individual records have been loaded into SQLite and/or MongoDB
    - surrogate key sequence state (max transaction_id is derived from data)
    """

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._init_tables()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_tables(self) -> None:
        conn = self._connect()
        cursor = conn.cursor()
        cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS dim_store (
                store_id INTEGER PRIMARY KEY AUTOINCREMENT,
                warehouse TEXT NOT NULL,
                location TEXT NOT NULL,
                UNIQUE(warehouse, location)
            );

            CREATE TABLE IF NOT EXISTS fact_sales (
                transaction_id INTEGER PRIMARY KEY,
                product_id INTEGER NOT NULL,
                product_name TEXT NOT NULL,
                category TEXT,
                store_id INTEGER NOT NULL,
                quantity REAL,
                price REAL,
                supplier TEXT,
                status TEXT,
                last_restocked TEXT,
                row_hash TEXT UNIQUE,
                loaded_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (store_id) REFERENCES dim_store(store_id)
            );

            CREATE TABLE IF NOT EXISTS etl_processed_files (
                file_path TEXT PRIMARY KEY,
                file_hash TEXT,
                sqlite_processed INTEGER DEFAULT 0,
                mongodb_processed INTEGER DEFAULT 0,
                processed_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS etl_loaded_records (
                row_hash TEXT PRIMARY KEY,
                source_type TEXT,
                sqlite_loaded INTEGER DEFAULT 0,
                mongodb_loaded INTEGER DEFAULT 0,
                first_seen_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        conn.commit()
        conn.close()

    def reset(self) -> None:
        """Drop and recreate all state tables (full-refresh)."""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.executescript(
            """
            DROP TABLE IF EXISTS fact_sales;
            DROP TABLE IF EXISTS dim_store;
            DROP TABLE IF EXISTS etl_processed_files;
            DROP TABLE IF EXISTS etl_loaded_records;
            """
        )
        conn.commit()
        conn.close()
        self._init_tables()

    def get_file_states(self) -> Dict[str, Tuple[str, int, int]]:
        """Return {resolved_path: (file_hash, sqlite_processed, mongodb_processed)}."""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT file_path, file_hash, sqlite_processed, mongodb_processed FROM etl_processed_files"
        )
        rows = {r[0]: (r[1], r[2], r[3]) for r in cursor.fetchall()}
        conn.close()
        return rows

    def get_loaded_hashes_for_target(
        self, target: str, source_type: Optional[str] = None
    ) -> Set[str]:
        """Return row hashes already loaded into the given target."""
        target_col = f"{target}_loaded"
        query = f"SELECT row_hash FROM etl_loaded_records WHERE {target_col} = 1"
        params: tuple = ()
        if source_type:
            query += " AND source_type = ?"
            params = (source_type,)

        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        hashes = {r[0] for r in cursor.fetchall()}
        conn.close()
        return hashes

    def mark_hashes_loaded(
        self, hashes: List[str], target: str, source_type: str = "csv"
    ) -> None:
        """Record that a list of row hashes have been loaded into a target."""
        if not hashes:
            return

        target_col = f"{target}_loaded"
        other_col = "sqlite_loaded" if target == "mongodb" else "mongodb_loaded"

        conn = self._connect()
        cursor = conn.cursor()

        # Insert rows for unseen hashes with the target flag already true.
        cursor.executemany(
            f"""
            INSERT OR IGNORE INTO etl_loaded_records
            (row_hash, source_type, {target_col}, {other_col})
            VALUES (?, ?, 1, 0)
            """,
            [(h, source_type) for h in hashes],
        )

        # Set the target flag for hashes that already existed.
        cursor.executemany(
            f"UPDATE etl_loaded_records SET {target_col} = 1 WHERE row_hash = ?",
            [(h,) for h in hashes],
        )

        conn.commit()
        conn.close()

    def mark_files_processed(
        self, files: List[Path], file_hashes: Dict[Path, str], target: str
    ) -> None:
        """Mark a list of source files as fully processed for a target."""
        if not files:
            return

        target_col = f"{target}_processed"
        other_col = "sqlite_processed" if target == "mongodb" else "mongodb_processed"

        conn = self._connect()
        cursor = conn.cursor()

        for f in files:
            key = str(f.resolve())
            h = file_hashes.get(f, "")

            cursor.execute(
                f"""
                UPDATE etl_processed_files
                SET {target_col} = 1, file_hash = ?, processed_at = CURRENT_TIMESTAMP
                WHERE file_path = ?
                """,
                (h, key),
            )
            if cursor.rowcount == 0:
                cursor.execute(
                    f"""
                    INSERT INTO etl_processed_files
                    (file_path, file_hash, {target_col}, {other_col})
                    VALUES (?, ?, 1, 0)
                    """,
                    (key, h),
                )

        conn.commit()
        conn.close()

    def get_max_transaction_id(self) -> int:
        """Return the current maximum transaction_id in fact_sales (0 if empty)."""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT COALESCE(MAX(transaction_id), 0) FROM fact_sales")
        value = cursor.fetchone()[0]
        conn.close()
        return int(value)


# ---------------------------------------------------------------------------
# Mock data helper
# ---------------------------------------------------------------------------
def ensure_mock_json(path: Path = JSON_PATH, n: int = 60) -> None:
    """Generate a small JSON feedback log file if one does not exist."""
    if path.exists():
        return

    products = ["widget a", "widget b", "widget c", "gadget x", "gadget y", "gadget z"]
    channels = ["web", "mobile", "in-store", "email", "phone"]
    tags_pool = [
        ["shipping"],
        ["quality"],
        ["price"],
        ["support"],
        ["shipping", "quality"],
        ["packaging"],
    ]

    records = []
    base_ts = datetime(2023, 1, 1, tzinfo=timezone.utc).timestamp()
    for i in range(n):
        records.append(
            {
                "log_id": str(uuid.uuid4()),
                "customer_id": f"C-{1000 + i}",
                "product_name": products[i % len(products)],
                "feedback": f"Customer feedback entry number {i + 1}",
                "rating": int(np.random.choice([1, 2, 3, 4, 5], p=[0.05, 0.10, 0.20, 0.35, 0.30])),
                "metadata": {
                    "channel": channels[i % len(channels)],
                    "tags": tags_pool[i % len(tags_pool)],
                },
                "timestamp": base_ts + i * 86400,
            }
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(records, handle, indent=2)

    logger.info(f"[SETUP] Generated mock JSON logs at {path} ({n} records)")


# ---------------------------------------------------------------------------
# File discovery
# ---------------------------------------------------------------------------
def _file_hash(path: Path) -> str:
    """Return the MD5 hex digest of a file (chunked for large files)."""
    hasher = hashlib.md5()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _required_targets(f: Path) -> List[str]:
    """Return the targets that must process a given file type."""
    return ["sqlite", "mongodb"] if f.suffix.lower() == ".csv" else ["mongodb"]


def _is_fully_processed(stored, f: Path, h: str) -> bool:
    """Check whether all required targets for the file have processed this hash."""
    ph, sp, mp = stored
    if ph != h:
        return False
    targets = _required_targets(f)
    if "sqlite" in targets and sp != 1:
        return False
    if "mongodb" in targets and mp != 1:
        return False
    return True


def discover_sources(
    landing_zone: Path, state: StateManager
) -> Tuple[List[Path], List[Path], Dict[Path, str], Dict[str, int]]:
    """Discover new, changed, and partially-processed source files.

    A file is skipped only when its content hash matches the stored hash AND
    all targets that consume that file type have marked it processed. Otherwise
    it is queued for reprocessing and target-side duplicate detection will
    skip already-loaded rows.
    """
    processed = state.get_file_states()

    csv_files: List[Path] = []
    json_files: List[Path] = []
    file_hashes: Dict[Path, str] = {}
    stats = {"new": 0, "changed": 0, "unchanged": 0}

    for pattern, container in [("*.csv", csv_files), ("*.json", json_files)]:
        for f in sorted(landing_zone.glob(pattern)):
            h = _file_hash(f)
            file_hashes[f] = h
            key = str(f.resolve())

            if key in processed:
                stored = processed[key]
                if _is_fully_processed(stored, f, h):
                    stats["unchanged"] += 1
                    continue
                else:
                    stats["changed"] += 1
            else:
                stats["new"] += 1

            container.append(f)

    return csv_files, json_files, file_hashes, stats


# ---------------------------------------------------------------------------
# Extract
# ---------------------------------------------------------------------------
def extract_csv_files(csv_files: List[Path]) -> pd.DataFrame:
    """Read and concatenate one or more CSV files."""
    if not csv_files:
        return pd.DataFrame()

    frames = [pd.read_csv(f) for f in csv_files]
    return pd.concat(frames, ignore_index=True)


def extract_json_files(json_files: List[Path]) -> List[dict]:
    """Read and flatten one or more JSON files (each a list or single object)."""
    records: List[dict] = []
    for f in json_files:
        with f.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        if isinstance(data, list):
            records.extend(data)
        else:
            records.append(data)
    return records


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _compute_csv_row_hash(row: pd.Series) -> str:
    """Deterministic SHA-256 hash of a cleaned CSV row."""
    # Exclude any bookkeeping columns that may exist in the Series
    skip = {"source_file", "row_hash", "transaction_id"}
    cols = sorted(c for c in row.index if c not in skip)

    parts = ["csv"]
    for col in cols:
        value = row[col]
        if pd.isna(value):
            parts.append("")
        elif isinstance(value, (pd.Timestamp, datetime)):
            parts.append(value.strftime("%Y-%m-%d"))
        elif isinstance(value, float):
            parts.append(f"{value:.6f}")
        else:
            parts.append(str(value).strip().lower())

    payload = "|".join(parts)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _compute_json_hash(record: dict) -> str:
    """Deterministic SHA-256 hash of a JSON record."""
    payload = json.dumps(record, sort_keys=True, default=str, ensure_ascii=True)
    return hashlib.sha256(f"json|{payload}".encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Transform - CSV (structured stream)
# ---------------------------------------------------------------------------
def transform_csv(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, int]]:
    """Clean the raw CSV into a normalized tabular DataFrame with row hashes.

    Returns the cleaned DataFrame plus a metrics dict describing how many
    raw rows were dropped due to missing critical IDs, exact duplicates, etc.
    """
    metrics = {
        "raw_rows": len(df),
        "missing_id_dropped": 0,
        "duplicate_dropped": 0,
        "cleaned_rows": 0,
    }
    if df.empty:
        return df, metrics

    # Strip whitespace from string columns
    str_cols = ["Product Name", "Category", "Warehouse", "Location", "Supplier", "Status"]
    for col in str_cols:
        df[col] = df[col].astype(str).str.strip()

    # Fix textual quantity anomalies and cast to numeric (NaN kept for hashing)
    text_to_num = {
        "two hundred": 200,
        "three hundred": 300,
        "one hundred": 100,
        "two hundred ": 200,
        " three hundred": 300,
    }
    df["Quantity"] = df["Quantity"].astype(str).str.strip().str.lower()
    df["Quantity"] = df["Quantity"].replace(text_to_num)
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")

    # Cast price to numeric (NaN kept for hashing)
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

    # Standardize dates to ISO datetime (CSV uses dd/mm/yyyy)
    df["Last Restocked"] = pd.to_datetime(df["Last Restocked"], dayfirst=True, errors="coerce")

    # Drop rows with missing critical identifiers
    df["Product ID"] = pd.to_numeric(df["Product ID"], errors="coerce")
    before_id_drop = len(df)
    df = df.dropna(subset=["Product ID", "Last Restocked"])
    metrics["missing_id_dropped"] = before_id_drop - len(df)

    # Drop exact duplicate transaction rows (whitespace already normalized)
    before_dedup = len(df)
    df = df.drop_duplicates()
    metrics["duplicate_dropped"] = before_dedup - len(df)

    # Stable row hash computed BEFORE mean imputation so it stays stable
    # across runs that add new data.
    df["row_hash"] = df.apply(_compute_csv_row_hash, axis=1)

    # Impute missing values after hashing so row identity does not drift
    quantity_mean = df["Quantity"].mean()
    df["Quantity"] = df["Quantity"].fillna(quantity_mean)

    avg_price_by_product = df.groupby("Product Name")["Price"].mean().to_dict()
    df["Price"] = df["Price"].fillna(df["Product Name"].map(avg_price_by_product))
    df["Price"] = df["Price"].fillna(df["Price"].mean())

    # Final type casting
    df["Product ID"] = df["Product ID"].astype(int)
    df["Quantity"] = df["Quantity"].astype(float)
    df["Price"] = df["Price"].astype(float)

    metrics["cleaned_rows"] = len(df)

    logger.info(
        f"[TRANSFORM] Cleaned {len(df)} rows; dropped {metrics['duplicate_dropped']} "
        f"exact duplicates; {metrics['missing_id_dropped']} rows quarantined "
        "for missing Product ID or Last Restocked."
    )
    return df, metrics


def build_star_schema(df: pd.DataFrame, start_id: int = 0) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Split a cleaned CSV DataFrame into a new-store dimension and a fact frame.

    Assigns a contiguous transaction_id sequence starting from start_id+1 so
    the same ID can be used by both SQLite and MongoDB targets.
    """
    if df.empty:
        empty_fact = pd.DataFrame(
            columns=[
                "transaction_id",
                "product_id",
                "product_name",
                "category",
                "warehouse",
                "location",
                "quantity",
                "price",
                "supplier",
                "status",
                "last_restocked",
                "row_hash",
            ]
        )
        empty_dim = pd.DataFrame(columns=["Warehouse", "Location"])
        return empty_dim, empty_fact

    dim_store = df[["Warehouse", "Location"]].drop_duplicates().reset_index(drop=True)

    fact = df.copy().reset_index(drop=True)
    fact["warehouse"] = fact["Warehouse"]
    fact["location"] = fact["Location"]
    fact = fact.rename(
        columns={
            "Product ID": "product_id",
            "Product Name": "product_name",
            "Category": "category",
            "Quantity": "quantity",
            "Price": "price",
            "Supplier": "supplier",
            "Status": "status",
            "Last Restocked": "last_restocked",
        }
    )

    fact["transaction_id"] = np.arange(start_id + 1, start_id + 1 + len(fact))

    return dim_store, fact


# ---------------------------------------------------------------------------
# Transform - JSON (flexible stream)
# ---------------------------------------------------------------------------
def transform_json(records: List[dict]) -> List[dict]:
    """Normalize timestamps and attach a stable _row_hash to each JSON record."""
    for rec in records:
        ts = rec.get("timestamp")
        if ts is not None and not isinstance(ts, datetime):
            try:
                if isinstance(ts, (int, float)):
                    dt = pd.to_datetime(ts, unit="s", utc=True)
                else:
                    dt = pd.to_datetime(ts, utc=True, errors="coerce")
                if pd.notna(dt):
                    rec["timestamp"] = dt.to_pydatetime()
            except Exception:
                pass

        # Use the natural log_id as the dedup key when present; otherwise hash.
        rec["_row_hash"] = rec.get("log_id") or _compute_json_hash(rec)

    return records


# ---------------------------------------------------------------------------
# Load - SQLite
# ---------------------------------------------------------------------------
def load_sqlite(db_path: Path, fact_sales: pd.DataFrame, dim_store_new: pd.DataFrame) -> Tuple[int, int, List[str]]:
    """Insert new rows into the SQLite warehouse.

    Uses INSERT OR IGNORE on the dim_store natural key and the fact_sales
    row_hash unique key so incremental re-runs are idempotent.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Ensure schema exists (CREATE IF NOT EXISTS is safe even if StateManager made it)
    cursor.executescript(
        """
        CREATE TABLE IF NOT EXISTS dim_store (
            store_id INTEGER PRIMARY KEY AUTOINCREMENT,
            warehouse TEXT NOT NULL,
            location TEXT NOT NULL,
            UNIQUE(warehouse, location)
        );
        CREATE TABLE IF NOT EXISTS fact_sales (
            transaction_id INTEGER PRIMARY KEY,
            product_id INTEGER NOT NULL,
            product_name TEXT NOT NULL,
            category TEXT,
            store_id INTEGER NOT NULL,
            quantity REAL,
            price REAL,
            supplier TEXT,
            status TEXT,
            last_restocked TEXT,
            row_hash TEXT UNIQUE,
            loaded_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (store_id) REFERENCES dim_store(store_id)
        );
        """
    )

    # Add any new stores (old ones are ignored)
    for _, row in dim_store_new.iterrows():
        cursor.execute(
            "INSERT OR IGNORE INTO dim_store (warehouse, location) VALUES (?, ?)",
            (row["Warehouse"], row["Location"]),
        )

    # Build a fresh store_id -> (warehouse, location) lookup
    cursor.execute("SELECT store_id, warehouse, location FROM dim_store")
    store_map = {(w, l): sid for sid, w, l in cursor.fetchall()}

    inserted_hashes: List[str] = []
    if not fact_sales.empty:
        # Map each fact row to its store_id
        fact = fact_sales.copy()
        fact["store_id"] = fact.apply(
            lambda r: store_map.get((r["warehouse"], r["location"])), axis=1
        )

        # Use pre-assigned transaction_id when available; otherwise generate from current max
        if "transaction_id" not in fact.columns:
            cursor.execute("SELECT COALESCE(MAX(transaction_id), 0) FROM fact_sales")
            start_id = cursor.fetchone()[0]
            fact["transaction_id"] = np.arange(start_id + 1, start_id + 1 + len(fact))

        rows = []
        for _, r in fact.iterrows():
            rows.append(
                (
                    int(r["transaction_id"]),
                    int(r["product_id"]),
                    r["product_name"],
                    r["category"],
                    int(r["store_id"]),
                    float(r["quantity"]),
                    float(r["price"]),
                    r["supplier"],
                    r["status"],
                    r["last_restocked"].strftime("%Y-%m-%d") if pd.notna(r["last_restocked"]) else None,
                    r["row_hash"],
                )
            )
            inserted_hashes.append(r["row_hash"])

        cursor.executemany(
            """
            INSERT OR IGNORE INTO fact_sales
            (transaction_id, product_id, product_name, category, store_id,
             quantity, price, supplier, status, last_restocked, row_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )

    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM fact_sales")
    fact_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM dim_store")
    dim_count = cursor.fetchone()[0]
    conn.close()

    logger.info(f"[LOAD - SQLITE] Inserted {len(inserted_hashes)} new fact_sales rows.")
    logger.info(f"[LOAD - SQLITE] Warehouse now has {fact_count} fact_sales and {dim_count} dim_store rows.")
    return fact_count, dim_count, inserted_hashes


# ---------------------------------------------------------------------------
# Load - MongoDB Atlas
# ---------------------------------------------------------------------------
def _to_sales_document(row) -> dict:
    """Convert a fact_sales row into a nested MongoDB document."""
    return {
        "_id": row["row_hash"],
        "transaction_id": int(row["transaction_id"]),
        "product": {
            "product_id": int(row["product_id"]),
            "product_name": row["product_name"],
            "category": row["category"],
        },
        "store": {
            "warehouse": row.get("warehouse"),
            "location": row.get("location"),
        },
        "transaction": {
            "quantity": float(row["quantity"]),
            "price": float(row["price"]),
            "supplier": row["supplier"],
            "status": row["status"],
            "last_restocked": row["last_restocked"] if pd.notna(row["last_restocked"]) else None,
        },
    }


def _clean_record(doc: dict) -> dict:
    """Remove NaN/NaT values that are not BSON-serializable."""
    cleaned = {}
    for key, value in doc.items():
        if isinstance(value, float) and np.isnan(value):
            cleaned[key] = None
        elif isinstance(value, dict):
            cleaned[key] = _clean_record(value)
        elif isinstance(value, list):
            cleaned[key] = [
                _clean_record(item) if isinstance(item, dict) else item for item in value
            ]
        else:
            cleaned[key] = value
    return cleaned


def load_mongodb(
    fact_sales: pd.DataFrame, json_records: List[dict], full_refresh: bool = False
) -> Tuple[int, int, List[str], List[str]]:
    """Insert new documents into MongoDB Atlas.

    Uses _id=row_hash for sales_documents and _id=log_id for feedback_logs.
    Existing _ids are pre-filtered using the collection itself, making the
    operation idempotent even if the local state table is out of sync.
    """
    if not PYMONGO_AVAILABLE:
        logger.error(
            "[LOAD - MONGODB] pymongo is not installed. Install it with: pip install pymongo"
        )
        return 0, 0, [], []

    load_env(ENV_PATH)
    uri = os.environ.get("MONGODB_URI", "")
    database_name = os.environ.get("MONGODB_DATABASE", "warehouse_db")

    if not uri:
        logger.error("[LOAD - MONGODB] MONGODB_URI not found in .env")
        return 0, 0, [], []

    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=8000, connectTimeoutMS=10000)
        client.admin.command("ping")
    except PyMongoError as exc:
        logger.error(f"[LOAD - MONGODB] Could not connect to MongoDB Atlas: {exc}")
        return 0, 0, [], []

    db = client[database_name]
    sales_col = db["sales_documents"]
    feedback_col = db["feedback_logs"]

    if full_refresh:
        sales_col.delete_many({})
        feedback_col.delete_many({})

    # Sales documents from the CSV-derived fact table
    sales_docs = [_to_sales_document(row) for _, row in fact_sales.iterrows()]
    if sales_docs:
        existing_sales_ids = set(sales_col.distinct("_id"))
        sales_docs = [d for d in sales_docs if d["_id"] not in existing_sales_ids]

    sales_inserted_hashes: List[str] = []
    if sales_docs:
        try:
            sales_result = sales_col.insert_many(sales_docs, ordered=False)
            sales_inserted_hashes = [str(_id) for _id in sales_result.inserted_ids]
            sales_count = len(sales_inserted_hashes)
        except BulkWriteError as bwe:
            # Count inserted and extract successfully inserted _ids
            sales_count = bwe.details.get("nInserted", 0)
            sales_inserted_hashes = [
                str(write.get("_id")) for write in bwe.details.get("writeErrors", [])
                if write.get("code") != 11000  # duplicate key
            ]
            logger.warning(
                f"[LOAD - MONGODB] Bulk write had partial errors; "
                f"{sales_count} sales documents inserted."
            )
    else:
        sales_count = 0

    # Feedback documents from the JSON logs
    feedback_docs = []
    for rec in json_records:
        doc = rec.copy()
        row_hash = doc.pop("_row_hash", None)
        if not row_hash:
            row_hash = _compute_json_hash(doc)
        doc["_id"] = row_hash
        feedback_docs.append(_clean_record(doc))

    if feedback_docs:
        existing_feedback_ids = set(feedback_col.distinct("_id"))
        feedback_docs = [d for d in feedback_docs if d["_id"] not in existing_feedback_ids]

    feedback_inserted_hashes: List[str] = []
    if feedback_docs:
        try:
            feedback_result = feedback_col.insert_many(feedback_docs, ordered=False)
            feedback_inserted_hashes = [str(_id) for _id in feedback_result.inserted_ids]
            feedback_count = len(feedback_inserted_hashes)
        except BulkWriteError as bwe:
            feedback_count = bwe.details.get("nInserted", 0)
            feedback_inserted_hashes = [
                str(write.get("_id")) for write in bwe.details.get("writeErrors", [])
                if write.get("code") != 11000
            ]
            logger.warning(
                f"[LOAD - MONGODB] Bulk write had partial errors; "
                f"{feedback_count} feedback documents inserted."
            )
    else:
        feedback_count = 0

    client.close()

    logger.info(
        f"[LOAD - MONGODB] Inserted {sales_count} new sales_documents into "
        f"'{database_name}.sales_documents'."
    )
    logger.info(
        f"[LOAD - MONGODB] Inserted {feedback_count} new feedback_logs into "
        f"'{database_name}.feedback_logs'."
    )
    return sales_count, feedback_count, sales_inserted_hashes, feedback_inserted_hashes


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------
def verify_sqlite(db_path: Path):
    """Run a quick count and date-range query against the SQLite warehouse."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*), MIN(last_restocked), MAX(last_restocked) FROM fact_sales")
    fact_count, min_date, max_date = cursor.fetchone()
    cursor.execute("SELECT COUNT(*) FROM dim_store")
    dim_count = cursor.fetchone()[0]
    conn.close()
    return fact_count, dim_count, min_date, max_date


def verify_mongodb():
    """Count documents in the MongoDB collections."""
    if not PYMONGO_AVAILABLE:
        return 0, 0

    load_env(ENV_PATH)
    uri = os.environ.get("MONGODB_URI", "")
    database_name = os.environ.get("MONGODB_DATABASE", "warehouse_db")
    if not uri:
        return 0, 0

    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        db = client[database_name]
        sales_count = db["sales_documents"].count_documents({})
        feedback_count = db["feedback_logs"].count_documents({})
        client.close()
        return sales_count, feedback_count
    except PyMongoError:
        return 0, 0


def export_mongo_verification(out_path: Path = None) -> Path:
    """Fetch one sample document from each MongoDB collection and save as JSON proof."""
    if out_path is None:
        out_path = SCRIPT_DIR / "mongo_verification.json"

    if not PYMONGO_AVAILABLE:
        logger.warning("[VERIFY - MONGODB] pymongo unavailable; skipping JSON export.")
        return out_path

    load_env(ENV_PATH)
    uri = os.environ.get("MONGODB_URI", "")
    database_name = os.environ.get("MONGODB_DATABASE", "warehouse_db")
    if not uri:
        return out_path

    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        db = client[database_name]
        sales_sample = db["sales_documents"].find_one({}, {"_id": 0})
        feedback_sample = db["feedback_logs"].find_one({}, {"_id": 0})
        client.close()

        payload = {
            "database": database_name,
            "sales_documents_sample": sales_sample,
            "feedback_logs_sample": feedback_sample,
        }
        with out_path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, default=str)
        logger.info(f"[VERIFY - MONGODB] Exported sample documents to {out_path}")
    except PyMongoError as exc:
        logger.warning(f"[VERIFY - MONGODB] Could not export sample documents: {exc}")

    return out_path


# ---------------------------------------------------------------------------
# Main runner
# ---------------------------------------------------------------------------
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="RetailPulse incremental multi-target ETL pipeline"
    )
    parser.add_argument(
        "--full-refresh",
        action="store_true",
        help="Rebuild the warehouse and MongoDB collections from scratch.",
    )
    return parser.parse_args()


def run(full_refresh: bool = False):
    start = time.time()

    ensure_mock_json()
    state = StateManager(DB_PATH)

    if full_refresh:
        logger.info("[MODE] Full-refresh: clearing all local state and target collections.")
        state.reset()

    # 1. Discover source files
    csv_files, json_files, file_hashes, file_stats = discover_sources(LANDING_ZONE, state)
    logger.info(
        f"[EXTRACT] Scanned landing zone: {file_stats['new']} new, "
        f"{file_stats['changed']} changed, {file_stats['unchanged']} unchanged file(s). "
        f"CSV to process: {len(csv_files)}, JSON to process: {len(json_files)}."
    )

    # 2. Extract
    df_csv = extract_csv_files(csv_files)
    json_records = extract_json_files(json_files)
    raw_csv_rows = len(df_csv)
    raw_json_objects = len(json_records)

    # 3. Transform
    df_csv_clean, csv_metrics = transform_csv(df_csv.copy())
    json_records = transform_json(json_records)

    # 4. Build the star schema once, assigning a shared transaction_id sequence
    start_id = state.get_max_transaction_id()
    dim_store_full, fact_full = build_star_schema(df_csv_clean, start_id=start_id)

    # 5. Pre-filter records already loaded into each target
    sqlite_existing_hashes = state.get_loaded_hashes_for_target("sqlite", "csv")
    mongo_existing_csv_hashes = state.get_loaded_hashes_for_target("mongodb", "csv")
    mongo_existing_json_hashes = state.get_loaded_hashes_for_target("mongodb", "json")

    fact_for_sqlite = pd.DataFrame()
    fact_for_mongo = pd.DataFrame()
    if not fact_full.empty:
        fact_for_sqlite = fact_full[
            ~fact_full["row_hash"].isin(sqlite_existing_hashes)
        ].copy()
        fact_for_mongo = fact_full[
            ~fact_full["row_hash"].isin(mongo_existing_csv_hashes)
        ].copy()

    json_for_mongo = [
        rec for rec in json_records if rec.get("_row_hash") not in mongo_existing_json_hashes
    ]

    # 6. Prepare inputs for each target
    fact_sqlite = fact_for_sqlite
    fact_mongo = fact_for_mongo

    # 6. Concurrent dual-target load
    sqlite_future = None
    mongo_future = None
    with ThreadPoolExecutor(max_workers=2) as executor:
        sqlite_future = executor.submit(load_sqlite, DB_PATH, fact_sqlite, dim_store_full)
        mongo_future = executor.submit(load_mongodb, fact_mongo, json_for_mongo, full_refresh)

        sqlite_fact, sqlite_dim, sqlite_inserted_hashes = sqlite_future.result()
        mongo_sales, mongo_fb, mongo_sales_hashes, mongo_fb_hashes = mongo_future.result()

    # 7. Update incremental state (serial, after both loads)
    state.mark_hashes_loaded(sqlite_inserted_hashes, "sqlite", "csv")
    state.mark_hashes_loaded(mongo_sales_hashes, "mongodb", "csv")
    state.mark_hashes_loaded(mongo_fb_hashes, "mongodb", "json")

    state.mark_files_processed(csv_files, file_hashes, "sqlite")
    state.mark_files_processed(csv_files, file_hashes, "mongodb")
    state.mark_files_processed(json_files, file_hashes, "mongodb")

    # 8. Verification
    sqlite_fact_v, sqlite_dim_v, min_date, max_date = verify_sqlite(DB_PATH)
    mongo_sales_v, mongo_feedback_v = verify_mongodb()
    mongo_verify_path = export_mongo_verification()

    elapsed = time.time() - start
    logger.info(
        f"[COMPLETE] Incremental pipeline execution finished in {elapsed:.2f} seconds."
    )

    # 9. Summary report
    summary = [
        "RetailPulse Incremental Multi-Target ETL Pipeline - Summary Report",
        "=" * 62,
        "Extraction:",
        f"  - File scan                : {file_stats['new']} new, {file_stats['changed']} changed, {file_stats['unchanged']} unchanged",
        f"  - CSV files to process     : {len(csv_files)}",
        f"  - JSON files to process    : {len(json_files)}",
        f"  - CSV raw rows             : {raw_csv_rows}",
        f"  - JSON raw objects         : {raw_json_objects}",
        "",
        "Transformation / Cleansing:",
        f"  - Raw CSV rows             : {csv_metrics['raw_rows']}",
        f"  - Quarantined (missing ID/date): {csv_metrics['missing_id_dropped']}",
        f"  - Dropped exact duplicates : {csv_metrics['duplicate_dropped']}",
        f"  - Cleaned CSV rows         : {csv_metrics['cleaned_rows']}",
        f"  - New rows for SQLite      : {len(fact_sqlite)}",
        f"  - New rows for MongoDB     : {len(fact_mongo)}",
        f"  - New feedback for MongoDB : {len(json_for_mongo)}",
        "",
        "SQLite Load:",
        f"  - fact_sales total rows    : {sqlite_fact_v}",
        f"  - dim_store total rows     : {sqlite_dim_v}",
        f"  - fact_sales date range    : {min_date} to {max_date}",
        "",
        "MongoDB Load:",
        f"  - sales_documents total    : {mongo_sales_v}",
        f"  - feedback_logs total      : {mongo_feedback_v}",
        "",
        "Verification query outputs:",
        "  SQLite:",
        f"    SELECT COUNT(*), MIN(last_restocked), MAX(last_restocked) FROM fact_sales",
        f"      → {sqlite_fact_v}, {min_date}, {max_date}",
        f"    SELECT COUNT(*) FROM dim_store",
        f"      → {sqlite_dim_v}",
        "  MongoDB:",
        f"    db.sales_documents.count_documents({{}})",
        f"      → {mongo_sales_v}",
        f"    db.feedback_logs.count_documents({{}})",
        f"      → {mongo_feedback_v}",
        "",
        "Verification artifacts:",
        f"  - SQLite DB                : {DB_PATH}",
        f"  - MongoDB samples          : {mongo_verify_path}",
        f"  - Summary report           : {SUMMARY_PATH}",
        "",
        f"Execution time              : {elapsed:.2f} seconds",
    ]
    SUMMARY_PATH.write_text("\n".join(summary), encoding="utf-8")
    logger.info(f"[SUMMARY] Written pipeline summary to {SUMMARY_PATH}")


def main():
    args = parse_args()
    full_refresh = args.full_refresh or os.environ.get("FULL_REFRESH", "").lower() in (
        "1",
        "true",
        "yes",
    )
    run(full_refresh=full_refresh)


if __name__ == "__main__":
    main()
