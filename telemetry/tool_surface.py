"""Export the real MCP surface, measure explicit serializations, compare stub JSON.

This developer utility is not an MCP tool and is never part of shop telemetry.
Exact token counts require a tokenizer; character-based estimates are labeled separately.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections.abc import Callable
from typing import Any

from contracts.models import TOOL_VERSION

CORE_TOOLS = frozenset({"list_services", "query_metric", "find_traces", "get_trace", "search_logs"})


def normalize_tools(value: Any) -> list[dict[str, Any]]:
    """Accept an MCP tools/list object, function-tools object, or either raw tool list."""
    raw = value["tools"] if isinstance(value, dict) else value
    if not isinstance(raw, list):
        raise ValueError("expected a tools list")
    result = []
    for tool in raw:
        if "function" in tool:
            function = tool["function"]
            tool = {
                "name": function["name"],
                "description": function.get("description", ""),
                "inputSchema": function["parameters"],
            }
        elif "inputSchema" not in tool:
            tool = {**tool, "inputSchema": tool.get("parameters", tool.get("input_schema"))}
        if not isinstance(tool.get("name"), str) or not isinstance(tool.get("inputSchema"), dict):
            raise ValueError("each tool requires name and inputSchema/parameters")
        result.append(tool)
    if len({tool["name"] for tool in result}) != len(result):
        raise ValueError("duplicate tool names")
    return result


def argument_inventory(schema: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """List nested arguments, local/effective requiredness, nullable types and constraints."""
    result: dict[str, dict[str, Any]] = {}

    def resolve(node: dict[str, Any], seen: frozenset[str] = frozenset()) -> dict[str, Any]:
        if "$ref" not in node:
            return node
        reference = node["$ref"]
        if reference in seen or not reference.startswith("#/"):
            raise ValueError("unsupported recursive/external schema reference")
        target = schema
        for part in reference[2:].split("/"):
            target = target[part.replace("~1", "/").replace("~0", "~")]
        return {
            **resolve(target, seen | {reference}),
            **{k: v for k, v in node.items() if k != "$ref"},
        }

    def visit(node: dict[str, Any], path: str, required: bool, effective: bool) -> None:
        node = resolve(node)
        variants = [resolve(v) for v in node.get("anyOf", [node])]
        types = sorted(
            {
                kind
                for v in variants
                for kind in (
                    v.get("type")
                    if isinstance(v.get("type"), list)
                    else [v.get("type", "unspecified")]
                )
            }
        )
        if path:
            entry = {
                "types": types,
                "required": required,
                "effectively_required": effective,
                "nullable": "null" in types,
            }
            for key in (
                "default",
                "enum",
                "const",
                "minimum",
                "maximum",
                "exclusiveMinimum",
                "exclusiveMaximum",
                "minLength",
                "maxLength",
                "pattern",
                "additionalProperties",
            ):
                if key in node:
                    entry[key] = node[key]
            for key in ("enum", "const", "minimum", "maximum", "pattern", "minLength", "maxLength"):
                values = [v[key] for v in variants if key in v]
                if key not in entry and len(values) == 1:
                    entry[key] = values[0]
            result[path] = entry
        for variant in variants:
            for name, child in variant.get("properties", {}).items():
                local = name in variant.get("required", [])
                visit(child, f"{path}.{name}" if path else name, local, effective and local)
            if isinstance(variant.get("items"), dict):
                visit(variant["items"], path + "[]", False, False)

    visit(schema, "", True, True)
    # Root openness matters even when every named parameter is unchanged.
    result["$root"] = {"additionalProperties": schema.get("additionalProperties", True)}
    return result


def compare_tools(real: Any, stub: Any) -> dict[str, Any]:
    actual = {t["name"]: t for t in normalize_tools(real)}
    standins = {t["name"]: t for t in normalize_tools(stub)}
    differences = []
    for name in sorted(actual.keys() | standins.keys()):
        if name not in standins:
            differences.append({"tool": name, "change": "only_in_real"})
        elif name not in actual:
            differences.append({"tool": name, "change": "only_in_stub"})
        else:
            real_args = argument_inventory(actual[name]["inputSchema"])
            stub_args = argument_inventory(standins[name]["inputSchema"])
            for path in sorted(real_args.keys() | stub_args.keys()):
                if real_args.get(path) != stub_args.get(path):
                    differences.append(
                        {
                            "tool": name,
                            "argument": path,
                            "real": real_args.get(path),
                            "stub": stub_args.get(path),
                        }
                    )
            if actual[name].get("description", "") != standins[name].get("description", ""):
                differences.append(
                    {
                        "tool": name,
                        "change": "description",
                        "real": actual[name].get("description", ""),
                        "stub": standins[name].get("description", ""),
                    }
                )
            for field in ("annotations", "outputSchema"):
                if actual[name].get(field) != standins[name].get(field):
                    differences.append(
                        {
                            "tool": name,
                            "change": field,
                            "real": actual[name].get(field),
                            "stub": standins[name].get(field),
                        }
                    )
    return {
        "status": "compared",
        "difference_count": len(differences),
        "differences": differences,
        "scope": (
            "names, parameter paths, requiredness, types, defaults, constraints, descriptions, "
            "MCP annotations and output schemas; cosmetic schema titles omitted"
        ),
        "tool_order": {
            "real": list(actual),
            "stub": list(standins),
            "changed": list(actual) != list(standins),
        },
    }


def function_tools(tools: Any) -> list[dict[str, Any]]:
    """Project MCP discovery to the function schemas sent to a model."""
    return [
        {
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool.get("description", ""),
                "parameters": tool["inputSchema"],
            },
        }
        for tool in normalize_tools(tools)
    ]


def build_report(
    tools: Any,
    *,
    token_counter: Callable[[str], int] | None = None,
    tokenizer_id: str | None = None,
    stub: Any = None,
    approximate_chars_per_token: float | None = None,
) -> dict[str, Any]:
    definitions = normalize_tools(tools)
    if token_counter is not None and not tokenizer_id:
        raise ValueError("a measured token count requires a tokenizer identifier")
    if approximate_chars_per_token is not None and (
        not math.isfinite(approximate_chars_per_token) or approximate_chars_per_token <= 0
    ):
        raise ValueError("approximate characters per token must be positive and finite")

    def size(value: Any) -> dict[str, Any]:
        serialized = json.dumps(
            value, ensure_ascii=True, sort_keys=True, separators=(",", ":"), allow_nan=False
        )
        tokens = token_counter(serialized) if token_counter else None
        if tokens is not None and (type(tokens) is not int or tokens < 0):
            raise ValueError("token counter must return a nonnegative integer")
        return {
            "characters": len(serialized),
            "utf8_bytes": len(serialized.encode()),
            "tokens": tokens,
            "approximate_tokens": (
                math.ceil(len(serialized) / approximate_chars_per_token)
                if approximate_chars_per_token is not None
                else None
            ),
            "sha256": hashlib.sha256(serialized.encode()).hexdigest(),
        }

    functions = function_tools(definitions)
    return {
        "tool_version": TOOL_VERSION,
        "tokenizer_id": tokenizer_id,
        "approximation": {
            "characters_per_token": approximate_chars_per_token,
            "method": "ceil(characters / characters_per_token)",
            "measured": False,
            "caveat": "Heuristic only; excludes model framing; not a tokenizer measurement.",
        }
        if approximate_chars_per_token is not None
        else None,
        "serialization": "compact ASCII JSON, sorted object keys, supplied tool order, no framing",
        "scope": "JSON token counts exclude the model chat/tool template and special tokens",
        "tool_count": len(definitions),
        "sizes": {
            "mcp_tools_list": size({"tools": definitions}),
            "function_tools": size(functions),
            "core_function_tools": size(
                [t for t in functions if t["function"]["name"] in CORE_TOOLS]
            ),
        },
        "inventory": [
            {
                "name": tool["name"],
                "description": tool.get("description", ""),
                "arguments": argument_inventory(tool["inputSchema"]),
                "mcp_definition_size": size(tool),
            }
            for tool in definitions
        ],
        "stub_comparison": compare_tools(definitions, stub)
        if stub is not None
        else {"status": "not_compared", "reason": "stub definitions not supplied"},
    }


async def discover_tools(public_directory) -> list[dict[str, Any]]:
    import sys

    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    parameters = StdioServerParameters(
        command=sys.executable,
        args=[
            "-m",
            "mcp_servers.telemetry.server",
            "--public-dir",
            str(public_directory.resolve()),
        ],
    )
    async with stdio_client(parameters) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            return [tool.model_dump(mode="json", exclude_none=True) for tool in tools.tools]
