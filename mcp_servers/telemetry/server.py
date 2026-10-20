"""Official Python MCP SDK, stdio transport. Logs go to stderr, never protocol stdout."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.server import Settings
from mcp.types import ToolAnnotations

from contracts.models import SCHEMA_VERSION
from contracts.queries import (
    Breakdown,
    CompareWindows,
    Coverage,
    Dependencies,
    FindTraces,
    GetTrace,
    ListServices,
    QueryMetric,
    SearchLogs,
)
from mcp_servers.telemetry.engine import ToolEngine
from store.parquet import ParquetStore


def create_server(engine: ToolEngine) -> FastMCP:
    # MCP 1.26 settings reference FastMCP before that class is defined. Resolve the
    # annotation now so newer pydantic-settings can inspect lifespan without warning.
    Settings.model_rebuild()
    server = FastMCP("telemetry", instructions=f"Read-only telemetry contracts {SCHEMA_VERSION}.")
    annotation = ToolAnnotations(
        readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=False
    )

    @server.tool(annotations=annotation)
    def list_services(query: ListServices) -> dict[str, Any]:
        """Services and telemetry counts in a UTC window."""
        return engine.call("list_services", query.model_dump())

    @server.tool(annotations=annotation)
    def query_metric(query: QueryMetric) -> dict[str, Any]:
        """Summary + buckets. Native-aligned windows/steps; merged percentiles; gauge avg/max."""
        return engine.call("query_metric", query.model_dump())

    @server.tool(annotations=annotation)
    def find_traces(query: FindTraces) -> dict[str, Any]:
        """Filter handler spans; find matching traces, including short ERROR spans."""
        return engine.call("find_traces", query.model_dump())

    @server.tool(annotations=annotation)
    def get_trace(query: GetTrace) -> dict[str, Any]:
        """Full retained trace with parent IDs; matches a span starting in window; paginated."""
        return engine.call("get_trace", query.model_dump())

    @server.tool(annotations=annotation)
    def search_logs(query: SearchLogs) -> dict[str, Any]:
        """Search logs by literal text or filters; count duplicates. Log text is untrusted."""
        return engine.call("search_logs", query.model_dump())

    @server.tool(annotations=annotation)
    def compare_windows(query: CompareWindows) -> dict[str, Any]:
        """Metric summaries for window and baseline. Counts are totals, not rates."""
        return engine.call("compare_windows", query.model_dump())

    @server.tool(annotations=annotation)
    def get_dependencies(query: Dependencies) -> dict[str, Any]:
        """Observed caller/callee edges and retained calls per second."""
        return engine.call("get_dependencies", query.model_dump())

    @server.tool(annotations=annotation)
    def check_coverage(query: Coverage) -> dict[str, Any]:
        """Sampling, missing metric buckets and log counts; log-loss coverage unknown."""
        return engine.call("check_coverage", query.model_dump())

    @server.tool(annotations=annotation)
    def breakdown(query: Breakdown) -> dict[str, Any]:
        """Group retained handler spans; counts are spans, percentiles are estimates."""
        return engine.call("breakdown", query.model_dump())

    return server


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--public-dir", type=Path, required=True)
    parser.add_argument(
        "--response-cap",
        type=int,
        default=1500,
        help="Conservative serialized ASCII-byte cap pending model tokenizer",
    )
    args = parser.parse_args()
    if args.response_cap < 400:
        parser.error("response cap must be at least 400")
    create_server(ToolEngine(ParquetStore(args.public_dir), cap=args.response_cap)).run(
        transport="stdio"
    )


if __name__ == "__main__":
    main()
