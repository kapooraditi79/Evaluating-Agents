"""STUB tool schemas for gate G0.

These mirror the nine tools proposed in PROJECT_CONTEXT.md (contract C4) closely enough
that tool COUNT and schema SIZE are realistic. They are NOT the contract: Person A owns
the real definitions. Replace this file with the real `tools/list` output once it exists.
"""

from __future__ import annotations

DATA_RANGE = ("2026-03-14T14:00:00Z", "2026-03-14T14:15:00Z")
LIMIT_MAX = 100
SERVICES = (
    "frontend",
    "checkout",
    "cart",
    "redis",
    "product-catalog",
    "postgres",
    "currency",
    "shipping",
    "payment",
    "email",
    "ad",
    "recommendation",
)
METRICS = (
    "request_count",
    "error_count",
    "latency_p50_ms",
    "latency_p95_ms",
    "latency_p99_ms",
    "cpu_utilization",
    "memory_mb",
)


def _ts(what: str) -> dict:
    return {"type": "string", "description": f"{what} (ISO-8601 UTC, e.g. 2026-03-14T14:05:00Z)"}


SERVICE = {"type": "string", "description": "Service name, e.g. payment, checkout, frontend"}
OPERATION = {"type": "string", "description": "Operation name, e.g. 'POST /checkout'"}
METRIC = {"type": "string", "enum": list(METRICS), "description": "Metric name"}
LIMIT = {
    "type": "integer",
    "minimum": 1,
    "maximum": LIMIT_MAX,
    "description": "Maximum number of items to return",
}
CURSOR = {"type": "string", "description": "next_cursor from a previous truncated result"}


def _tool(name: str, description: str, properties: dict, required: list[str]) -> dict:
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required,
                "additionalProperties": False,
            },
        },
    }


TOOLS = [
    _tool(
        "list_services",
        "List the services that have telemetry in a time window.",
        {"start": _ts("Window start"), "end": _ts("Window end")},
        [],
    ),
    _tool(
        "query_metric",
        "Time series and summary of one metric for one service over a window.",
        {
            "service": SERVICE,
            "metric": METRIC,
            "start": _ts("Window start"),
            "end": _ts("Window end"),
            "operation": OPERATION,
            "step_seconds": {
                "type": "integer",
                "minimum": 10,
                "maximum": 600,
                "description": "Resolution of the series in seconds",
            },
        },
        ["service", "metric", "start", "end"],
    ),
    _tool(
        "compare_windows",
        "Compare one metric of one service between an incident window and a baseline window.",
        {
            "service": SERVICE,
            "metric": METRIC,
            "incident_start": _ts("Incident window start"),
            "incident_end": _ts("Incident window end"),
            "baseline_start": _ts("Baseline window start"),
            "baseline_end": _ts("Baseline window end"),
        },
        ["service", "metric", "incident_start", "incident_end", "baseline_start", "baseline_end"],
    ),
    _tool(
        "find_traces",
        "Find trace summaries matching filters. Use status=ERROR to find failing requests; "
        "failing requests can be very fast, so do not rely on duration alone.",
        {
            "start": _ts("Window start"),
            "end": _ts("Window end"),
            "service": SERVICE,
            "operation": OPERATION,
            "status": {"type": "string", "enum": ["OK", "ERROR"]},
            "min_duration_ms": {"type": "number", "minimum": 0},
            "region": {"type": "string", "enum": ["us", "eu", "ap"]},
            "limit": LIMIT,
            "cursor": CURSOR,
        },
        ["start", "end"],
    ),
    _tool(
        "get_trace",
        "Return every span of one trace, in order, with parent/child relationships.",
        {
            "trace_id": {
                "type": "string",
                "description": "32-character hex trace id taken from an earlier result",
            }
        },
        ["trace_id"],
    ),
    _tool(
        "breakdown",
        "Grouped statistics of one metric, grouped by an attribute, over a window.",
        {
            "start": _ts("Window start"),
            "end": _ts("Window end"),
            "group_by": {
                "type": "string",
                "enum": ["service", "operation", "status", "version", "region"],
            },
            "metric": METRIC,
            "service": SERVICE,
        },
        ["start", "end", "group_by", "metric"],
    ),
    _tool(
        "search_logs",
        "Search log lines. Results are capped and repeated messages are de-duplicated.",
        {
            "start": _ts("Window start"),
            "end": _ts("Window end"),
            "service": SERVICE,
            "severity": {"type": "string", "enum": ["ERROR", "WARN", "INFO"]},
            "contains": {"type": "string", "description": "Case-insensitive text to match"},
            "trace_id": {"type": "string", "description": "Only logs of this trace"},
            "limit": LIMIT,
            "cursor": CURSOR,
        },
        ["start", "end"],
    ),
    _tool(
        "get_dependencies",
        "Observed caller-to-callee edges with call counts and error rates, inferred from traces.",
        {"start": _ts("Window start"), "end": _ts("Window end")},
        ["start", "end"],
    ),
    _tool(
        "check_coverage",
        "Report trace sampling rate, metric gaps and unusual log volume in a window.",
        {"start": _ts("Window start"), "end": _ts("Window end"), "service": SERVICE},
        ["start", "end"],
    ),
]
