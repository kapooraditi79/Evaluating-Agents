import asyncio
import json
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from contracts.models import GroundTruth
from contracts.queries import QUERY_MODELS
from mcp_servers.telemetry.engine import ToolEngine
from store import ParquetStore
from telemetry.suite import balance_audit, balanced_plan, build_references, build_suite


def test_committed_tool_exchange_golden_files():
    from pathlib import Path

    root = Path("fixtures/v0.1.1")
    index = json.loads((root / "reference_index.json").read_text())
    for label, paths in index.items():
        exchange = json.loads((root / "examples" / f"{label}.json").read_text())
        engine = ToolEngine(ParquetStore(root / paths["public"]))
        assert engine.call(exchange["tool"], exchange["arguments"]) == exchange["response"]
    pagination = json.loads((root / "examples/pagination.json").read_text())
    engine = ToolEngine(ParquetStore(root / index["fast_failure"]["public"]))
    for page in pagination["pages"]:
        assert engine.call(pagination["tool"], page["arguments"]) == page["response"]


def test_balanced_metadata_and_shortcut_audit(tmp_path, config):
    assert balance_audit(balanced_plan())["passed"]
    report = build_suite(tmp_path, config)
    assert report["n"] == 16
    assert report["metadata"]["passed"]
    assert report["latest_error_shortcut"]["passed"]
    records = json.loads((tmp_path / "suite.json").read_text())["records"]
    actual = []
    for record in records:
        manifest = json.loads((tmp_path / record["public"] / "manifest.json").read_text())
        from contracts.models import utc_ns

        fraction = (
            utc_ns(manifest["reference_time"]) - utc_ns(manifest["data_range"]["start"])
        ) / (utc_ns(manifest["data_range"]["end"]) - utc_ns(manifest["data_range"]["start"]))
        actual.append(
            {
                **record,
                "template": "alert" if manifest["question"].startswith("Alert") else "report",
                "reference_fraction": fraction,
            }
        )
    assert balance_audit(actual)["passed"]


def test_reference_bundles_and_two_cause_schema(tmp_path, config):
    bundles = build_references(tmp_path, config)
    assert len(bundles) == 3
    pages = json.loads((tmp_path / "examples/pagination.json").read_text())["pages"]
    assert pages[0]["response"]["truncated"]
    assert pages[0]["response"]["query_id"] == pages[1]["response"]["query_id"]
    truth = GroundTruth.model_validate_json(
        (tmp_path / "private/two_cause_schema_example.json").read_text()
    )
    assert [c.role for c in truth.root_causes] == ["primary", "trigger"]


def test_real_stdio_mcp_discovery_and_calls(bundles):
    async def exercise():
        bundle = bundles["errors"]
        parameters = StdioServerParameters(
            command=sys.executable,
            args=[
                "-W",
                "error",
                "-m",
                "mcp_servers.telemetry.server",
                "--public-dir",
                str(bundle.public),
            ],
        )
        async with stdio_client(parameters) as (read, write):
            async with ClientSession(read, write) as client:
                await client.initialize()
                listed = await client.list_tools()
                assert {t.name for t in listed.tools} == set(QUERY_MODELS)
                assert all(t.annotations.readOnlyHint for t in listed.tools)
                window = bundle.manifest.data_range.model_dump()
                for name, arguments in {
                    "list_services": {},
                    "query_metric": {"service": "payment", "metric": "error_rate"},
                    "find_traces": {"service": "payment", "status": "ERROR"},
                    "search_logs": {"service": "payment", "severity": "ERROR"},
                    "get_trace": {
                        "trace_id": ParquetStore(bundle.public).tables["spans"][0]["trace_id"]
                    },
                    "get_dependencies": {},
                    "check_coverage": {"service": "payment"},
                    "breakdown": {"group_by": "service"},
                    "compare_windows": {
                        "service": "payment",
                        "metric": "error_rate",
                        "baseline_window": window,
                    },
                }.items():
                    result = await client.call_tool(
                        name, {"query": {"window": window, **arguments}}
                    )
                    assert not result.isError
                    data = result.structuredContent or json.loads(result.content[0].text)
                    assert "error" not in data, data
                    assert data["returned"] > 0
                denied = await client.call_tool(
                    "search_logs", {"query": {"window": window, "path": "../../private/truth.json"}}
                )
                assert denied.isError

    asyncio.run(asyncio.wait_for(exercise(), timeout=45))
