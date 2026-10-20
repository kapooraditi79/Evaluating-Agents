# search_logs-2: function inputs and outputs

Captured during a real stdio MCP request. Calls are listed in entry order; the output of an outer call is produced after its nested calls complete. The call number matches the raw calls.txt file. Expand a function to inspect its exact data. Infrastructure objects are described by type; model objects are shown as JSON. Python constructors return None; constructed_object shows the resulting model. Repeated generator-expression events are in stages.json and calls.txt.

<details>

<summary>Call 1: mcp.server.lowlevel.server.Server.call_tool.&lt;locals&gt;.decorator.&lt;locals&gt;.handler</summary>

Source: `.\.venv\Lib\site-packages\mcp\server\lowlevel\server.py`, line 521.

```json
{
  "call": 1,
  "parent_call": null,
  "function": "mcp.server.lowlevel.server.Server.call_tool.<locals>.decorator.<locals>.handler",
  "source": ".\\.venv\\Lib\\site-packages\\mcp\\server\\lowlevel\\server.py",
  "line": 521,
  "inputs": {
    "req": {
      "method": "tools/call",
      "params": {
        "task": null,
        "meta": null,
        "name": "search_logs",
        "arguments": {
          "query": {
            "window": {
              "start": "2026-03-14T14:00:00Z",
              "end": "2026-03-14T14:10:00Z"
            },
            "service": "email",
            "severity": "ERROR",
            "contains": "timed out",
            "limit": 2,
            "cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:2"
          }
        }
      },
      "jsonrpc": "2.0",
      "id": 4
    },
    "self": "<mcp.server.lowlevel.server.Server>"
  },
  "closure_values": {
    "func": "<builtins.method>",
    "self": "<mcp.server.lowlevel.server.Server>",
    "validate_input": false
  },
  "output": {
    "meta": null,
    "content": [
      {
        "type": "text",
        "text": "{\n  \"data\": {\n    \"columns\": [\n      \"handle\",\n      \"ts_ns\",\n      \"service\",\n      \"severity\",\n      \"body\",\n      \"trace_id\",\n      \"span_id\",\n      \"count\"\n    ],\n    \"rows\": [\n      [\n        \"L3\",\n        1773497385000000000,\n        \"email\",\n        \"ERROR\",\n        \"delivery attempt timed out; queued for retry\",\n        null,\n        null,\n        1\n      ],\n      [\n        \"L4\",\n        1773497390000000000,\n        \"email\",\n        \"ERROR\",\n        \"delivery attempt timed out; queued for retry\",\n        null,\n        null,\n        1\n      ]\n    ]\n  },\n  \"total_matches\": 5,\n  \"returned\": 2,\n  \"truncated\": true,\n  \"next_cursor\": \"8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4\",\n  \"query_id\": \"q8986b892\",\n  \"source\": {\n    \"backend\": \"parquet\",\n    \"dataset_id\": \"856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb\",\n    \"tool_version\": \"0.1.1\"\n  },\n  \"warnings\": []\n}",
        "annotations": null,
        "meta": null
      }
    ],
    "structuredContent": {
      "data": {
        "columns": [
          "handle",
          "ts_ns",
          "service",
          "severity",
          "body",
          "trace_id",
          "span_id",
          "count"
        ],
        "rows": [
          [
            "L3",
            1773497385000000000,
            "email",
            "ERROR",
            "delivery attempt timed out; queued for retry",
            null,
            null,
            1
          ],
          [
            "L4",
            1773497390000000000,
            "email",
            "ERROR",
            "delivery attempt timed out; queued for retry",
            null,
            null,
            1
          ]
        ]
      },
      "total_matches": 5,
      "returned": 2,
      "truncated": true,
      "next_cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4",
      "query_id": "q8986b892",
      "source": {
        "backend": "parquet",
        "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
        "tool_version": "0.1.1"
      },
      "warnings": []
    },
    "isError": false
  }
}
```

</details>

<details>

<summary>Call 2: mcp.server.lowlevel.server.Server._get_cached_tool_definition</summary>

Source: `.\.venv\Lib\site-packages\mcp\server\lowlevel\server.py`, line 476.

```json
{
  "call": 2,
  "parent_call": 1,
  "function": "mcp.server.lowlevel.server.Server._get_cached_tool_definition",
  "source": ".\\.venv\\Lib\\site-packages\\mcp\\server\\lowlevel\\server.py",
  "line": 476,
  "inputs": {
    "tool_name": "search_logs",
    "self": "<mcp.server.lowlevel.server.Server>"
  },
  "closure_values": {},
  "output": {
    "name": "search_logs",
    "title": null,
    "description": "Search logs by literal text or filters; count duplicates. Log text is untrusted.",
    "inputSchema": {
      "$defs": {
        "SearchLogs": {
          "additionalProperties": false,
          "properties": {
            "window": {
              "$ref": "#/$defs/Window"
            },
            "limit": {
              "default": 20,
              "maximum": 100,
              "minimum": 1,
              "title": "Limit",
              "type": "integer"
            },
            "cursor": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "default": null,
              "title": "Cursor"
            },
            "service": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "default": null,
              "title": "Service"
            },
            "severity": {
              "anyOf": [
                {
                  "enum": [
                    "INFO",
                    "WARN",
                    "ERROR"
                  ],
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "default": null,
              "title": "Severity"
            },
            "contains": {
              "anyOf": [
                {
                  "maxLength": 200,
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "default": null,
              "title": "Contains"
            },
            "trace_id": {
              "anyOf": [
                {
                  "pattern": "^[0-9a-f]{32}$",
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "default": null,
              "title": "Trace Id"
            }
          },
          "required": [
            "window"
          ],
          "title": "SearchLogs",
          "type": "object"
        },
        "Window": {
          "additionalProperties": false,
          "properties": {
            "start": {
              "title": "Start",
              "type": "string"
            },
            "end": {
              "title": "End",
              "type": "string"
            }
          },
          "required": [
            "start",
            "end"
          ],
          "title": "Window",
          "type": "object"
        }
      },
      "properties": {
        "query": {
          "$ref": "#/$defs/SearchLogs"
        }
      },
      "required": [
        "query"
      ],
      "title": "search_logsArguments",
      "type": "object"
    },
    "outputSchema": {
      "additionalProperties": true,
      "title": "search_logsDictOutput",
      "type": "object"
    },
    "icons": null,
    "annotations": {
      "title": null,
      "readOnlyHint": true,
      "destructiveHint": false,
      "idempotentHint": true,
      "openWorldHint": false
    },
    "meta": null,
    "execution": null
  }
}
```

</details>

<details>

<summary>Call 4: mcp.server.fastmcp.server.FastMCP.call_tool</summary>

Source: `.\.venv\Lib\site-packages\mcp\server\fastmcp\server.py`, line 343.

```json
{
  "call": 4,
  "parent_call": 1,
  "function": "mcp.server.fastmcp.server.FastMCP.call_tool",
  "source": ".\\.venv\\Lib\\site-packages\\mcp\\server\\fastmcp\\server.py",
  "line": 343,
  "inputs": {
    "name": "search_logs",
    "arguments": {
      "query": {
        "window": {
          "start": "2026-03-14T14:00:00Z",
          "end": "2026-03-14T14:10:00Z"
        },
        "service": "email",
        "severity": "ERROR",
        "contains": "timed out",
        "limit": 2,
        "cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:2"
      }
    },
    "self": "<mcp.server.fastmcp.server.FastMCP>"
  },
  "closure_values": {},
  "output": [
    [
      {
        "type": "text",
        "text": "{\n  \"data\": {\n    \"columns\": [\n      \"handle\",\n      \"ts_ns\",\n      \"service\",\n      \"severity\",\n      \"body\",\n      \"trace_id\",\n      \"span_id\",\n      \"count\"\n    ],\n    \"rows\": [\n      [\n        \"L3\",\n        1773497385000000000,\n        \"email\",\n        \"ERROR\",\n        \"delivery attempt timed out; queued for retry\",\n        null,\n        null,\n        1\n      ],\n      [\n        \"L4\",\n        1773497390000000000,\n        \"email\",\n        \"ERROR\",\n        \"delivery attempt timed out; queued for retry\",\n        null,\n        null,\n        1\n      ]\n    ]\n  },\n  \"total_matches\": 5,\n  \"returned\": 2,\n  \"truncated\": true,\n  \"next_cursor\": \"8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4\",\n  \"query_id\": \"q8986b892\",\n  \"source\": {\n    \"backend\": \"parquet\",\n    \"dataset_id\": \"856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb\",\n    \"tool_version\": \"0.1.1\"\n  },\n  \"warnings\": []\n}",
        "annotations": null,
        "meta": null
      }
    ],
    {
      "data": {
        "columns": [
          "handle",
          "ts_ns",
          "service",
          "severity",
          "body",
          "trace_id",
          "span_id",
          "count"
        ],
        "rows": [
          [
            "L3",
            1773497385000000000,
            "email",
            "ERROR",
            "delivery attempt timed out; queued for retry",
            null,
            null,
            1
          ],
          [
            "L4",
            1773497390000000000,
            "email",
            "ERROR",
            "delivery attempt timed out; queued for retry",
            null,
            null,
            1
          ]
        ]
      },
      "total_matches": 5,
      "returned": 2,
      "truncated": true,
      "next_cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4",
      "query_id": "q8986b892",
      "source": {
        "backend": "parquet",
        "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
        "tool_version": "0.1.1"
      },
      "warnings": []
    }
  ]
}
```

</details>

<details>

<summary>Call 5: mcp.server.fastmcp.server.FastMCP.get_context</summary>

Source: `.\.venv\Lib\site-packages\mcp\server\fastmcp\server.py`, line 332.

```json
{
  "call": 5,
  "parent_call": 4,
  "function": "mcp.server.fastmcp.server.FastMCP.get_context",
  "source": ".\\.venv\\Lib\\site-packages\\mcp\\server\\fastmcp\\server.py",
  "line": 332,
  "inputs": {
    "self": "<mcp.server.fastmcp.server.FastMCP>"
  },
  "closure_values": {},
  "output": {}
}
```

</details>

<details>

<summary>Call 8: mcp.server.fastmcp.server.Context.__init__</summary>

Source: `.\.venv\Lib\site-packages\mcp\server\fastmcp\server.py`, line 1135.

```json
{
  "call": 8,
  "parent_call": 5,
  "function": "mcp.server.fastmcp.server.Context.__init__",
  "source": ".\\.venv\\Lib\\site-packages\\mcp\\server\\fastmcp\\server.py",
  "line": 1135,
  "inputs": {
    "request_context": "<mcp.shared.context.RequestContext>",
    "fastmcp": "<mcp.server.fastmcp.server.FastMCP>",
    "kwargs": {},
    "self": {}
  },
  "closure_values": {
    "__class__": "<class mcp.server.fastmcp.server.Context>"
  },
  "output": null,
  "constructed_object": {}
}
```

</details>

<details>

<summary>Call 9: pydantic.main.BaseModel.__init__</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 253.

```json
{
  "call": 9,
  "parent_call": 8,
  "function": "pydantic.main.BaseModel.__init__",
  "source": ".\\.venv\\Lib\\site-packages\\pydantic\\main.py",
  "line": 253,
  "inputs": {
    "data": {},
    "self": {}
  },
  "closure_values": {},
  "output": null,
  "constructed_object": {}
}
```

</details>

<details>

<summary>Call 34: mcp.server.fastmcp.tools.tool_manager.ToolManager.call_tool</summary>

Source: `.\.venv\Lib\site-packages\mcp\server\fastmcp\tools\tool_manager.py`, line 81.

```json
{
  "call": 34,
  "parent_call": 4,
  "function": "mcp.server.fastmcp.tools.tool_manager.ToolManager.call_tool",
  "source": ".\\.venv\\Lib\\site-packages\\mcp\\server\\fastmcp\\tools\\tool_manager.py",
  "line": 81,
  "inputs": {
    "name": "search_logs",
    "arguments": {
      "query": {
        "window": {
          "start": "2026-03-14T14:00:00Z",
          "end": "2026-03-14T14:10:00Z"
        },
        "service": "email",
        "severity": "ERROR",
        "contains": "timed out",
        "limit": 2,
        "cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:2"
      }
    },
    "context": {},
    "convert_result": true,
    "self": "<mcp.server.fastmcp.tools.tool_manager.ToolManager>"
  },
  "closure_values": {},
  "output": [
    [
      {
        "type": "text",
        "text": "{\n  \"data\": {\n    \"columns\": [\n      \"handle\",\n      \"ts_ns\",\n      \"service\",\n      \"severity\",\n      \"body\",\n      \"trace_id\",\n      \"span_id\",\n      \"count\"\n    ],\n    \"rows\": [\n      [\n        \"L3\",\n        1773497385000000000,\n        \"email\",\n        \"ERROR\",\n        \"delivery attempt timed out; queued for retry\",\n        null,\n        null,\n        1\n      ],\n      [\n        \"L4\",\n        1773497390000000000,\n        \"email\",\n        \"ERROR\",\n        \"delivery attempt timed out; queued for retry\",\n        null,\n        null,\n        1\n      ]\n    ]\n  },\n  \"total_matches\": 5,\n  \"returned\": 2,\n  \"truncated\": true,\n  \"next_cursor\": \"8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4\",\n  \"query_id\": \"q8986b892\",\n  \"source\": {\n    \"backend\": \"parquet\",\n    \"dataset_id\": \"856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb\",\n    \"tool_version\": \"0.1.1\"\n  },\n  \"warnings\": []\n}",
        "annotations": null,
        "meta": null
      }
    ],
    {
      "data": {
        "columns": [
          "handle",
          "ts_ns",
          "service",
          "severity",
          "body",
          "trace_id",
          "span_id",
          "count"
        ],
        "rows": [
          [
            "L3",
            1773497385000000000,
            "email",
            "ERROR",
            "delivery attempt timed out; queued for retry",
            null,
            null,
            1
          ],
          [
            "L4",
            1773497390000000000,
            "email",
            "ERROR",
            "delivery attempt timed out; queued for retry",
            null,
            null,
            1
          ]
        ]
      },
      "total_matches": 5,
      "returned": 2,
      "truncated": true,
      "next_cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4",
      "query_id": "q8986b892",
      "source": {
        "backend": "parquet",
        "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
        "tool_version": "0.1.1"
      },
      "warnings": []
    }
  ]
}
```

