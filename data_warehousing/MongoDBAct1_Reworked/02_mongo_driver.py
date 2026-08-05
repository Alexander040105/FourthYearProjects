"""
MongoDB Data Lake driver singleton.

Provides a single, shared, connection-pooled MongoClient for the
juanmart_data_lake database.
"""

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from pymongo import MongoClient
    from pymongo.errors import ServerSelectionTimeoutError

    _PymongoImportError: Optional[Exception] = None
except Exception as err:  # pragma: no cover
    MongoClient = None  # type: ignore[misc,assignment]
    ServerSelectionTimeoutError = Exception  # type: ignore[misc,assignment]
    _PymongoImportError = err


@dataclass(frozen=True)
class MongoConfig:
    """Configuration container for MongoDB connection settings."""

    uri: str
    database: str
    server_selection_timeout_ms: int = 5000
    connect_timeout_ms: int = 10000
    max_pool_size: int = 100
    min_pool_size: int = 0
    retry_writes: bool = True
    app_name: str = "mongo-driver-module"

    @classmethod
    def from_env(cls, config_file: Optional[Path] = None) -> "MongoConfig":
        """
        Build a MongoConfig from, in order of precedence:
          1. Environment variables
          2. A JSON config file
          3. Sensible hard-coded defaults for the lab
        """
        env = os.environ

        if config_file and config_file.exists():
            with open(config_file, "r", encoding="utf-8") as fh:
                config_data: Dict[str, Any] = json.load(fh)
        else:
            config_data = {}

        uri = env.get("MONGODB_URI") or str(config_data.get("uri") or "mongodb://localhost:27017")
        database = env.get("MONGODB_DATABASE") or str(config_data.get("database") or "juanmart_data_lake")

        return cls(
            uri=uri,
            database=database,
            server_selection_timeout_ms=_coerce_int(
                env.get("MONGODB_SERVER_SELECTION_TIMEOUT_MS")
                or config_data.get("server_selection_timeout_ms"),
                5000,
            ),
            connect_timeout_ms=_coerce_int(
                env.get("MONGODB_CONNECT_TIMEOUT_MS")
                or config_data.get("connect_timeout_ms"),
                10000,
            ),
            max_pool_size=_coerce_int(
                env.get("MONGODB_MAX_POOL_SIZE")
                or config_data.get("max_pool_size"),
                100,
            ),
            min_pool_size=_coerce_int(
                env.get("MONGODB_MIN_POOL_SIZE")
                or config_data.get("min_pool_size"),
                0,
            ),
            retry_writes=_coerce_bool(
                env.get("MONGODB_RETRY_WRITES")
                or config_data.get("retry_writes"),
                True,
            ),
            app_name=env.get("MONGODB_APP_NAME")
            or str(config_data.get("app_name") or "juanmart-lab-1.0"),
        )


class DataLakeDriver:
    """Singleton wrapper that manages a shared MongoDB client instance."""

    _instance: Optional["DataLakeDriver"] = None
    _client: Optional[MongoClient] = None
    _config: Optional[MongoConfig] = None

    def __new__(cls, config: Optional[MongoConfig] = None) -> "DataLakeDriver":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config: Optional[MongoConfig] = None) -> None:
        if self._config is not None and config is None:
            return
        if config is not None and config == self._config:
            return
        if self._client is not None:
            self._client.close()
            self._client = None
        self._config = config or MongoConfig.from_env()
        self._client = None

    def get_client(self) -> MongoClient:
        """Return a connected, shared MongoClient, creating it if needed."""
        if _PymongoImportError is not None:
            raise RuntimeError(
                f"Cannot create MongoClient because pymongo is unavailable: {_PymongoImportError}"
            ) from _PymongoImportError

        if self._client is None:
            self._client = MongoClient(
                self._config.uri,
                serverSelectionTimeoutMS=self._config.server_selection_timeout_ms,
                connectTimeoutMS=self._config.connect_timeout_ms,
                maxPoolSize=self._config.max_pool_size,
                minPoolSize=self._config.min_pool_size,
                retryWrites=self._config.retry_writes,
                appname=self._config.app_name,
            )
        return self._client

    def get_database(self, database_name: Optional[str] = None) -> Any:
        """Return the named MongoDB database object."""
        db_name = database_name or self._config.database
        return self.get_client()[db_name]

    def get_collection(self, collection_name: str, database_name: Optional[str] = None) -> Any:
        """Return a MongoDB collection object from the configured database."""
        return self.get_database(database_name)[collection_name]

    def health_check(self) -> bool:
        """Quick ping to confirm the server is reachable."""
        try:
            client = self.get_client()
            client.admin.command("ping")
            return True
        except ServerSelectionTimeoutError:
            return False

    def close(self) -> None:
        """Close the shared client and clear the cached instance."""
        if self._client is not None:
            self._client.close()
            self._client = None
        DataLakeDriver._instance = None
        DataLakeDriver._client = None
        DataLakeDriver._config = None


def _coerce_int(value: Any, default: int) -> int:
    """Return an int, falling back to default when value is missing or invalid."""
    if value is None:
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _coerce_bool(value: Any, default: bool) -> bool:
    """Return a bool, falling back to default when value is missing or invalid."""
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    return str(value).lower() in ("true", "1", "yes", "on")


def get_driver(config: Optional[MongoConfig] = None) -> DataLakeDriver:
    """Factory that returns the singleton DataLakeDriver instance."""
    return DataLakeDriver(config)
