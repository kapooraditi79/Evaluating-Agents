"""Canonical result-set identity and stable, whole-result item references."""
# gives the query an id so that we can later identify which request produced some evidence
from __future__ import annotations

import hashlib
import json
from typing import Any

from contracts.models import Window, iso_time, utc_ns
from contracts.queries import Query


# converts the input object into a dictionary
# remove the limit and cursor       [as they are not required. total result set checked]
# standardised timestamps
# includes dataset ID, tool name, and tool version
def canonical_query(dataset_id: str, tool_version: str, tool: str, args: Query) -> str:
    arguments = args.model_dump(exclude={"limit", "cursor"})
    if tool == "compare_windows":
        arguments.pop("step_seconds", None)  # only summaries are returned
    if tool in {"query_metric", "compare_windows"}:
        if arguments["metric"] not in {"cpu_utilization", "memory_mb"}:
            arguments["aggregation"] = "avg"  # gauges alone use this switch
    for name in ("window", "baseline_window"):
        if name in arguments:
            window = Window.model_validate(arguments[name])
            arguments[name] = {
                "start": iso_time(utc_ns(window.start)),
                "end": iso_time(utc_ns(window.end)),
            }
    return json.dumps(
        {
            "dataset_id": dataset_id,
            "tool_version": tool_version,
            "tool": tool,
            "arguments": arguments,
        },
        sort_keys=True,
        separators=(",", ":"),
    )

# converts the above json [from czzanonical query] into a fingerprint[a fixed length string]
def digest_query(canonical: str) -> str:
    return hashlib.sha256(canonical.encode()).hexdigest()

# so the request does not have to carry the full json everywhere


class QueryIds:
    # takes first the first 8 chars of the long fingerprint and adds q'
    def __init__(self) -> None:
        # remembers the relationship using 2 dictionaries
        self.assigned: dict[str, str] = {}          # full standardized request-> short ID
        self.by_canonical: dict[str, str] = {}      # short id-> full standardized request

    def get(self, canonical: str) -> str:
        if canonical in self.by_canonical:
            return self.by_canonical[canonical]
        digest = digest_query(canonical)
        for length in range(8, 65):
            key = "q" + digest[:length]
            if key not in self.assigned:
                self.assigned[key] = canonical
                self.by_canonical[canonical] = key
                return key
        raise ValueError("full SHA-256 collision")


def verifies(query_id: str, canonical: str) -> bool:
    """Verifier helper: session log supplies the canonical call and allocated prefix length."""
    # checks whether an ID matches a request
    return (
        query_id.startswith("q")
        and 6 <= len(query_id[1:]) <= 64
        and digest_query(canonical).startswith(query_id[1:])
    )


def compact_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, separators=(",", ":"), allow_nan=False)
