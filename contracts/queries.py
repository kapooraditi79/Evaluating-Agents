"""Tool argument schemas; every data query has an explicit half-open UTC window."""

from typing import Literal

from pydantic import Field

from contracts.models import Contract, Hex32, Window


class Query(Contract):
    window: Window
    limit: int = Field(default=20, ge=1, le=100, strict=True)
    cursor: str | None = None


class ListServices(Query):
    pass


class QueryMetric(Query):
    service: str
    metric: Literal[
        "request_count",
        "error_count",
        "error_rate",
        "latency_p50_ms",
        "latency_p95_ms",
        "latency_p99_ms",
        "cpu_utilization",
        "memory_mb",
    ]
    operation: str | None = None
    step_seconds: int = Field(default=60, gt=0, le=86400, strict=True)
    aggregation: Literal["avg", "max"] = "avg"


class FindTraces(Query):
    service: str | None = None
    operation: str | None = None
    status: Literal["OK", "ERROR"] | None = None
    min_duration_ms: float = Field(default=0.0, ge=0, allow_inf_nan=False, strict=True)
    attributes: dict[str, str] = Field(default_factory=dict)


class GetTrace(Query):
    trace_id: Hex32


class SearchLogs(Query):
    service: str | None = None
    severity: Literal["INFO", "WARN", "ERROR"] | None = None
    contains: str | None = Field(default=None, max_length=200)
    trace_id: Hex32 | None = None


class Coverage(Query):
    service: str | None = None

 
class Dependencies(Query):
    pass


class CompareWindows(QueryMetric):
    baseline_window: Window


class Breakdown(Query):
    group_by: Literal["service", "operation", "status", "version", "region"]
    metric: Literal["request_count", "error_count", "latency_p95_ms"] = "request_count"


QUERY_MODELS = {
    "list_services": ListServices,
    "query_metric": QueryMetric,
    "find_traces": FindTraces,
    "get_trace": GetTrace,
    "search_logs": SearchLogs,
    "check_coverage": Coverage,
    "get_dependencies": Dependencies,
    "compare_windows": CompareWindows,
    "breakdown": Breakdown,
}
