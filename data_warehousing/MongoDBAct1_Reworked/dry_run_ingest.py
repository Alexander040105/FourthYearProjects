"""
Dry-run the raw ingestion pipeline using mongomock.

This is useful when a real mongod is not available. It produces a
lake_ingest_execution.log with the exact same format and document counts
as a real run, but it uses an in-memory mock MongoDB.
"""

import importlib.util
from pathlib import Path
import pymongo
import mongomock


class MockMongoClient(mongomock.MongoClient):
    """mongomock client that ignores the extra pymongo kwargs."""

    def __init__(self, *args, **kwargs):
        # Drop all the extra PyMongo connection-pool / timeout kwargs.
        for key in [
            "serverSelectionTimeoutMS",
            "connectTimeoutMS",
            "maxPoolSize",
            "minPoolSize",
            "retryWrites",
            "appname",
        ]:
            kwargs.pop(key, None)
        # mongomock does not support a mongodb:// URI as the first arg;
        # replace it with the default host string.
        if args and isinstance(args[0], str):
            args = ("localhost",) + args[1:]
        super().__init__(*args, **kwargs)


# Patch pymongo so the driver loads the mock client.
pymongo.MongoClient = MockMongoClient
pymongo.errors.ServerSelectionTimeoutError = Exception

INGEST_PATH = Path(__file__).with_name("03_raw_ingest_lake.py")
spec = importlib.util.spec_from_file_location(
    "raw_ingest", str(INGEST_PATH)
)
raw_ingest = importlib.util.module_from_spec(spec)
spec.loader.exec_module(raw_ingest)

if __name__ == "__main__":
    raw_ingest.main()
