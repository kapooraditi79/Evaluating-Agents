"""Independent regressions found by auditing the first Person A implementation."""

import json

import pyarrow as pa
import pyarrow.parquet as pq
import pytest
from opentelemetry.sdk.trace import TracerProvider
from pydantic import ValidationError

from contracts.models import Metric, iso_time, utc_ns
from mcp_servers.telemetry.engine import ToolEngine
from store import ParquetStore
from telemetry.config import Fault
from telemetry.generator import generate, write_table
from telemetry.histograms import histogram, percentile
from telemetry.identity import dataset_identity
from telemetry.leakage import audit_public


def rewrite(bundle, destination, transform):
    original = ParquetStore(bundle.public)
    tables = original.tables
    transform(tables)
    metadata = original.manifest.model_dump(exclude={"id"})
    identity = dataset_identity(tables, metadata)
    public = destination / "public" / identity
    public.mkdir(parents=True)
    for kind, rows in tables.items():
        write_table(public / f"{kind}.parquet", rows, kind)
    (public / "manifest.json").write_text(json.dumps({**metadata, "id": identity}))
    return ParquetStore(public)


@pytest.mark.parametrize(
    "metric,value,unit,maximum",
    [
        ("request_count", -1, "requests", None),
        ("request_count", 1.5, "requests", None),
        ("error_count", None, "requests", None),
        ("cpu_utilization", 1.5, "ratio", 1.5),
        ("memory_mb", 200, "MB", 100),
    ],
)
def test_invalid_metric_values_rejected(metric, value, unit, maximum):
    with pytest.raises(ValidationError):
        Metric(
            ts_ns=0,
            service="payment",
            operation=None,
            metric=metric,
            value=value,
            unit=unit,
            max_value=maximum,
        )


@pytest.mark.parametrize("q", [0, -0.1, 1.1])
def test_invalid_percentile_quantile(q):
    with pytest.raises(ValueError):
        percentile([1, 0], [10.0], q)


def test_negative_histogram_duration_rejected():
    with pytest.raises(ValueError):
        histogram([-5.0], [10.0])


def test_generation_ignores_ambient_trace_context(tmp_path, config):
    plain = generate(tmp_path / "plain", seed=9, environment=config)
    provider = TracerProvider(shutdown_on_exit=False)
    try:
        with provider.get_tracer("outer").start_as_current_span("unrelated-development-work"):
            nested = generate(tmp_path / "nested", seed=9, environment=config)
    finally:
        provider.shutdown()
    assert nested.manifest.id == plain.manifest.id


def test_fractional_fault_timing_is_preserved(tmp_path, config):
    fault = Fault(service="payment", mechanism="latency", onset_fraction=0.451, end_fraction=0.901)
    bundle = generate(tmp_path, environment=config, faults=[fault])
    cause = bundle.truth.root_causes[0]
    start = utc_ns(config.start)
    assert cause.onset_time == iso_time(start + 81_180_000_000)
    assert cause.end_time == iso_time(start + 162_180_000_000)


def test_failed_handler_does_not_execute_children(tmp_path, config):
    bundle = generate(
        tmp_path, environment=config, faults=[Fault(service="checkout", mechanism="errors")]
    )
    spans = ParquetStore(bundle.public).tables["spans"]
    failing = [r for r in spans if r["service"] == "checkout" and r["status"] == "ERROR"]
    assert failing
    for parent in failing:
        assert parent["duration_ms"] == 2
        assert not any(r["parent_span_id"] == parent["span_id"] for r in spans)


def test_unrelated_errors_are_decoys_not_checkout_causes(tmp_path, config):
    bundle = generate(
        tmp_path, environment=config, faults=[Fault(service="email", mechanism="errors")]
    )
    assert bundle.truth.no_fault
    assert not bundle.truth.root_causes
    assert any(d["service"] == "email" for d in bundle.truth.decoys)


def test_retry_policy_alone_is_harmless(tmp_path, config):
    healthy = generate(tmp_path / "healthy", seed=11, environment=config)
    retry_only = generate(
        tmp_path / "retry",
        seed=11,
        environment=config,
        faults=[Fault(service="checkout", mechanism="retries")],
    )
    assert retry_only.truth.no_fault
    assert healthy.manifest.id == retry_only.manifest.id


def test_regional_resource_gauge_is_not_global_saturation(tmp_path, config):
    global_case = generate(
        tmp_path / "all",
        environment=config,
        faults=[Fault(service="payment", mechanism="cpu_saturation")],
    )
    regional = generate(
        tmp_path / "east",
        environment=config,
        faults=[Fault(service="payment", mechanism="cpu_saturation", region="east")],
    )

    def peak(bundle):
        return max(
            r["value"]
            for r in ParquetStore(bundle.public).tables["metrics"]
            if r["service"] == "payment" and r["metric"] == "cpu_utilization"
        )

    assert 0.25 < peak(regional) < peak(global_case)


