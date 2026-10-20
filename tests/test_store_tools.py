import json
from math import ceil

import pytest

from contracts.models import TOOL_VERSION
from contracts.queries import QUERY_MODELS, QueryMetric
from mcp_servers.telemetry.engine import ToolEngine
from store import ParquetStore, QueryError
from store.evidence import QueryIds, canonical_query, compact_json, verifies
from telemetry.config import Fault
from telemetry.generator import generate
from telemetry.histograms import histogram, percentile


def as_dicts(result):
    return [
        dict(zip(result["data"]["columns"], row, strict=True)) for row in result["data"]["rows"]
    ]


def test_fast_failing_traces_and_no_matches(engine):
    window = engine.store.manifest.data_range.model_dump()
    result = engine.call("find_traces", {"window": window, "service": "payment", "status": "ERROR"})
    assert result["returned"] > 0
    assert all(r["max_matching_duration_ms"] == 2 for r in as_dicts(result))
    empty = engine.call("search_logs", {"window": window, "contains": "this phrase is absent"})
    assert empty["total_matches"] == 0 and not empty["truncated"]
    invalid = engine.call("find_traces", {"window": window, "service": "../../private"})
    assert invalid["error"]["code"] == "UNKNOWN_SERVICE"


def test_pagination_ids_handles_caps_and_foreign_cursor(engine):
    arguments = {
        "window": engine.store.manifest.data_range.model_dump(),
        "service": "payment",
        "limit": 1,
    }
    first = engine.call("find_traces", arguments)
    second = engine.call("find_traces", {**arguments, "cursor": first["next_cursor"], "limit": 2})
    assert first["query_id"] == second["query_id"]
    assert first["data"]["rows"][0][0] == "T1"
    assert second["data"]["rows"][0][0] == "T2"
    args = QUERY_MODELS["find_traces"].model_validate(arguments)
    assert verifies(
        first["query_id"],
        canonical_query(engine.store.manifest.id, TOOL_VERSION, "find_traces", args),
    )
    wrong = engine.call(
        "find_traces", {**arguments, "service": "frontend", "cursor": first["next_cursor"]}
    )
    assert wrong["error"]["code"] == "INVALID_CURSOR"
    larger = engine.call("find_traces", {**arguments, "limit": 100})
    assert len(compact_json(larger).encode()) <= 1500
    assert larger["truncated"] and larger["returned"] < 100


def test_hash_collision_extends_deterministically(monkeypatch):
    monkeypatch.setattr(
        "store.evidence.digest_query",
        lambda text: "a" * 8 + ("b" if text == "one" else "c") + "d" * 55,
    )
    ids = QueryIds()
    assert ids.get("one") == "qaaaaaaaa"
    assert ids.get("two") == "qaaaaaaaac"
    assert ids.get("one") == "qaaaaaaaa"


def test_percentile_matches_raw_nearest_rank_within_bin_error(bundles):
    store = ParquetStore(bundles["slow"].public)
    args = QueryMetric(window=store.manifest.data_range, service="payment", metric="latency_p95_ms")
    result = ToolEngine(store).call("query_metric", args.model_dump())
    summary = as_dicts(result)[0]
    raw = sorted(r["duration_ms"] for r in store.tables["spans"] if r["service"] == "payment")
    actual = raw[ceil(0.95 * len(raw)) - 1]
    assert abs(summary["value"] - actual) <= summary["absolute_error_bound"]


def test_histogram_merge_not_average_of_percentiles():
    bounds = [10.0, 100.0, 1000.0]
    first, second = histogram([1.0] * 100, bounds), histogram([999.0], bounds)
    merged = [a + b for a, b in zip(first, second, strict=True)]
    assert percentile(merged, bounds, 0.95)[0] == 5
    assert percentile([0, 0, 0, 1], bounds, 0.95) == (None, None)


def test_error_rate_and_gauge_aggregation(engine):
    window = engine.store.manifest.data_range.model_dump()
    result = engine.call(
        "query_metric", {"window": window, "service": "payment", "metric": "error_rate"}
    )
    rows = engine.store.tables["metrics"]

    def count(name):
        return sum(r["value"] for r in rows if r["service"] == "payment" and r["metric"] == name)

    assert as_dicts(result)[0]["value"] == count("error_count") / count("request_count")


