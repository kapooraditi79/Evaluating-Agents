import hashlib
import json
from typing import Any


def dataset_identity(tables: dict[str, list[dict[str, Any]]], metadata: dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(
            {"tables": tables, "metadata": metadata},
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode()
    ).hexdigest()
