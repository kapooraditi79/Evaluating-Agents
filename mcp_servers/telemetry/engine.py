"""Protocol-independent tool execution, pagination, identity, validation and bounded output."""
# This module receives tool requests, validates them, queries telemetry data,
# adds identifiers to results, manages pagination, and limits response size.

# Flow: The agent requests data -> this engine validates the request ->
# the store retrieves data -> the engine formats and returns a bounded response.

from __future__ import annotations  # Allows flexible type annotations without evaluating them immediately.

import logging  # Records unexpected failures so they can be investigated.
import re  # Checks whether pagination cursor values have the correct format.
from collections.abc import Callable  # Describes a function that can be passed into this class.
from typing import Any  # Allows type hints for values whose types may vary.

from pydantic import ValidationError  # Identifies requests that fail input validation.

from contracts.models import TOOL_VERSION, TableData, ToolResult, ToolSource, WarningItem
# Imports the structures needed to build a standard, structured tool response.
# The response will contain data, counts, source information, and any warnings.

from contracts.queries import QUERY_MODELS  # Provides the validation model for each supported tool.
from store.base import TelemetryStore  # Defines how this engine communicates with a telemetry data store.
from store.evidence import QueryIds, canonical_query, compact_json, digest_query
# Imports helpers for tracking queries, creating consistent query representations,
# measuring response size, and generating compact identifiers for query contents.

from store.parquet import QueryError  # Provides a controlled error type for expected query failures.


PREFIXES = {  # Maps each tool to the letter used to identify its returned rows.
    "list_services": "V",  # Service rows receive handles such as V1 and V2.
    "query_metric": "M",  # Metric rows receive handles such as M1 and M2.
    "compare_windows": "M",  # Comparison rows use the metric prefix too.
    "find_traces": "T",  # Trace-search rows receive handles such as T1.
    "get_trace": "S",  # Individual trace results use the S prefix.
    "search_logs": "L",  # Log results receive handles such as L1.
    "get_dependencies": "D",  # Dependency results use the D prefix.
    "check_coverage": "C",  # Coverage results use the C prefix.
    "breakdown": "B",  # Breakdown results use the B prefix.
}  # These short handles help refer to particular results later.


