import json
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

try:
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure, PyMongoError, ServerSelectionTimeoutError
except ImportError:  # pragma: no cover - handled at runtime
    MongoClient = None
    ConnectionFailure = PyMongoError = ServerSelectionTimeoutError = Exception

LOGGER = logging.getLogger(__name__)


def _load_dotenv() -> None:
    """Load a .env file from the script folder or its parent into os.environ."""
    script_dir = Path(__file__).resolve().parent
    for env_file in (script_dir / ".env", script_dir.parent / ".env"):
        if env_file.exists():
            with env_file.open("r", encoding="utf-8") as handle:
                for line in handle:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    key, value = line.split("=", 1)
                    if os.environ.get(key.strip()) is None:
                        os.environ[key.strip()] = value.strip()
            break


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
    def from_env(cls, config_file: Optional[str] = None) -> "MongoConfig":
        """Load settings from the environment and an optional JSON config file."""

        _load_dotenv()
        env = os.environ
        config_path = None
        if config_file:
            config_path = Path(config_file)
        elif env.get("MONGODB_CONFIG_FILE"):
            config_path = Path(env["MONGODB_CONFIG_FILE"])
        else:
            default_config = Path(__file__).with_name("mongo_config.json")
            if default_config.exists():
                config_path = default_config

        config_data: Dict[str, Any] = {}
        if config_path is not None:
            try:
                with config_path.open("r", encoding="utf-8") as handle:
                    config_data = json.load(handle)
            except FileNotFoundError:
                LOGGER.debug("Config file not found at %s", config_path)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON in config file: {config_path}") from exc

        uri = env.get("MONGODB_URI") or str(config_data.get("uri") or "")
        database = env.get("MONGODB_DATABASE") or str(config_data.get("database") or "juanmart_data_lake")

        if not uri:
            raise ValueError(
                "MongoDB URI is missing. Set MONGODB_URI or provide a config file with 'uri'."
            )

        return cls(
            uri=uri,
            database=database,
            server_selection_timeout_ms=_coerce_int(
                env.get("MONGODB_SERVER_SELECTION_TIMEOUT_MS"),
                config_data.get("server_selection_timeout_ms"),
                default=5000,
            ),
            connect_timeout_ms=_coerce_int(
                env.get("MONGODB_CONNECT_TIMEOUT_MS"),
                config_data.get("connect_timeout_ms"),
                default=10000,
            ),
            max_pool_size=_coerce_int(
                env.get("MONGODB_MAX_POOL_SIZE"),
                config_data.get("max_pool_size"),
                default=100,
            ),
            min_pool_size=_coerce_int(
                env.get("MONGODB_MIN_POOL_SIZE"),
                config_data.get("min_pool_size"),
                default=0,
            ),
            retry_writes=_coerce_bool(
                env.get("MONGODB_RETRY_WRITES"),
                config_data.get("retry_writes"),
                default=True,
            ),
            app_name=str(
                env.get("MONGODB_APP_NAME") or config_data.get("app_name") or "mongo-driver-module"
            ),
        )


class MongoConnectionManager:
    """Singleton wrapper that manages a shared MongoDB client instance."""

    _instance: Optional["MongoConnectionManager"] = None
    _client: Optional[MongoClient] = None
    _config: Optional[MongoConfig] = None

    def __new__(cls, config: Optional[MongoConfig] = None) -> "MongoConnectionManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config: Optional[MongoConfig] = None) -> None:
        if self._config is not None and config is None:
            return
        self._config = config or MongoConfig.from_env()
        self._client = None

    def get_client(self) -> MongoClient:
        if MongoClient is None:
            raise RuntimeError("pymongo is not installed. Install it with: pip install pymongo")

        if self._client is None:
            self._client = MongoClient(
                self._config.uri,
                serverSelectionTimeoutMS=self._config.server_selection_timeout_ms,
                connectTimeoutMS=self._config.connect_timeout_ms,
                maxPoolSize=self._config.max_pool_size,
                minPoolSize=self._config.min_pool_size,
                retryWrites=self._config.retry_writes,
                appName=self._config.app_name,
            )
        return self._client

    def get_database(self):
        return self.get_client()[self._config.database]

    def health_check(self) -> Dict[str, Any]:
        try:
            result = self.get_client().admin.command("ping")
        except (ConnectionFailure, ServerSelectionTimeoutError, PyMongoError) as exc:
            raise RuntimeError(f"Database health check failed: {exc}") from exc

        return {
            "ok": bool(result.get("ok") == 1.0),
            "database": self._config.database,
            "ping_result": result,
        }

    def close(self) -> None:
        if self._client is not None:
            self._client.close()
            self._client = None


def get_connection_manager(config: Optional[MongoConfig] = None) -> MongoConnectionManager:
    return MongoConnectionManager(config=config)


def _coerce_int(*values: Any, default: int) -> int:
    for value in values:
        if value is None:
            continue
        if isinstance(value, bool):
            raise ValueError("Boolean values are not valid for integer settings")
        try:
            return int(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Expected an integer value, got: {value}") from exc
    return default


def _coerce_bool(*values: Any, default: bool) -> bool:
    for value in values:
        if value is None:
            continue
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            lowered = value.strip().lower()
            if lowered in {"1", "true", "yes", "on"}:
                return True
            if lowered in {"0", "false", "no", "off"}:
                return False
        raise ValueError(f"Expected a boolean value, got: {value}")
    return default


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
    try:
        manager = get_connection_manager()
        print(manager.health_check())
    except Exception as exc:  # pragma: no cover - example entry point
        LOGGER.exception("MongoDB health check failed")
        raise SystemExit(str(exc)) from exc
