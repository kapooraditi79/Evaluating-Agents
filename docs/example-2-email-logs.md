# Example 2: find email error messages

> Find email ERROR messages containing "timed out" between 14:00 and 14:10. Send me two rows.

A **log** is a saved message from a service. **ERROR** is the message's severity: how serious the service says it is. **A row** is one line of results.

Read steps **1 to 10 in order**. Each **Data out** becomes the input to the function named under **Goes to**. Step 11 shows how the next-page marker becomes an input to another request. All example times are on **14 March 2026, UTC**.

Here is the route you will follow:

```text
AI sends inputs
  -> mcp_servers/telemetry/server.py: search_logs()
  -> mcp_servers/telemetry/engine.py: call()
       -> store/evidence.py: make a request ID -> back to engine.py
       -> store/parquet.py: query() finds matching messages
       <- engine.py receives all five matching rows
  <- server.py receives the chosen two rows
AI receives the reply
```

## Before the question: where do the saved messages enter?

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

`ParquetStore.__init__()` reads `spans.parquet`, `logs.parquet`, `metrics.parquet` and `histograms.parquet`. These are saved table files. This example uses the rows from **`logs.parquet`**.

**Data out:** `store.tables["logs"]` holds five saved messages. `engine.store` points to that store.

**Goes to:** step 1 when a request arrives. Later requests reuse the loaded data.

## 1. The AI chooses a tool and fills in the inputs

**Where:** the AI client, outside your server code.

**Function it calls:** `ClientSession.call_tool()` from the MCP library.

**Data in:** your question in ordinary words.

**What happens:** the AI chooses the tool name `search_logs` and fills in:

```json
{
  "query": {
    "service": "email",
    "severity": "ERROR",
    "contains": "timed out",
    "window": {
      "start": "2026-03-14T14:00:00Z",
      "end": "2026-03-14T14:10:00Z"
    },
    "limit": 2
  }
}
```

`window` means start and end time. `contains` is the text to find inside each message. `limit` means the maximum number of result rows to send back.

**Data out:** tool name `search_logs` and the inputs above.