</details>

<details>

<summary>Call 35: mcp.server.fastmcp.tools.tool_manager.ToolManager.get_tool</summary>

Source: `.\.venv\Lib\site-packages\mcp\server\fastmcp\tools\tool_manager.py`, line 37.

```json
{
  "call": 35,
  "parent_call": 34,
  "function": "mcp.server.fastmcp.tools.tool_manager.ToolManager.get_tool",
  "source": ".\\.venv\\Lib\\site-packages\\mcp\\server\\fastmcp\\tools\\tool_manager.py",
  "line": 37,
  "inputs": {
    "name": "search_logs",
    "self": "<mcp.server.fastmcp.tools.tool_manager.ToolManager>"
  },
  "closure_values": {},
  "output": "<mcp.server.fastmcp.tools.base.Tool>"
}
```

</details>

<details>

<summary>Call 37: mcp.server.fastmcp.tools.base.Tool.run</summary>

Source: `.\.venv\Lib\site-packages\mcp\server\fastmcp\tools\base.py`, line 93.

```json
{
  "call": 37,
  "parent_call": 34,
  "function": "mcp.server.fastmcp.tools.base.Tool.run",
  "source": ".\\.venv\\Lib\\site-packages\\mcp\\server\\fastmcp\\tools\\base.py",
  "line": 93,
  "inputs": {
    "arguments": {
      "query": {
        "window": {
          "start": "2026-03-14T14:00:00Z",
          "end": "2026-03-14T14:10:00Z"
        },
        "service": "email",
        "severity": "ERROR",
        "contains": "timed out",
        "limit": 2,
        "cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:2"
      }
    },
    "context": {},
    "convert_result": true,
    "self": "<mcp.server.fastmcp.tools.base.Tool>"
  },
  "closure_values": {},
  "output": [
    [
      {
        "type": "text",
        "text": "{\n  \"data\": {\n    \"columns\": [\n      \"handle\",\n      \"ts_ns\",\n      \"service\",\n      \"severity\",\n      \"body\",\n      \"trace_id\",\n      \"span_id\",\n      \"count\"\n    ],\n    \"rows\": [\n      [\n        \"L3\",\n        1773497385000000000,\n        \"email\",\n        \"ERROR\",\n        \"delivery attempt timed out; queued for retry\",\n        null,\n        null,\n        1\n      ],\n      [\n        \"L4\",\n        1773497390000000000,\n        \"email\",\n        \"ERROR\",\n        \"delivery attempt timed out; queued for retry\",\n        null,\n        null,\n        1\n      ]\n    ]\n  },\n  \"total_matches\": 5,\n  \"returned\": 2,\n  \"truncated\": true,\n  \"next_cursor\": \"8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4\",\n  \"query_id\": \"q8986b892\",\n  \"source\": {\n    \"backend\": \"parquet\",\n    \"dataset_id\": \"856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb\",\n    \"tool_version\": \"0.1.1\"\n  },\n  \"warnings\": []\n}",
        "annotations": null,
        "meta": null
      }
    ],
    {
      "data": {
        "columns": [
          "handle",
          "ts_ns",
          "service",
          "severity",
          "body",
          "trace_id",
          "span_id",
          "count"
        ],
        "rows": [
          [
            "L3",
            1773497385000000000,
            "email",
            "ERROR",
            "delivery attempt timed out; queued for retry",
            null,
            null,
            1
          ],
          [
            "L4",
            1773497390000000000,
            "email",
            "ERROR",
            "delivery attempt timed out; queued for retry",
            null,
            null,
            1
          ]
        ]
      },
      "total_matches": 5,
      "returned": 2,
      "truncated": true,
      "next_cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4",
      "query_id": "q8986b892",
      "source": {
        "backend": "parquet",
        "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
        "tool_version": "0.1.1"
      },
      "warnings": []
    }
  ]
}
```

</details>

<details>

<summary>Call 38: mcp.server.fastmcp.utilities.func_metadata.FuncMetadata.call_fn_with_arg_validation</summary>

Source: `.\.venv\Lib\site-packages\mcp\server\fastmcp\utilities\func_metadata.py`, line 74.

```json
{
  "call": 38,
  "parent_call": 37,
  "function": "mcp.server.fastmcp.utilities.func_metadata.FuncMetadata.call_fn_with_arg_validation",
  "source": ".\\.venv\\Lib\\site-packages\\mcp\\server\\fastmcp\\utilities\\func_metadata.py",
  "line": 74,
  "inputs": {
    "fn": "<builtins.function>",
    "fn_is_async": false,
    "arguments_to_validate": {
      "query": {
        "window": {
          "start": "2026-03-14T14:00:00Z",
          "end": "2026-03-14T14:10:00Z"
        },
        "service": "email",
        "severity": "ERROR",
        "contains": "timed out",
        "limit": 2,
        "cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:2"
      }
    },
    "arguments_to_pass_directly": null,
    "self": "<mcp.server.fastmcp.utilities.func_metadata.FuncMetadata>"
  },
  "closure_values": {},
  "output": {
    "data": {
      "columns": [
        "handle",
        "ts_ns",
        "service",
        "severity",
        "body",
        "trace_id",
        "span_id",
        "count"
      ],
      "rows": [
        [
          "L3",
          1773497385000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ],
        [
          "L4",
          1773497390000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ]
      ]
    },
    "total_matches": 5,
    "returned": 2,
    "truncated": true,
    "next_cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4",
    "query_id": "q8986b892",
    "source": {
      "backend": "parquet",
      "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
      "tool_version": "0.1.1"
    },
    "warnings": []
  }
}
```

</details>

<details>

<summary>Call 39: mcp.server.fastmcp.utilities.func_metadata.FuncMetadata.pre_parse_json</summary>

Source: `.\.venv\Lib\site-packages\mcp\server\fastmcp\utilities\func_metadata.py`, line 133.

```json
{
  "call": 39,
  "parent_call": 38,
  "function": "mcp.server.fastmcp.utilities.func_metadata.FuncMetadata.pre_parse_json",
  "source": ".\\.venv\\Lib\\site-packages\\mcp\\server\\fastmcp\\utilities\\func_metadata.py",
  "line": 133,
  "inputs": {
    "data": {
      "query": {
        "window": {
          "start": "2026-03-14T14:00:00Z",
          "end": "2026-03-14T14:10:00Z"
        },
        "service": "email",
        "severity": "ERROR",
        "contains": "timed out",
        "limit": 2,
        "cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:2"
      }
    },
    "self": "<mcp.server.fastmcp.utilities.func_metadata.FuncMetadata>"
  },
  "closure_values": {},
  "output": {
    "query": {
      "window": {
        "start": "2026-03-14T14:00:00Z",
        "end": "2026-03-14T14:10:00Z"
      },
      "service": "email",
      "severity": "ERROR",
      "contains": "timed out",
      "limit": 2,
      "cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:2"
    }
  }
}
```

</details>

<details>

<summary>Call 49: pydantic.main.BaseModel.model_validate</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 693.

```json
{
  "call": 49,
  "parent_call": 38,
  "function": "pydantic.main.BaseModel.model_validate",
  "source": ".\\.venv\\Lib\\site-packages\\pydantic\\main.py",
  "line": 693,
  "inputs": {
    "obj": {
      "query": {
        "window": {
          "start": "2026-03-14T14:00:00Z",
          "end": "2026-03-14T14:10:00Z"
        },
        "service": "email",
        "severity": "ERROR",
        "contains": "timed out",
        "limit": 2,
        "cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:2"
      }
    },
    "strict": null,
    "extra": null,
    "from_attributes": null,
    "context": null,
    "by_alias": null,
    "by_name": null,
    "cls": "<class mcp.server.fastmcp.utilities.func_metadata.search_logsArguments>"
  },
  "closure_values": {},
  "output": {
    "query": {
      "window": {
        "start": "2026-03-14T14:00:00Z",
        "end": "2026-03-14T14:10:00Z"
      },
      "limit": 2,
      "cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:2",
      "service": "email",
      "severity": "ERROR",
      "contains": "timed out",
      "trace_id": null
    }
  }
}
```

</details>

<details>

<summary>Call 51: contracts.models.Window.ordered</summary>

Source: `.\contracts\models.py`, line 45.

```json
{
  "call": 51,
  "parent_call": 50,
  "function": "contracts.models.Window.ordered",
  "source": ".\\contracts\\models.py",
  "line": 45,
  "inputs": {
    "self": {
      "start": "2026-03-14T14:00:00Z",
      "end": "2026-03-14T14:10:00Z"
    }
  },
  "closure_values": {},
  "output": {
    "start": "2026-03-14T14:00:00Z",
    "end": "2026-03-14T14:10:00Z"
  }
}
```

</details>

<details>

<summary>Call 52: contracts.models.utc_ns</summary>

Source: `.\contracts\models.py`, line 21.

```json
{
  "call": 52,
  "parent_call": 51,
  "function": "contracts.models.utc_ns",
  "source": ".\\contracts\\models.py",
  "line": 21,
  "inputs": {
    "value": "2026-03-14T14:00:00Z"
  },
  "closure_values": {},
  "output": 1773496800000000000
}
```

</details>

<details>

<summary>Call 59: contracts.models.utc_ns</summary>

Source: `.\contracts\models.py`, line 21.

```json
{
  "call": 59,
  "parent_call": 51,
  "function": "contracts.models.utc_ns",
  "source": ".\\contracts\\models.py",
  "line": 21,
  "inputs": {
    "value": "2026-03-14T14:10:00Z"
  },
  "closure_values": {},
  "output": 1773497400000000000
}
```

</details>

<details>

<summary>Call 66: mcp.server.fastmcp.utilities.func_metadata.ArgModelBase.model_dump_one_level</summary>

Source: `.\.venv\Lib\site-packages\mcp\server\fastmcp\utilities\func_metadata.py`, line 50.

```json
{
  "call": 66,
  "parent_call": 38,
  "function": "mcp.server.fastmcp.utilities.func_metadata.ArgModelBase.model_dump_one_level",
  "source": ".\\.venv\\Lib\\site-packages\\mcp\\server\\fastmcp\\utilities\\func_metadata.py",
  "line": 50,
  "inputs": {
    "self": {
      "query": {
        "window": {
          "start": "2026-03-14T14:00:00Z",
          "end": "2026-03-14T14:10:00Z"
        },
        "limit": 2,
        "cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:2",
        "service": "email",
        "severity": "ERROR",
        "contains": "timed out",
        "trace_id": null
      }
    }
  },
  "closure_values": {},
  "output": {
    "query": {
      "window": {
        "start": "2026-03-14T14:00:00Z",
        "end": "2026-03-14T14:10:00Z"
      },
      "limit": 2,
      "cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:2",
      "service": "email",
      "severity": "ERROR",
      "contains": "timed out",
      "trace_id": null
    }
  }
}
```

</details>

<details>

<summary>Call 72: mcp_servers.telemetry.server.create_server.&lt;locals&gt;.search_logs</summary>

Source: `.\mcp_servers\telemetry\server.py`, line 58.

```json
{
  "call": 72,
  "parent_call": 38,
  "function": "mcp_servers.telemetry.server.create_server.<locals>.search_logs",
  "source": ".\\mcp_servers\\telemetry\\server.py",
  "line": 58,
  "inputs": {
    "query": {
      "window": {
        "start": "2026-03-14T14:00:00Z",
        "end": "2026-03-14T14:10:00Z"
      },
      "limit": 2,
      "cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:2",
      "service": "email",
      "severity": "ERROR",
      "contains": "timed out",
      "trace_id": null
    }
  },
  "closure_values": {
    "engine": "<mcp_servers.telemetry.engine.ToolEngine>"
  },
  "output": {
    "data": {
      "columns": [
        "handle",
        "ts_ns",
        "service",
        "severity",
        "body",
        "trace_id",
        "span_id",
        "count"
      ],
      "rows": [
        [
          "L3",
          1773497385000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ],
        [
          "L4",
          1773497390000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ]
      ]
    },
    "total_matches": 5,
    "returned": 2,
    "truncated": true,
    "next_cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4",
    "query_id": "q8986b892",
    "source": {
      "backend": "parquet",
      "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
      "tool_version": "0.1.1"
    },
    "warnings": []
  }
}
```

</details>

<details>

<summary>Call 73: pydantic.main.BaseModel.model_dump</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 427.

```json
{
  "call": 73,
  "parent_call": 72,
  "function": "pydantic.main.BaseModel.model_dump",
  "source": ".\\.venv\\Lib\\site-packages\\pydantic\\main.py",
  "line": 427,
  "inputs": {
    "mode": "python",
    "include": null,
    "exclude": null,
    "context": null,
    "by_alias": null,
    "exclude_unset": false,
    "exclude_defaults": false,
    "exclude_none": false,
    "exclude_computed_fields": false,
    "round_trip": false,
    "warnings": true,
    "fallback": null,
    "serialize_as_any": false,
    "polymorphic_serialization": null,
    "self": {
      "window": {
        "start": "2026-03-14T14:00:00Z",
        "end": "2026-03-14T14:10:00Z"
      },
      "limit": 2,
      "cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:2",
      "service": "email",
      "severity": "ERROR",
      "contains": "timed out",
      "trace_id": null
    }
  },
  "closure_values": {},
  "output": {
    "window": {
      "start": "2026-03-14T14:00:00Z",
      "end": "2026-03-14T14:10:00Z"
    },
    "limit": 2,
    "cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:2",
    "service": "email",
    "severity": "ERROR",
    "contains": "timed out",
    "trace_id": null
  }
}
```

