# Example 1: ask how slow the frontend was

> Show frontend p95 response time from 14:00 to 14:05. Send me two rows.

**Response time** means how long a request takes. **p95** estimates the time at or below which 95% of requests finish. **A row** is one line of results.

Read steps **1 to 10 in order**. Each **Data out** becomes the input to the function named under **Goes to**. All example times are on **14 March 2026, UTC**.

Here is the route you will follow:

```text
AI sends inputs
  -> mcp_servers/telemetry/server.py: query_metric()
  -> mcp_servers/telemetry/engine.py: call()
       -> store/evidence.py: make a request ID -> back to engine.py
       -> store/parquet.py: query()
            -> telemetry/histograms.py: percentile() -> back to parquet.py
       <- engine.py receives all calculated rows
  <- server.py receives the chosen two rows
AI receives the reply
```

## Before the question: where does the saved data enter?

**File:** [mcp_servers/telemetry/server.py](../mcp_servers/telemetry/server.py#L86)

**Function:** `main()`

**Data in:** the dataset folder passed through `--public-dir`. This is the folder containing your open [manifest.json](../fixtures/v0.1.1/public/856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb/manifest.json). That file describes the dataset and its available times.

`main()` makes these pieces in order:

| Call | File containing its code | What comes out |
|---|---|---|
| `ParquetStore(folder)` | [store/parquet.py](../store/parquet.py#L30) | An object holding the saved data in memory. Its `__init__()` reads the files. |
| `ToolEngine(store)` | [mcp_servers/telemetry/engine.py](../mcp_servers/telemetry/engine.py#L32) | The object that checks requests and prepares replies. It creates `QueryIds()` from `store/evidence.py` to remember request IDs. |
| `create_server(engine)` | [mcp_servers/telemetry/server.py](../mcp_servers/telemetry/server.py#L29) | A server with nine tools attached to it. |
| `server.run(transport="stdio")` | MCP library, called from `server.py` | A running server waiting for requests. `stdio` means messages travel through the program's input/output streams. |

`ParquetStore.__init__()` loads four table files: `spans.parquet`, `logs.parquet`, `metrics.parquet` and `histograms.parquet`. This example uses the loaded metrics and histograms. A **histogram** groups request times into ranges and records a count for each range.

**Data out:** `store.tables` holds the loaded rows. `engine.store` points to that store.

**Goes to:** step 1 when a request arrives. Later requests reuse the loaded data.

## 1. The AI chooses a tool and fills in the inputs

**Where:** the AI client, outside your server code.

**Function it calls:** `ClientSession.call_tool()` from the MCP library.

**Data in:** your question in ordinary words.

**What happens:** the AI chooses the tool name `query_metric` and fills in:

```json
{
  "query": {
    "service": "frontend",
    "metric": "latency_p95_ms",
    "window": {
      "start": "2026-03-14T14:00:00Z",
      "end": "2026-03-14T14:05:00Z"
    },
    "limit": 2
  }
}
```

`window` means start and end time. `limit` means the maximum number of result rows to send back. `latency_p95_ms` is the code's name for p95 response time in milliseconds.

**Data out:** tool name `query_metric` and the inputs above.

**Goes to:** the MCP library. It carries the request to your server and checks the input rules in [contracts/queries.py](../contracts/queries.py#L20).

## 2. `server.py` receives the request

**File:** [mcp_servers/telemetry/server.py](../mcp_servers/telemetry/server.py#L44)

**Function:** `query_metric(query)`

**Data in:** a `QueryMetric` object: a checked container holding the fields from step 1.

**What happens:** these two actions are on one line:

```python
return engine.call("query_metric", query.model_dump())
```

`model_dump()` turns the container into a Python dictionary, meaning named fields with their values. The outer `query` box disappears. Optional fields have been filled in:

```python
{
    "service": "frontend",
    "metric": "latency_p95_ms",
    "window": {
        "start": "2026-03-14T14:00:00Z",
        "end": "2026-03-14T14:05:00Z"
    },
    "limit": 2,
    "cursor": None,
    "operation": None,
    "step_seconds": 60,
    "aggregation": "avg"
}
```

`cursor=None` means start at the first row. `operation=None` includes all frontend operations. `step_seconds=60` also asks for one result per minute. The `aggregation` setting does not change this p95 calculation.

**Data out:** `"query_metric"` and this dictionary.

**Goes to:** `ToolEngine.call()` in `engine.py`. The function in `server.py` waits for its answer.

## 3. `engine.py` checks the inputs

**File:** [mcp_servers/telemetry/engine.py](../mcp_servers/telemetry/engine.py#L48)

**Function:** `ToolEngine.call(tool, arguments)`

**Data in:** the tool name and dictionary from step 2.

**What happens:** it checks the tool exists and calls `QueryMetric.model_validate(arguments)`. `model_validate()` means "check these fields against the input rules."

The rules are in [contracts/queries.py](../contracts/queries.py#L20). The time checks use these functions from [contracts/models.py](../contracts/models.py#L21):

| Function | Receives | Produces |
|---|---|---|
| `Window.ordered()` | Start and end time | The same time range after checking start is earlier than end. |
| `utc_ns()` | Each time string | The start becomes `1773496800000000000`; the end becomes `1773497100000000000`. These are the same times written as integer nanoseconds. |

**Data out:** `args`, a checked `QueryMetric` object containing the same request.

**Goes to:** step 4. The engine keeps `args` for the data lookup in step 5.

## 4. `evidence.py` gives this request a name

**Calling file:** [mcp_servers/telemetry/engine.py](../mcp_servers/telemetry/engine.py#L61)

**Helper file:** [store/evidence.py](../store/evidence.py#L13)

**Data in:** the dataset ID, tool version, tool name and checked request.

| Function | What it does | Data out -> next function |
|---|---|---|
| `canonical_query(...)` | Writes the request as consistently formatted text. It leaves out the page size and next-page marker. | Request text -> `QueryIds.get()` and `digest_query()`. |
| `QueryIds.get(request_text)` | Finds an existing short ID, or makes one for a new request. | `q4e6231a4` -> the engine saves it for the reply. |
| `digest_query(request_text)` | Makes a repeatable long string from the text. | A string starting `4e6231a4...` -> the engine uses it in the next-page marker. |

The output text includes the dataset ID, version `0.1.1`, tool `query_metric` and all the request fields except `limit` and `cursor`. Asking for a different page still means the same question, so it keeps the same identity.

Smaller calls inside these functions:

- `args.model_dump()` supplies the fields.
- `Window.model_validate()`, `utc_ns()` and `iso_time()` check and consistently format the times. The last two are in `contracts/models.py`; they produce `2026-03-14T14:00:00Z` and `2026-03-14T14:05:00Z`.
- `json.dumps()` turns the fields into text.
- `digest_query()` calls `encode()`, `hashlib.sha256()` and `hexdigest()` to make the long string. It also runs inside `QueryIds.get()` when a new ID is needed.

**Data out:** request ID `q4e6231a4` and the long next-page string. The request fields themselves are unchanged.

**Goes to:** the engine saves the IDs and passes `args` to the store.

## 5. `parquet.py` chooses the right data

**File:** [store/parquet.py](../store/parquet.py#L247)

**Function:** `ParquetStore.query("query_metric", args)`

**Data in:** `args` from step 3, plus the rows already held in `self.tables`.

**What happens:** `query()` selects its `query_metric` part of the code. It checks the service exists, then calls these helpers in the same file:

| Function | Data in | Data out |
|---|---|---|
| `_window(args.window)` | 14:00 to 14:05 | The integer start/end pair from step 3, after checking those times are available. |
| `_window(args.window, aligned=True)` | Same time range | Same pair, after checking it fits the saved 10-second intervals. |
| `_gaps(...)` -> `_missing_buckets(...)` | Frontend, requested metric and time bounds | `_missing_buckets()` returns `0`. `_gaps()` returns `False`: no required interval is missing. |

**Data out:** checked time bounds, selected service and `warnings=[]`, meaning no warnings.

**Goes to:** `point()` inside the same `query()` function, to build a whole-period result and then a result for each minute.

## 6. `histograms.py` calculates p95

**Starting file:** [store/parquet.py](../store/parquet.py#L305)

**Starting function:** `point("summary", start, end)`

**Data in:** the full five-minute period and frontend selection.

| Call, in order | File | Data in -> data out |
|---|---|---|
| `point()` calls `_metric_value()` | `store/parquet.py` | Service, metric and time bounds -> selected saved histogram rows. |
| `_metric_value()` adds their counts | `store/parquet.py` | Selected rows -> combined counts for 300 requests, passed to `percentile()`. |
| `percentile()` calls `validate_bounds()` | [telemetry/histograms.py](../telemetry/histograms.py#L26) | Response-time range limits -> `None`, meaning the checks passed. |
| `percentile()` finishes | `telemetry/histograms.py` | Counts, ranges and `0.95` -> `(120.0, 40.0)`. |
| `_metric_value()` returns | `store/parquet.py` | That pair -> the same pair, sent back to `point()`. |
| `point()` returns a row | `store/parquet.py` | That pair, times and unit -> `['summary', start, end, 120.0, 40.0, 'ms']`. |

`120.0` means an estimated p95 of 120 ms. `40.0` is the possible estimation error from using saved ranges.

The arithmetic: 95% of 300 is 285. The 285th request falls in the range from 80 to 160 ms. The code uses the middle, 120 ms, with half the range width, 40 ms, as its possible error.

**Data out:** one summary row.

**Goes to:** the `rows` list in `ParquetStore.query()`. These same calls repeat for each of the five minutes.

## 7. `parquet.py` returns all six calculated rows

**File:** [store/parquet.py](../store/parquet.py#L247)

**Function finishing:** `ParquetStore.query()`

**Data in:** the summary row and five minute rows.

**Data out:** column names, six rows and `warnings=[]`. Here are those rows with the integer times written as readable times:

| Kind | Start | End | p95, ms | Possible estimation error, ms |
|---|---|---|---:|---:|
| summary | 14:00 | 14:05 | 120 | 40 |
| bucket | 14:00 | 14:01 | 120 | 40 |
| bucket | 14:01 | 14:02 | 120 | 40 |
| bucket | 14:02 | 14:03 | 120 | 40 |
| bucket | 14:03 | 14:04 | 120 | 40 |
| bucket | 14:04 | 14:05 | 1920 | 640 |

`summary` means the whole period. `bucket` means a smaller time interval: one minute here.

**Goes to:** this line back in `engine.py: ToolEngine.call()`:

```python
columns, all_rows, warnings = self.store.query(tool, args)
```

The store calculates all six rows. The next step chooses how many to send back.

## 8. `engine.py` chooses two rows and builds the reply

**File:** [mcp_servers/telemetry/engine.py](../mcp_servers/telemetry/engine.py#L79)

**Functions:** `ToolEngine.call()` and its inner helper, `envelope()`.

**Data in:** six rows, `limit=2`, request ID `q4e6231a4` and no warnings.

**What happens:** the engine takes the first two rows and gives them labels `M1` and `M2`. A label lets the AI refer to one result.

`envelope()` means "build the reply" in this code. It uses these checks from [contracts/models.py](../contracts/models.py#L252):

| Call | Data in | Data out |
|---|---|---|
| `TableData(...)` -> `rectangular()` | Column names and selected rows | A checked table: each row has the right number of values. |
| `ToolSource(...)` | Dataset ID and tool version | A record of where the answer came from. |
| `ToolResult(...)` -> `consistent()` | Table, IDs, counts and source | A checked reply. The table check runs again while building it. |
| `.model_dump()` | Checked reply | A Python dictionary ready to return. |

Then `compact_json()` in [store/evidence.py](../store/evidence.py#L70) writes the reply as text. `self.count()` in `engine.py` measures that text: 480 bytes after one row and 552 bytes after two. Both fit the default 1500-byte allowance.

`envelope()` and the size checks run after each added row, then again for the final reply. No warning objects are made because the warning list is empty.

**Data out:** two selected rows, their labels, counts and a marker for requesting the remaining rows.

**Goes to:** the waiting `query_metric()` function in `server.py`.

## 9. `server.py` returns the reply to the AI client

**File:** [mcp_servers/telemetry/server.py](../mcp_servers/telemetry/server.py#L44)

**Function finishing:** `query_metric()`

**Data in:** the reply dictionary from the engine.

**What happens:** its `return` passes that dictionary back to the MCP library, which carries it to the AI client.

**Data out:** the reply below. Read the `columns` list left to right to understand each row.

```json
{
  "data": {
    "columns": ["handle", "kind", "start_ns", "end_ns", "value", "absolute_error_bound", "unit"],
    "rows": [
      ["M1", "summary", 1773496800000000000, 1773497100000000000, 120.0, 40.0, "ms"],
      ["M2", "bucket", 1773496800000000000, 1773496860000000000, 120.0, 40.0, "ms"]
    ]
  },
  "total_matches": 6,
  "returned": 2,
  "truncated": true,
  "next_cursor": "4e6231a4fa2bc2925490d28c0ebc84335601f75441a9c2aa9d27b6b867525692:2",
  "query_id": "q4e6231a4",
  "source": {
    "backend": "parquet",
    "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
    "tool_version": "0.1.1"
  },
  "warnings": []
}
```

`returned=2`: two rows sent. `total_matches=6`: six rows exist. `truncated=true`: more rows remain. `next_cursor`: the next-page marker to include in another request.

**Goes to:** the AI client, which reads the result.

## 10. The AI explains the result to you

**Where:** the AI client, outside your server code.

**Data in:** the two returned rows.

An AI could say:

> The estimated p95 for the five-minute period is 120 ms. The first minute is also 120 ms. Four more rows are available.

The slow final minute, 1920 ms, was calculated in step 7 but was not included in this two-row reply. The AI must request another page to see it.

**Data out:** an explanation for you, or another tool request if the AI needs more rows.

## Optional: extra calls inside the MCP library

MCP lets an AI client call your Python tools. The following files are installed under `.venv/Lib/site-packages/`. Read this after the ten steps if you want to follow the library itself.

| Direction | File under `site-packages` | Functions | Data in -> data out |
|---|---|---|---|
| In | `mcp/client/session.py`, `mcp/shared/session.py` | `ClientSession.call_tool()` -> `BaseSession.send_request()` | Tool name and inputs -> a request message with a number. |
| In | `mcp/client/stdio/__init__.py`, `mcp/server/stdio.py` | `stdin_writer()` -> `stdin_reader()` -> `JSONRPCMessage.model_validate_json()` | Request message -> text -> checked message on the server. |
| In | `mcp/shared/session.py`, `mcp/server/session.py` | `_receive_loop()` -> `_received_request()` -> `_handle_incoming()` | Checked message -> request ready to handle. |
| In | `mcp/server/lowlevel/server.py` | `_handle_message()` -> `_handle_request()` -> registered `handler()` -> `_get_cached_tool_definition()` | Request -> tool name, inputs and saved tool definition. |
| In | `mcp/server/fastmcp/server.py` | `FastMCP.call_tool()` -> `get_context()` | Name and inputs -> a call with information about this request. |
| In | `mcp/server/fastmcp/tools/tool_manager.py`, `mcp/server/fastmcp/tools/base.py` | `ToolManager.call_tool()` -> `get_tool()` -> `Tool.run()` | Name and inputs -> the saved tool function to run. |
| In | `mcp/server/fastmcp/utilities/func_metadata.py` | `call_fn_with_arg_validation()` -> `pre_parse_json()` -> input `.model_validate()` -> `model_dump_one_level()` | Input dictionary -> checked `QueryMetric` -> your `server.py: query_metric()`. |
| Out | `mcp/server/fastmcp/utilities/func_metadata.py` | `convert_result()` -> `_convert_to_content()`; output `.model_validate()` -> `.model_dump()` | Your reply -> a text copy and a checked dictionary copy. |
| Out | `mcp/server/lowlevel/server.py` | Registered `handler()` -> `jsonschema.validate()` | Those copies -> a checked `CallToolResult`. |
| Out | `mcp/shared/session.py`, `mcp/server/stdio.py` | `RequestResponder.respond()` -> `_send_response()` -> `stdout_writer()` | Result -> numbered response -> text sent to the client. |
| Out | `mcp/client/stdio/__init__.py`, `mcp/shared/session.py` | `stdout_reader()` -> `_receive_loop()` -> `_handle_response()` | Text -> response for the waiting client. |
| Out | `mcp/client/session.py` | `_validate_tool_result()`; `call_tool()` finishes | Response -> checked result. Its `structuredContent` holds the reply in step 9. |

Arrows in this table show the route of the data. Some library functions call helpers and then resume; they do not all directly call the next row. `pre_parse_json()` leaves our input unchanged. The library checks `Window.ordered()` before step 2, and the engine checks it again in step 3. This successful result has `isError=False`.

[Back to the starting page](telemetry-call-map.md)
