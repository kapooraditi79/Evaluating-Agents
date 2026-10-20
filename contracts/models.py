"""Strict public/private models. Diagnosis labels describe behavior, not injections."""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from pathlib import Path
from typing import Annotated, Any, Literal, Self

from pydantic import BaseModel, Field, model_validator

SCHEMA_VERSION = "0.1.0"
TOOL_VERSION = "0.1.1"
Hex16 = Annotated[str, Field(pattern=r"^[0-9a-f]{16}$")]
Hex32 = Annotated[str, Field(pattern=r"^[0-9a-f]{32}$")]
EPOCH = datetime(1970, 1, 1, tzinfo=UTC)


def utc_ns(value: str) -> int:
    """Parse explicit UTC with up to nine fractional digits and no float rounding."""
    match = re.fullmatch(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})(?:\.(\d{1,9}))?Z", value)
    if match is None:
        raise ValueError("timestamp must be ISO-8601 UTC with Z")
    delta = datetime.fromisoformat(match[1] + "+00:00") - EPOCH
    fraction = int((match[2] or "").ljust(9, "0"))
    return (delta.days * 86400 + delta.seconds) * 1_000_000_000 + fraction


def iso_time(ns: int) -> str:
    seconds, fraction = divmod(ns, 1_000_000_000)
    base = (EPOCH + timedelta(seconds=seconds)).strftime("%Y-%m-%dT%H:%M:%S")
    return base + (f".{fraction:09d}".rstrip("0") if fraction else "") + "Z"


class Contract(BaseModel):
    model_config = {"extra": "forbid", "allow_inf_nan": False}


class Window(Contract):
    start: str
    end: str

    @model_validator(mode="after")
    def ordered(self) -> Self:
        if utc_ns(self.start) >= utc_ns(self.end):
            raise ValueError("start must precede end")
        return self


class Source(Contract):
    type: Literal["parquet"] = "parquet"
    path: Literal["."] = "."


class Manifest(Contract):
    schema_version: Literal["0.1.0"] = SCHEMA_VERSION
    id: str = Field(pattern=r"^[0-9a-f]{16,64}$")
    question: str
    data_range: Window
    reference_time: str
    source: Source = Field(default_factory=Source)
    bucket_seconds: int = Field(default=10, gt=0)
    trace_sampling_rate: float = Field(default=1, gt=0, le=1)

    @model_validator(mode="after")
    def timing(self) -> Self:
        if (
            not utc_ns(self.data_range.start)
            <= utc_ns(self.reference_time)
            < utc_ns(self.data_range.end)
        ):
            raise ValueError("reference_time must lie within data_range")
        bucket_ns = self.bucket_seconds * 1_000_000_000
        if utc_ns(self.data_range.start) % bucket_ns or utc_ns(self.data_range.end) % bucket_ns:
            raise ValueError("data_range must align to native metric buckets")
        return self


class Diagnosis(StrEnum):
    SLOW_DEPENDENCY = "slow_dependency"
    ELEVATED_ERRORS = "elevated_errors"
    RESOURCE_SATURATION = "resource_saturation"
    MEMORY_LEAK_RESTARTS = "memory_leak_restarts"
    DEPENDENCY_UNAVAILABLE = "dependency_unavailable"
    BAD_RELEASE = "bad_release"
    RETRY_AMPLIFICATION = "retry_amplification"
    QUERY_AMPLIFICATION = "query_amplification"
    UNKNOWN = "unknown"


class Scope(Contract):
    kind: Literal["all", "region", "version", "endpoint"] = "all"
    value: str | None = None

    @model_validator(mode="after")
    def has_value(self) -> Self:
        if (self.kind == "all") != (self.value is None):
            raise ValueError("scope value required exactly when kind is not all")
        return self


class Cause(Contract):
    service: str
    fault_type: Diagnosis
    role: Literal["primary", "trigger"] = "primary"
    propagation_path: list[str] = Field(min_length=1)
    onset_time: str
    end_time: str | None = None
    scope: Scope = Field(default_factory=Scope)
    injection_mechanism: str | None = None  # PRIVATE, never in agent inputs

    @model_validator(mode="after")
    def consistency(self) -> Self:
        onset = utc_ns(self.onset_time)
        if self.end_time is not None and utc_ns(self.end_time) <= onset:
            raise ValueError("cause end must follow onset")
        if self.propagation_path[0] != self.service:
            raise ValueError("propagation_path begins with cause service")
        return self


class GroundTruth(Contract):
    schema_version: Literal["0.1.0"] = SCHEMA_VERSION
    id: str
    root_causes: list[Cause]
    no_fault: bool
    affected_services: list[str] = Field(default_factory=list)
    symptom: dict[str, str]
    decoys: list[dict[str, Any]] = Field(default_factory=list)
    degradations: list[str] = Field(default_factory=list)
    features: list[str] = Field(default_factory=list)
    tier: Literal["easy", "hard"] = "easy"
    generator_version: str = SCHEMA_VERSION
    seed: int

    @model_validator(mode="after")
    def causes_match(self) -> Self:
        if self.no_fault != (not self.root_causes):
            raise ValueError("no_fault iff root_causes is empty")
        if self.root_causes and not any(c.role == "primary" for c in self.root_causes):
            raise ValueError("a trigger requires a primary cause")
        return self


