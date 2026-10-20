"""Backend-independent read-only telemetry access."""

from store.parquet import ParquetStore, QueryError

__all__ = ["ParquetStore", "QueryError"]
