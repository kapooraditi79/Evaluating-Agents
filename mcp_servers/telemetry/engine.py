"""Protocol-independent tool execution, pagination, identity, validation and bounded output."""

from __future__ import annotations

import logging
import re
from collections.abc import Callable
from typing import Any

from pydantic import ValidationError

from contracts.models import TOOL_VERSION, TableData, ToolResult, ToolSource, WarningItem
from contracts.queries import QUERY_MODELS
from store.base import TelemetryStore
from store.evidence import QueryIds, canonical_query, compact_json, digest_query
from store.parquet import QueryError

PREFIXES = {
    "list_services": "V",
    "query_metric": "M",
    "compare_windows": "M",
    "find_traces": "T",
    "get_trace": "S",
    "search_logs": "L",
    "get_dependencies": "D",
    "check_coverage": "C",
    "breakdown": "B",
}


class ToolEngine:
    def __init__(
        self,
        store: TelemetryStore,
        cap: int = 1500,
        token_counter: Callable[[str], int] | None = None,
    ):
        if type(cap) is not int or cap < 400:
            raise ValueError("response budget must be an integer >= 400")
        self.store = store
        self.cap = cap
        # Conservative ASCII-byte budget pending the exact model tokenizer.
        # This is not a measured token count.
        self.count = token_counter or (lambda text: len(text.encode("utf-8")))
        self.ids = QueryIds()
        self.tool_version = TOOL_VERSION

    def call(self, tool: str, arguments: dict[str, Any]) -> dict[str, Any]:
        if tool not in QUERY_MODELS:
            return {"error": {"code": "UNKNOWN_TOOL", "message": "tool is not available"}}
        try:
            args = QUERY_MODELS[tool].model_validate(arguments)
        except ValidationError:
            return {
                "error": {
                    "code": "INVALID_ARGUMENT",
                    "message": "arguments do not match the tool schema",
                }
            }
        try:
            canonical = canonical_query(self.store.manifest.id, self.tool_version, tool, args)
            query_id = self.ids.get(canonical)
            digest = digest_query(canonical)
            offset = 0
            if args.cursor is not None:
                parts = args.cursor.split(":")
                if (
                    len(parts) != 2
                    or parts[0] != digest
                    or re.fullmatch(r"[0-9]{1,18}", parts[1]) is None
                ):
                    raise QueryError("INVALID_CURSOR", "cursor does not belong to this result set")
                offset = int(parts[1])
            columns, all_rows, warnings = self.store.query(tool, args)
            if offset > len(all_rows):
                raise QueryError("INVALID_CURSOR", "cursor is outside this result set")
            selected: list[list[Any]] = []

            def envelope() -> dict[str, Any]:
                returned = len(selected)
                more = offset + returned < len(all_rows)
                return ToolResult(
                    data=TableData(columns=["handle", *columns], rows=selected),
                    total_matches=len(all_rows),
                    returned=returned,
                    truncated=more,
                    next_cursor=f"{digest}:{offset + returned}" if more else None,
                    query_id=query_id,
                    source=ToolSource(
                        dataset_id=self.store.manifest.id, tool_version=self.tool_version
                    ),
                    warnings=[WarningItem.model_validate(w) for w in warnings],
                ).model_dump()

            for position in range(offset, min(offset + args.limit, len(all_rows))):
                selected.append([f"{PREFIXES[tool]}{position + 1}", *all_rows[position]])
                if self.count(compact_json(envelope())) > self.cap:
                    selected.pop()
                    break
            result = envelope()
            if self.count(compact_json(result)) > self.cap or (
                not selected and offset < len(all_rows)
            ):
                raise QueryError(
                    "OUTPUT_TOO_LARGE",
                    "a result row or metadata exceeds the response budget; narrow the query",
                )
            return result
        except QueryError as exc:
            return {"error": {"code": exc.code, "message": exc.message}}
        except Exception:
            logging.getLogger(__name__).exception("Telemetry query failed: %s", tool)
            return {
                "error": {
                    "code": "QUERY_FAILED",
                    "message": "query failed; this is not an empty result",
                }
            }