</details>

<details>

<summary>Call 75: mcp_servers.telemetry.engine.ToolEngine.call</summary>

Source: `.\mcp_servers\telemetry\engine.py`, line 48.

```json
{
  "call": 75,
  "parent_call": 72,
  "function": "mcp_servers.telemetry.engine.ToolEngine.call",
  "source": ".\\mcp_servers\\telemetry\\engine.py",
  "line": 48,
  "inputs": {
    "tool": "search_logs",
    "arguments": {
      "window": {
        "start": "2026-03-14T14:00:00Z",
        "end": "2026-03-14T14:10:00Z"
      },
      "limit": 2,
      "cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:2",
      "service": "email",
      "severity": "ERROR",
      "contains": "timed out",
      "trace_id": null
    },
    "self": "<mcp_servers.telemetry.engine.ToolEngine>"
  },
  "closure_values": {},
  "output": {
    "data": {
      "columns": [
        "handle",
        "ts_ns",
        "service",
        "severity",
        "body",
        "trace_id",
        "span_id",
        "count"
      ],
      "rows": [
        [
          "L3",
          1773497385000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ],
        [
          "L4",
          1773497390000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ]
      ]
    },
    "total_matches": 5,
    "returned": 2,
    "truncated": true,
    "next_cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4",
    "query_id": "q8986b892",
    "source": {
      "backend": "parquet",
      "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
      "tool_version": "0.1.1"
    },
    "warnings": []
  }
}
```

</details>

<details>

<summary>Call 76: pydantic.main.BaseModel.model_validate</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 693.

```json
{
  "call": 76,
  "parent_call": 75,
  "function": "pydantic.main.BaseModel.model_validate",
  "source": ".\\.venv\\Lib\\site-packages\\pydantic\\main.py",
  "line": 693,
  "inputs": {
    "obj": {
      "window": {
        "start": "2026-03-14T14:00:00Z",
        "end": "2026-03-14T14:10:00Z"
      },
      "limit": 2,
      "cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:2",
      "service": "email",
      "severity": "ERROR",
      "contains": "timed out",
      "trace_id": null
    },
    "strict": null,
    "extra": null,
    "from_attributes": null,
    "context": null,
    "by_alias": null,
    "by_name": null,
    "cls": "<class contracts.queries.SearchLogs>"
  },
  "closure_values": {},
  "output": {
    "window": {
      "start": "2026-03-14T14:00:00Z",
      "end": "2026-03-14T14:10:00Z"
    },
    "limit": 2,
    "cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:2",
    "service": "email",
    "severity": "ERROR",
    "contains": "timed out",
    "trace_id": null
  }
}
```

</details>

<details>

<summary>Call 78: contracts.models.Window.ordered</summary>

Source: `.\contracts\models.py`, line 45.

```json
{
  "call": 78,
  "parent_call": 77,
  "function": "contracts.models.Window.ordered",
  "source": ".\\contracts\\models.py",
  "line": 45,
  "inputs": {
    "self": {
      "start": "2026-03-14T14:00:00Z",
      "end": "2026-03-14T14:10:00Z"
    }
  },
  "closure_values": {},
  "output": {
    "start": "2026-03-14T14:00:00Z",
    "end": "2026-03-14T14:10:00Z"
  }
}
```

</details>

<details>

<summary>Call 79: contracts.models.utc_ns</summary>

Source: `.\contracts\models.py`, line 21.

```json
{
  "call": 79,
  "parent_call": 78,
  "function": "contracts.models.utc_ns",
  "source": ".\\contracts\\models.py",
  "line": 21,
  "inputs": {
    "value": "2026-03-14T14:00:00Z"
  },
  "closure_values": {},
  "output": 1773496800000000000
}
```

</details>

<details>

<summary>Call 86: contracts.models.utc_ns</summary>

Source: `.\contracts\models.py`, line 21.

```json
{
  "call": 86,
  "parent_call": 78,
  "function": "contracts.models.utc_ns",
  "source": ".\\contracts\\models.py",
  "line": 21,
  "inputs": {
    "value": "2026-03-14T14:10:00Z"
  },
  "closure_values": {},
  "output": 1773497400000000000
}
```

</details>

<details>

<summary>Call 93: store.evidence.canonical_query</summary>

Source: `.\store\evidence.py`, line 13.

```json
{
  "call": 93,
  "parent_call": 75,
  "function": "store.evidence.canonical_query",
  "source": ".\\store\\evidence.py",
  "line": 13,
  "inputs": {
    "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
    "tool_version": "0.1.1",
    "tool": "search_logs",
    "args": {
      "window": {
        "start": "2026-03-14T14:00:00Z",
        "end": "2026-03-14T14:10:00Z"
      },
      "limit": 2,
      "cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:2",
      "service": "email",
      "severity": "ERROR",
      "contains": "timed out",
      "trace_id": null
    }
  },
  "closure_values": {},
  "output": "{\"arguments\":{\"contains\":\"timed out\",\"service\":\"email\",\"severity\":\"ERROR\",\"trace_id\":null,\"window\":{\"end\":\"2026-03-14T14:10:00Z\",\"start\":\"2026-03-14T14:00:00Z\"}},\"dataset_id\":\"856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb\",\"tool\":\"search_logs\",\"tool_version\":\"0.1.1\"}"
}
```

</details>

<details>

<summary>Call 94: pydantic.main.BaseModel.model_dump</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 427.

```json
{
  "call": 94,
  "parent_call": 93,
  "function": "pydantic.main.BaseModel.model_dump",
  "source": ".\\.venv\\Lib\\site-packages\\pydantic\\main.py",
  "line": 427,
  "inputs": {
    "mode": "python",
    "include": null,
    "exclude": [
      "cursor",
      "limit"
    ],
    "context": null,
    "by_alias": null,
    "exclude_unset": false,
    "exclude_defaults": false,
    "exclude_none": false,
    "exclude_computed_fields": false,
    "round_trip": false,
    "warnings": true,
    "fallback": null,
    "serialize_as_any": false,
    "polymorphic_serialization": null,
    "self": {
      "window": {
        "start": "2026-03-14T14:00:00Z",
        "end": "2026-03-14T14:10:00Z"
      },
      "limit": 2,
      "cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:2",
      "service": "email",
      "severity": "ERROR",
      "contains": "timed out",
      "trace_id": null
    }
  },
  "closure_values": {},
  "output": {
    "window": {
      "start": "2026-03-14T14:00:00Z",
      "end": "2026-03-14T14:10:00Z"
    },
    "service": "email",
    "severity": "ERROR",
    "contains": "timed out",
    "trace_id": null
  }
}
```

</details>

<details>

<summary>Call 96: pydantic.main.BaseModel.model_validate</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 693.

```json
{
  "call": 96,
  "parent_call": 93,
  "function": "pydantic.main.BaseModel.model_validate",
  "source": ".\\.venv\\Lib\\site-packages\\pydantic\\main.py",
  "line": 693,
  "inputs": {
    "obj": {
      "start": "2026-03-14T14:00:00Z",
      "end": "2026-03-14T14:10:00Z"
    },
    "strict": null,
    "extra": null,
    "from_attributes": null,
    "context": null,
    "by_alias": null,
    "by_name": null,
    "cls": "<class contracts.models.Window>"
  },
  "closure_values": {},
  "output": {
    "start": "2026-03-14T14:00:00Z",
    "end": "2026-03-14T14:10:00Z"
  }
}
```

</details>

<details>

<summary>Call 98: contracts.models.Window.ordered</summary>

Source: `.\contracts\models.py`, line 45.

```json
{
  "call": 98,
  "parent_call": 97,
  "function": "contracts.models.Window.ordered",
  "source": ".\\contracts\\models.py",
  "line": 45,
  "inputs": {
    "self": {
      "start": "2026-03-14T14:00:00Z",
      "end": "2026-03-14T14:10:00Z"
    }
  },
  "closure_values": {},
  "output": {
    "start": "2026-03-14T14:00:00Z",
    "end": "2026-03-14T14:10:00Z"
  }
}
```

</details>

<details>

<summary>Call 99: contracts.models.utc_ns</summary>

Source: `.\contracts\models.py`, line 21.

```json
{
  "call": 99,
  "parent_call": 98,
  "function": "contracts.models.utc_ns",
  "source": ".\\contracts\\models.py",
  "line": 21,
  "inputs": {
    "value": "2026-03-14T14:00:00Z"
  },
  "closure_values": {},
  "output": 1773496800000000000
}
```

</details>

<details>

<summary>Call 106: contracts.models.utc_ns</summary>

Source: `.\contracts\models.py`, line 21.

```json
{
  "call": 106,
  "parent_call": 98,
  "function": "contracts.models.utc_ns",
  "source": ".\\contracts\\models.py",
  "line": 21,
  "inputs": {
    "value": "2026-03-14T14:10:00Z"
  },
  "closure_values": {},
  "output": 1773497400000000000
}
```

</details>

<details>

<summary>Call 113: contracts.models.utc_ns</summary>

Source: `.\contracts\models.py`, line 21.

```json
{
  "call": 113,
  "parent_call": 93,
  "function": "contracts.models.utc_ns",
  "source": ".\\contracts\\models.py",
  "line": 21,
  "inputs": {
    "value": "2026-03-14T14:00:00Z"
  },
  "closure_values": {},
  "output": 1773496800000000000
}
```

</details>

<details>

<summary>Call 120: contracts.models.iso_time</summary>

Source: `.\contracts\models.py`, line 31.

```json
{
  "call": 120,
  "parent_call": 93,
  "function": "contracts.models.iso_time",
  "source": ".\\contracts\\models.py",
  "line": 31,
  "inputs": {
    "ns": 1773496800000000000
  },
  "closure_values": {},
  "output": "2026-03-14T14:00:00Z"
}
```

</details>

<details>

<summary>Call 123: contracts.models.utc_ns</summary>

Source: `.\contracts\models.py`, line 21.

```json
{
  "call": 123,
  "parent_call": 93,
  "function": "contracts.models.utc_ns",
  "source": ".\\contracts\\models.py",
  "line": 21,
  "inputs": {
    "value": "2026-03-14T14:10:00Z"
  },
  "closure_values": {},
  "output": 1773497400000000000
}
```

</details>

<details>

<summary>Call 130: contracts.models.iso_time</summary>

Source: `.\contracts\models.py`, line 31.

```json
{
  "call": 130,
  "parent_call": 93,
  "function": "contracts.models.iso_time",
  "source": ".\\contracts\\models.py",
  "line": 31,
  "inputs": {
    "ns": 1773497400000000000
  },
  "closure_values": {},
  "output": "2026-03-14T14:10:00Z"
}
```

</details>

<details>

<summary>Call 140: store.evidence.QueryIds.get</summary>

Source: `.\store\evidence.py`, line 48.

```json
{
  "call": 140,
  "parent_call": 75,
  "function": "store.evidence.QueryIds.get",
  "source": ".\\store\\evidence.py",
  "line": 48,
  "inputs": {
    "canonical": "{\"arguments\":{\"contains\":\"timed out\",\"service\":\"email\",\"severity\":\"ERROR\",\"trace_id\":null,\"window\":{\"end\":\"2026-03-14T14:10:00Z\",\"start\":\"2026-03-14T14:00:00Z\"}},\"dataset_id\":\"856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb\",\"tool\":\"search_logs\",\"tool_version\":\"0.1.1\"}",
    "self": "<store.evidence.QueryIds>"
  },
  "closure_values": {},
  "output": "q8986b892"
}
```

</details>

<details>

<summary>Call 141: store.evidence.digest_query</summary>

Source: `.\store\evidence.py`, line 39.

```json
{
  "call": 141,
  "parent_call": 75,
  "function": "store.evidence.digest_query",
  "source": ".\\store\\evidence.py",
  "line": 39,
  "inputs": {
    "canonical": "{\"arguments\":{\"contains\":\"timed out\",\"service\":\"email\",\"severity\":\"ERROR\",\"trace_id\":null,\"window\":{\"end\":\"2026-03-14T14:10:00Z\",\"start\":\"2026-03-14T14:00:00Z\"}},\"dataset_id\":\"856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb\",\"tool\":\"search_logs\",\"tool_version\":\"0.1.1\"}"
  },
  "closure_values": {},
  "output": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21"
}
```

</details>

<details>

<summary>Call 316: store.parquet.ParquetStore.query</summary>

Source: `.\store\parquet.py`, line 247.

```json
{
  "call": 316,
  "parent_call": 75,
  "function": "store.parquet.ParquetStore.query",
  "source": ".\\store\\parquet.py",
  "line": 247,
  "inputs": {
    "tool": "search_logs",
    "args": {
      "window": {
        "start": "2026-03-14T14:00:00Z",
        "end": "2026-03-14T14:10:00Z"
      },
      "limit": 2,
      "cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:2",
      "service": "email",
      "severity": "ERROR",
      "contains": "timed out",
      "trace_id": null
    },
    "self": "<store.parquet.ParquetStore>"
  },
  "closure_values": {},
  "output": [
    [
      "ts_ns",
      "service",
      "severity",
      "body",
      "trace_id",
      "span_id",
      "count"
    ],
    [
      [
        1773497375000000000,
        "email",
        "ERROR",
        "delivery attempt timed out; queued for retry",
        null,
        null,
        1
      ],
      [
        1773497380000000000,
        "email",
        "ERROR",
        "delivery attempt timed out; queued for retry",
        null,
        null,
        1
      ],
      [
        1773497385000000000,
        "email",
        "ERROR",
        "delivery attempt timed out; queued for retry",
        null,
        null,
        1
      ],
      [
        1773497390000000000,
        "email",
        "ERROR",
        "delivery attempt timed out; queued for retry",
        null,
        null,
        1
      ],
      [
        1773497395000000000,
        "email",
        "ERROR",
        "delivery attempt timed out; queued for retry",
        null,
        null,
        1
      ]
    ],
    []
  ]
}
```