def test_missing_buckets_are_warned_and_zero_is_not_a_gap(tmp_path, config):
    gapped = generate(tmp_path / "gap", environment=config, metric_gap=True)
    engine = ToolEngine(ParquetStore(gapped.public))
    result = engine.call(
        "query_metric",
        {
            "window": gapped.manifest.data_range.model_dump(),
            "service": "payment",
            "metric": "request_count",
        },
    )
    assert any(w["code"] == "METRIC_GAP" for w in result["warnings"])
    clean = generate(tmp_path / "clean", environment=config)
    engine = ToolEngine(ParquetStore(clean.public))
    result = engine.call(
        "query_metric",
        {
            "window": clean.manifest.data_range.model_dump(),
            "service": "payment",
            "metric": "error_count",
        },
    )
    assert as_dicts(result)[0]["value"] == 0
    assert not result["warnings"]


def test_all_tools_deny_arbitrary_paths_and_do_not_read_private(engine, bundles, monkeypatch):
    from pathlib import Path

    original = Path.read_text

    def guard(path, *args, **kwargs):
        assert "private" not in path.parts
        return original(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", guard)
    engine = ToolEngine(ParquetStore(bundles["errors"].public))
    window = engine.store.manifest.data_range.model_dump()
    for tool in QUERY_MODELS:
        result = engine.call(tool, {"window": window, "path": "../../private/truth.json"})
        assert result["error"]["code"] == "INVALID_ARGUMENT"
    result = engine.call("search_logs", {"window": window, "contains": "private/truth.json"})
    assert result["total_matches"] == 0
    assert (
        engine.call("read_file", {"path": "private/truth.json"})["error"]["code"] == "UNKNOWN_TOOL"
    )


def test_private_root_and_content_tampering_rejected(bundles, tmp_path):
    import shutil

    with pytest.raises(QueryError):
        ParquetStore(bundles["healthy"].private)
    copy = tmp_path / "public" / bundles["healthy"].manifest.id
    shutil.copytree(bundles["healthy"].public, copy)
    manifest = json.loads((copy / "manifest.json").read_text())
    manifest["question"] = "altered question"
    (copy / "manifest.json").write_text(json.dumps(manifest))
    with pytest.raises(QueryError, match="identity"):
        ParquetStore(copy)


def test_remaining_tools_and_validation(engine):
    window = engine.store.manifest.data_range.model_dump()
    requests = {
        "list_services": {},
        "get_dependencies": {},
        "check_coverage": {},
        "breakdown": {"group_by": "service"},
        "compare_windows": {
            "service": "payment",
            "metric": "error_rate",
            "baseline_window": window,
        },
        "get_trace": {"trace_id": engine.store.tables["spans"][0]["trace_id"]},
    }
    for tool, extra in requests.items():
        result = engine.call(tool, {"window": window, **extra})
        assert "error" not in result, (tool, result)
        assert len(compact_json(result).encode()) <= 1500
    assert (
        engine.call("find_traces", {"window": window, "limit": 0})["error"]["code"]
        == "INVALID_ARGUMENT"
    )
    invalid = engine.call(
        "query_metric",
        {"window": window, "service": "payment", "metric": "request_count", "step_seconds": 7},
    )
    assert invalid["error"]["code"] == "INVALID_STEP"


def test_gauge_max_exceeds_average(tmp_path, config):
    bundle = generate(
        tmp_path, environment=config, faults=[Fault(service="payment", mechanism="cpu_saturation")]
    )
    engine = ToolEngine(ParquetStore(bundle.public))
    args = {
        "window": bundle.manifest.data_range.model_dump(),
        "service": "payment",
        "metric": "cpu_utilization",
    }
    average = as_dicts(engine.call("query_metric", args))[0]["value"]
    maximum = as_dicts(engine.call("query_metric", {**args, "aggregation": "max"}))[0]["value"]
    assert 0.25 < average < maximum == 0.98