**Goes to:** the MCP library. It carries the request to your server and checks the input rules in [contracts/queries.py](../contracts/queries.py#L49).

## 2. `server.py` receives the request

**File:** [mcp_servers/telemetry/server.py](../mcp_servers/telemetry/server.py#L59)

**Function:** `search_logs(query)`

**Data in:** a `SearchLogs` object: a checked container holding the fields from step 1.

**What happens:** these two actions are on one line:

```python
return engine.call("search_logs", query.model_dump())
```

`model_dump()` turns the container into a Python dictionary, meaning named fields with their values. The outer `query` box disappears. The optional fields have been filled in:

```python
{
    "service": "email",
    "severity": "ERROR",
    "contains": "timed out",
    "window": {
        "start": "2026-03-14T14:00:00Z",
        "end": "2026-03-14T14:10:00Z"
    },
    "limit": 2,
    "cursor": None,
    "trace_id": None
}
```

`cursor=None` means start at the first row. `trace_id=None` means we are not restricting the search to one particular request's trace.

**Data out:** `"search_logs"` and this dictionary.

**Goes to:** `ToolEngine.call()` in `engine.py`. The function in `server.py` waits for its answer.

## 3. `engine.py` checks the inputs

**File:** [mcp_servers/telemetry/engine.py](../mcp_servers/telemetry/engine.py#L48)

**Function:** `ToolEngine.call(tool, arguments)`

**Data in:** the tool name and dictionary from step 2.

**What happens:** it checks the tool exists and calls `SearchLogs.model_validate(arguments)`. `model_validate()` means "check these fields against the input rules."

The rules are in [contracts/queries.py](../contracts/queries.py#L49). The time checks use these functions from [contracts/models.py](../contracts/models.py#L21):

| Function | Receives | Produces |
|---|---|---|
| `Window.ordered()` | Start and end time | The same time range after checking start is earlier than end. |
| `utc_ns()` | Each time string | Start becomes `1773496800000000000`; end becomes `1773497400000000000`. These are the same times written as integer nanoseconds. |

**Data out:** `args`, a checked `SearchLogs` object containing the same request.

**Goes to:** step 4. The engine keeps `args` for the data lookup in step 5.

## 4. `evidence.py` gives this request a name

**Calling file:** [mcp_servers/telemetry/engine.py](../mcp_servers/telemetry/engine.py#L61)

**Helper file:** [store/evidence.py](../store/evidence.py#L13)

**Data in:** the dataset ID, tool version, tool name and checked request.

| Function | What it does | Data out -> next function |
|---|---|---|
| `canonical_query(...)` | Writes the request as consistently formatted text. It leaves out the page size and next-page marker. | Request text -> `QueryIds.get()` and `digest_query()`. |
| `QueryIds.get(request_text)` | Finds an existing short ID, or makes one for a new request. | `q8986b892` -> the engine saves it for the reply. |
| `digest_query(request_text)` | Makes a repeatable long string from the text. | A string starting `8986b892...` -> the engine uses it in the next-page marker. |

The output text includes the dataset ID, version `0.1.1`, tool `search_logs` and all the request fields except `limit` and `cursor`. Asking for another page still means the same search.

Smaller calls inside these functions:

- `args.model_dump()` supplies the fields.
- `Window.model_validate()`, `utc_ns()` and `iso_time()` check and consistently format the times. The last two are in `contracts/models.py`; they produce `2026-03-14T14:00:00Z` and `2026-03-14T14:10:00Z`.
- `json.dumps()` turns the fields into text.
- `digest_query()` calls `encode()`, `hashlib.sha256()` and `hexdigest()` to make the long string. It also runs inside `QueryIds.get()` when a new ID is needed.

**Data out:** request ID `q8986b892` and the long next-page string. The search fields themselves are unchanged.

**Goes to:** the engine saves the IDs and passes `args` to the store.

## 5. `parquet.py` finds matching messages

**File:** [store/parquet.py](../store/parquet.py#L247)

**Function:** `ParquetStore.query("search_logs", args)`

**Data in:** `args` from step 3 and the rows held in `self.tables["logs"]`.

**What happens:** `query()` calls `_window(args.window)` in the same file. `_window()` uses `utc_ns()` from `contracts/models.py` to check the requested and available times.

`_window()` returns `(1773496800000000000, 1773497400000000000)`: the requested 14:00 to 14:10 range. The start is included; the end is excluded.

The `search_logs` part of `query()` then keeps a message only if it:

1. Falls inside that time range.
2. Belongs to the `email` service.
3. Has severity `ERROR`.
4. Contains `timed out`. `casefold()` makes this text comparison ignore uppercase/lowercase differences.

**Data out:** five matching message dictionaries. The first is:

```python
{
    "ts_ns": 1773497375000000000,
    "service": "email",
    "severity": "ERROR",
    "body": "delivery attempt timed out; queued for retry",
    "trace_id": None,
    "span_id": None,
    "attributes": {}
}
```

`body` is the message text. `ts_ns` is its time as an integer. `trace_id` and `span_id` would link the log to a traced request, if present. They are missing here.

**Goes to:** the duplicate check inside the same `query()` function.

## 6. `parquet.py` counts duplicates and puts the messages in order

**File:** [store/parquet.py](../store/parquet.py)

**Function still running:** the `search_logs` part of `ParquetStore.query()`.

**Data in:** five matching dictionaries from step 5.

| Call or action | Data in | Data out |
|---|---|---|
| `json.dumps(row, sort_keys=True)` | One complete log dictionary | Text used to identify that exact log. |
| `unique.get(key)` | That text | An earlier copy if present, otherwise `None`. Each fixture log is new, so its count starts at `1`. |
| `sorted(..., key=lambda ...)` | The logs and their counts | Logs ordered by time. The small `lambda` function supplies `(time, service, span_id_or_empty, body)` as the sort order. |

Although all five logs have the same message text, their times differ. They are five different records, each with count `1`.

**Data out:** five ordered records, each with a duplicate count.

**Goes to:** the final row-building lines of `ParquetStore.query()`, still in the same file.

## 7. `parquet.py` returns all five matching rows

**File:** [store/parquet.py](../store/parquet.py)

**Function finishing:** `ParquetStore.query()`

**Data in:** the five ordered records.

**Data out:** column names, all five rows and `warnings=[]`, meaning no warnings. Here are the rows with readable times:

| Time | Service | Severity | Message | Count |
|---|---|---|---|---:|
| 14:09:35 | email | ERROR | delivery attempt timed out; queued for retry | 1 |
| 14:09:40 | email | ERROR | delivery attempt timed out; queued for retry | 1 |
| 14:09:45 | email | ERROR | delivery attempt timed out; queued for retry | 1 |
| 14:09:50 | email | ERROR | delivery attempt timed out; queued for retry | 1 |
| 14:09:55 | email | ERROR | delivery attempt timed out; queued for retry | 1 |

**Goes to:** this line back in `engine.py: ToolEngine.call()`:

```python
columns, all_rows, warnings = self.store.query(tool, args)
```

All five rows reach the engine. The next step chooses how many to send back.

## 8. `engine.py` chooses two rows and builds the reply

**File:** [mcp_servers/telemetry/engine.py](../mcp_servers/telemetry/engine.py#L79)

**Functions:** `ToolEngine.call()` and its inner helper, `envelope()`.

**Data in:** five rows, `limit=2`, request ID `q8986b892` and no warnings.

**What happens:** the engine takes the first two rows and gives them labels `L1` and `L2`. A label lets the AI refer to one result.

`envelope()` means "build the reply" in this code. It uses these checks from [contracts/models.py](../contracts/models.py#L252):

| Call | Data in | Data out |
|---|---|---|
| `TableData(...)` -> `rectangular()` | Column names and selected rows | A checked table: each row has the right number of values. |
| `ToolSource(...)` | Dataset ID and tool version | A record of where the answer came from. |
| `ToolResult(...)` -> `consistent()` | Table, IDs, counts and source | A checked reply. The table check runs again while building it. |
| `.model_dump()` | Checked reply | A Python dictionary ready to return. |

Then `compact_json()` in [store/evidence.py](../store/evidence.py#L70) writes the reply as text. `self.count()` in `engine.py` measures that text: 509 bytes after one row and 611 bytes after two. Both fit the default 1500-byte allowance.

`envelope()` and the size checks run after each added row, then again for the final reply. No warning objects are made because the warning list is empty.

**Data out:** two selected rows, their labels, counts and a marker for requesting the remaining rows.

**Goes to:** the waiting `search_logs()` function in `server.py`.

## 9. `server.py` returns the reply to the AI client

**File:** [mcp_servers/telemetry/server.py](../mcp_servers/telemetry/server.py#L59)

**Function finishing:** `search_logs()`

**Data in:** the reply dictionary from the engine.

**What happens:** its `return` passes that dictionary back to the MCP library, which carries it to the AI client.

**Data out:** the reply below. Read the `columns` list left to right to understand each row.

```json
{
  "data": {
    "columns": ["handle", "ts_ns", "service", "severity", "body", "trace_id", "span_id", "count"],
    "rows": [
      ["L1", 1773497375000000000, "email", "ERROR", "delivery attempt timed out; queued for retry", null, null, 1],
      ["L2", 1773497380000000000, "email", "ERROR", "delivery attempt timed out; queued for retry", null, null, 1]
    ]
  },
  "total_matches": 5,
  "returned": 2,
  "truncated": true,
  "next_cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:2",
  "query_id": "q8986b892",
  "source": {
    "backend": "parquet",
    "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
    "tool_version": "0.1.1"
  },
  "warnings": []
}
```

`returned=2`: two rows sent. `total_matches=5`: five rows exist. `truncated=true`: more rows remain. `next_cursor`: the next-page marker to include in another request. `null` is JSON's way of writing a missing value, like Python's `None`.

**Goes to:** the AI client, which reads the result.

## 10. The AI explains the result to you

**Where:** the AI client, outside your server code.

**Data in:** the two returned rows.

An AI could say:

> I found five matching error records. The first two are at 14:09:35 and 14:09:40. Both say delivery timed out and was queued for retry. Three more records are available.

**Data out:** an explanation for you, or another tool request if the AI needs more rows.

## 11. The next-page marker becomes a new input

Suppose the AI wants the next two logs.

**Data in:** the `next_cursor` string from step 9.

The AI repeats the inputs from step 1 and adds this field **inside `query`**:

```json
{
  "cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:2"
}
```

The request travels through `server.py` to `engine.py` as before. Here are the calls that change:

| Function or action | File | Data in -> data out |
|---|---|---|
| `canonical_query()` | `store/evidence.py` | Same search plus cursor -> same request text, because it leaves out the cursor. |
| `QueryIds.get()` | `store/evidence.py` | Same request text -> existing ID `q8986b892`. |
| `digest_query()` | `store/evidence.py` | Same request text -> same long ID string. |
| `args.cursor.split(":")` | Called in `engine.py` | Cursor -> long ID string and `"2"`. |
| `re.fullmatch(...)`, then `int("2")` | Called in `engine.py` | Text `"2"` -> a checked integer `2`. The engine also checks the long ID belongs to this search. |
| `ParquetStore.query()` | `store/parquet.py` | Same search -> the same five matching rows, found again. |
| `envelope()` and the size checks | `engine.py`, using `store/evidence.py` and `contracts/models.py` | Engine starts at row position 2 -> sends the third and fourth rows as `L3` and `L4`. |

**Data out:** `L3` at 14:09:45 and `L4` at 14:09:50. The query ID stays `q8986b892`. The next marker ends in `:4`, meaning the next request should skip the first four rows.

**Goes to:** `server.py: search_logs()`, then the MCP library, then the AI client, just as in steps 9 and 10.

## Optional: extra calls inside the MCP library

MCP lets an AI client call your Python tools. The following files are installed under `.venv/Lib/site-packages/`. Read this after the numbered steps if you want to follow the library itself.

| Direction | File under `site-packages` | Functions | Data in -> data out |
|---|---|---|---|
| In | `mcp/client/session.py`, `mcp/shared/session.py` | `ClientSession.call_tool()` -> `BaseSession.send_request()` | Tool name and inputs -> a request message with a number. |
| In | `mcp/client/stdio/__init__.py`, `mcp/server/stdio.py` | `stdin_writer()` -> `stdin_reader()` -> `JSONRPCMessage.model_validate_json()` | Request message -> text -> checked message on the server. |
| In | `mcp/shared/session.py`, `mcp/server/session.py` | `_receive_loop()` -> `_received_request()` -> `_handle_incoming()` | Checked message -> request ready to handle. |
| In | `mcp/server/lowlevel/server.py` | `_handle_message()` -> `_handle_request()` -> registered `handler()` -> `_get_cached_tool_definition()` | Request -> tool name, inputs and saved tool definition. |
| In | `mcp/server/fastmcp/server.py` | `FastMCP.call_tool()` -> `get_context()` | Name and inputs -> a call with information about this request. |
| In | `mcp/server/fastmcp/tools/tool_manager.py`, `mcp/server/fastmcp/tools/base.py` | `ToolManager.call_tool()` -> `get_tool()` -> `Tool.run()` | Name and inputs -> the saved tool function to run. |
| In | `mcp/server/fastmcp/utilities/func_metadata.py` | `call_fn_with_arg_validation()` -> `pre_parse_json()` -> input `.model_validate()` -> `model_dump_one_level()` | Input dictionary -> checked `SearchLogs` -> your `server.py: search_logs()`. |
| Out | `mcp/server/fastmcp/utilities/func_metadata.py` | `convert_result()` -> `_convert_to_content()`; output `.model_validate()` -> `.model_dump()` | Your reply -> a text copy and a checked dictionary copy. |
| Out | `mcp/server/lowlevel/server.py` | Registered `handler()` -> `jsonschema.validate()` | Those copies -> a checked `CallToolResult`. |
| Out | `mcp/shared/session.py`, `mcp/server/stdio.py` | `RequestResponder.respond()` -> `_send_response()` -> `stdout_writer()` | Result -> numbered response -> text sent to the client. |
| Out | `mcp/client/stdio/__init__.py`, `mcp/shared/session.py` | `stdout_reader()` -> `_receive_loop()` -> `_handle_response()` | Text -> response for the waiting client. |
| Out | `mcp/client/session.py` | `_validate_tool_result()`; `call_tool()` finishes | Response -> checked result. Its `structuredContent` holds the reply in step 9. |

Arrows in this table show the route of the data. Some library functions call helpers and then resume; they do not all directly call the next row. `pre_parse_json()` leaves our input unchanged. The library checks `Window.ordered()` before step 2, and the engine checks it again in step 3. This successful result has `isError=False`.

[Back to the starting page](telemetry-call-map.md)