</details>

<details>

<summary>Call 317: store.parquet.ParquetStore._window</summary>

Source: `.\store\parquet.py`, line 119.

```json
{
  "call": 317,
  "parent_call": 316,
  "function": "store.parquet.ParquetStore._window",
  "source": ".\\store\\parquet.py",
  "line": 119,
  "inputs": {
    "window": {
      "start": "2026-03-14T14:00:00Z",
      "end": "2026-03-14T14:10:00Z"
    },
    "aligned": false,
    "self": "<store.parquet.ParquetStore>"
  },
  "closure_values": {},
  "output": [
    1773496800000000000,
    1773497400000000000
  ]
}
```

</details>

<details>

<summary>Call 318: contracts.models.utc_ns</summary>

Source: `.\contracts\models.py`, line 21.

```json
{
  "call": 318,
  "parent_call": 317,
  "function": "contracts.models.utc_ns",
  "source": ".\\contracts\\models.py",
  "line": 21,
  "inputs": {
    "value": "2026-03-14T14:00:00Z"
  },
  "closure_values": {},
  "output": 1773496800000000000
}
```

</details>

<details>

<summary>Call 325: contracts.models.utc_ns</summary>

Source: `.\contracts\models.py`, line 21.

```json
{
  "call": 325,
  "parent_call": 317,
  "function": "contracts.models.utc_ns",
  "source": ".\\contracts\\models.py",
  "line": 21,
  "inputs": {
    "value": "2026-03-14T14:10:00Z"
  },
  "closure_values": {},
  "output": 1773497400000000000
}
```

</details>

<details>

<summary>Call 332: contracts.models.utc_ns</summary>

Source: `.\contracts\models.py`, line 21.

```json
{
  "call": 332,
  "parent_call": 317,
  "function": "contracts.models.utc_ns",
  "source": ".\\contracts\\models.py",
  "line": 21,
  "inputs": {
    "value": "2026-03-14T14:00:00Z"
  },
  "closure_values": {},
  "output": 1773496800000000000
}
```

</details>

<details>

<summary>Call 339: contracts.models.utc_ns</summary>

Source: `.\contracts\models.py`, line 21.

```json
{
  "call": 339,
  "parent_call": 317,
  "function": "contracts.models.utc_ns",
  "source": ".\\contracts\\models.py",
  "line": 21,
  "inputs": {
    "value": "2026-03-14T14:10:00Z"
  },
  "closure_values": {},
  "output": 1773497400000000000
}
```

</details>

<details>

<summary>Call 399: store.parquet.ParquetStore.query.&lt;locals&gt;.&lt;lambda&gt;</summary>

Source: `.\store\parquet.py`, line 423.

```json
{
  "call": 399,
  "parent_call": 398,
  "function": "store.parquet.ParquetStore.query.<locals>.<lambda>",
  "source": ".\\store\\parquet.py",
  "line": 423,
  "inputs": {
    "p": [
      {
        "ts_ns": 1773497375000000000,
        "service": "email",
        "severity": "ERROR",
        "body": "delivery attempt timed out; queued for retry",
        "trace_id": null,
        "span_id": null,
        "attributes": {}
      },
      1
    ]
  },
  "closure_values": {},
  "output": [
    1773497375000000000,
    "email",
    "",
    "delivery attempt timed out; queued for retry"
  ]
}
```

</details>

<details>

<summary>Call 400: store.parquet.ParquetStore.query.&lt;locals&gt;.&lt;lambda&gt;</summary>

Source: `.\store\parquet.py`, line 423.

```json
{
  "call": 400,
  "parent_call": 398,
  "function": "store.parquet.ParquetStore.query.<locals>.<lambda>",
  "source": ".\\store\\parquet.py",
  "line": 423,
  "inputs": {
    "p": [
      {
        "ts_ns": 1773497380000000000,
        "service": "email",
        "severity": "ERROR",
        "body": "delivery attempt timed out; queued for retry",
        "trace_id": null,
        "span_id": null,
        "attributes": {}
      },
      1
    ]
  },
  "closure_values": {},
  "output": [
    1773497380000000000,
    "email",
    "",
    "delivery attempt timed out; queued for retry"
  ]
}
```

</details>

<details>

<summary>Call 401: store.parquet.ParquetStore.query.&lt;locals&gt;.&lt;lambda&gt;</summary>

Source: `.\store\parquet.py`, line 423.

```json
{
  "call": 401,
  "parent_call": 398,
  "function": "store.parquet.ParquetStore.query.<locals>.<lambda>",
  "source": ".\\store\\parquet.py",
  "line": 423,
  "inputs": {
    "p": [
      {
        "ts_ns": 1773497385000000000,
        "service": "email",
        "severity": "ERROR",
        "body": "delivery attempt timed out; queued for retry",
        "trace_id": null,
        "span_id": null,
        "attributes": {}
      },
      1
    ]
  },
  "closure_values": {},
  "output": [
    1773497385000000000,
    "email",
    "",
    "delivery attempt timed out; queued for retry"
  ]
}
```

</details>

<details>

<summary>Call 402: store.parquet.ParquetStore.query.&lt;locals&gt;.&lt;lambda&gt;</summary>

Source: `.\store\parquet.py`, line 423.

```json
{
  "call": 402,
  "parent_call": 398,
  "function": "store.parquet.ParquetStore.query.<locals>.<lambda>",
  "source": ".\\store\\parquet.py",
  "line": 423,
  "inputs": {
    "p": [
      {
        "ts_ns": 1773497390000000000,
        "service": "email",
        "severity": "ERROR",
        "body": "delivery attempt timed out; queued for retry",
        "trace_id": null,
        "span_id": null,
        "attributes": {}
      },
      1
    ]
  },
  "closure_values": {},
  "output": [
    1773497390000000000,
    "email",
    "",
    "delivery attempt timed out; queued for retry"
  ]
}
```

</details>

<details>

<summary>Call 403: store.parquet.ParquetStore.query.&lt;locals&gt;.&lt;lambda&gt;</summary>

Source: `.\store\parquet.py`, line 423.

```json
{
  "call": 403,
  "parent_call": 398,
  "function": "store.parquet.ParquetStore.query.<locals>.<lambda>",
  "source": ".\\store\\parquet.py",
  "line": 423,
  "inputs": {
    "p": [
      {
        "ts_ns": 1773497395000000000,
        "service": "email",
        "severity": "ERROR",
        "body": "delivery attempt timed out; queued for retry",
        "trace_id": null,
        "span_id": null,
        "attributes": {}
      },
      1
    ]
  },
  "closure_values": {},
  "output": [
    1773497395000000000,
    "email",
    "",
    "delivery attempt timed out; queued for retry"
  ]
}
```

</details>

<details>

<summary>Call 408: mcp_servers.telemetry.engine.ToolEngine.call.&lt;locals&gt;.envelope</summary>

Source: `.\mcp_servers\telemetry\engine.py`, line 79.

```json
{
  "call": 408,
  "parent_call": 75,
  "function": "mcp_servers.telemetry.engine.ToolEngine.call.<locals>.envelope",
  "source": ".\\mcp_servers\\telemetry\\engine.py",
  "line": 79,
  "inputs": {
    "self": "<mcp_servers.telemetry.engine.ToolEngine>"
  },
  "closure_values": {
    "all_rows": [
      [
        1773497375000000000,
        "email",
        "ERROR",
        "delivery attempt timed out; queued for retry",
        null,
        null,
        1
      ],
      [
        1773497380000000000,
        "email",
        "ERROR",
        "delivery attempt timed out; queued for retry",
        null,
        null,
        1
      ],
      [
        1773497385000000000,
        "email",
        "ERROR",
        "delivery attempt timed out; queued for retry",
        null,
        null,
        1
      ],
      [
        1773497390000000000,
        "email",
        "ERROR",
        "delivery attempt timed out; queued for retry",
        null,
        null,
        1
      ],
      [
        1773497395000000000,
        "email",
        "ERROR",
        "delivery attempt timed out; queued for retry",
        null,
        null,
        1
      ]
    ],
    "columns": [
      "ts_ns",
      "service",
      "severity",
      "body",
      "trace_id",
      "span_id",
      "count"
    ],
    "digest": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21",
    "offset": 2,
    "query_id": "q8986b892",
    "selected": [
      [
        "L3",
        1773497385000000000,
        "email",
        "ERROR",
        "delivery attempt timed out; queued for retry",
        null,
        null,
        1
      ]
    ],
    "self": "<mcp_servers.telemetry.engine.ToolEngine>",
    "warnings": []
  },
  "output": {
    "data": {
      "columns": [
        "handle",
        "ts_ns",
        "service",
        "severity",
        "body",
        "trace_id",
        "span_id",
        "count"
      ],
      "rows": [
        [
          "L3",
          1773497385000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ]
      ]
    },
    "total_matches": 5,
    "returned": 1,
    "truncated": true,
    "next_cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:3",
    "query_id": "q8986b892",
    "source": {
      "backend": "parquet",
      "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
      "tool_version": "0.1.1"
    },
    "warnings": []
  }
}
```

</details>

<details>

<summary>Call 411: pydantic.main.BaseModel.__init__</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 253.

```json
{
  "call": 411,
  "parent_call": 408,
  "function": "pydantic.main.BaseModel.__init__",
  "source": ".\\.venv\\Lib\\site-packages\\pydantic\\main.py",
  "line": 253,
  "inputs": {
    "data": {
      "columns": [
        "handle",
        "ts_ns",
        "service",
        "severity",
        "body",
        "trace_id",
        "span_id",
        "count"
      ],
      "rows": [
        [
          "L3",
          1773497385000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ]
      ]
    },
    "self": {}
  },
  "closure_values": {},
  "output": null,
  "constructed_object": {
    "columns": [
      "handle",
      "ts_ns",
      "service",
      "severity",
      "body",
      "trace_id",
      "span_id",
      "count"
    ],
    "rows": [
      [
        "L3",
        1773497385000000000,
        "email",
        "ERROR",
        "delivery attempt timed out; queued for retry",
        null,
        null,
        1
      ]
    ]
  }
}
```

</details>

<details>

<summary>Call 413: contracts.models.TableData.rectangular</summary>

Source: `.\contracts\models.py`, line 256.

```json
{
  "call": 413,
  "parent_call": 412,
  "function": "contracts.models.TableData.rectangular",
  "source": ".\\contracts\\models.py",
  "line": 256,
  "inputs": {
    "self": {
      "columns": [
        "handle",
        "ts_ns",
        "service",
        "severity",
        "body",
        "trace_id",
        "span_id",
        "count"
      ],
      "rows": [
        [
          "L3",
          1773497385000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ]
      ]
    }
  },
  "closure_values": {},
  "output": {
    "columns": [
      "handle",
      "ts_ns",
      "service",
      "severity",
      "body",
      "trace_id",
      "span_id",
      "count"
    ],
    "rows": [
      [
        "L3",
        1773497385000000000,
        "email",
        "ERROR",
        "delivery attempt timed out; queued for retry",
        null,
        null,
        1
      ]
    ]
  }
}
```

</details>

<details>

<summary>Call 422: pydantic.main.BaseModel.__init__</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 253.

```json
{
  "call": 422,
  "parent_call": 408,
  "function": "pydantic.main.BaseModel.__init__",
  "source": ".\\.venv\\Lib\\site-packages\\pydantic\\main.py",
  "line": 253,
  "inputs": {
    "data": {
      "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
      "tool_version": "0.1.1"
    },
    "self": {}
  },
  "closure_values": {},
  "output": null,
  "constructed_object": {
    "backend": "parquet",
    "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
    "tool_version": "0.1.1"
  }
}
```

</details>

<details>

<summary>Call 424: pydantic.main.BaseModel.__init__</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 253.

```json
{
  "call": 424,
  "parent_call": 408,
  "function": "pydantic.main.BaseModel.__init__",
  "source": ".\\.venv\\Lib\\site-packages\\pydantic\\main.py",
  "line": 253,
  "inputs": {
    "data": {
      "data": {
        "columns": [
          "handle",
          "ts_ns",
          "service",
          "severity",
          "body",
          "trace_id",
          "span_id",
          "count"
        ],
        "rows": [
          [
            "L3",
            1773497385000000000,
            "email",
            "ERROR",
            "delivery attempt timed out; queued for retry",
            null,
            null,
            1
          ]
        ]
      },
      "total_matches": 5,
      "returned": 1,
      "truncated": true,
      "next_cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:3",
      "query_id": "q8986b892",
      "source": {
        "backend": "parquet",
        "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
        "tool_version": "0.1.1"
      },
      "warnings": []
    },
    "self": {}
  },
  "closure_values": {},
  "output": null,
  "constructed_object": {
    "data": {
      "columns": [
        "handle",
        "ts_ns",
        "service",
        "severity",
        "body",
        "trace_id",
        "span_id",
        "count"
      ],
      "rows": [
        [
          "L3",
          1773497385000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ]
      ]
    },
    "total_matches": 5,
    "returned": 1,
    "truncated": true,
    "next_cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:3",
    "query_id": "q8986b892",
    "source": {
      "backend": "parquet",
      "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
      "tool_version": "0.1.1"
    },
    "warnings": []
  }
}
```

</details>

<details>

<summary>Call 426: contracts.models.TableData.rectangular</summary>

Source: `.\contracts\models.py`, line 256.

```json
{
  "call": 426,
  "parent_call": 425,
  "function": "contracts.models.TableData.rectangular",
  "source": ".\\contracts\\models.py",
  "line": 256,
  "inputs": {
    "self": {
      "columns": [
        "handle",
        "ts_ns",
        "service",
        "severity",
        "body",
        "trace_id",
        "span_id",
        "count"
      ],
      "rows": [
        [
          "L3",
          1773497385000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ]
      ]
    }
  },
  "closure_values": {},
  "output": {
    "columns": [
      "handle",
      "ts_ns",
      "service",
      "severity",
      "body",
      "trace_id",
      "span_id",
      "count"
    ],
    "rows": [
      [
        "L3",
        1773497385000000000,
        "email",
        "ERROR",
        "delivery attempt timed out; queued for retry",
        null,
        null,
        1
      ]
    ]
  }
}
```

