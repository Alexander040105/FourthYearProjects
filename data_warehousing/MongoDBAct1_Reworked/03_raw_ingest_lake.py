"""
Raw JSON payload ingestion into the JuanMart Data Lake landing collection.
"""

import importlib.util
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# Load the local 02_mongo_driver.py module.
DRIVER_PATH = Path(__file__).with_name("02_mongo_driver.py")
DRIVER_MODULE = None


def _load_driver_module():
    spec = importlib.util.spec_from_file_location("mongo_driver", str(DRIVER_PATH))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


DRIVER_MODULE = _load_driver_module()


def _configure_logging(log_file: Path) -> None:
    fmt = "%(asctime)s - %(levelname)s - %(message)s"
    handlers = [logging.FileHandler(log_file, mode="w"), logging.StreamHandler()]
    logging.basicConfig(level=logging.INFO, format=fmt, handlers=handlers, force=True)


def load_payload(payload_path: Path) -> List[Dict[str, Any]]:
    with open(payload_path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    if isinstance(data, dict):
        return [data]
    return list(data)


def normalize_documents(payload: List[Any]) -> List[Dict[str, Any]]:
    documents = []
    for doc in payload:
        if not isinstance(doc, dict):
            logging.warning("Skipping non-object item: %r", doc)
            continue
        documents.append(doc)
    return documents


def enrich_documents(documents: List[Dict[str, Any]], source_path: Path) -> List[Dict[str, Any]]:
    ingested_at = datetime.now(timezone.utc)
    enriched = []
    for doc in documents:
        doc_copy = doc.copy()
        doc_copy["_source_file"] = source_path.name
        doc_copy["ingestedAt"] = ingested_at
        enriched.append(doc_copy)
    return enriched


def _ensure_landing_collection(database: Any, collection_name: str) -> Any:
    if collection_name not in database.list_collection_names():
        try:
            database.create_collection(
                collection_name,
                capped=True,
                size=52428800,
                max=50000,
            )
        except Exception:
            database.create_collection(collection_name)
        collection = database[collection_name]
        collection.create_index("source")
        collection.create_index("eventType")
        collection.create_index([("ingestedAt", -1)])
        collection.create_index([("source", 1), ("eventType", 1)])
        collection.create_index([("source", 1), ("ingestedAt", -1)])
    return database[collection_name]


def _format_audit_lines(total: int, stream_counts: Dict[str, int]) -> List[str]:
    lines = [
        "=" * 54,
        "DATA LAKE LANDING AUDIT ",
        "=" * 54,
        f"TOTAL DOCUMENTS LANDED : {total:,}",
        f"WEB_STORE STREAM : {stream_counts.get('WEB_STORE', 0):,} documents",
        f"POS_TERMINALS STREAM : {stream_counts.get('POS_TERMINALS', 0):,} documents",
        f"MOBILE_APP STREAM : {stream_counts.get('MOBILE_APP', 0):,} documents",
        "=" * 54,
    ]
    return lines


def ingest_payload(payload_file: Path, collection_name: str = "raw_checkout_landing") -> int:
    log_file = payload_file.with_name("lake_ingest_execution.log")
    _configure_logging(log_file)

    logger = logging.getLogger(__name__)

    logger.info("Initializing Data Lake MongoClient connection pool...")
    driver = DRIVER_MODULE.get_driver()
    logger.info("[+] Successfully established Data Lake connection to: %s", driver._config.database)

    logger.info("[*] Commencing raw JSON payload stream ingestion...")

    source_path = payload_file.expanduser().resolve()
    payload = load_payload(source_path)
    documents = normalize_documents(payload)
    if not documents:
        logger.warning("[-] No documents found in payload file. Exiting.")
        return 0

    database = driver.get_database()
    logger.info("[-] Staging %s raw JSON documents into collection: %s", f"{len(documents):,}", collection_name)
    collection = _ensure_landing_collection(database, collection_name)

    prepared_documents = enrich_documents(documents, source_path)
    result = collection.insert_many(prepared_documents, ordered=False)
    inserted = len(result.inserted_ids)

    logger.info("[+] Ingestion Complete. Bulk Insert Acknowledged: %s", result.acknowledged)

    stream_counts = {
        bucket["_id"]: bucket["count"]
        for bucket in collection.aggregate([{"$group": {"_id": "$source", "count": {"$sum": 1}}}])
    }
    total = collection.count_documents({})

    for line in _format_audit_lines(total, stream_counts):
        logger.info(line)

    return inserted


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Ingest raw JSON payload into the Data Lake landing collection.")
    parser.add_argument(
        "--payload",
        type=Path,
        default=Path(__file__).with_name("mock_payload.json"),
        help="Path to the raw JSON payload file.",
    )
    parser.add_argument(
        "--collection",
        default="raw_checkout_landing",
        help="Target landing collection name.",
    )
    args = parser.parse_args()

    try:
        count = ingest_payload(args.payload, args.collection)
        print(f"Inserted {count} documents.")
    finally:
        logging.info("[+] Data Lake MongoClient connection pool gracefully closed.")
        DRIVER_MODULE.get_driver().close()


if __name__ == "__main__":
    main()
