import asyncio
import json
import math
from pathlib import Path

import pytest

from mcp_servers.telemetry.engine import ToolEngine
from mcp_servers.telemetry.server import create_server
from store import ParquetStore
from telemetry.tool_surface import argument_inventory, build_report, compare_tools


def test_surface_report_uses_actual_schemas_and_does_not_invent_tokens(bundles):
    server = create_server(ToolEngine(ParquetStore(bundles["healthy"].public)))
    tools = [t.model_dump(mode="json", exclude_none=True) for t in asyncio.run(server.list_tools())]
    report = build_report(tools)
    assert report["tool_count"] == 9
    assert report["sizes"]["mcp_tools_list"]["tokens"] is None
    assert report["stub_comparison"]["status"] == "not_compared"
    assert (
        report["sizes"]["core_function_tools"]["utf8_bytes"]
        < report["sizes"]["function_tools"]["utf8_bytes"]
    )
    query = next(t for t in report["inventory"] if t["name"] == "query_metric")
    assert query["arguments"]["query"]["required"]
    assert query["arguments"]["query.window.start"]["effectively_required"]
    assert query["arguments"]["query.service"]["required"]
    assert not query["arguments"]["query.operation"]["required"]
    assert query["arguments"]["query.operation"]["nullable"]
    old = json.loads(Path("docs/tooling/tools-before.json").read_text())
    comparison = compare_tools(tools, old)
    assert comparison["differences"]
    assert all(d.get("change") == "description" for d in comparison["differences"])
    assert (
        report["sizes"]["mcp_tools_list"]["utf8_bytes"]
        < build_report(old)["sizes"]["mcp_tools_list"]["utf8_bytes"]
    )


def test_token_counts_require_named_tokenizer_and_count_exact_serialization():
    tools = [{"name": "x", "inputSchema": {"type": "object", "properties": {}}}]
    with pytest.raises(ValueError, match="identifier"):
        build_report(tools, token_counter=len)
    # This test callback counts characters, not model tokens; never saved as a measurement.
    report = build_report(tools, token_counter=len, tokenizer_id="test-character-counter")
    assert (
        report["sizes"]["mcp_tools_list"]["tokens"]
        == report["sizes"]["mcp_tools_list"]["characters"]
    )


def test_stub_diff_catches_names_types_requiredness_and_extra_arguments():
    real = [
        {
            "name": "x",
            "inputSchema": {
                "type": "object",
                "additionalProperties": False,
                "properties": {"service": {"type": "string"}, "limit": {"type": "integer"}},
                "required": ["service"],
            },
        }
    ]
    stub = [
        {
            "type": "function",
            "function": {
                "name": "x",
                "parameters": {
                    "type": "object",
                    "properties": {"service": {"type": "integer"}, "other": {"type": "string"}},
                    "required": [],
                },
            },
        },
        {"type": "function", "function": {"name": "stub_only", "parameters": {"type": "object"}}},
    ]
    report = compare_tools(real, stub)
    paths = {d.get("argument") for d in report["differences"]}
    assert {"service", "limit", "other", "$root"} <= paths
    assert any(d.get("change") == "only_in_stub" for d in report["differences"])


def test_inventory_handles_nullable_type_lists():
    inventory = argument_inventory(
        {
            "type": "object",
            "properties": {"name": {"type": ["string", "null"]}},
            "required": ["name"],
        }
    )
    assert inventory["name"]["required"] and inventory["name"]["nullable"]


def test_character_estimate_is_separate_from_exact_tokens():
    tools = [{"name": "x", "inputSchema": {"type": "object"}}]
    report = build_report(tools, approximate_chars_per_token=3.6)
    size = report["sizes"]["mcp_tools_list"]
    assert size["tokens"] is None
    assert size["approximate_tokens"] == math.ceil(size["characters"] / 3.6)
    assert not report["approximation"]["measured"]
    for invalid in (0, -1, float("nan"), float("inf")):
        with pytest.raises(ValueError, match="positive and finite"):
            build_report(tools, approximate_chars_per_token=invalid)