</details>

<details>

<summary>Call 434: contracts.models.ToolResult.consistent</summary>

Source: `.\contracts\models.py`, line 286.

```json
{
  "call": 434,
  "parent_call": 425,
  "function": "contracts.models.ToolResult.consistent",
  "source": ".\\contracts\\models.py",
  "line": 286,
  "inputs": {
    "self": {
      "data": {
        "columns": [
          "handle",
          "ts_ns",
          "service",
          "severity",
          "body",
          "trace_id",
          "span_id",
          "count"
        ],
        "rows": [
          [
            "L3",
            1773497385000000000,
            "email",
            "ERROR",
            "delivery attempt timed out; queued for retry",
            null,
            null,
            1
          ]
        ]
      },
      "total_matches": 5,
      "returned": 1,
      "truncated": true,
      "next_cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:3",
      "query_id": "q8986b892",
      "source": {
        "backend": "parquet",
        "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
        "tool_version": "0.1.1"
      },
      "warnings": []
    }
  },
  "closure_values": {},
  "output": {
    "data": {
      "columns": [
        "handle",
        "ts_ns",
        "service",
        "severity",
        "body",
        "trace_id",
        "span_id",
        "count"
      ],
      "rows": [
        [
          "L3",
          1773497385000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ]
      ]
    },
    "total_matches": 5,
    "returned": 1,
    "truncated": true,
    "next_cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:3",
    "query_id": "q8986b892",
    "source": {
      "backend": "parquet",
      "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
      "tool_version": "0.1.1"
    },
    "warnings": []
  }
}
```

</details>

<details>

<summary>Call 437: pydantic.main.BaseModel.model_dump</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 427.

```json
{
  "call": 437,
  "parent_call": 408,
  "function": "pydantic.main.BaseModel.model_dump",
  "source": ".\\.venv\\Lib\\site-packages\\pydantic\\main.py",
  "line": 427,
  "inputs": {
    "mode": "python",
    "include": null,
    "exclude": null,
    "context": null,
    "by_alias": null,
    "exclude_unset": false,
    "exclude_defaults": false,
    "exclude_none": false,
    "exclude_computed_fields": false,
    "round_trip": false,
    "warnings": true,
    "fallback": null,
    "serialize_as_any": false,
    "polymorphic_serialization": null,
    "self": {
      "data": {
        "columns": [
          "handle",
          "ts_ns",
          "service",
          "severity",
          "body",
          "trace_id",
          "span_id",
          "count"
        ],
        "rows": [
          [
            "L3",
            1773497385000000000,
            "email",
            "ERROR",
            "delivery attempt timed out; queued for retry",
            null,
            null,
            1
          ]
        ]
      },
      "total_matches": 5,
      "returned": 1,
      "truncated": true,
      "next_cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:3",
      "query_id": "q8986b892",
      "source": {
        "backend": "parquet",
        "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
        "tool_version": "0.1.1"
      },
      "warnings": []
    }
  },
  "closure_values": {},
  "output": {
    "data": {
      "columns": [
        "handle",
        "ts_ns",
        "service",
        "severity",
        "body",
        "trace_id",
        "span_id",
        "count"
      ],
      "rows": [
        [
          "L3",
          1773497385000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ]
      ]
    },
    "total_matches": 5,
    "returned": 1,
    "truncated": true,
    "next_cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:3",
    "query_id": "q8986b892",
    "source": {
      "backend": "parquet",
      "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
      "tool_version": "0.1.1"
    },
    "warnings": []
  }
}
```

</details>

<details>

<summary>Call 439: store.evidence.compact_json</summary>

Source: `.\store\evidence.py`, line 70.

```json
{
  "call": 439,
  "parent_call": 75,
  "function": "store.evidence.compact_json",
  "source": ".\\store\\evidence.py",
  "line": 70,
  "inputs": {
    "value": {
      "data": {
        "columns": [
          "handle",
          "ts_ns",
          "service",
          "severity",
          "body",
          "trace_id",
          "span_id",
          "count"
        ],
        "rows": [
          [
            "L3",
            1773497385000000000,
            "email",
            "ERROR",
            "delivery attempt timed out; queued for retry",
            null,
            null,
            1
          ]
        ]
      },
      "total_matches": 5,
      "returned": 1,
      "truncated": true,
      "next_cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:3",
      "query_id": "q8986b892",
      "source": {
        "backend": "parquet",
        "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
        "tool_version": "0.1.1"
      },
      "warnings": []
    }
  },
  "closure_values": {},
  "output": "{\"data\":{\"columns\":[\"handle\",\"ts_ns\",\"service\",\"severity\",\"body\",\"trace_id\",\"span_id\",\"count\"],\"rows\":[[\"L3\",1773497385000000000,\"email\",\"ERROR\",\"delivery attempt timed out; queued for retry\",null,null,1]]},\"total_matches\":5,\"returned\":1,\"truncated\":true,\"next_cursor\":\"8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:3\",\"query_id\":\"q8986b892\",\"source\":{\"backend\":\"parquet\",\"dataset_id\":\"856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb\",\"tool_version\":\"0.1.1\"},\"warnings\":[]}"
}
```

</details>

<details>

<summary>Call 447: mcp_servers.telemetry.engine.ToolEngine.__init__.&lt;locals&gt;.&lt;lambda&gt;</summary>

Source: `.\mcp_servers\telemetry\engine.py`, line 44.

```json
{
  "call": 447,
  "parent_call": 75,
  "function": "mcp_servers.telemetry.engine.ToolEngine.__init__.<locals>.<lambda>",
  "source": ".\\mcp_servers\\telemetry\\engine.py",
  "line": 44,
  "inputs": {
    "text": "{\"data\":{\"columns\":[\"handle\",\"ts_ns\",\"service\",\"severity\",\"body\",\"trace_id\",\"span_id\",\"count\"],\"rows\":[[\"L3\",1773497385000000000,\"email\",\"ERROR\",\"delivery attempt timed out; queued for retry\",null,null,1]]},\"total_matches\":5,\"returned\":1,\"truncated\":true,\"next_cursor\":\"8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:3\",\"query_id\":\"q8986b892\",\"source\":{\"backend\":\"parquet\",\"dataset_id\":\"856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb\",\"tool_version\":\"0.1.1\"},\"warnings\":[]}"
  },
  "closure_values": {},
  "output": 509
}
```

</details>

<details>

<summary>Call 451: mcp_servers.telemetry.engine.ToolEngine.call.&lt;locals&gt;.envelope</summary>

Source: `.\mcp_servers\telemetry\engine.py`, line 79.

```json
{
  "call": 451,
  "parent_call": 75,
  "function": "mcp_servers.telemetry.engine.ToolEngine.call.<locals>.envelope",
  "source": ".\\mcp_servers\\telemetry\\engine.py",
  "line": 79,
  "inputs": {
    "self": "<mcp_servers.telemetry.engine.ToolEngine>"
  },
  "closure_values": {
    "all_rows": [
      [
        1773497375000000000,
        "email",
        "ERROR",
        "delivery attempt timed out; queued for retry",
        null,
        null,
        1
      ],
      [
        1773497380000000000,
        "email",
        "ERROR",
        "delivery attempt timed out; queued for retry",
        null,
        null,
        1
      ],
      [
        1773497385000000000,
        "email",
        "ERROR",
        "delivery attempt timed out; queued for retry",
        null,
        null,
        1
      ],
      [
        1773497390000000000,
        "email",
        "ERROR",
        "delivery attempt timed out; queued for retry",
        null,
        null,
        1
      ],
      [
        1773497395000000000,
        "email",
        "ERROR",
        "delivery attempt timed out; queued for retry",
        null,
        null,
        1
      ]
    ],
    "columns": [
      "ts_ns",
      "service",
      "severity",
      "body",
      "trace_id",
      "span_id",
      "count"
    ],
    "digest": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21",
    "offset": 2,
    "query_id": "q8986b892",
    "selected": [
      [
        "L3",
        1773497385000000000,
        "email",
        "ERROR",
        "delivery attempt timed out; queued for retry",
        null,
        null,
        1
      ],
      [
        "L4",
        1773497390000000000,
        "email",
        "ERROR",
        "delivery attempt timed out; queued for retry",
        null,
        null,
        1
      ]
    ],
    "self": "<mcp_servers.telemetry.engine.ToolEngine>",
    "warnings": []
  },
  "output": {
    "data": {
      "columns": [
        "handle",
        "ts_ns",
        "service",
        "severity",
        "body",
        "trace_id",
        "span_id",
        "count"
      ],
      "rows": [
        [
          "L3",
          1773497385000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ],
        [
          "L4",
          1773497390000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ]
      ]
    },
    "total_matches": 5,
    "returned": 2,
    "truncated": true,
    "next_cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4",
    "query_id": "q8986b892",
    "source": {
      "backend": "parquet",
      "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
      "tool_version": "0.1.1"
    },
    "warnings": []
  }
}
```

</details>

<details>

<summary>Call 454: pydantic.main.BaseModel.__init__</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 253.

```json
{
  "call": 454,
  "parent_call": 451,
  "function": "pydantic.main.BaseModel.__init__",
  "source": ".\\.venv\\Lib\\site-packages\\pydantic\\main.py",
  "line": 253,
  "inputs": {
    "data": {
      "columns": [
        "handle",
        "ts_ns",
        "service",
        "severity",
        "body",
        "trace_id",
        "span_id",
        "count"
      ],
      "rows": [
        [
          "L3",
          1773497385000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ],
        [
          "L4",
          1773497390000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ]
      ]
    },
    "self": {}
  },
  "closure_values": {},
  "output": null,
  "constructed_object": {
    "columns": [
      "handle",
      "ts_ns",
      "service",
      "severity",
      "body",
      "trace_id",
      "span_id",
      "count"
    ],
    "rows": [
      [
        "L3",
        1773497385000000000,
        "email",
        "ERROR",
        "delivery attempt timed out; queued for retry",
        null,
        null,
        1
      ],
      [
        "L4",
        1773497390000000000,
        "email",
        "ERROR",
        "delivery attempt timed out; queued for retry",
        null,
        null,
        1
      ]
    ]
  }
}
```

</details>

<details>

<summary>Call 456: contracts.models.TableData.rectangular</summary>

Source: `.\contracts\models.py`, line 256.

```json
{
  "call": 456,
  "parent_call": 455,
  "function": "contracts.models.TableData.rectangular",
  "source": ".\\contracts\\models.py",
  "line": 256,
  "inputs": {
    "self": {
      "columns": [
        "handle",
        "ts_ns",
        "service",
        "severity",
        "body",
        "trace_id",
        "span_id",
        "count"
      ],
      "rows": [
        [
          "L3",
          1773497385000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ],
        [
          "L4",
          1773497390000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ]
      ]
    }
  },
  "closure_values": {},
  "output": {
    "columns": [
      "handle",
      "ts_ns",
      "service",
      "severity",
      "body",
      "trace_id",
      "span_id",
      "count"
    ],
    "rows": [
      [
        "L3",
        1773497385000000000,
        "email",
        "ERROR",
        "delivery attempt timed out; queued for retry",
        null,
        null,
        1
      ],
      [
        "L4",
        1773497390000000000,
        "email",
        "ERROR",
        "delivery attempt timed out; queued for retry",
        null,
        null,
        1
      ]
    ]
  }
}
```

</details>

<details>

<summary>Call 468: pydantic.main.BaseModel.__init__</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 253.

```json
{
  "call": 468,
  "parent_call": 451,
  "function": "pydantic.main.BaseModel.__init__",
  "source": ".\\.venv\\Lib\\site-packages\\pydantic\\main.py",
  "line": 253,
  "inputs": {
    "data": {
      "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
      "tool_version": "0.1.1"
    },
    "self": {}
  },
  "closure_values": {},
  "output": null,
  "constructed_object": {
    "backend": "parquet",
    "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
    "tool_version": "0.1.1"
  }
}
```

</details>

<details>

<summary>Call 470: pydantic.main.BaseModel.__init__</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 253.

```json
{
  "call": 470,
  "parent_call": 451,
  "function": "pydantic.main.BaseModel.__init__",
  "source": ".\\.venv\\Lib\\site-packages\\pydantic\\main.py",
  "line": 253,
  "inputs": {
    "data": {
      "data": {
        "columns": [
          "handle",
          "ts_ns",
          "service",
          "severity",
          "body",
          "trace_id",
          "span_id",
          "count"
        ],
        "rows": [
          [
            "L3",
            1773497385000000000,
            "email",
            "ERROR",
            "delivery attempt timed out; queued for retry",
            null,
            null,
            1
          ],
          [
            "L4",
            1773497390000000000,
            "email",
            "ERROR",
            "delivery attempt timed out; queued for retry",
            null,
            null,
            1
          ]
        ]
      },
      "total_matches": 5,
      "returned": 2,
      "truncated": true,
      "next_cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4",
      "query_id": "q8986b892",
      "source": {
        "backend": "parquet",
        "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
        "tool_version": "0.1.1"
      },
      "warnings": []
    },
    "self": {}
  },
  "closure_values": {},
  "output": null,
  "constructed_object": {
    "data": {
      "columns": [
        "handle",
        "ts_ns",
        "service",
        "severity",
        "body",
        "trace_id",
        "span_id",
        "count"
      ],
      "rows": [
        [
          "L3",
          1773497385000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ],
        [
          "L4",
          1773497390000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ]
      ]
    },
    "total_matches": 5,
    "returned": 2,
    "truncated": true,
    "next_cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4",
    "query_id": "q8986b892",
    "source": {
      "backend": "parquet",
      "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
      "tool_version": "0.1.1"
    },
    "warnings": []
  }
}
```

