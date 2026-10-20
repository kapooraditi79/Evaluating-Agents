from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

from contracts.models import export_schemas
from telemetry.config import load_environment
from telemetry.suite import build_references, build_suite


async def smoke(public: Path) -> None:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    from store import ParquetStore

    window = ParquetStore(public).manifest.data_range.model_dump()
    parameters = StdioServerParameters(
        command=sys.executable,
        args=["-m", "mcp_servers.telemetry.server", "--public-dir", str(public.resolve())],
    )
    async with stdio_client(parameters) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            available = await session.list_tools()
            result = await session.call_tool("list_services", {"query": {"window": window}})
            if result.isError:
                raise RuntimeError(result)
            payload = result.structuredContent
            if payload is None:
                payload = json.loads(result.content[0].text)
            if "error" in payload:
                raise RuntimeError(payload)
            print(
                json.dumps(
                    {"tools": [t.name for t in available.tools], "sample": payload}, indent=2
                )
            )


def main() -> None:
    parser = argparse.ArgumentParser(description="Person A data and tool workflow; no GPU required")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("references", "suite"):
        command = sub.add_parser(name)
        command.add_argument("--output", type=Path, required=True)
        command.add_argument("--config", type=Path)
    command = sub.add_parser("schemas")
    command.add_argument("--output", type=Path, default=Path("contracts/schemas"))
    command = sub.add_parser("smoke")
    command.add_argument("--public-dir", type=Path, required=True)
    command = sub.add_parser("tools-report")
    command.add_argument("--public-dir", type=Path, required=True)
    command.add_argument("--output", type=Path, required=True)
    command.add_argument("--stub-json", type=Path)
    command.add_argument("--approx-chars-per-token", type=float)
    args = parser.parse_args()
    if args.command == "schemas":
        export_schemas(args.output)
    elif args.command == "smoke":
        asyncio.run(smoke(args.public_dir))
    elif args.command == "tools-report":
        from telemetry.generator import _json
        from telemetry.tool_surface import build_report, discover_tools, function_tools

        definitions = asyncio.run(discover_tools(args.public_dir))
        stub = json.loads(args.stub_json.read_text(encoding="utf-8")) if args.stub_json else None
        report = build_report(
            definitions, stub=stub, approximate_chars_per_token=args.approx_chars_per_token
        )
        _json(args.output, report)
        _json(args.output.with_name(args.output.stem + ".definitions.json"), {"tools": definitions})
        _json(
            args.output.with_name(args.output.stem + ".functions.json"), function_tools(definitions)
        )
        print(
            json.dumps(
                {
                    "output": str(args.output),
                    "sizes": report["sizes"],
                    "stub_comparison": report["stub_comparison"]["status"],
                },
                indent=2,
            )
        )
    elif args.command == "references":
        result = build_references(args.output, load_environment(args.config))
        print(json.dumps({"datasets": [str(b.public) for b in result]}, indent=2))
    else:
        print(json.dumps(build_suite(args.output, load_environment(args.config)), indent=2))


if __name__ == "__main__":
    main()
