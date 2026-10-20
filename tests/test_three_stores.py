"""D13: shop public evidence, agent runs and evaluator private data never mix."""

import json
import shutil
from pathlib import Path

import pyarrow.parquet as pq
import pytest

from contracts.queries import QUERY_MODELS
from mcp_servers.telemetry.engine import ToolEngine
from store import ParquetStore, QueryError
from telemetry.boundaries import in_reserved_store
from telemetry.leakage import audit_public


@pytest.mark.parametrize("store_name", ["runs", "private", "RUNS", "PRIVATE"])
def test_valid_looking_dataset_in_reserved_store_is_never_opened(
    tmp_path, bundles, monkeypatch, store_name
):
    source = bundles["healthy"].public
    target = tmp_path / store_name / "public" / source.name
    shutil.copytree(source, target)
    monkeypatch.setattr(
        Path, "read_text", lambda *args, **kwargs: pytest.fail("opened reserved manifest")
    )
    monkeypatch.setattr(
        pq, "read_table", lambda *args, **kwargs: pytest.fail("opened reserved telemetry")
    )
    with pytest.raises(QueryError, match="runs/ or private/"):
        ParquetStore(target)


def test_public_audit_rejects_nested_stores_without_reading_them(tmp_path, monkeypatch):
    (tmp_path / "manifest.json").write_text('{"question":"ordinary shop question"}')
    for store_name in ("runs", "private"):
        directory = tmp_path / store_name
        directory.mkdir()
        (directory / "records.json").write_text('{"marker":"EVALUATOR_ONLY_VALUE"}')
    original = Path.read_text

    def guarded(path, *args, **kwargs):
        assert not in_reserved_store(path), "audit tried to read another store"
        return original(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", guarded)
    violations = audit_public(tmp_path)
    assert "store boundary: runs" in violations
    assert "store boundary: private" in violations
    for store_name in ("runs", "private"):
        assert audit_public(tmp_path / store_name) == [
            "store boundary: root is inside runs/ or private/"
        ]


def test_all_tools_read_only_shop_files_and_reject_store_paths(bundles, tmp_path, monkeypatch):
    for name in ("runs", "private"):
        directory = tmp_path / name
        directory.mkdir()
        (directory / "records.json").write_text('{"marker":"EVALUATOR_ONLY_VALUE"}')
    text_read, parquet_read = Path.read_text, pq.read_table

    def guarded_text(path, *args, **kwargs):
        assert not in_reserved_store(path)
        return text_read(path, *args, **kwargs)

    def guarded_parquet(path, *args, **kwargs):
        assert not in_reserved_store(Path(path))
        return parquet_read(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", guarded_text)
    monkeypatch.setattr(pq, "read_table", guarded_parquet)
    store = ParquetStore(bundles["errors"].public)
    engine = ToolEngine(store)
    window = store.manifest.data_range.model_dump()
    arguments = {
        "list_services": {},
        "query_metric": {"service": "payment", "metric": "error_rate"},
        "find_traces": {"service": "payment"},
        "get_trace": {"trace_id": store.tables["spans"][0]["trace_id"]},
        "search_logs": {},
        "compare_windows": {
            "service": "payment",
            "metric": "error_rate",
            "baseline_window": window,
        },
        "breakdown": {"group_by": "service"},
        "get_dependencies": {},
        "check_coverage": {},
    }
    assert set(arguments) == set(QUERY_MODELS)
    for tool, extra in arguments.items():
        query = {"window": window, **extra}
        result = engine.call(tool, query)
        assert "error" not in result, (tool, result)
        assert "EVALUATOR_ONLY_VALUE" not in json.dumps(result)
        for store_name in ("runs", "private"):
            rejected = engine.call(
                tool, {**query, "path": str(tmp_path / store_name / "records.json")}
            )
            assert rejected["error"]["code"] == "INVALID_ARGUMENT"