</details>

<details>

<summary>Call 472: contracts.models.TableData.rectangular</summary>

Source: `.\contracts\models.py`, line 256.

```json
{
  "call": 472,
  "parent_call": 471,
  "function": "contracts.models.TableData.rectangular",
  "source": ".\\contracts\\models.py",
  "line": 256,
  "inputs": {
    "self": {
      "columns": [
        "handle",
        "ts_ns",
        "service",
        "severity",
        "body",
        "trace_id",
        "span_id",
        "count"
      ],
      "rows": [
        [
          "L3",
          1773497385000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ],
        [
          "L4",
          1773497390000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ]
      ]
    }
  },
  "closure_values": {},
  "output": {
    "columns": [
      "handle",
      "ts_ns",
      "service",
      "severity",
      "body",
      "trace_id",
      "span_id",
      "count"
    ],
    "rows": [
      [
        "L3",
        1773497385000000000,
        "email",
        "ERROR",
        "delivery attempt timed out; queued for retry",
        null,
        null,
        1
      ],
      [
        "L4",
        1773497390000000000,
        "email",
        "ERROR",
        "delivery attempt timed out; queued for retry",
        null,
        null,
        1
      ]
    ]
  }
}
```

</details>

<details>

<summary>Call 483: contracts.models.ToolResult.consistent</summary>

Source: `.\contracts\models.py`, line 286.

```json
{
  "call": 483,
  "parent_call": 471,
  "function": "contracts.models.ToolResult.consistent",
  "source": ".\\contracts\\models.py",
  "line": 286,
  "inputs": {
    "self": {
      "data": {
        "columns": [
          "handle",
          "ts_ns",
          "service",
          "severity",
          "body",
          "trace_id",
          "span_id",
          "count"
        ],
        "rows": [
          [
            "L3",
            1773497385000000000,
            "email",
            "ERROR",
            "delivery attempt timed out; queued for retry",
            null,
            null,
            1
          ],
          [
            "L4",
            1773497390000000000,
            "email",
            "ERROR",
            "delivery attempt timed out; queued for retry",
            null,
            null,
            1
          ]
        ]
      },
      "total_matches": 5,
      "returned": 2,
      "truncated": true,
      "next_cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4",
      "query_id": "q8986b892",
      "source": {
        "backend": "parquet",
        "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
        "tool_version": "0.1.1"
      },
      "warnings": []
    }
  },
  "closure_values": {},
  "output": {
    "data": {
      "columns": [
        "handle",
        "ts_ns",
        "service",
        "severity",
        "body",
        "trace_id",
        "span_id",
        "count"
      ],
      "rows": [
        [
          "L3",
          1773497385000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ],
        [
          "L4",
          1773497390000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ]
      ]
    },
    "total_matches": 5,
    "returned": 2,
    "truncated": true,
    "next_cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4",
    "query_id": "q8986b892",
    "source": {
      "backend": "parquet",
      "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
      "tool_version": "0.1.1"
    },
    "warnings": []
  }
}
```

</details>

<details>

<summary>Call 486: pydantic.main.BaseModel.model_dump</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 427.

```json
{
  "call": 486,
  "parent_call": 451,
  "function": "pydantic.main.BaseModel.model_dump",
  "source": ".\\.venv\\Lib\\site-packages\\pydantic\\main.py",
  "line": 427,
  "inputs": {
    "mode": "python",
    "include": null,
    "exclude": null,
    "context": null,
    "by_alias": null,
    "exclude_unset": false,
    "exclude_defaults": false,
    "exclude_none": false,
    "exclude_computed_fields": false,
    "round_trip": false,
    "warnings": true,
    "fallback": null,
    "serialize_as_any": false,
    "polymorphic_serialization": null,
    "self": {
      "data": {
        "columns": [
          "handle",
          "ts_ns",
          "service",
          "severity",
          "body",
          "trace_id",
          "span_id",
          "count"
        ],
        "rows": [
          [
            "L3",
            1773497385000000000,
            "email",
            "ERROR",
            "delivery attempt timed out; queued for retry",
            null,
            null,
            1
          ],
          [
            "L4",
            1773497390000000000,
            "email",
            "ERROR",
            "delivery attempt timed out; queued for retry",
            null,
            null,
            1
          ]
        ]
      },
      "total_matches": 5,
      "returned": 2,
      "truncated": true,
      "next_cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4",
      "query_id": "q8986b892",
      "source": {
        "backend": "parquet",
        "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
        "tool_version": "0.1.1"
      },
      "warnings": []
    }
  },
  "closure_values": {},
  "output": {
    "data": {
      "columns": [
        "handle",
        "ts_ns",
        "service",
        "severity",
        "body",
        "trace_id",
        "span_id",
        "count"
      ],
      "rows": [
        [
          "L3",
          1773497385000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ],
        [
          "L4",
          1773497390000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ]
      ]
    },
    "total_matches": 5,
    "returned": 2,
    "truncated": true,
    "next_cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4",
    "query_id": "q8986b892",
    "source": {
      "backend": "parquet",
      "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
      "tool_version": "0.1.1"
    },
    "warnings": []
  }
}
```

</details>

<details>

<summary>Call 488: store.evidence.compact_json</summary>

Source: `.\store\evidence.py`, line 70.

```json
{
  "call": 488,
  "parent_call": 75,
  "function": "store.evidence.compact_json",
  "source": ".\\store\\evidence.py",
  "line": 70,
  "inputs": {
    "value": {
      "data": {
        "columns": [
          "handle",
          "ts_ns",
          "service",
          "severity",
          "body",
          "trace_id",
          "span_id",
          "count"
        ],
        "rows": [
          [
            "L3",
            1773497385000000000,
            "email",
            "ERROR",
            "delivery attempt timed out; queued for retry",
            null,
            null,
            1
          ],
          [
            "L4",
            1773497390000000000,
            "email",
            "ERROR",
            "delivery attempt timed out; queued for retry",
            null,
            null,
            1
          ]
        ]
      },
      "total_matches": 5,
      "returned": 2,
      "truncated": true,
      "next_cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4",
      "query_id": "q8986b892",
      "source": {
        "backend": "parquet",
        "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
        "tool_version": "0.1.1"
      },
      "warnings": []
    }
  },
  "closure_values": {},
  "output": "{\"data\":{\"columns\":[\"handle\",\"ts_ns\",\"service\",\"severity\",\"body\",\"trace_id\",\"span_id\",\"count\"],\"rows\":[[\"L3\",1773497385000000000,\"email\",\"ERROR\",\"delivery attempt timed out; queued for retry\",null,null,1],[\"L4\",1773497390000000000,\"email\",\"ERROR\",\"delivery attempt timed out; queued for retry\",null,null,1]]},\"total_matches\":5,\"returned\":2,\"truncated\":true,\"next_cursor\":\"8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4\",\"query_id\":\"q8986b892\",\"source\":{\"backend\":\"parquet\",\"dataset_id\":\"856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb\",\"tool_version\":\"0.1.1\"},\"warnings\":[]}"
}
```

</details>

<details>

<summary>Call 496: mcp_servers.telemetry.engine.ToolEngine.__init__.&lt;locals&gt;.&lt;lambda&gt;</summary>

Source: `.\mcp_servers\telemetry\engine.py`, line 44.

```json
{
  "call": 496,
  "parent_call": 75,
  "function": "mcp_servers.telemetry.engine.ToolEngine.__init__.<locals>.<lambda>",
  "source": ".\\mcp_servers\\telemetry\\engine.py",
  "line": 44,
  "inputs": {
    "text": "{\"data\":{\"columns\":[\"handle\",\"ts_ns\",\"service\",\"severity\",\"body\",\"trace_id\",\"span_id\",\"count\"],\"rows\":[[\"L3\",1773497385000000000,\"email\",\"ERROR\",\"delivery attempt timed out; queued for retry\",null,null,1],[\"L4\",1773497390000000000,\"email\",\"ERROR\",\"delivery attempt timed out; queued for retry\",null,null,1]]},\"total_matches\":5,\"returned\":2,\"truncated\":true,\"next_cursor\":\"8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4\",\"query_id\":\"q8986b892\",\"source\":{\"backend\":\"parquet\",\"dataset_id\":\"856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb\",\"tool_version\":\"0.1.1\"},\"warnings\":[]}"
  },
  "closure_values": {},
  "output": 611
}
```

</details>

<details>

<summary>Call 499: mcp_servers.telemetry.engine.ToolEngine.call.&lt;locals&gt;.envelope</summary>

Source: `.\mcp_servers\telemetry\engine.py`, line 79.

```json
{
  "call": 499,
  "parent_call": 75,
  "function": "mcp_servers.telemetry.engine.ToolEngine.call.<locals>.envelope",
  "source": ".\\mcp_servers\\telemetry\\engine.py",
  "line": 79,
  "inputs": {
    "self": "<mcp_servers.telemetry.engine.ToolEngine>"
  },
  "closure_values": {
    "all_rows": [
      [
        1773497375000000000,
        "email",
        "ERROR",
        "delivery attempt timed out; queued for retry",
        null,
        null,
        1
      ],
      [
        1773497380000000000,
        "email",
        "ERROR",
        "delivery attempt timed out; queued for retry",
        null,
        null,
        1
      ],
      [
        1773497385000000000,
        "email",
        "ERROR",
        "delivery attempt timed out; queued for retry",
        null,
        null,
        1
      ],
      [
        1773497390000000000,
        "email",
        "ERROR",
        "delivery attempt timed out; queued for retry",
        null,
        null,
        1
      ],
      [
        1773497395000000000,
        "email",
        "ERROR",
        "delivery attempt timed out; queued for retry",
        null,
        null,
        1
      ]
    ],
    "columns": [
      "ts_ns",
      "service",
      "severity",
      "body",
      "trace_id",
      "span_id",
      "count"
    ],
    "digest": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21",
    "offset": 2,
    "query_id": "q8986b892",
    "selected": [
      [
        "L3",
        1773497385000000000,
        "email",
        "ERROR",
        "delivery attempt timed out; queued for retry",
        null,
        null,
        1
      ],
      [
        "L4",
        1773497390000000000,
        "email",
        "ERROR",
        "delivery attempt timed out; queued for retry",
        null,
        null,
        1
      ]
    ],
    "self": "<mcp_servers.telemetry.engine.ToolEngine>",
    "warnings": []
  },
  "output": {
    "data": {
      "columns": [
        "handle",
        "ts_ns",
        "service",
        "severity",
        "body",
        "trace_id",
        "span_id",
        "count"
      ],
      "rows": [
        [
          "L3",
          1773497385000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ],
        [
          "L4",
          1773497390000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ]
      ]
    },
    "total_matches": 5,
    "returned": 2,
    "truncated": true,
    "next_cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4",
    "query_id": "q8986b892",
    "source": {
      "backend": "parquet",
      "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
      "tool_version": "0.1.1"
    },
    "warnings": []
  }
}
```

</details>

<details>

<summary>Call 502: pydantic.main.BaseModel.__init__</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 253.

```json
{
  "call": 502,
  "parent_call": 499,
  "function": "pydantic.main.BaseModel.__init__",
  "source": ".\\.venv\\Lib\\site-packages\\pydantic\\main.py",
  "line": 253,
  "inputs": {
    "data": {
      "columns": [
        "handle",
        "ts_ns",
        "service",
        "severity",
        "body",
        "trace_id",
        "span_id",
        "count"
      ],
      "rows": [
        [
          "L3",
          1773497385000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ],
        [
          "L4",
          1773497390000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ]
      ]
    },
    "self": {}
  },
  "closure_values": {},
  "output": null,
  "constructed_object": {
    "columns": [
      "handle",
      "ts_ns",
      "service",
      "severity",
      "body",
      "trace_id",
      "span_id",
      "count"
    ],
    "rows": [
      [
        "L3",
        1773497385000000000,
        "email",
        "ERROR",
        "delivery attempt timed out; queued for retry",
        null,
        null,
        1
      ],
      [
        "L4",
        1773497390000000000,
        "email",
        "ERROR",
        "delivery attempt timed out; queued for retry",
        null,
        null,
        1
      ]
    ]
  }
}
```

</details>

<details>

<summary>Call 504: contracts.models.TableData.rectangular</summary>

Source: `.\contracts\models.py`, line 256.

```json
{
  "call": 504,
  "parent_call": 503,
  "function": "contracts.models.TableData.rectangular",
  "source": ".\\contracts\\models.py",
  "line": 256,
  "inputs": {
    "self": {
      "columns": [
        "handle",
        "ts_ns",
        "service",
        "severity",
        "body",
        "trace_id",
        "span_id",
        "count"
      ],
      "rows": [
        [
          "L3",
          1773497385000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ],
        [
          "L4",
          1773497390000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ]
      ]
    }
  },
  "closure_values": {},
  "output": {
    "columns": [
      "handle",
      "ts_ns",
      "service",
      "severity",
      "body",
      "trace_id",
      "span_id",
      "count"
    ],
    "rows": [
      [
        "L3",
        1773497385000000000,
        "email",
        "ERROR",
        "delivery attempt timed out; queued for retry",
        null,
        null,
        1
      ],
      [
        "L4",
        1773497390000000000,
        "email",
        "ERROR",
        "delivery attempt timed out; queued for retry",
        null,
        null,
        1
      ]
    ]
  }
}
```

</details>

<details>

<summary>Call 516: pydantic.main.BaseModel.__init__</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 253.

```json
{
  "call": 516,
  "parent_call": 499,
  "function": "pydantic.main.BaseModel.__init__",
  "source": ".\\.venv\\Lib\\site-packages\\pydantic\\main.py",
  "line": 253,
  "inputs": {
    "data": {
      "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
      "tool_version": "0.1.1"
    },
    "self": {}
  },
  "closure_values": {},
  "output": null,
  "constructed_object": {
    "backend": "parquet",
    "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
    "tool_version": "0.1.1"
  }
}
```

</details>

<details>