def test_missing_error_counts_warn_and_use_paired_observations(bundles, tmp_path):
    def remove(tables):
        target = next(
            r
            for r in tables["metrics"]
            if r["service"] == "payment" and r["metric"] == "error_count" and r["value"] > 0
        )
        tables["metrics"].remove(target)

    store = rewrite(bundles["errors"], tmp_path, remove)
    result = ToolEngine(store).call(
        "query_metric",
        {
            "window": store.manifest.data_range.model_dump(),
            "service": "payment",
            "metric": "error_rate",
        },
    )
    assert any(w["code"] == "METRIC_GAP" for w in result["warnings"])
    points = {
        (r["ts_ns"], r["metric"]): r["value"]
        for r in store.tables["metrics"]
        if r["service"] == "payment"
    }
    paired = [
        t for t, metric in points if metric == "request_count" and (t, "error_count") in points
    ]
    expected = sum(points[t, "error_count"] for t in paired) / sum(
        points[t, "request_count"] for t in paired
    )
    value_index = result["data"]["columns"].index("value")
    assert result["data"]["rows"][0][value_index] == expected
    coverage = ToolEngine(store).call(
        "check_coverage", {"window": store.manifest.data_range.model_dump(), "service": "payment"}
    )
    missing_index = coverage["data"]["columns"].index("missing_metric_buckets")
    assert coverage["data"]["rows"][0][missing_index] == 1


@pytest.mark.parametrize("table", ["metrics", "histograms"])
def test_partial_operation_gaps_are_not_masked_by_other_operations(bundles, tmp_path, table):
    def remove(tables):
        target = next(
            r
            for r in tables[table]
            if r["service"] == "frontend"
            and r["operation"] == "POST /checkout"
            and (table == "histograms" or r["metric"] == "request_count")
        )
        tables[table].remove(target)

    store = rewrite(bundles["healthy"], tmp_path, remove)
    metric = "latency_p95_ms" if table == "histograms" else "request_count"
    result = ToolEngine(store).call(
        "query_metric",
        {"window": store.manifest.data_range.model_dump(), "service": "frontend", "metric": metric},
    )
    assert any(w["code"] == "METRIC_GAP" for w in result["warnings"])


def test_service_discovery_survives_total_metric_loss(bundles, tmp_path):
    def remove(tables):
        tables["metrics"] = [r for r in tables["metrics"] if r["service"] != "payment"]

    store = rewrite(bundles["healthy"], tmp_path, remove)
    result = ToolEngine(store).call(
        "query_metric",
        {
            "window": store.manifest.data_range.model_dump(),
            "service": "payment",
            "metric": "request_count",
        },
    )
    assert "error" not in result
    assert any(w["code"] == "METRIC_GAP" for w in result["warnings"])


def test_leakage_audit_decodes_json_escapes_and_arrow_field_metadata(tmp_path):
    (tmp_path / "manifest.json").write_text('{"question":"\\u0073eed"}')
    assert audit_public(tmp_path)
    (tmp_path / "manifest.json").write_text("{}")
    field = pa.field("body", pa.string(), metadata={b"note": b"ground truth"})
    pq.write_table(
        pa.Table.from_pylist([{"body": "ordinary message"}], schema=pa.schema([field])),
        tmp_path / "logs.parquet",
    )
    assert any("metadata" in item for item in audit_public(tmp_path))


def test_backend_failure_is_not_an_argument_error(engine):
    def broken(tool, args):
        raise RuntimeError("backend unavailable")

    engine.store.query = broken
    result = engine.call("list_services", {"window": engine.store.manifest.data_range.model_dump()})
    assert result["error"]["code"] == "QUERY_FAILED"


def test_malformed_cursor_is_typed_input_error(engine):
    arguments = {"window": engine.store.manifest.data_range.model_dump()}
    from contracts.models import TOOL_VERSION
    from contracts.queries import ListServices
    from store.evidence import canonical_query, digest_query

    digest = digest_query(
        canonical_query(
            engine.store.manifest.id,
            TOOL_VERSION,
            "list_services",
            ListServices.model_validate(arguments),
        )
    )
    result = engine.call("list_services", {**arguments, "cursor": digest + ":²"})
    assert result["error"]["code"] == "INVALID_CURSOR"


def test_failed_leakage_check_never_publishes_dataset(tmp_path, config, monkeypatch):
    monkeypatch.setattr("telemetry.generator.audit_public", lambda *args: ["reproduced leak"])
    with pytest.raises(ValueError, match="leakage"):
        generate(tmp_path, environment=config)
    assert not list(tmp_path.glob("public/*/manifest.json"))
    assert not list(tmp_path.glob("private/*/truth.json"))
    assert not list(tmp_path.glob(".pending-*"))


