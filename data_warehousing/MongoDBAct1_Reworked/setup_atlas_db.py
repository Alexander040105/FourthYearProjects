"""
Set up the juanmart_data_lake.raw_checkout_landing collection on MongoDB Atlas.

Loads credentials from a .env file (data_warehousing/.env or the script directory),
connects, and creates the collection and indexes.
"""

import importlib.util
import os
from pathlib import Path
from typing import Any


def _load_dotenv() -> None:
    """Load key=value entries from a .env file into os.environ."""
    script_dir = Path(__file__).resolve().parent
    candidates = [
        script_dir / ".env",
        script_dir.parent / ".env",
        Path(".env").resolve(),
    ]
    for env_file in candidates:
        if env_file.exists():
            with env_file.open("r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    key, value = line.split("=", 1)
                    os.environ.setdefault(key.strip(), value.strip())
            break


def _load_driver_module() -> Any:
    driver_path = Path(__file__).with_name("02_mongo_driver.py")
    spec = importlib.util.spec_from_file_location("mongo_driver", str(driver_path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load driver from {driver_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    _load_dotenv()
    os.environ.setdefault("MONGODB_DATABASE", "juanmart_data_lake")

    mongo_driver = _load_driver_module()
    driver = mongo_driver.get_driver()
    database = driver.get_database()

    collection_name = "raw_checkout_landing"
    existing = set(database.list_collection_names())

    if collection_name in existing:
        print(f"[i] Collection '{collection_name}' already exists.")
    else:
        print(f"[*] Creating collection '{collection_name}'...")
        try:
            database.create_collection(
                collection_name,
                capped=True,
                size=52428800,
                max=50000,
            )
            print(f"[+] Created capped collection '{collection_name}'.")
        except Exception as exc:
            print(f"[-] Capped collection not supported here ({exc}); creating normal collection.")
            database.create_collection(collection_name)
            print(f"[+] Created normal collection '{collection_name}'.")

    collection = database[collection_name]
    print("[*] Creating indexes...")
    collection.create_index("source")
    collection.create_index("eventType")
    collection.create_index([("ingestedAt", -1)])
    collection.create_index([("source", 1), ("eventType", 1)])
    collection.create_index([("source", 1), ("ingestedAt", -1)])
    collection.create_index([("eventType", 1), ("ingestedAt", -1)])

    print("[+] Database setup complete.")
    driver.close()


if __name__ == "__main__":
    main()
