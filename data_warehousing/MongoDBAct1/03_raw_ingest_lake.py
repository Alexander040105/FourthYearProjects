#!/usr/bin/env python3
"""Ingest a mock JSON payload into the MongoDB landing collection."""

import argparse
import importlib.util
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

LOGGER = logging.getLogger(__name__)


def load_driver_module():
    driver_path = Path(__file__).with_name("02_mongo_driver.py")
    spec = importlib.util.spec_from_file_location("mongo_driver", driver_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load MongoDB driver module from {driver_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


DRIVER_MODULE = load_driver_module()
get_connection_manager = DRIVER_MODULE.get_connection_manager


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest a raw JSON payload into MongoDB")
    parser.add_argument(
        "payload_file",
        nargs="?",
        default=str(Path(__file__).with_name("mock_payload.json")),
        help="Path to the JSON file to ingest (defaults to mock_payload.json)",
    )
    parser.add_argument(
        "--collection",
        default="rawLanding",
        help="Target collection name in MongoDB (default: rawLanding)",
    )
    parser.add_argument(
        "--database",
        default=None,
        help="Optional database override; otherwise the configured database is used",
    )
    return parser.parse_args()


def load_payload(path: Path) -> Any:
    if not path.exists():
        raise FileNotFoundError(f"Payload file not found: {path}")

    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def normalize_documents(payload: Any) -> List[Dict[str, Any]]:
    if isinstance(payload, dict):
        return [payload]
    if isinstance(payload, list):
        documents = []
        for item in payload:
            if not isinstance(item, dict):
                raise ValueError("Each payload item must be a JSON object")
            documents.append(item)
        return documents
    raise ValueError("Payload must be a JSON object or an array of objects")


def enrich_documents(documents: List[Dict[str, Any]], source_file: Path) -> List[Dict[str, Any]]:
    timestamp = datetime.now(timezone.utc).isoformat()
    enriched: List[Dict[str, Any]] = []
    for document in documents:
        record = dict(document)
        record["_source_file"] = str(source_file)
        record["ingestedAt"] = timestamp
        enriched.append(record)
    return enriched


def ingest_payload(payload_file: str, collection_name: str, database_name: Optional[str] = None) -> int:
    source_path = Path(payload_file).expanduser().resolve()
    payload = load_payload(source_path)
    documents = normalize_documents(payload)
    if not documents:
        return 0

    manager = get_connection_manager()
    database = manager.get_database() if database_name is None else manager.get_client()[database_name]

    if collection_name not in database.list_collection_names():
        database.create_collection(collection_name)

    collection = database[collection_name]
    prepared_documents = enrich_documents(documents, source_path)
    result = collection.insert_many(prepared_documents, ordered=False)
    return len(result.inserted_ids)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
    args = parse_args()
    try:
        inserted_count = ingest_payload(args.payload_file, args.collection, args.database)
        print(f"Inserted {inserted_count} document(s) into {args.collection}")
    except Exception as exc:  # pragma: no cover - example entry point
        LOGGER.exception("Raw payload ingestion failed")
        raise SystemExit(str(exc)) from exc