class ToolEngine:  # Defines the component responsible for executing tool requests.
    def __init__(  # Runs once when a ToolEngine object is created.
        self,  # Refers to the ToolEngine object being created.
        store: TelemetryStore,  # Supplies the data store from which telemetry will be queried.
        cap: int = 1500,  # Sets the default maximum response-size budget.
        token_counter: Callable[[str], int] | None = None,  # Optionally supplies a function to measure response size.
    ):  # Ends the constructor's parameter list.
        if type(cap) is not int or cap < 400:  # Checks that the response budget is a valid integer of at least 400.
            raise ValueError("response budget must be an integer >= 400")  # Stops setup if the budget is invalid.

        self.store = store  # Saves the data store so future tool calls can query it.
        self.cap = cap  # Saves the maximum permitted response size.

        # This fallback counts UTF-8 bytes, not actual LLM tokens.
        # A real tokenizer can be supplied when a more accurate token estimate is needed.
        self.count = token_counter or (lambda text: len(text.encode("utf-8")))
        # Uses the supplied counting function, or counts the encoded bytes if none was supplied.

        self.ids = QueryIds()  # Creates a helper for assigning consistent IDs to queries.
        self.tool_version = TOOL_VERSION  # Saves the tool version so results can identify which version produced them.

    def call(self, tool: str, arguments: dict[str, Any]) -> dict[str, Any]:
        # Entry point: receives a tool name and the arguments requested by the agent.
        # Flow: check tool name -> validate arguments -> query data -> format results -> return response.

        if tool not in QUERY_MODELS:  # Checks whether this tool exists in the supported tool definitions.
            return {"error": {"code": "UNKNOWN_TOOL", "message": "tool is not available"}}
            # Stops immediately if the agent requests an unsupported tool.

        try:  # Starts validation of the supplied arguments.
            args = QUERY_MODELS[tool].model_validate(arguments)
            # Selects this tool's schema and checks that the arguments follow it.
            # For example, required fields and value types must be correct.
        except ValidationError:  # Runs if the supplied arguments do not match the schema.
            return {
                "error": {
                    "code": "INVALID_ARGUMENT",  # Gives the caller a machine-readable error code.
                    "message": "arguments do not match the tool schema",  # Explains the validation failure.
                }
            }  # Returns the error instead of querying the data store.

        try:  # Begins the main query-processing flow, including pagination and response-size checks.
            canonical = canonical_query(self.store.manifest.id, self.tool_version, tool, args)
            # Builds a consistent representation of the dataset, tool version, tool name, and validated arguments.
            # This helps distinguish requests that ask different questions or use different datasets.

            query_id = self.ids.get(canonical)  # Gets the identifier associated with this query representation.
            digest = digest_query(canonical)  # Creates a compact digest used to validate pagination cursors.
            offset = 0  # Starts at the first result unless the caller requests another page.

            if args.cursor is not None:  # Checks whether the caller wants to continue from an earlier page.
                parts = args.cursor.split(":")  # Splits the cursor into its digest and row-offset components.
                if (  # Checks that the cursor has the expected structure and belongs to this query.
                    len(parts) != 2  # Rejects cursors that do not contain exactly two components.
                    or parts[0] != digest  # Rejects cursors created for a different query or result set.
                    or re.fullmatch(r"[0-9]{1,18}", parts[1]) is None
                    # Rejects offsets that are not between 1 and 18 decimal digits.
                ):
                    raise QueryError("INVALID_CURSOR", "cursor does not belong to this result set")
                    # Stops processing when the cursor is malformed or belongs to another result set.

                offset = int(parts[1])  # Converts the validated cursor offset into an integer.

            columns, all_rows, warnings = self.store.query(tool, args)
            # Asks the data store to execute the requested query.
            # Receives the column names, all matching rows, and any warnings from the store.

            if offset > len(all_rows):  # Checks whether the requested starting position exceeds the available results.
                raise QueryError("INVALID_CURSOR", "cursor is outside this result set")
                # Rejects a cursor that points beyond the end of the result set.

            selected: list[list[Any]] = []  # Creates an initially empty list for rows that will be returned.
            # The engine builds this list gradually so it can stop before the response becomes too large.

            def envelope() -> dict[str, Any]:  # Defines a helper that packages the currently selected rows into a response.
                returned = len(selected)  # Counts how many rows have been selected for this response.
                more = offset + returned < len(all_rows)
                # Checks whether matching rows remain after the current page.

                return ToolResult(  # Constructs the standard response object.
                    data=TableData(columns=["handle", *columns], rows=selected),
                    # Adds a handle column before the original data columns and attaches the selected rows.

                    total_matches=len(all_rows),  # Reports the total number of matching rows, not just this page.
                    returned=returned,  # Reports how many rows are included in this response.
                    truncated=more,  # Indicates whether additional matching rows remain to be retrieved.
                    next_cursor=f"{digest}:{offset + returned}" if more else None,
                    # If more rows remain, supplies a cursor for the next page; otherwise, supplies no cursor.

                    query_id=query_id,  # Attaches the identifier for this query.
                    source=ToolSource(  # Describes where the results came from.
                        dataset_id=self.store.manifest.id,  # Identifies the dataset that was queried.
                        tool_version=self.tool_version  # Records the version of the tool engine.
                    ),  # Finishes the source information.

                    warnings=[WarningItem.model_validate(w) for w in warnings],
                    # Validates and formats any warnings produced by the data store.
                ).model_dump()  # Converts the structured response into a regular Python dictionary.

            for position in range(offset, min(offset + args.limit, len(all_rows))):
                # Iterates through the requested page, stopping at the page limit or the end of the results.

                selected.append([f"{PREFIXES[tool]}{position + 1}", *all_rows[position]])
                # Adds the current row to the response.
                # The first value is its handle, such as M1; the remaining values are the original row fields.

                if self.count(compact_json(envelope())) > self.cap:
                    # Builds the current response, converts it to compact JSON, and checks its estimated size.
                    # This check happens after each row is added to catch responses that exceed the budget.

                    selected.pop()  # Removes the latest row because adding it made the response too large.
                    break  # Stops adding rows; earlier rows may still fit within the response budget.

            result = envelope()  # Builds the final response using only the rows that fit.

            if self.count(compact_json(result)) > self.cap or (
                not selected and offset < len(all_rows)
            ):
                # Checks whether the response metadata alone is too large, or whether no row could fit
                # even though matching data remains available.

                raise QueryError(
                    "OUTPUT_TOO_LARGE",  # Identifies the problem for the caller.
                    "a result row or metadata exceeds the response budget; narrow the query",
                    # Suggests narrowing the query, for example by reducing its time range or limit.
                )  # Stops instead of returning an oversized response or silently hiding all results.

            return result  # Returns the successful, size-limited response to the caller.

        except QueryError as exc:  # Handles expected query errors, such as an invalid cursor or oversized output.
            return {"error": {"code": exc.code, "message": exc.message}}
            # Returns the error code and explanation without pretending the query succeeded.

        except Exception:  # Catches other unexpected errors that were not handled above.
            logging.getLogger(__name__).exception("Telemetry query failed: %s", tool)
            # Logs the tool name and exception details for debugging.

            return {
                "error": {
                    "code": "QUERY_FAILED",  # Gives the caller a general failure code.
                    "message": "query failed; this is not an empty result",
                    # Makes clear that a failure must not be interpreted as zero matching rows.
                }
            }  # Returns a safe error response rather than exposing internal exception details.