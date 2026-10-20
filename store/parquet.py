"""Fixed-file public dataset reader. No user-provided paths or backend query language."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

import pyarrow as pa
import pyarrow.parquet as pq
from pydantic import ValidationError

from contracts.models import Histogram, Log, Manifest, Metric, Span, Window, utc_ns
from contracts.queries import Query
from telemetry.boundaries import in_reserved_store
from telemetry.histograms import histogram, percentile
from telemetry.identity import dataset_identity

NS = 1_000_000_000


class QueryError(Exception):
    def __init__(self, code: str, message: str):
        self.code, self.message = code, message
        super().__init__(message)


class ParquetStore:
    def __init__(self, public_directory: Path):
        original = public_directory.absolute()
        if in_reserved_store(original):
            raise QueryError("INVALID_DATASET", "shop datasets cannot be inside runs/ or private/")
        if any(p.is_symlink() or p.is_junction() for p in (original, *original.parents)):
            raise QueryError("INVALID_DATASET", "linked dataset directories are unsupported")
        root = original.resolve()
        if in_reserved_store(root) or root.parent.name != "public":
            raise QueryError("INVALID_DATASET", "select a public/<dataset_id> shop dataset")
        self.tables: dict[str, list[dict[str, Any]]] = {}
        try:
            manifest_file = root / "manifest.json"
            if manifest_file.is_symlink() or manifest_file.is_junction():
                raise ValueError("linked manifest")
            self.manifest = Manifest.model_validate_json(manifest_file.read_text(encoding="utf-8"))
            if root.name != self.manifest.id or root.parent.name != "public":
                raise ValueError("dataset must be a public/<dataset_id> directory")
            for name, model in (
                ("spans", Span),
                ("logs", Log),
                ("metrics", Metric),
                ("histograms", Histogram),
            ):
                path = root / f"{name}.parquet"
                if path.is_symlink() or path.is_junction() or path.resolve().parent != root:
                    raise ValueError("linked telemetry file")
                rows = pq.read_table(path).to_pylist()
                for row in rows:
                    if "attributes" in row:
                        row["attributes"] = json.loads(row["attributes"])
                self.tables[name] = [model.model_validate(row).model_dump() for row in rows]
        except (OSError, ValueError, ValidationError, pa.ArrowException) as exc:
            raise QueryError("INVALID_DATASET", "public dataset is missing or invalid") from exc
        if (
            dataset_identity(self.tables, self.manifest.model_dump(exclude={"id"}))
            != self.manifest.id
        ):
            raise QueryError(
                "INVALID_DATASET", "public dataset content does not match its identity"
            )
        self.services = sorted({r["service"] for rows in self.tables.values() for r in rows})
        self.operations: dict[str, set[str]] = defaultdict(set)
        for rows in self.tables.values():
            for row in rows:
                if row.get("operation") is not None:
                    self.operations[row["service"]].add(row["operation"])
        self._validate_relations()

    def _validate_relations(self) -> None:
        """Reject impossible or ambiguous records, while allowing explicit missing rows."""
        for table in ("metrics", "histograms"):
            seen = set()
            for row in self.tables[table]:
                key = (row["ts_ns"], row["service"], row["operation"], row.get("metric"))
                if key in seen:
                    raise QueryError("INVALID_DATASET", "duplicate metric or histogram key")
                seen.add(key)
                if row["ts_ns"] % (self.manifest.bucket_seconds * NS) or not utc_ns(
                    self.manifest.data_range.start
                ) <= row["ts_ns"] < utc_ns(self.manifest.data_range.end):
                    raise QueryError(
                        "INVALID_DATASET", "bucket lies off-grid or outside data range"
                    )
        counts = {
            (r["ts_ns"], r["service"], r["operation"], r["metric"]): r["value"]
            for r in self.tables["metrics"]
            if r["metric"] in {"request_count", "error_count"}
        }
        for key, value in counts.items():
            request_key = (*key[:3], "request_count")
            if key[3] == "error_count" and request_key in counts and value > counts[request_key]:
                raise QueryError("INVALID_DATASET", "errors exceed requests")
        bounds = None
        for row in self.tables["histograms"]:
            if bounds is not None and row["bounds_ms"] != bounds:
                raise QueryError("INVALID_DATASET", "histogram bounds differ")
            bounds = row["bounds_ms"]
            request_key = (row["ts_ns"], row["service"], row["operation"], "request_count")
            if request_key in counts and sum(row["counts"]) != counts[request_key]:
                raise QueryError(
                    "INVALID_DATASET", "histogram population differs from request count"
                )
        seen_spans = set()
        for row in self.tables["spans"]:
            key = (row["trace_id"], row["span_id"])
            if key in seen_spans:
                raise QueryError("INVALID_DATASET", "duplicate span identifier")
            seen_spans.add(key)

    def _window(self, window: Window, aligned: bool = False) -> tuple[int, int]:
        start, end = utc_ns(window.start), utc_ns(window.end)
        if start < utc_ns(self.manifest.data_range.start) or end > utc_ns(
            self.manifest.data_range.end
        ):
            raise QueryError("INVALID_WINDOW", "window falls outside available data")
        native = self.manifest.bucket_seconds * NS
        if aligned and (start % native or end % native):
            raise QueryError("UNALIGNED_WINDOW", "metric windows must align to native buckets")
        return start, end

    def _spans(self, window: Window) -> list[dict[str, Any]]:
        start, end = self._window(window)
        return [r for r in self.tables["spans"] if start <= r["start_ns"] < end]

    def _gaps(
        self,
        service: str,
        operation: str | None,
        start: int,
        end: int,
        metric: str = "request_count",
    ) -> bool:
        return bool(self._missing_buckets(service, operation, start, end, metric))

    def _missing_buckets(
        self, service: str, operation: str | None, start: int, end: int, metric: str | None = None
    ) -> int:
        metrics = {
            (r["ts_ns"], r["operation"], r["metric"])
            for r in self.tables["metrics"]
            if r["service"] == service
        }
        histograms = {
            (r["ts_ns"], r["operation"])
            for r in self.tables["histograms"]
            if r["service"] == service
        }
        operations = [operation] if operation is not None else sorted(self.operations[service])
        handler_metrics = (
            "request_count",
            "error_count",
            "latency_p50_ms",
            "latency_p95_ms",
            "latency_p99_ms",
        )
        required = (
            handler_metrics
            if metric is None
            else ("request_count", "error_count")
            if metric == "error_rate"
            else ("request_count",)
            if metric.startswith("latency_")
            else (metric,)
        )
        missing = 0
        for timestamp in range(start, end, self.manifest.bucket_seconds * NS):
            absent = False
            if metric is None or metric in {"cpu_utilization", "memory_mb"}:
                gauges = ("cpu_utilization", "memory_mb") if metric is None else (metric,)
                absent = any((timestamp, None, gauge) not in metrics for gauge in gauges)
            if metric not in {"cpu_utilization", "memory_mb"}:
                absent |= not operations or any(
                    (timestamp, op, name) not in metrics for op in operations for name in required
                )
                if metric is None or metric.startswith("latency_"):
                    absent |= any((timestamp, op) not in histograms for op in operations)
            missing += absent
        return missing

    def _metric_value(
        self,
        service: str,
        metric: str,
        operation: str | None,
        start: int,
        end: int,
        aggregation: str,
    ) -> tuple[float | None, float | None]:
        rows = [
            r
            for r in self.tables["metrics"]
            if r["service"] == service
            and start <= r["ts_ns"] < end
            and (operation is None or r["operation"] == operation)
        ]
        if metric.startswith("latency_"):
            hist = [
                h
                for h in self.tables["histograms"]
                if h["service"] == service
                and start <= h["ts_ns"] < end
                and (operation is None or h["operation"] == operation)
            ]
            if not hist:
                return None, None
            bounds = hist[0]["bounds_ms"]
            if any(h["bounds_ms"] != bounds for h in hist):
                raise QueryError("INVALID_DATASET", "histogram bounds differ")
            counts = [sum(h["counts"][i] for h in hist) for i in range(len(bounds) + 1)]
            q = {"latency_p50_ms": 0.5, "latency_p95_ms": 0.95, "latency_p99_ms": 0.99}[metric]
            return percentile(counts, bounds, q)
        if metric == "error_rate":
            request_points = {
                (r["ts_ns"], r["operation"]): r["value"]
                for r in rows
                if r["metric"] == "request_count"
            }
            error_points = {
                (r["ts_ns"], r["operation"]): r["value"]
                for r in rows
                if r["metric"] == "error_count"
            }
            paired = request_points.keys() & error_points.keys()
            requests = [request_points[key] for key in sorted(paired)]
            errors = [error_points[key] for key in sorted(paired)]
            if not requests or not errors or sum(requests) == 0:
                return None, None
            return sum(errors) / sum(requests), None
        values = [r for r in rows if r["metric"] == metric]
        if not values:
            return None, None
        if metric in {"request_count", "error_count"}:
            return sum(r["value"] for r in values), None
        if aggregation == "max":
            return max(r["max_value"] for r in values), None
        return sum(r["value"] for r in values) / len(values), None

    def query(
        self, tool: str, args: Query
    ) -> tuple[list[str], list[list[Any]], list[dict[str, str]]]:
        start, end = self._window(args.window)
        service = getattr(args, "service", None)
        if service is not None and service not in self.services:
            raise QueryError("UNKNOWN_SERVICE", "service is not present in this dataset")
        warnings: list[dict[str, str]] = []
        if (
            tool in {"find_traces", "get_trace", "get_dependencies", "breakdown"}
            and self.manifest.trace_sampling_rate < 1
        ):
            warnings.append(
                {"code": "SAMPLED_TRACES", "message": "span statistics use retained traces only"}
            )
        if tool == "list_services":
            columns = ["service", "span_count", "log_count", "metric_points"]
            rows = [
                [
                    s,
                    sum(r["service"] == s for r in self._spans(args.window)),
                    sum(
                        r["service"] == s and start <= r["ts_ns"] < end for r in self.tables["logs"]
                    ),
                    sum(
                        r["service"] == s and start <= r["ts_ns"] < end
                        for r in self.tables["metrics"]
                    ),
                ]
                for s in self.services
            ]
        elif tool in {"query_metric", "compare_windows"}:
            start, end = self._window(args.window, aligned=True)
            step = args.step_seconds * NS
            if args.step_seconds % self.manifest.bucket_seconds:
                raise QueryError("INVALID_STEP", "step must be a multiple of native bucket width")
            if args.operation is not None and args.operation not in self.operations[service]:
                raise QueryError("UNKNOWN_OPERATION", "operation is not present for service")
            if args.metric in {"cpu_utilization", "memory_mb"} and args.operation:
                raise QueryError("INVALID_ARGUMENT", "resource gauges do not have an operation")
            gap_metric = args.metric
            if self._gaps(service, args.operation, start, end, gap_metric):
                warnings.append(
                    {"code": "METRIC_GAP", "message": "one or more native buckets are missing"}
                )
            columns = ["kind", "start_ns", "end_ns", "value", "absolute_error_bound", "unit"]
            unit = (
                "ms"
                if args.metric.startswith("latency")
                else (
                    "MB"
                    if args.metric == "memory_mb"
                    else "ratio"
                    if args.metric in {"error_rate", "cpu_utilization"}
                    else "requests"
                )
            )

            def point(kind: str, left: int, right: int) -> list[Any]:
                value, error_bound = self._metric_value(
                    service, args.metric, args.operation, left, right, args.aggregation
                )
                return [kind, left, right, value, error_bound, unit]

            rows = [point("summary", start, end)]
            if tool == "compare_windows":
                left, right = self._window(args.baseline_window, aligned=True)
                if self._gaps(service, args.operation, left, right, gap_metric):
                    warnings.append(
                        {"code": "METRIC_GAP", "message": "baseline contains missing buckets"}
                    )
                rows.append(point("baseline", left, right))
            else:
                cursor = start
                while cursor < end:
                    right = min((cursor // step + 1) * step, end)
                    rows.append(point("bucket", cursor, right))
                    cursor = right
            if args.metric.startswith("latency") and any(r[3] is None for r in rows):
                warnings.append(
                    {
                        "code": "NO_FINITE_PERCENTILE",
                        "message": "empty data or overflow bin; value is null",
                    }
                )
        elif tool == "find_traces":
            if set(args.attributes) - {"service.version", "app.region"}:
                raise QueryError(
                    "INVALID_ATTRIBUTE", "only version and region filters are supported"
                )
            selected = [
                r
                for r in self._spans(args.window)
                if (service is None or r["service"] == service)
                and (args.operation is None or r["operation"] == args.operation)
                and (args.status is None or r["status"] == args.status)
                and r["duration_ms"] >= args.min_duration_ms
                and all(r["attributes"].get(k) == v for k, v in args.attributes.items())
            ]
            grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
            for row in selected:
                grouped[row["trace_id"]].append(row)
            ordered = sorted(
                grouped.items(), key=lambda pair: (min(r["start_ns"] for r in pair[1]), pair[0])
            )
            columns = [
                "trace_id",
                "matching_service",
                "matching_start_ns",
                "max_matching_duration_ms",
                "status",
                "matching_status",
            ]
            root_status = {
                r["trace_id"]: r["status"]
                for r in self.tables["spans"]
                if r["parent_span_id"] is None
            }
            if any(tid not in root_status for tid in grouped):
                warnings.append(
                    {
                        "code": "INCOMPLETE_TRACE",
                        "message": "trace root missing; request status is UNKNOWN",
                    }
                )
            rows = [
                [
                    tid,
                    items[0]["service"],
                    min(r["start_ns"] for r in items),
                    max(r["duration_ms"] for r in items),
                    root_status.get(tid, "UNKNOWN"),
                    "ERROR" if any(r["status"] == "ERROR" for r in items) else "OK",
                ]
                for tid, items in ordered
            ]
        elif tool == "get_trace":
            # A trace matches if any span starts in the window; return its entire tree.
            matching = {r["trace_id"] for r in self._spans(args.window)}
            selected = (
                [r for r in self.tables["spans"] if r["trace_id"] == args.trace_id]
                if args.trace_id in matching
                else []
            )
            selected.sort(key=lambda r: (r["start_ns"], r["span_id"]))
            columns = [
                "trace_id",
                "span_id",
                "parent_span_id",
                "service",
                "operation",
                "start_ns",
                "duration_ms",
                "status",
                "status_message",
                "attributes",
            ]
            rows = [[r[c] for c in columns] for r in selected]
        elif tool == "search_logs":
            selected = [
                r
                for r in self.tables["logs"]
                if start <= r["ts_ns"] < end
                and (service is None or r["service"] == service)
                and (args.severity is None or r["severity"] == args.severity)
                and (args.contains is None or args.contains.casefold() in r["body"].casefold())
                and (args.trace_id is None or r["trace_id"] == args.trace_id)
            ]
            # Collapse exact duplicates, preserving their counts and trace links.
            unique: dict[str, tuple[dict[str, Any], int]] = {}
            for row in selected:
                key = json.dumps(row, sort_keys=True)
                old = unique.get(key)
                unique[key] = (row, old[1] + 1 if old else 1)
            ordered = sorted(
                unique.values(),
                key=lambda p: (p[0]["ts_ns"], p[0]["service"], p[0]["span_id"] or "", p[0]["body"]),
            )
            columns = ["ts_ns", "service", "severity", "body", "trace_id", "span_id", "count"]
            rows = [[r[c] for c in columns[:-1]] + [count] for r, count in ordered]
        elif tool == "get_dependencies":
            spans = self._spans(args.window)
            by_id = {(r["trace_id"], r["span_id"]): r for r in self.tables["spans"]}
            counts: dict[tuple[str, str], int] = defaultdict(int)
            for row in spans:
                parent = by_id.get((row["trace_id"], row["parent_span_id"]))
                if parent:
                    counts[parent["service"], row["service"]] += 1
            columns = ["caller", "callee", "observed_calls", "calls_per_second"]
            rows = [
                [a, b, count, count / ((end - start) / NS)]
                for (a, b), count in sorted(counts.items())
            ]
        elif tool == "check_coverage":
            start, end = self._window(args.window, aligned=True)
            columns = ["service", "trace_sampling_rate", "missing_metric_buckets", "retained_logs"]
            rows = []
            for s in [service] if service else self.services:
                missing = self._missing_buckets(s, None, start, end)
                rows.append(
                    [
                        s,
                        self.manifest.trace_sampling_rate,
                        missing,
                        sum(
                            r["service"] == s and start <= r["ts_ns"] < end
                            for r in self.tables["logs"]
                        ),
                    ]
                )
            if any(row[2] for row in rows):
                warnings.append(
                    {
                        "code": "METRIC_GAP",
                        "message": "required telemetry cells are missing; see per-service counts",
                    }
                )
            if self.manifest.trace_sampling_rate < 1:
                warnings.append(
                    {"code": "SAMPLED_TRACES", "message": "trace retention is below 100 percent"}
                )
            warnings.append(
                {
                    "code": "LOG_COVERAGE_UNKNOWN",
                    "message": "log counts alone cannot establish log loss",
                }
            )
        elif tool == "breakdown":
            groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
            for row in self._spans(args.window):
                key = (
                    row[args.group_by]
                    if args.group_by in {"service", "operation", "status"}
                    else row["attributes"][
                        "service.version" if args.group_by == "version" else "app.region"
                    ]
                )
                groups[key].append(row)
            columns = [args.group_by, "value", "absolute_error_bound"]
            rows = []
            if args.metric == "latency_p95_ms" and not self.tables["histograms"]:
                raise QueryError("MISSING_HISTOGRAMS", "latency bin bounds are unavailable")
            bounds = self.tables["histograms"][0]["bounds_ms"] if self.tables["histograms"] else []
            for key, items in sorted(groups.items()):
                value, error_bound = len(items), None
                if args.metric == "error_count":
                    value = sum(r["status"] == "ERROR" for r in items)
                elif args.metric == "latency_p95_ms":
                    value, error_bound = percentile(
                        histogram([r["duration_ms"] for r in items], bounds), bounds, 0.95
                    )
                rows.append([key, value, error_bound])
            warnings.append(
                {
                    "code": "SPAN_STATISTICS",
                    "message": "breakdown counts handler spans, not user requests",
                }
            )
        else:
            raise QueryError("UNKNOWN_TOOL", "tool is not available")
        return columns, rows, warnings