def test_zero_requests_are_present_buckets_not_gaps(tmp_path, config):
    bundle = generate(tmp_path, environment=config.model_copy(update={"bucket_seconds": 1}))
    store = ParquetStore(bundle.public)
    start = utc_ns(bundle.manifest.data_range.start)
    # Checkout/payment runs at t=0,3,...; no payment request starts in [1,2).
    result = ToolEngine(store).call(
        "query_metric",
        {
            "service": "payment",
            "metric": "request_count",
            "step_seconds": 1,
            "window": {
                "start": iso_time(start + 1_000_000_000),
                "end": iso_time(start + 2_000_000_000),
            },
        },
    )
    index = result["data"]["columns"].index("value")
    assert result["data"]["rows"][0][index] == 0
    assert not result["warnings"]


def test_prompt_injection_survives_log_loss_and_is_marked_privately(tmp_path, config):
    from telemetry.generator import ADVERSARIAL_BODY

    bundle = generate(
        tmp_path, environment=config.model_copy(update={"log_keep_rate": 0}), injection_log=True
    )
    logs = ParquetStore(bundle.public).tables["logs"]
    assert len(logs) == 1 and logs[0]["body"] == ADVERSARIAL_BODY
    assert "prompt_injection" in bundle.truth.features


def test_nonempty_reference_output_is_never_overwritten(tmp_path, config):
    from telemetry.suite import build_references

    sentinel = tmp_path / "reference_index.json"
    sentinel.write_text("existing index")
    with pytest.raises(FileExistsError):
        build_references(tmp_path, config)
    assert sentinel.read_text() == "existing index"


def test_invalid_backend_shape_is_a_query_error(engine):
    engine.store.query = lambda *args: (["service"], [[]], [])
    result = engine.call("list_services", {"window": engine.store.manifest.data_range.model_dump()})
    assert result["error"]["code"] == "QUERY_FAILED"


def test_reader_rejects_duplicate_metric_keys(bundles, tmp_path):
    from store import QueryError

    def duplicate(tables):
        tables["metrics"].append(dict(tables["metrics"][0]))

    with pytest.raises(QueryError, match="duplicate"):
        rewrite(bundles["healthy"], tmp_path, duplicate)


def test_junction_root_is_rejected_without_opening_files(bundles, monkeypatch):
    from pathlib import Path

    from store import QueryError

    public = bundles["healthy"].public.absolute()
    original = Path.is_junction
    monkeypatch.setattr(Path, "is_junction", lambda p: p == public or original(p))
    monkeypatch.setattr(Path, "read_text", lambda *args, **kwargs: pytest.fail("read linked data"))
    with pytest.raises(QueryError, match="linked"):
        ParquetStore(public)


@pytest.mark.parametrize("cap", [0, -1, 399, True])
def test_invalid_budget_is_configuration_error(engine, cap):
    with pytest.raises(ValueError):
        ToolEngine(engine.store, cap=cap)


def test_equivalent_defaults_have_same_query_identity(engine):
    arguments = {"window": engine.store.manifest.data_range.model_dump()}
    omitted = engine.call("find_traces", arguments)
    explicit = engine.call("find_traces", {**arguments, "min_duration_ms": 0})
    assert omitted["query_id"] == explicit["query_id"]
    metric = {**arguments, "service": "payment", "metric": "request_count"}
    assert (
        engine.call("query_metric", metric)["query_id"]
        == engine.call("query_metric", {**metric, "aggregation": "max"})["query_id"]
    )


def test_optional_error_span_does_not_make_whole_request_failed(tmp_path, config):
    bundle = generate(
        tmp_path, environment=config, faults=[Fault(service="email", mechanism="errors")]
    )
    result = ToolEngine(ParquetStore(bundle.public)).call(
        "find_traces",
        {
            "window": bundle.manifest.data_range.model_dump(),
            "service": "email",
            "status": "ERROR",
        },
    )
    assert result["returned"]
    columns = result["data"]["columns"]
    assert all(row[columns.index("status")] == "OK" for row in result["data"]["rows"])
    assert all(row[columns.index("matching_status")] == "ERROR" for row in result["data"]["rows"])


@pytest.mark.parametrize("value", [True, "20"])
def test_invalid_limit_types_are_not_silently_repaired(engine, value):
    result = engine.call(
        "list_services", {"window": engine.store.manifest.data_range.model_dump(), "limit": value}
    )
    assert result["error"]["code"] == "INVALID_ARGUMENT"