class Span(Contract):
    trace_id: Hex32
    span_id: Hex16
    parent_span_id: Hex16 | None
    service: str
    operation: str
    start_ns: int = Field(ge=0)
    end_ns: int = Field(ge=0)
    duration_ms: float = Field(ge=0)
    status: Literal["OK", "ERROR"]
    status_message: str
    attributes: dict[str, Any]

    @model_validator(mode="after")
    def timing(self) -> Self:
        if self.end_ns < self.start_ns:
            raise ValueError("negative duration")
        if abs(self.duration_ms - (self.end_ns - self.start_ns) / 1e6) > 1e-6:
            raise ValueError("duration does not match timestamps")
        if not {"service.version", "app.region"} <= self.attributes.keys():
            raise ValueError("version and region required")
        return self


class Log(Contract):
    ts_ns: int = Field(ge=0)
    service: str
    severity: Literal["INFO", "WARN", "ERROR"]
    body: str
    trace_id: Hex32 | None = None
    span_id: Hex16 | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)


MetricName = Literal[
    "request_count",
    "error_count",
    "latency_p50_ms",
    "latency_p95_ms",
    "latency_p99_ms",
    "cpu_utilization",
    "memory_mb",
]


class Metric(Contract):
    ts_ns: int = Field(ge=0)
    service: str
    operation: str | None
    metric: MetricName
    value: float | None
    unit: str
    max_value: float | None = None  # gauge maximum; value is native-bucket average

    @model_validator(mode="after")
    def semantics(self) -> Self:
        latency = self.metric.startswith("latency_")
        gauge = self.metric in {"cpu_utilization", "memory_mb"}
        if self.value is None and not latency:
            raise ValueError("only empty or unbounded latency estimates may be null")
        if self.value is not None and self.value < 0:
            raise ValueError("metric values must be nonnegative")
        if self.metric in {"request_count", "error_count"} and not self.value.is_integer():
            raise ValueError("counts must be whole numbers")
        expected_unit = (
            "ms"
            if latency
            else (
                "ratio"
                if self.metric == "cpu_utilization"
                else "MB"
                if self.metric == "memory_mb"
                else "requests"
            )
        )
        if self.unit != expected_unit:
            raise ValueError("unit does not match metric")
        if gauge:
            if self.operation is not None or self.max_value is None or self.max_value < self.value:
                raise ValueError("gauges require no operation and a maximum >= average")
            if self.metric == "cpu_utilization" and self.max_value > 1:
                raise ValueError("CPU ratio must lie in [0,1]")
        elif self.max_value is not None or self.operation is None:
            raise ValueError("handler metrics require an operation and no gauge maximum")
        return self


class Histogram(Contract):
    ts_ns: int = Field(ge=0)
    service: str
    operation: str
    bounds_ms: list[float]
    counts: list[int]

    @model_validator(mode="after")
    def valid_bins(self) -> Self:
        if not self.bounds_ms or self.bounds_ms[0] <= 0:
            raise ValueError("positive finite bounds required")
        if any(b <= a for a, b in zip(self.bounds_ms, self.bounds_ms[1:], strict=False)):
            raise ValueError("bounds must increase")
        if len(self.counts) != len(self.bounds_ms) + 1 or any(n < 0 for n in self.counts):
            raise ValueError("counts must have len(bounds)+1 nonnegative entries")
        return self


class TableData(Contract):
    columns: list[str]
    rows: list[list[Any]]

    @model_validator(mode="after")
    def rectangular(self) -> Self:
        if len(set(self.columns)) != len(self.columns):
            raise ValueError("columns must be unique")
        if any(len(row) != len(self.columns) for row in self.rows):
            raise ValueError("row width must match columns")
        return self


class WarningItem(Contract):
    code: str
    message: str


class ToolSource(Contract):
    backend: Literal["parquet"] = "parquet"
    dataset_id: str
    tool_version: str = TOOL_VERSION


class ToolResult(Contract):
    data: TableData
    total_matches: int = Field(ge=0)
    returned: int = Field(ge=0)
    truncated: bool
    next_cursor: str | None
    query_id: str
    source: ToolSource
    warnings: list[WarningItem] = Field(default_factory=list)

    @model_validator(mode="after")
    def consistent(self) -> Self:
        if self.returned != len(self.data.rows) or self.returned > self.total_matches:
            raise ValueError("result counts do not match rows")
        if self.truncated != (self.next_cursor is not None):
            raise ValueError("truncated results require a continuation cursor")
        if not self.data.columns or self.data.columns[0] != "handle":
            raise ValueError("first column must be handle")
        if len({row[0] for row in self.data.rows}) != self.returned:
            raise ValueError("handles must be unique")
        return self


class ToolError(Contract):
    error: dict[str, str]


def export_schemas(destination: Path) -> None:
    from contracts.queries import QUERY_MODELS

    destination.mkdir(parents=True, exist_ok=True)
    for model in (Manifest, GroundTruth, Span, Log, Metric, Histogram, ToolResult, ToolError):
        (destination / f"{model.__name__}.json").write_text(
            json.dumps(model.model_json_schema(), indent=2) + "\n", encoding="utf-8"
        )
    for name, model in QUERY_MODELS.items():
        (destination / f"{name}.json").write_text(
            json.dumps(model.model_json_schema(), indent=2) + "\n", encoding="utf-8"
        )
    (destination / "Diagnosis.json").write_text(
        json.dumps({"type": "string", "enum": [d.value for d in Diagnosis]}, indent=2) + "\n",
        encoding="utf-8",
    )