<summary>Call 518: pydantic.main.BaseModel.__init__</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 253.

```json
{
  "call": 518,
  "parent_call": 499,
  "function": "pydantic.main.BaseModel.__init__",
  "source": ".\\.venv\\Lib\\site-packages\\pydantic\\main.py",
  "line": 253,
  "inputs": {
    "data": {
      "data": {
        "columns": [
          "handle",
          "ts_ns",
          "service",
          "severity",
          "body",
          "trace_id",
          "span_id",
          "count"
        ],
        "rows": [
          [
            "L3",
            1773497385000000000,
            "email",
            "ERROR",
            "delivery attempt timed out; queued for retry",
            null,
            null,
            1
          ],
          [
            "L4",
            1773497390000000000,
            "email",
            "ERROR",
            "delivery attempt timed out; queued for retry",
            null,
            null,
            1
          ]
        ]
      },
      "total_matches": 5,
      "returned": 2,
      "truncated": true,
      "next_cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4",
      "query_id": "q8986b892",
      "source": {
        "backend": "parquet",
        "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
        "tool_version": "0.1.1"
      },
      "warnings": []
    },
    "self": {}
  },
  "closure_values": {},
  "output": null,
  "constructed_object": {
    "data": {
      "columns": [
        "handle",
        "ts_ns",
        "service",
        "severity",
        "body",
        "trace_id",
        "span_id",
        "count"
      ],
      "rows": [
        [
          "L3",
          1773497385000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ],
        [
          "L4",
          1773497390000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ]
      ]
    },
    "total_matches": 5,
    "returned": 2,
    "truncated": true,
    "next_cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4",
    "query_id": "q8986b892",
    "source": {
      "backend": "parquet",
      "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
      "tool_version": "0.1.1"
    },
    "warnings": []
  }
}
```

</details>

<details>

<summary>Call 520: contracts.models.TableData.rectangular</summary>

Source: `.\contracts\models.py`, line 256.

```json
{
  "call": 520,
  "parent_call": 519,
  "function": "contracts.models.TableData.rectangular",
  "source": ".\\contracts\\models.py",
  "line": 256,
  "inputs": {
    "self": {
      "columns": [
        "handle",
        "ts_ns",
        "service",
        "severity",
        "body",
        "trace_id",
        "span_id",
        "count"
      ],
      "rows": [
        [
          "L3",
          1773497385000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ],
        [
          "L4",
          1773497390000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ]
      ]
    }
  },
  "closure_values": {},
  "output": {
    "columns": [
      "handle",
      "ts_ns",
      "service",
      "severity",
      "body",
      "trace_id",
      "span_id",
      "count"
    ],
    "rows": [
      [
        "L3",
        1773497385000000000,
        "email",
        "ERROR",
        "delivery attempt timed out; queued for retry",
        null,
        null,
        1
      ],
      [
        "L4",
        1773497390000000000,
        "email",
        "ERROR",
        "delivery attempt timed out; queued for retry",
        null,
        null,
        1
      ]
    ]
  }
}
```

</details>

<details>

<summary>Call 531: contracts.models.ToolResult.consistent</summary>

Source: `.\contracts\models.py`, line 286.

```json
{
  "call": 531,
  "parent_call": 519,
  "function": "contracts.models.ToolResult.consistent",
  "source": ".\\contracts\\models.py",
  "line": 286,
  "inputs": {
    "self": {
      "data": {
        "columns": [
          "handle",
          "ts_ns",
          "service",
          "severity",
          "body",
          "trace_id",
          "span_id",
          "count"
        ],
        "rows": [
          [
            "L3",
            1773497385000000000,
            "email",
            "ERROR",
            "delivery attempt timed out; queued for retry",
            null,
            null,
            1
          ],
          [
            "L4",
            1773497390000000000,
            "email",
            "ERROR",
            "delivery attempt timed out; queued for retry",
            null,
            null,
            1
          ]
        ]
      },
      "total_matches": 5,
      "returned": 2,
      "truncated": true,
      "next_cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4",
      "query_id": "q8986b892",
      "source": {
        "backend": "parquet",
        "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
        "tool_version": "0.1.1"
      },
      "warnings": []
    }
  },
  "closure_values": {},
  "output": {
    "data": {
      "columns": [
        "handle",
        "ts_ns",
        "service",
        "severity",
        "body",
        "trace_id",
        "span_id",
        "count"
      ],
      "rows": [
        [
          "L3",
          1773497385000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ],
        [
          "L4",
          1773497390000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ]
      ]
    },
    "total_matches": 5,
    "returned": 2,
    "truncated": true,
    "next_cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4",
    "query_id": "q8986b892",
    "source": {
      "backend": "parquet",
      "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
      "tool_version": "0.1.1"
    },
    "warnings": []
  }
}
```

</details>

<details>

<summary>Call 534: pydantic.main.BaseModel.model_dump</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 427.

```json
{
  "call": 534,
  "parent_call": 499,
  "function": "pydantic.main.BaseModel.model_dump",
  "source": ".\\.venv\\Lib\\site-packages\\pydantic\\main.py",
  "line": 427,
  "inputs": {
    "mode": "python",
    "include": null,
    "exclude": null,
    "context": null,
    "by_alias": null,
    "exclude_unset": false,
    "exclude_defaults": false,
    "exclude_none": false,
    "exclude_computed_fields": false,
    "round_trip": false,
    "warnings": true,
    "fallback": null,
    "serialize_as_any": false,
    "polymorphic_serialization": null,
    "self": {
      "data": {
        "columns": [
          "handle",
          "ts_ns",
          "service",
          "severity",
          "body",
          "trace_id",
          "span_id",
          "count"
        ],
        "rows": [
          [
            "L3",
            1773497385000000000,
            "email",
            "ERROR",
            "delivery attempt timed out; queued for retry",
            null,
            null,
            1
          ],
          [
            "L4",
            1773497390000000000,
            "email",
            "ERROR",
            "delivery attempt timed out; queued for retry",
            null,
            null,
            1
          ]
        ]
      },
      "total_matches": 5,
      "returned": 2,
      "truncated": true,
      "next_cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4",
      "query_id": "q8986b892",
      "source": {
        "backend": "parquet",
        "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
        "tool_version": "0.1.1"
      },
      "warnings": []
    }
  },
  "closure_values": {},
  "output": {
    "data": {
      "columns": [
        "handle",
        "ts_ns",
        "service",
        "severity",
        "body",
        "trace_id",
        "span_id",
        "count"
      ],
      "rows": [
        [
          "L3",
          1773497385000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ],
        [
          "L4",
          1773497390000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ]
      ]
    },
    "total_matches": 5,
    "returned": 2,
    "truncated": true,
    "next_cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4",
    "query_id": "q8986b892",
    "source": {
      "backend": "parquet",
      "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
      "tool_version": "0.1.1"
    },
    "warnings": []
  }
}
```

</details>

<details>

<summary>Call 536: store.evidence.compact_json</summary>

Source: `.\store\evidence.py`, line 70.

```json
{
  "call": 536,
  "parent_call": 75,
  "function": "store.evidence.compact_json",
  "source": ".\\store\\evidence.py",
  "line": 70,
  "inputs": {
    "value": {
      "data": {
        "columns": [
          "handle",
          "ts_ns",
          "service",
          "severity",
          "body",
          "trace_id",
          "span_id",
          "count"
        ],
        "rows": [
          [
            "L3",
            1773497385000000000,
            "email",
            "ERROR",
            "delivery attempt timed out; queued for retry",
            null,
            null,
            1
          ],
          [
            "L4",
            1773497390000000000,
            "email",
            "ERROR",
            "delivery attempt timed out; queued for retry",
            null,
            null,
            1
          ]
        ]
      },
      "total_matches": 5,
      "returned": 2,
      "truncated": true,
      "next_cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4",
      "query_id": "q8986b892",
      "source": {
        "backend": "parquet",
        "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
        "tool_version": "0.1.1"
      },
      "warnings": []
    }
  },
  "closure_values": {},
  "output": "{\"data\":{\"columns\":[\"handle\",\"ts_ns\",\"service\",\"severity\",\"body\",\"trace_id\",\"span_id\",\"count\"],\"rows\":[[\"L3\",1773497385000000000,\"email\",\"ERROR\",\"delivery attempt timed out; queued for retry\",null,null,1],[\"L4\",1773497390000000000,\"email\",\"ERROR\",\"delivery attempt timed out; queued for retry\",null,null,1]]},\"total_matches\":5,\"returned\":2,\"truncated\":true,\"next_cursor\":\"8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4\",\"query_id\":\"q8986b892\",\"source\":{\"backend\":\"parquet\",\"dataset_id\":\"856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb\",\"tool_version\":\"0.1.1\"},\"warnings\":[]}"
}
```

</details>

<details>

<summary>Call 544: mcp_servers.telemetry.engine.ToolEngine.__init__.&lt;locals&gt;.&lt;lambda&gt;</summary>

Source: `.\mcp_servers\telemetry\engine.py`, line 44.

```json
{
  "call": 544,
  "parent_call": 75,
  "function": "mcp_servers.telemetry.engine.ToolEngine.__init__.<locals>.<lambda>",
  "source": ".\\mcp_servers\\telemetry\\engine.py",
  "line": 44,
  "inputs": {
    "text": "{\"data\":{\"columns\":[\"handle\",\"ts_ns\",\"service\",\"severity\",\"body\",\"trace_id\",\"span_id\",\"count\"],\"rows\":[[\"L3\",1773497385000000000,\"email\",\"ERROR\",\"delivery attempt timed out; queued for retry\",null,null,1],[\"L4\",1773497390000000000,\"email\",\"ERROR\",\"delivery attempt timed out; queued for retry\",null,null,1]]},\"total_matches\":5,\"returned\":2,\"truncated\":true,\"next_cursor\":\"8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4\",\"query_id\":\"q8986b892\",\"source\":{\"backend\":\"parquet\",\"dataset_id\":\"856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb\",\"tool_version\":\"0.1.1\"},\"warnings\":[]}"
  },
  "closure_values": {},
  "output": 611
}
```

</details>

<details>

<summary>Call 547: mcp.server.fastmcp.utilities.func_metadata.FuncMetadata.convert_result</summary>

Source: `.\.venv\Lib\site-packages\mcp\server\fastmcp\utilities\func_metadata.py`, line 97.

```json
{
  "call": 547,
  "parent_call": 37,
  "function": "mcp.server.fastmcp.utilities.func_metadata.FuncMetadata.convert_result",
  "source": ".\\.venv\\Lib\\site-packages\\mcp\\server\\fastmcp\\utilities\\func_metadata.py",
  "line": 97,
  "inputs": {
    "result": {
      "data": {
        "columns": [
          "handle",
          "ts_ns",
          "service",
          "severity",
          "body",
          "trace_id",
          "span_id",
          "count"
        ],
        "rows": [
          [
            "L3",
            1773497385000000000,
            "email",
            "ERROR",
            "delivery attempt timed out; queued for retry",
            null,
            null,
            1
          ],
          [
            "L4",
            1773497390000000000,
            "email",
            "ERROR",
            "delivery attempt timed out; queued for retry",
            null,
            null,
            1
          ]
        ]
      },
      "total_matches": 5,
      "returned": 2,
      "truncated": true,
      "next_cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4",
      "query_id": "q8986b892",
      "source": {
        "backend": "parquet",
        "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
        "tool_version": "0.1.1"
      },
      "warnings": []
    },
    "self": "<mcp.server.fastmcp.utilities.func_metadata.FuncMetadata>"
  },
  "closure_values": {},
  "output": [
    [
      {
        "type": "text",
        "text": "{\n  \"data\": {\n    \"columns\": [\n      \"handle\",\n      \"ts_ns\",\n      \"service\",\n      \"severity\",\n      \"body\",\n      \"trace_id\",\n      \"span_id\",\n      \"count\"\n    ],\n    \"rows\": [\n      [\n        \"L3\",\n        1773497385000000000,\n        \"email\",\n        \"ERROR\",\n        \"delivery attempt timed out; queued for retry\",\n        null,\n        null,\n        1\n      ],\n      [\n        \"L4\",\n        1773497390000000000,\n        \"email\",\n        \"ERROR\",\n        \"delivery attempt timed out; queued for retry\",\n        null,\n        null,\n        1\n      ]\n    ]\n  },\n  \"total_matches\": 5,\n  \"returned\": 2,\n  \"truncated\": true,\n  \"next_cursor\": \"8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4\",\n  \"query_id\": \"q8986b892\",\n  \"source\": {\n    \"backend\": \"parquet\",\n    \"dataset_id\": \"856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb\",\n    \"tool_version\": \"0.1.1\"\n  },\n  \"warnings\": []\n}",
        "annotations": null,
        "meta": null
      }
    ],
    {
      "data": {
        "columns": [
          "handle",
          "ts_ns",
          "service",
          "severity",
          "body",
          "trace_id",
          "span_id",
          "count"
        ],
        "rows": [
          [
            "L3",
            1773497385000000000,
            "email",
            "ERROR",
            "delivery attempt timed out; queued for retry",
            null,
            null,
            1
          ],
          [
            "L4",
            1773497390000000000,
            "email",
            "ERROR",
            "delivery attempt timed out; queued for retry",
            null,
            null,
            1
          ]
        ]
      },
      "total_matches": 5,
      "returned": 2,
      "truncated": true,
      "next_cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4",
      "query_id": "q8986b892",
      "source": {
        "backend": "parquet",
        "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
        "tool_version": "0.1.1"
      },
      "warnings": []
    }
  ]
}
```

</details>

<details>

<summary>Call 549: mcp.server.fastmcp.utilities.func_metadata._convert_to_content</summary>

Source: `.\.venv\Lib\site-packages\mcp\server\fastmcp\utilities\func_metadata.py`, line 499.

