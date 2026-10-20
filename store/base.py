from typing import Any, Protocol

from contracts.models import Manifest
from contracts.queries import Query


class TelemetryStore(Protocol):
    manifest: Manifest

    def query(
        self, tool: str, args: Query
    ) -> tuple[list[str], list[list[Any]], list[dict[str, str]]]:
        """Return deterministic unpaged columns, rows, warnings; failures raise typed errors."""
        ...
