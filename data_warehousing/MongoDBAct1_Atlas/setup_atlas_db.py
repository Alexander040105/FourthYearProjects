"""
Set up the landing database on Atlas using the original driver logic.

This mirrors the original 01_datalake_setup.mongodb.js script: it creates the
rawLanding collection and inserts a sample document so the database exists.
"""

import importlib.util
from pathlib import Path


def _load_driver():
    driver_path = Path(__file__).with_name("02_mongo_driver.py")
    spec = importlib.util.spec_from_file_location("mongo_driver", str(driver_path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load driver from {driver_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    mongo_driver = _load_driver()
    manager = mongo_driver.get_connection_manager()
    database = manager.get_database()

    collection_name = "rawLanding"
    if collection_name not in database.list_collection_names():
        database.create_collection(collection_name)
        print(f"[+] Created collection '{collection_name}'.")
    else:
        print(f"[i] Collection '{collection_name}' already exists.")

    collection = database[collection_name]
    collection.insert_one({
        "source": "landing",
        "createdAt": __import__("datetime").datetime.now(__import__("datetime").timezone.utc),
        "status": "new",
    })
    print("[+] Inserted sample landing document.")

    manager.close()


if __name__ == "__main__":
    main()
