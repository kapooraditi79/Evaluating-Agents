r"""Capture two real stdio MCP requests for docs/telemetry-call-map.md.

Run from the repository root:
    .\.venv\Scripts\python.exe docs/tooling/capture_call_walkthrough.py

The profiler observes calls; it does not replace the query implementations.
Generated files stay in docs/tooling/call-walkthrough/.
"""

from __future__ import annotations

import argparse
import asyncio
import html
import inspect
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
OUTPUT = ROOT / "docs/tooling/call-walkthrough"
PUBLIC = ROOT / (
    "fixtures/v0.1.1/public/856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb"
)


def snapshot(value: Any) -> Any:
    """Preserve query data, but describe infrastructure objects by their type."""
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Path):
        return value.as_posix()
    if isinstance(value, dict):
        return {str(key): snapshot(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [snapshot(item) for item in value]
    if isinstance(value, (set, frozenset)):
        return sorted((snapshot(item) for item in value), key=lambda item: json.dumps(item))
    if isinstance(value, type):
        return f"<class {value.__module__}.{value.__qualname__}>"
    from pydantic import BaseModel

    if isinstance(value, BaseModel):
        try:
            return value.model_dump(mode="json")
        except Exception:
            pass  # A constructor can be observed before its fields are populated.
    return f"<{type(value).__module__}.{type(value).__qualname__}>"


class Capture:
    def __init__(self) -> None:
        self.stack: list[tuple[int, int | None]] = []
        self.calls: list[dict[str, Any]] = []
        self.stages: list[dict[str, Any]] = []
        self.counts: Counter[str] = Counter()

    def profile(self, frame, event, arg) -> None:
        if event == "c_call" and arg is sys.setprofile:
            return  # The recorder stopping is outside the production request path.
        if event in {"call", "c_call"}:
            python = event == "call"
            module = (
                frame.f_globals.get("__name__", "")
                if python
                else (getattr(arg, "__module__", None) or "builtins")
            )
            name = frame.f_code.co_qualname if python else getattr(arg, "__qualname__", str(arg))
            label = f"{module}.{name}"
            sequence = len(self.calls) + 1
            self.calls.append(
                {
                    "sequence": sequence,
                    "depth": len(self.stack),
                    "kind": "Python" if python else "C/builtin",
                    "function": label,
                    "line": frame.f_code.co_firstlineno if python else frame.f_lineno,
                }
            )
            self.counts[label] += 1
            detailed = python and (
                module.startswith(("contracts.", "store.", "mcp_servers.telemetry."))
                or module == "telemetry.histograms"
                or module.startswith("mcp.server.fastmcp.")
                or (
                    module == "mcp.server.lowlevel.server"
                    and (name.endswith(".handler") or name.endswith("._get_cached_tool_definition"))
                )
                or (
                    module == "pydantic.main"
                    and frame.f_code.co_name in {"model_validate", "model_dump", "__init__"}
                )
            )
            stage_index = None
            if detailed:
                argument_count = frame.f_code.co_argcount + frame.f_code.co_kwonlyargcount
                argument_count += bool(frame.f_code.co_flags & inspect.CO_VARARGS)
                argument_count += bool(frame.f_code.co_flags & inspect.CO_VARKEYWORDS)
                names = frame.f_code.co_varnames[:argument_count]
                values = {
                    key: snapshot(frame.f_locals[key])
                    for key in names
                    if key in frame.f_locals and key not in {"self", "cls"}
                }
                # Include the object being serialized/validated as data where possible.
                if "self" in frame.f_locals:
                    values["self"] = snapshot(frame.f_locals["self"])
                if "cls" in frame.f_locals:
                    values["cls"] = snapshot(frame.f_locals["cls"])
                closure = (
                    {}
                    if "<genexpr>" in name
                    else {
                        key: snapshot(frame.f_locals[key])
                        for key in frame.f_code.co_freevars
                        if key in frame.f_locals
                    }
                )
                stage_index = len(self.stages)
                self.stages.append(
                    {
                        "call": sequence,
                        "parent_call": self.stack[-1][0] if self.stack else None,
                        "function": label,
                        "source": frame.f_code.co_filename.replace(str(ROOT), "."),
                        "line": frame.f_code.co_firstlineno,
                        "inputs": values,
                        "closure_values": closure,
                    }
                )
            self.stack.append((sequence, stage_index))
        elif event in {"return", "c_return", "c_exception"} and self.stack:
            _, stage_index = self.stack.pop()
            if stage_index is not None:
                self.stages[stage_index]["output"] = snapshot(arg)
                if frame.f_code.co_name == "__init__" and "self" in frame.f_locals:
                    self.stages[stage_index]["constructed_object"] = snapshot(
                        frame.f_locals["self"]
                    )

    def save(self, name: str) -> None:
        OUTPUT.mkdir(parents=True, exist_ok=True)
        (OUTPUT / f"{name}-stages.json").write_text(
            json.dumps(self.stages, indent=2, ensure_ascii=True), encoding="utf-8"
        )
        (OUTPUT / f"{name}-calls.txt").write_text(
            "Scope: low-level MCP tools/call handler entry through its return.\n"
            "All observed Python and C/builtin call events on the server thread.\n"
            "Coroutine resumptions may appear as repeated calls.\n"
            "Format: sequence | depth | kind | function | source line\n\n"
            + "\n".join(
                f"{call['sequence']:05} | {call['depth']:02} | {call['kind']} | "
                f"{call['function']} | {call['line']}"
                for call in self.calls
            )
            + "\n",
            encoding="utf-8",
        )
        (OUTPUT / f"{name}-counts.json").write_text(
            json.dumps(dict(self.counts.most_common()), indent=2), encoding="utf-8"
        )
        details = [
            f"# {name}: function inputs and outputs\n",
            "Captured during a real stdio MCP request. Calls are listed in entry order; "
            "the output of an outer call is produced after its nested calls complete. "
            "The call number matches the raw calls.txt file. Expand a function to inspect "
            "its exact data. Infrastructure objects are described by type; model objects "
            "are shown as JSON. Python constructors return None; constructed_object shows "
            "the resulting model. Repeated generator-expression events are in stages.json "
            "and calls.txt.\n",
        ]
        for stage in self.stages:
            if "<genexpr>" in stage["function"]:
                continue
            details.extend(
                [
                    "<details>\n",
                    f"<summary>Call {stage['call']}: {html.escape(stage['function'])}</summary>\n",
                    f"Source: `{stage['source']}`, line {stage['line']}.\n",
                    "```json\n" + json.dumps(stage, indent=2) + "\n```\n",
                    "</details>\n",
                ]
            )
        (OUTPUT / f"{name}-details.md").write_text("\n".join(details), encoding="utf-8")


def serve() -> None:
    import mcp.types as types

    from mcp_servers.telemetry.engine import ToolEngine
    from mcp_servers.telemetry.server import create_server
    from store.parquet import ParquetStore

    server = create_server(ToolEngine(ParquetStore(PUBLIC)))
    original = server._mcp_server.request_handlers[types.CallToolRequest]
    calls: Counter[str] = Counter()

    async def traced_handler(request):
        name = request.params.name
        calls[name] += 1
        capture = Capture()
        previous = sys.getprofile()
        sys.setprofile(capture.profile)
        try:
            result = await original(request)
        finally:
            sys.setprofile(previous)
            capture.save(f"{name}-{calls[name]}")
        return result

    server._mcp_server.request_handlers[types.CallToolRequest] = traced_handler
    server.run(transport="stdio")


async def exercise() -> None:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    window = {"start": "2026-03-14T14:00:00Z", "end": "2026-03-14T14:05:00Z"}
    metric = {"window": window, "service": "frontend", "metric": "latency_p95_ms", "limit": 2}
    logs = {
        "window": {"start": "2026-03-14T14:00:00Z", "end": "2026-03-14T14:10:00Z"},
        "service": "email",
        "severity": "ERROR",
        "contains": "timed out",
        "limit": 2,
    }
    parameters = StdioServerParameters(
        command=sys.executable, args=[str(Path(__file__).resolve()), "--serve"], cwd=str(ROOT)
    )
    records = []
    async with stdio_client(parameters) as (read, write):
        async with ClientSession(read, write) as client:
            await client.initialize()
            available = await client.list_tools()
            assert len(available.tools) == 9
            for name, args in [("query_metric", metric), ("search_logs", logs)]:
                result = await client.call_tool(name, {"query": args})
                assert not result.isError, result
                payload = result.structuredContent
                assert payload is not None and "error" not in payload, payload
                assert payload["returned"] == 2, payload
                records.append(
                    {
                        "tool": name,
                        "arguments": {"query": args},
                        "result": payload,
                        "mcp_result": result.model_dump(mode="json"),
                    }
                )
            next_logs = {**logs, "cursor": records[1]["result"]["next_cursor"]}
            page = await client.call_tool("search_logs", {"query": next_logs})
            assert not page.isError and page.structuredContent is not None
            assert page.structuredContent["query_id"] == records[1]["result"]["query_id"]
            assert page.structuredContent["data"]["rows"][0][0] == "L3"
            records.append(
                {
                    "tool": "search_logs",
                    "arguments": {"query": next_logs},
                    "result": page.structuredContent,
                    "mcp_result": page.model_dump(mode="json"),
                }
            )
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "requests-and-results.json").write_text(
        json.dumps(records, indent=2), encoding="utf-8"
    )
    print(
        json.dumps(
            [
                {
                    "tool": row["tool"],
                    "query_id": row["result"]["query_id"],
                    "total_matches": row["result"]["total_matches"],
                    "returned": row["result"]["returned"],
                }
                for row in records
            ],
            indent=2,
        )
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--serve", action="store_true")
    options = parser.parse_args()
    if options.serve:
        serve()
    else:
        asyncio.run(exercise())