```json
{
  "call": 549,
  "parent_call": 547,
  "function": "mcp.server.fastmcp.utilities.func_metadata._convert_to_content",
  "source": ".\\.venv\\Lib\\site-packages\\mcp\\server\\fastmcp\\utilities\\func_metadata.py",
  "line": 499,
  "inputs": {
    "result": {
      "data": {
        "columns": [
          "handle",
          "ts_ns",
          "service",
          "severity",
          "body",
          "trace_id",
          "span_id",
          "count"
        ],
        "rows": [
          [
            "L3",
            1773497385000000000,
            "email",
            "ERROR",
            "delivery attempt timed out; queued for retry",
            null,
            null,
            1
          ],
          [
            "L4",
            1773497390000000000,
            "email",
            "ERROR",
            "delivery attempt timed out; queued for retry",
            null,
            null,
            1
          ]
        ]
      },
      "total_matches": 5,
      "returned": 2,
      "truncated": true,
      "next_cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4",
      "query_id": "q8986b892",
      "source": {
        "backend": "parquet",
        "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
        "tool_version": "0.1.1"
      },
      "warnings": []
    }
  },
  "closure_values": {},
  "output": [
    {
      "type": "text",
      "text": "{\n  \"data\": {\n    \"columns\": [\n      \"handle\",\n      \"ts_ns\",\n      \"service\",\n      \"severity\",\n      \"body\",\n      \"trace_id\",\n      \"span_id\",\n      \"count\"\n    ],\n    \"rows\": [\n      [\n        \"L3\",\n        1773497385000000000,\n        \"email\",\n        \"ERROR\",\n        \"delivery attempt timed out; queued for retry\",\n        null,\n        null,\n        1\n      ],\n      [\n        \"L4\",\n        1773497390000000000,\n        \"email\",\n        \"ERROR\",\n        \"delivery attempt timed out; queued for retry\",\n        null,\n        null,\n        1\n      ]\n    ]\n  },\n  \"total_matches\": 5,\n  \"returned\": 2,\n  \"truncated\": true,\n  \"next_cursor\": \"8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4\",\n  \"query_id\": \"q8986b892\",\n  \"source\": {\n    \"backend\": \"parquet\",\n    \"dataset_id\": \"856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb\",\n    \"tool_version\": \"0.1.1\"\n  },\n  \"warnings\": []\n}",
      "annotations": null,
      "meta": null
    }
  ]
}
```

</details>

<details>

<summary>Call 557: pydantic.main.BaseModel.__init__</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 253.

```json
{
  "call": 557,
  "parent_call": 549,
  "function": "pydantic.main.BaseModel.__init__",
  "source": ".\\.venv\\Lib\\site-packages\\pydantic\\main.py",
  "line": 253,
  "inputs": {
    "data": {
      "type": "text",
      "text": "{\n  \"data\": {\n    \"columns\": [\n      \"handle\",\n      \"ts_ns\",\n      \"service\",\n      \"severity\",\n      \"body\",\n      \"trace_id\",\n      \"span_id\",\n      \"count\"\n    ],\n    \"rows\": [\n      [\n        \"L3\",\n        1773497385000000000,\n        \"email\",\n        \"ERROR\",\n        \"delivery attempt timed out; queued for retry\",\n        null,\n        null,\n        1\n      ],\n      [\n        \"L4\",\n        1773497390000000000,\n        \"email\",\n        \"ERROR\",\n        \"delivery attempt timed out; queued for retry\",\n        null,\n        null,\n        1\n      ]\n    ]\n  },\n  \"total_matches\": 5,\n  \"returned\": 2,\n  \"truncated\": true,\n  \"next_cursor\": \"8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4\",\n  \"query_id\": \"q8986b892\",\n  \"source\": {\n    \"backend\": \"parquet\",\n    \"dataset_id\": \"856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb\",\n    \"tool_version\": \"0.1.1\"\n  },\n  \"warnings\": []\n}"
    },
    "self": "<mcp.types.TextContent>"
  },
  "closure_values": {},
  "output": null,
  "constructed_object": {
    "type": "text",
    "text": "{\n  \"data\": {\n    \"columns\": [\n      \"handle\",\n      \"ts_ns\",\n      \"service\",\n      \"severity\",\n      \"body\",\n      \"trace_id\",\n      \"span_id\",\n      \"count\"\n    ],\n    \"rows\": [\n      [\n        \"L3\",\n        1773497385000000000,\n        \"email\",\n        \"ERROR\",\n        \"delivery attempt timed out; queued for retry\",\n        null,\n        null,\n        1\n      ],\n      [\n        \"L4\",\n        1773497390000000000,\n        \"email\",\n        \"ERROR\",\n        \"delivery attempt timed out; queued for retry\",\n        null,\n        null,\n        1\n      ]\n    ]\n  },\n  \"total_matches\": 5,\n  \"returned\": 2,\n  \"truncated\": true,\n  \"next_cursor\": \"8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4\",\n  \"query_id\": \"q8986b892\",\n  \"source\": {\n    \"backend\": \"parquet\",\n    \"dataset_id\": \"856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb\",\n    \"tool_version\": \"0.1.1\"\n  },\n  \"warnings\": []\n}",
    "annotations": null,
    "meta": null
  }
}
```

</details>

<details>

<summary>Call 559: pydantic.main.BaseModel.model_validate</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 693.

```json
{
  "call": 559,
  "parent_call": 547,
  "function": "pydantic.main.BaseModel.model_validate",
  "source": ".\\.venv\\Lib\\site-packages\\pydantic\\main.py",
  "line": 693,
  "inputs": {
    "obj": {
      "data": {
        "columns": [
          "handle",
          "ts_ns",
          "service",
          "severity",
          "body",
          "trace_id",
          "span_id",
          "count"
        ],
        "rows": [
          [
            "L3",
            1773497385000000000,
            "email",
            "ERROR",
            "delivery attempt timed out; queued for retry",
            null,
            null,
            1
          ],
          [
            "L4",
            1773497390000000000,
            "email",
            "ERROR",
            "delivery attempt timed out; queued for retry",
            null,
            null,
            1
          ]
        ]
      },
      "total_matches": 5,
      "returned": 2,
      "truncated": true,
      "next_cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4",
      "query_id": "q8986b892",
      "source": {
        "backend": "parquet",
        "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
        "tool_version": "0.1.1"
      },
      "warnings": []
    },
    "strict": null,
    "extra": null,
    "from_attributes": null,
    "context": null,
    "by_alias": null,
    "by_name": null,
    "cls": "<class mcp.server.fastmcp.utilities.func_metadata.search_logsDictOutput>"
  },
  "closure_values": {},
  "output": {
    "data": {
      "columns": [
        "handle",
        "ts_ns",
        "service",
        "severity",
        "body",
        "trace_id",
        "span_id",
        "count"
      ],
      "rows": [
        [
          "L3",
          1773497385000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ],
        [
          "L4",
          1773497390000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ]
      ]
    },
    "total_matches": 5,
    "returned": 2,
    "truncated": true,
    "next_cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4",
    "query_id": "q8986b892",
    "source": {
      "backend": "parquet",
      "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
      "tool_version": "0.1.1"
    },
    "warnings": []
  }
}
```

</details>

<details>

<summary>Call 561: pydantic.main.BaseModel.model_dump</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 427.

```json
{
  "call": 561,
  "parent_call": 547,
  "function": "pydantic.main.BaseModel.model_dump",
  "source": ".\\.venv\\Lib\\site-packages\\pydantic\\main.py",
  "line": 427,
  "inputs": {
    "mode": "json",
    "include": null,
    "exclude": null,
    "context": null,
    "by_alias": true,
    "exclude_unset": false,
    "exclude_defaults": false,
    "exclude_none": false,
    "exclude_computed_fields": false,
    "round_trip": false,
    "warnings": true,
    "fallback": null,
    "serialize_as_any": false,
    "polymorphic_serialization": null,
    "self": {
      "data": {
        "columns": [
          "handle",
          "ts_ns",
          "service",
          "severity",
          "body",
          "trace_id",
          "span_id",
          "count"
        ],
        "rows": [
          [
            "L3",
            1773497385000000000,
            "email",
            "ERROR",
            "delivery attempt timed out; queued for retry",
            null,
            null,
            1
          ],
          [
            "L4",
            1773497390000000000,
            "email",
            "ERROR",
            "delivery attempt timed out; queued for retry",
            null,
            null,
            1
          ]
        ]
      },
      "total_matches": 5,
      "returned": 2,
      "truncated": true,
      "next_cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4",
      "query_id": "q8986b892",
      "source": {
        "backend": "parquet",
        "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
        "tool_version": "0.1.1"
      },
      "warnings": []
    }
  },
  "closure_values": {},
  "output": {
    "data": {
      "columns": [
        "handle",
        "ts_ns",
        "service",
        "severity",
        "body",
        "trace_id",
        "span_id",
        "count"
      ],
      "rows": [
        [
          "L3",
          1773497385000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ],
        [
          "L4",
          1773497390000000000,
          "email",
          "ERROR",
          "delivery attempt timed out; queued for retry",
          null,
          null,
          1
        ]
      ]
    },
    "total_matches": 5,
    "returned": 2,
    "truncated": true,
    "next_cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4",
    "query_id": "q8986b892",
    "source": {
      "backend": "parquet",
      "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
      "tool_version": "0.1.1"
    },
    "warnings": []
  }
}
```

</details>

<details>

<summary>Call 2870: pydantic.main.BaseModel.__init__</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 253.

```json
{
  "call": 2870,
  "parent_call": 1,
  "function": "pydantic.main.BaseModel.__init__",
  "source": ".\\.venv\\Lib\\site-packages\\pydantic\\main.py",
  "line": 253,
  "inputs": {
    "data": {
      "content": [
        {
          "type": "text",
          "text": "{\n  \"data\": {\n    \"columns\": [\n      \"handle\",\n      \"ts_ns\",\n      \"service\",\n      \"severity\",\n      \"body\",\n      \"trace_id\",\n      \"span_id\",\n      \"count\"\n    ],\n    \"rows\": [\n      [\n        \"L3\",\n        1773497385000000000,\n        \"email\",\n        \"ERROR\",\n        \"delivery attempt timed out; queued for retry\",\n        null,\n        null,\n        1\n      ],\n      [\n        \"L4\",\n        1773497390000000000,\n        \"email\",\n        \"ERROR\",\n        \"delivery attempt timed out; queued for retry\",\n        null,\n        null,\n        1\n      ]\n    ]\n  },\n  \"total_matches\": 5,\n  \"returned\": 2,\n  \"truncated\": true,\n  \"next_cursor\": \"8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4\",\n  \"query_id\": \"q8986b892\",\n  \"source\": {\n    \"backend\": \"parquet\",\n    \"dataset_id\": \"856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb\",\n    \"tool_version\": \"0.1.1\"\n  },\n  \"warnings\": []\n}",
          "annotations": null,
          "meta": null
        }
      ],
      "structuredContent": {
        "data": {
          "columns": [
            "handle",
            "ts_ns",
            "service",
            "severity",
            "body",
            "trace_id",
            "span_id",
            "count"
          ],
          "rows": [
            [
              "L3",
              1773497385000000000,
              "email",
              "ERROR",
              "delivery attempt timed out; queued for retry",
              null,
              null,
              1
            ],
            [
              "L4",
              1773497390000000000,
              "email",
              "ERROR",
              "delivery attempt timed out; queued for retry",
              null,
              null,
              1
            ]
          ]
        },
        "total_matches": 5,
        "returned": 2,
        "truncated": true,
        "next_cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4",
        "query_id": "q8986b892",
        "source": {
          "backend": "parquet",
          "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
          "tool_version": "0.1.1"
        },
        "warnings": []
      },
      "isError": false
    },
    "self": "<mcp.types.CallToolResult>"
  },
  "closure_values": {},
  "output": null,
  "constructed_object": {
    "meta": null,
    "content": [
      {
        "type": "text",
        "text": "{\n  \"data\": {\n    \"columns\": [\n      \"handle\",\n      \"ts_ns\",\n      \"service\",\n      \"severity\",\n      \"body\",\n      \"trace_id\",\n      \"span_id\",\n      \"count\"\n    ],\n    \"rows\": [\n      [\n        \"L3\",\n        1773497385000000000,\n        \"email\",\n        \"ERROR\",\n        \"delivery attempt timed out; queued for retry\",\n        null,\n        null,\n        1\n      ],\n      [\n        \"L4\",\n        1773497390000000000,\n        \"email\",\n        \"ERROR\",\n        \"delivery attempt timed out; queued for retry\",\n        null,\n        null,\n        1\n      ]\n    ]\n  },\n  \"total_matches\": 5,\n  \"returned\": 2,\n  \"truncated\": true,\n  \"next_cursor\": \"8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4\",\n  \"query_id\": \"q8986b892\",\n  \"source\": {\n    \"backend\": \"parquet\",\n    \"dataset_id\": \"856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb\",\n    \"tool_version\": \"0.1.1\"\n  },\n  \"warnings\": []\n}",
        "annotations": null,
        "meta": null
      }
    ],
    "structuredContent": {
      "data": {
        "columns": [
          "handle",
          "ts_ns",
          "service",
          "severity",
          "body",
          "trace_id",
          "span_id",
          "count"
        ],
        "rows": [
          [
            "L3",
            1773497385000000000,
            "email",
            "ERROR",
            "delivery attempt timed out; queued for retry",
            null,
            null,
            1
          ],
          [
            "L4",
            1773497390000000000,
            "email",
            "ERROR",
            "delivery attempt timed out; queued for retry",
            null,
            null,
            1
          ]
        ]
      },
      "total_matches": 5,
      "returned": 2,
      "truncated": true,
      "next_cursor": "8986b89280c72f1747e821ed66a6b976a2f7c46f464128b10d06a3dcb61b6a21:4",
      "query_id": "q8986b892",
      "source": {
        "backend": "parquet",
        "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
        "tool_version": "0.1.1"
      },
      "warnings": []
    },
    "isError": false
  }
}
```

</details>
