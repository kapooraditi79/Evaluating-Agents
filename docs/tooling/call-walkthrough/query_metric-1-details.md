# query_metric-1: function inputs and outputs

These inputs and outputs were observed during a real stdio MCP request. Calls are listed in entry order; the output of an outer call is produced after its nested calls complete. Expand a function to inspect its data. Infrastructure objects are described by type; model objects are shown as JSON. Python constructors return None; constructed_object shows the resulting model. Call numbers preserve the observed sequence; gaps include library calls and repeated generator-expression resumptions.

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
        "name": "query_metric",
        "arguments": {
          "query": {
            "window": {
              "start": "2026-03-14T14:00:00Z",
              "end": "2026-03-14T14:05:00Z"
            },
            "service": "frontend",
            "metric": "latency_p95_ms",
            "limit": 2
          }
        }
      },
      "jsonrpc": "2.0",
      "id": 2
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
        "text": "{\n  \"data\": {\n    \"columns\": [\n      \"handle\",\n      \"kind\",\n      \"start_ns\",\n      \"end_ns\",\n      \"value\",\n      \"absolute_error_bound\",\n      \"unit\"\n    ],\n    \"rows\": [\n      [\n        \"M1\",\n        \"summary\",\n        1773496800000000000,\n        1773497100000000000,\n        120.0,\n        40.0,\n        \"ms\"\n      ],\n      [\n        \"M2\",\n        \"bucket\",\n        1773496800000000000,\n        1773496860000000000,\n        120.0,\n        40.0,\n        \"ms\"\n      ]\n    ]\n  },\n  \"total_matches\": 6,\n  \"returned\": 2,\n  \"truncated\": true,\n  \"next_cursor\": \"4e6231a4fa2bc2925490d28c0ebc84335601f75441a9c2aa9d27b6b867525692:2\",\n  \"query_id\": \"q4e6231a4\",\n  \"source\": {\n    \"backend\": \"parquet\",\n    \"dataset_id\": \"856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb\",\n    \"tool_version\": \"0.1.1\"\n  },\n  \"warnings\": []\n}",
        "annotations": null,
        "meta": null
      }
    ],
    "structuredContent": {
      "data": {
        "columns": [
          "handle",
          "kind",
          "start_ns",
          "end_ns",
          "value",
          "absolute_error_bound",
          "unit"
        ],
        "rows": [
          [
            "M1",
            "summary",
            1773496800000000000,
            1773497100000000000,
            120.0,
            40.0,
            "ms"
          ],
          [
            "M2",
            "bucket",
            1773496800000000000,
            1773496860000000000,
            120.0,
            40.0,
            "ms"
          ]
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
    "tool_name": "query_metric",
    "self": "<mcp.server.lowlevel.server.Server>"
  },
  "closure_values": {},
  "output": {
    "name": "query_metric",
    "title": null,
    "description": "Summary + buckets. Native-aligned windows/steps; merged percentiles; gauge avg/max.",
    "inputSchema": {
      "$defs": {
        "QueryMetric": {
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
              "title": "Service",
              "type": "string"
            },
            "metric": {
              "enum": [
                "request_count",
                "error_count",
                "error_rate",
                "latency_p50_ms",
                "latency_p95_ms",
                "latency_p99_ms",
                "cpu_utilization",
                "memory_mb"
              ],
              "title": "Metric",
              "type": "string"
            },
            "operation": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "default": null,
              "title": "Operation"
            },
            "step_seconds": {
              "default": 60,
              "exclusiveMinimum": 0,
              "maximum": 86400,
              "title": "Step Seconds",
              "type": "integer"
            },
            "aggregation": {
              "default": "avg",
              "enum": [
                "avg",
                "max"
              ],
              "title": "Aggregation",
              "type": "string"
            }
          },
          "required": [
            "window",
            "service",
            "metric"
          ],
          "title": "QueryMetric",
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
          "$ref": "#/$defs/QueryMetric"
        }
      },
      "required": [
        "query"
      ],
      "title": "query_metricArguments",
      "type": "object"
    },
    "outputSchema": {
      "additionalProperties": true,
      "title": "query_metricDictOutput",
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
    "name": "query_metric",
    "arguments": {
      "query": {
        "window": {
          "start": "2026-03-14T14:00:00Z",
          "end": "2026-03-14T14:05:00Z"
        },
        "service": "frontend",
        "metric": "latency_p95_ms",
        "limit": 2
      }
    },
    "self": "<mcp.server.fastmcp.server.FastMCP>"
  },
  "closure_values": {},
  "output": [
    [
      {
        "type": "text",
        "text": "{\n  \"data\": {\n    \"columns\": [\n      \"handle\",\n      \"kind\",\n      \"start_ns\",\n      \"end_ns\",\n      \"value\",\n      \"absolute_error_bound\",\n      \"unit\"\n    ],\n    \"rows\": [\n      [\n        \"M1\",\n        \"summary\",\n        1773496800000000000,\n        1773497100000000000,\n        120.0,\n        40.0,\n        \"ms\"\n      ],\n      [\n        \"M2\",\n        \"bucket\",\n        1773496800000000000,\n        1773496860000000000,\n        120.0,\n        40.0,\n        \"ms\"\n      ]\n    ]\n  },\n  \"total_matches\": 6,\n  \"returned\": 2,\n  \"truncated\": true,\n  \"next_cursor\": \"4e6231a4fa2bc2925490d28c0ebc84335601f75441a9c2aa9d27b6b867525692:2\",\n  \"query_id\": \"q4e6231a4\",\n  \"source\": {\n    \"backend\": \"parquet\",\n    \"dataset_id\": \"856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb\",\n    \"tool_version\": \"0.1.1\"\n  },\n  \"warnings\": []\n}",
        "annotations": null,
        "meta": null
      }
    ],
    {
      "data": {
        "columns": [
          "handle",
          "kind",
          "start_ns",
          "end_ns",
          "value",
          "absolute_error_bound",
          "unit"
        ],
        "rows": [
          [
            "M1",
            "summary",
            1773496800000000000,
            1773497100000000000,
            120.0,
            40.0,
            "ms"
          ],
          [
            "M2",
            "bucket",
            1773496800000000000,
            1773496860000000000,
            120.0,
            40.0,
            "ms"
          ]
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

<summary>Call 48: mcp.server.fastmcp.tools.tool_manager.ToolManager.call_tool</summary>

Source: `.\.venv\Lib\site-packages\mcp\server\fastmcp\tools\tool_manager.py`, line 81.

```json
{
  "call": 48,
  "parent_call": 4,
  "function": "mcp.server.fastmcp.tools.tool_manager.ToolManager.call_tool",
  "source": ".\\.venv\\Lib\\site-packages\\mcp\\server\\fastmcp\\tools\\tool_manager.py",
  "line": 81,
  "inputs": {
    "name": "query_metric",
    "arguments": {
      "query": {
        "window": {
          "start": "2026-03-14T14:00:00Z",
          "end": "2026-03-14T14:05:00Z"
        },
        "service": "frontend",
        "metric": "latency_p95_ms",
        "limit": 2
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
        "text": "{\n  \"data\": {\n    \"columns\": [\n      \"handle\",\n      \"kind\",\n      \"start_ns\",\n      \"end_ns\",\n      \"value\",\n      \"absolute_error_bound\",\n      \"unit\"\n    ],\n    \"rows\": [\n      [\n        \"M1\",\n        \"summary\",\n        1773496800000000000,\n        1773497100000000000,\n        120.0,\n        40.0,\n        \"ms\"\n      ],\n      [\n        \"M2\",\n        \"bucket\",\n        1773496800000000000,\n        1773496860000000000,\n        120.0,\n        40.0,\n        \"ms\"\n      ]\n    ]\n  },\n  \"total_matches\": 6,\n  \"returned\": 2,\n  \"truncated\": true,\n  \"next_cursor\": \"4e6231a4fa2bc2925490d28c0ebc84335601f75441a9c2aa9d27b6b867525692:2\",\n  \"query_id\": \"q4e6231a4\",\n  \"source\": {\n    \"backend\": \"parquet\",\n    \"dataset_id\": \"856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb\",\n    \"tool_version\": \"0.1.1\"\n  },\n  \"warnings\": []\n}",
        "annotations": null,
        "meta": null
      }
    ],
    {
      "data": {
        "columns": [
          "handle",
          "kind",
          "start_ns",
          "end_ns",
          "value",
          "absolute_error_bound",
          "unit"
        ],
        "rows": [
          [
            "M1",
            "summary",
            1773496800000000000,
            1773497100000000000,
            120.0,
            40.0,
            "ms"
          ],
          [
            "M2",
            "bucket",
            1773496800000000000,
            1773496860000000000,
            120.0,
            40.0,
            "ms"
          ]
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
  ]
}
```

</details>

<details>

<summary>Call 49: mcp.server.fastmcp.tools.tool_manager.ToolManager.get_tool</summary>

Source: `.\.venv\Lib\site-packages\mcp\server\fastmcp\tools\tool_manager.py`, line 37.

```json
{
  "call": 49,
  "parent_call": 48,
  "function": "mcp.server.fastmcp.tools.tool_manager.ToolManager.get_tool",
  "source": ".\\.venv\\Lib\\site-packages\\mcp\\server\\fastmcp\\tools\\tool_manager.py",
  "line": 37,
  "inputs": {
    "name": "query_metric",
    "self": "<mcp.server.fastmcp.tools.tool_manager.ToolManager>"
  },
  "closure_values": {},
  "output": "<mcp.server.fastmcp.tools.base.Tool>"
}
```

</details>

<details>

<summary>Call 51: mcp.server.fastmcp.tools.base.Tool.run</summary>

Source: `.\.venv\Lib\site-packages\mcp\server\fastmcp\tools\base.py`, line 93.

```json
{
  "call": 51,
  "parent_call": 48,
  "function": "mcp.server.fastmcp.tools.base.Tool.run",
  "source": ".\\.venv\\Lib\\site-packages\\mcp\\server\\fastmcp\\tools\\base.py",
  "line": 93,
  "inputs": {
    "arguments": {
      "query": {
        "window": {
          "start": "2026-03-14T14:00:00Z",
          "end": "2026-03-14T14:05:00Z"
        },
        "service": "frontend",
        "metric": "latency_p95_ms",
        "limit": 2
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
        "text": "{\n  \"data\": {\n    \"columns\": [\n      \"handle\",\n      \"kind\",\n      \"start_ns\",\n      \"end_ns\",\n      \"value\",\n      \"absolute_error_bound\",\n      \"unit\"\n    ],\n    \"rows\": [\n      [\n        \"M1\",\n        \"summary\",\n        1773496800000000000,\n        1773497100000000000,\n        120.0,\n        40.0,\n        \"ms\"\n      ],\n      [\n        \"M2\",\n        \"bucket\",\n        1773496800000000000,\n        1773496860000000000,\n        120.0,\n        40.0,\n        \"ms\"\n      ]\n    ]\n  },\n  \"total_matches\": 6,\n  \"returned\": 2,\n  \"truncated\": true,\n  \"next_cursor\": \"4e6231a4fa2bc2925490d28c0ebc84335601f75441a9c2aa9d27b6b867525692:2\",\n  \"query_id\": \"q4e6231a4\",\n  \"source\": {\n    \"backend\": \"parquet\",\n    \"dataset_id\": \"856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb\",\n    \"tool_version\": \"0.1.1\"\n  },\n  \"warnings\": []\n}",
        "annotations": null,
        "meta": null
      }
    ],
    {
      "data": {
        "columns": [
          "handle",
          "kind",
          "start_ns",
          "end_ns",
          "value",
          "absolute_error_bound",
          "unit"
        ],
        "rows": [
          [
            "M1",
            "summary",
            1773496800000000000,
            1773497100000000000,
            120.0,
            40.0,
            "ms"
          ],
          [
            "M2",
            "bucket",
            1773496800000000000,
            1773496860000000000,
            120.0,
            40.0,
            "ms"
          ]
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
  ]
}
```

</details>

<details>

<summary>Call 52: mcp.server.fastmcp.utilities.func_metadata.FuncMetadata.call_fn_with_arg_validation</summary>

Source: `.\.venv\Lib\site-packages\mcp\server\fastmcp\utilities\func_metadata.py`, line 74.

```json
{
  "call": 52,
  "parent_call": 51,
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
          "end": "2026-03-14T14:05:00Z"
        },
        "service": "frontend",
        "metric": "latency_p95_ms",
        "limit": 2
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
        "kind",
        "start_ns",
        "end_ns",
        "value",
        "absolute_error_bound",
        "unit"
      ],
      "rows": [
        [
          "M1",
          "summary",
          1773496800000000000,
          1773497100000000000,
          120.0,
          40.0,
          "ms"
        ],
        [
          "M2",
          "bucket",
          1773496800000000000,
          1773496860000000000,
          120.0,
          40.0,
          "ms"
        ]
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
}
```

</details>

<details>

<summary>Call 53: mcp.server.fastmcp.utilities.func_metadata.FuncMetadata.pre_parse_json</summary>

Source: `.\.venv\Lib\site-packages\mcp\server\fastmcp\utilities\func_metadata.py`, line 133.

```json
{
  "call": 53,
  "parent_call": 52,
  "function": "mcp.server.fastmcp.utilities.func_metadata.FuncMetadata.pre_parse_json",
  "source": ".\\.venv\\Lib\\site-packages\\mcp\\server\\fastmcp\\utilities\\func_metadata.py",
  "line": 133,
  "inputs": {
    "data": {
      "query": {
        "window": {
          "start": "2026-03-14T14:00:00Z",
          "end": "2026-03-14T14:05:00Z"
        },
        "service": "frontend",
        "metric": "latency_p95_ms",
        "limit": 2
      }
    },
    "self": "<mcp.server.fastmcp.utilities.func_metadata.FuncMetadata>"
  },
  "closure_values": {},
  "output": {
    "query": {
      "window": {
        "start": "2026-03-14T14:00:00Z",
        "end": "2026-03-14T14:05:00Z"
      },
      "service": "frontend",
      "metric": "latency_p95_ms",
      "limit": 2
    }
  }
}
```

</details>

<details>

<summary>Call 63: pydantic.main.BaseModel.model_validate</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 693.

```json
{
  "call": 63,
  "parent_call": 52,
  "function": "pydantic.main.BaseModel.model_validate",
  "source": ".\\.venv\\Lib\\site-packages\\pydantic\\main.py",
  "line": 693,
  "inputs": {
    "obj": {
      "query": {
        "window": {
          "start": "2026-03-14T14:00:00Z",
          "end": "2026-03-14T14:05:00Z"
        },
        "service": "frontend",
        "metric": "latency_p95_ms",
        "limit": 2
      }
    },
    "strict": null,
    "extra": null,
    "from_attributes": null,
    "context": null,
    "by_alias": null,
    "by_name": null,
    "cls": "<class mcp.server.fastmcp.utilities.func_metadata.query_metricArguments>"
  },
  "closure_values": {},
  "output": {
    "query": {
      "window": {
        "start": "2026-03-14T14:00:00Z",
        "end": "2026-03-14T14:05:00Z"
      },
      "limit": 2,
      "cursor": null,
      "service": "frontend",
      "metric": "latency_p95_ms",
      "operation": null,
      "step_seconds": 60,
      "aggregation": "avg"
    }
  }
}
```

</details>

<details>

<summary>Call 65: contracts.models.Window.ordered</summary>

Source: `.\contracts\models.py`, line 45.

```json
{
  "call": 65,
  "parent_call": 64,
  "function": "contracts.models.Window.ordered",
  "source": ".\\contracts\\models.py",
  "line": 45,
  "inputs": {
    "self": {
      "start": "2026-03-14T14:00:00Z",
      "end": "2026-03-14T14:05:00Z"
    }
  },
  "closure_values": {},
  "output": {
    "start": "2026-03-14T14:00:00Z",
    "end": "2026-03-14T14:05:00Z"
  }
}
```

</details>

<details>

<summary>Call 66: contracts.models.utc_ns</summary>

Source: `.\contracts\models.py`, line 21.

```json
{
  "call": 66,
  "parent_call": 65,
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

<summary>Call 73: contracts.models.utc_ns</summary>

Source: `.\contracts\models.py`, line 21.

```json
{
  "call": 73,
  "parent_call": 65,
  "function": "contracts.models.utc_ns",
  "source": ".\\contracts\\models.py",
  "line": 21,
  "inputs": {
    "value": "2026-03-14T14:05:00Z"
  },
  "closure_values": {},
  "output": 1773497100000000000
}
```

</details>

<details>

<summary>Call 80: mcp.server.fastmcp.utilities.func_metadata.ArgModelBase.model_dump_one_level</summary>

Source: `.\.venv\Lib\site-packages\mcp\server\fastmcp\utilities\func_metadata.py`, line 50.

```json
{
  "call": 80,
  "parent_call": 52,
  "function": "mcp.server.fastmcp.utilities.func_metadata.ArgModelBase.model_dump_one_level",
  "source": ".\\.venv\\Lib\\site-packages\\mcp\\server\\fastmcp\\utilities\\func_metadata.py",
  "line": 50,
  "inputs": {
    "self": {
      "query": {
        "window": {
          "start": "2026-03-14T14:00:00Z",
          "end": "2026-03-14T14:05:00Z"
        },
        "limit": 2,
        "cursor": null,
        "service": "frontend",
        "metric": "latency_p95_ms",
        "operation": null,
        "step_seconds": 60,
        "aggregation": "avg"
      }
    }
  },
  "closure_values": {},
  "output": {
    "query": {
      "window": {
        "start": "2026-03-14T14:00:00Z",
        "end": "2026-03-14T14:05:00Z"
      },
      "limit": 2,
      "cursor": null,
      "service": "frontend",
      "metric": "latency_p95_ms",
      "operation": null,
      "step_seconds": 60,
      "aggregation": "avg"
    }
  }
}
```

</details>

<details>

<summary>Call 86: mcp_servers.telemetry.server.create_server.&lt;locals&gt;.query_metric</summary>

Source: `.\mcp_servers\telemetry\server.py`, line 43.

```json
{
  "call": 86,
  "parent_call": 52,
  "function": "mcp_servers.telemetry.server.create_server.<locals>.query_metric",
  "source": ".\\mcp_servers\\telemetry\\server.py",
  "line": 43,
  "inputs": {
    "query": {
      "window": {
        "start": "2026-03-14T14:00:00Z",
        "end": "2026-03-14T14:05:00Z"
      },
      "limit": 2,
      "cursor": null,
      "service": "frontend",
      "metric": "latency_p95_ms",
      "operation": null,
      "step_seconds": 60,
      "aggregation": "avg"
    }
  },
  "closure_values": {
    "engine": "<mcp_servers.telemetry.engine.ToolEngine>"
  },
  "output": {
    "data": {
      "columns": [
        "handle",
        "kind",
        "start_ns",
        "end_ns",
        "value",
        "absolute_error_bound",
        "unit"
      ],
      "rows": [
        [
          "M1",
          "summary",
          1773496800000000000,
          1773497100000000000,
          120.0,
          40.0,
          "ms"
        ],
        [
          "M2",
          "bucket",
          1773496800000000000,
          1773496860000000000,
          120.0,
          40.0,
          "ms"
        ]
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
}
```

</details>

<details>

<summary>Call 87: pydantic.main.BaseModel.model_dump</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 427.

```json
{
  "call": 87,
  "parent_call": 86,
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
        "end": "2026-03-14T14:05:00Z"
      },
      "limit": 2,
      "cursor": null,
      "service": "frontend",
      "metric": "latency_p95_ms",
      "operation": null,
      "step_seconds": 60,
      "aggregation": "avg"
    }
  },
  "closure_values": {},
  "output": {
    "window": {
      "start": "2026-03-14T14:00:00Z",
      "end": "2026-03-14T14:05:00Z"
    },
    "limit": 2,
    "cursor": null,
    "service": "frontend",
    "metric": "latency_p95_ms",
    "operation": null,
    "step_seconds": 60,
    "aggregation": "avg"
  }
}
```

</details>

<details>

<summary>Call 89: mcp_servers.telemetry.engine.ToolEngine.call</summary>

Source: `.\mcp_servers\telemetry\engine.py`, line 48.

```json
{
  "call": 89,
  "parent_call": 86,
  "function": "mcp_servers.telemetry.engine.ToolEngine.call",
  "source": ".\\mcp_servers\\telemetry\\engine.py",
  "line": 48,
  "inputs": {
    "tool": "query_metric",
    "arguments": {
      "window": {
        "start": "2026-03-14T14:00:00Z",
        "end": "2026-03-14T14:05:00Z"
      },
      "limit": 2,
      "cursor": null,
      "service": "frontend",
      "metric": "latency_p95_ms",
      "operation": null,
      "step_seconds": 60,
      "aggregation": "avg"
    },
    "self": "<mcp_servers.telemetry.engine.ToolEngine>"
  },
  "closure_values": {},
  "output": {
    "data": {
      "columns": [
        "handle",
        "kind",
        "start_ns",
        "end_ns",
        "value",
        "absolute_error_bound",
        "unit"
      ],
      "rows": [
        [
          "M1",
          "summary",
          1773496800000000000,
          1773497100000000000,
          120.0,
          40.0,
          "ms"
        ],
        [
          "M2",
          "bucket",
          1773496800000000000,
          1773496860000000000,
          120.0,
          40.0,
          "ms"
        ]
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
}
```

</details>

<details>

<summary>Call 90: pydantic.main.BaseModel.model_validate</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 693.

```json
{
  "call": 90,
  "parent_call": 89,
  "function": "pydantic.main.BaseModel.model_validate",
  "source": ".\\.venv\\Lib\\site-packages\\pydantic\\main.py",
  "line": 693,
  "inputs": {
    "obj": {
      "window": {
        "start": "2026-03-14T14:00:00Z",
        "end": "2026-03-14T14:05:00Z"
      },
      "limit": 2,
      "cursor": null,
      "service": "frontend",
      "metric": "latency_p95_ms",
      "operation": null,
      "step_seconds": 60,
      "aggregation": "avg"
    },
    "strict": null,
    "extra": null,
    "from_attributes": null,
    "context": null,
    "by_alias": null,
    "by_name": null,
    "cls": "<class contracts.queries.QueryMetric>"
  },
  "closure_values": {},
  "output": {
    "window": {
      "start": "2026-03-14T14:00:00Z",
      "end": "2026-03-14T14:05:00Z"
    },
    "limit": 2,
    "cursor": null,
    "service": "frontend",
    "metric": "latency_p95_ms",
    "operation": null,
    "step_seconds": 60,
    "aggregation": "avg"
  }
}
```

</details>

<details>

<summary>Call 92: contracts.models.Window.ordered</summary>

Source: `.\contracts\models.py`, line 45.

```json
{
  "call": 92,
  "parent_call": 91,
  "function": "contracts.models.Window.ordered",
  "source": ".\\contracts\\models.py",
  "line": 45,
  "inputs": {
    "self": {
      "start": "2026-03-14T14:00:00Z",
      "end": "2026-03-14T14:05:00Z"
    }
  },
  "closure_values": {},
  "output": {
    "start": "2026-03-14T14:00:00Z",
    "end": "2026-03-14T14:05:00Z"
  }
}
```

</details>

<details>

<summary>Call 93: contracts.models.utc_ns</summary>

Source: `.\contracts\models.py`, line 21.

```json
{
  "call": 93,
  "parent_call": 92,
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

<summary>Call 100: contracts.models.utc_ns</summary>

Source: `.\contracts\models.py`, line 21.

```json
{
  "call": 100,
  "parent_call": 92,
  "function": "contracts.models.utc_ns",
  "source": ".\\contracts\\models.py",
  "line": 21,
  "inputs": {
    "value": "2026-03-14T14:05:00Z"
  },
  "closure_values": {},
  "output": 1773497100000000000
}
```

</details>

<details>

<summary>Call 107: store.evidence.canonical_query</summary>

Source: `.\store\evidence.py`, line 13.

```json
{
  "call": 107,
  "parent_call": 89,
  "function": "store.evidence.canonical_query",
  "source": ".\\store\\evidence.py",
  "line": 13,
  "inputs": {
    "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
    "tool_version": "0.1.1",
    "tool": "query_metric",
    "args": {
      "window": {
        "start": "2026-03-14T14:00:00Z",
        "end": "2026-03-14T14:05:00Z"
      },
      "limit": 2,
      "cursor": null,
      "service": "frontend",
      "metric": "latency_p95_ms",
      "operation": null,
      "step_seconds": 60,
      "aggregation": "avg"
    }
  },
  "closure_values": {},
  "output": "{\"arguments\":{\"aggregation\":\"avg\",\"metric\":\"latency_p95_ms\",\"operation\":null,\"service\":\"frontend\",\"step_seconds\":60,\"window\":{\"end\":\"2026-03-14T14:05:00Z\",\"start\":\"2026-03-14T14:00:00Z\"}},\"dataset_id\":\"856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb\",\"tool\":\"query_metric\",\"tool_version\":\"0.1.1\"}"
}
```

</details>

<details>

<summary>Call 108: pydantic.main.BaseModel.model_dump</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 427.

```json
{
  "call": 108,
  "parent_call": 107,
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
        "end": "2026-03-14T14:05:00Z"
      },
      "limit": 2,
      "cursor": null,
      "service": "frontend",
      "metric": "latency_p95_ms",
      "operation": null,
      "step_seconds": 60,
      "aggregation": "avg"
    }
  },
  "closure_values": {},
  "output": {
    "window": {
      "start": "2026-03-14T14:00:00Z",
      "end": "2026-03-14T14:05:00Z"
    },
    "service": "frontend",
    "metric": "latency_p95_ms",
    "operation": null,
    "step_seconds": 60,
    "aggregation": "avg"
  }
}
```

</details>

<details>

<summary>Call 110: pydantic.main.BaseModel.model_validate</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 693.

```json
{
  "call": 110,
  "parent_call": 107,
  "function": "pydantic.main.BaseModel.model_validate",
  "source": ".\\.venv\\Lib\\site-packages\\pydantic\\main.py",
  "line": 693,
  "inputs": {
    "obj": {
      "start": "2026-03-14T14:00:00Z",
      "end": "2026-03-14T14:05:00Z"
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
    "end": "2026-03-14T14:05:00Z"
  }
}
```

</details>

<details>

<summary>Call 112: contracts.models.Window.ordered</summary>

Source: `.\contracts\models.py`, line 45.

```json
{
  "call": 112,
  "parent_call": 111,
  "function": "contracts.models.Window.ordered",
  "source": ".\\contracts\\models.py",
  "line": 45,
  "inputs": {
    "self": {
      "start": "2026-03-14T14:00:00Z",
      "end": "2026-03-14T14:05:00Z"
    }
  },
  "closure_values": {},
  "output": {
    "start": "2026-03-14T14:00:00Z",
    "end": "2026-03-14T14:05:00Z"
  }
}
```

</details>

<details>

<summary>Call 113: contracts.models.utc_ns</summary>

Source: `.\contracts\models.py`, line 21.

```json
{
  "call": 113,
  "parent_call": 112,
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

<summary>Call 120: contracts.models.utc_ns</summary>

Source: `.\contracts\models.py`, line 21.

```json
{
  "call": 120,
  "parent_call": 112,
  "function": "contracts.models.utc_ns",
  "source": ".\\contracts\\models.py",
  "line": 21,
  "inputs": {
    "value": "2026-03-14T14:05:00Z"
  },
  "closure_values": {},
  "output": 1773497100000000000
}
```

</details>

<details>

<summary>Call 127: contracts.models.utc_ns</summary>

Source: `.\contracts\models.py`, line 21.

```json
{
  "call": 127,
  "parent_call": 107,
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

<summary>Call 134: contracts.models.iso_time</summary>

Source: `.\contracts\models.py`, line 31.

```json
{
  "call": 134,
  "parent_call": 107,
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

<summary>Call 137: contracts.models.utc_ns</summary>

Source: `.\contracts\models.py`, line 21.

```json
{
  "call": 137,
  "parent_call": 107,
  "function": "contracts.models.utc_ns",
  "source": ".\\contracts\\models.py",
  "line": 21,
  "inputs": {
    "value": "2026-03-14T14:05:00Z"
  },
  "closure_values": {},
  "output": 1773497100000000000
}
```

</details>

<details>

<summary>Call 144: contracts.models.iso_time</summary>

Source: `.\contracts\models.py`, line 31.

```json
{
  "call": 144,
  "parent_call": 107,
  "function": "contracts.models.iso_time",
  "source": ".\\contracts\\models.py",
  "line": 31,
  "inputs": {
    "ns": 1773497100000000000
  },
  "closure_values": {},
  "output": "2026-03-14T14:05:00Z"
}
```

</details>

<details>

<summary>Call 154: store.evidence.QueryIds.get</summary>

Source: `.\store\evidence.py`, line 48.

```json
{
  "call": 154,
  "parent_call": 89,
  "function": "store.evidence.QueryIds.get",
  "source": ".\\store\\evidence.py",
  "line": 48,
  "inputs": {
    "canonical": "{\"arguments\":{\"aggregation\":\"avg\",\"metric\":\"latency_p95_ms\",\"operation\":null,\"service\":\"frontend\",\"step_seconds\":60,\"window\":{\"end\":\"2026-03-14T14:05:00Z\",\"start\":\"2026-03-14T14:00:00Z\"}},\"dataset_id\":\"856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb\",\"tool\":\"query_metric\",\"tool_version\":\"0.1.1\"}",
    "self": "<store.evidence.QueryIds>"
  },
  "closure_values": {},
  "output": "q4e6231a4"
}
```

</details>

<details>

<summary>Call 155: store.evidence.digest_query</summary>

Source: `.\store\evidence.py`, line 39.

```json
{
  "call": 155,
  "parent_call": 154,
  "function": "store.evidence.digest_query",
  "source": ".\\store\\evidence.py",
  "line": 39,
  "inputs": {
    "canonical": "{\"arguments\":{\"aggregation\":\"avg\",\"metric\":\"latency_p95_ms\",\"operation\":null,\"service\":\"frontend\",\"step_seconds\":60,\"window\":{\"end\":\"2026-03-14T14:05:00Z\",\"start\":\"2026-03-14T14:00:00Z\"}},\"dataset_id\":\"856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb\",\"tool\":\"query_metric\",\"tool_version\":\"0.1.1\"}"
  },
  "closure_values": {},
  "output": "4e6231a4fa2bc2925490d28c0ebc84335601f75441a9c2aa9d27b6b867525692"
}
```

</details>

<details>

<summary>Call 159: store.evidence.digest_query</summary>

Source: `.\store\evidence.py`, line 39.

```json
{
  "call": 159,
  "parent_call": 89,
  "function": "store.evidence.digest_query",
  "source": ".\\store\\evidence.py",
  "line": 39,
  "inputs": {
    "canonical": "{\"arguments\":{\"aggregation\":\"avg\",\"metric\":\"latency_p95_ms\",\"operation\":null,\"service\":\"frontend\",\"step_seconds\":60,\"window\":{\"end\":\"2026-03-14T14:05:00Z\",\"start\":\"2026-03-14T14:00:00Z\"}},\"dataset_id\":\"856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb\",\"tool\":\"query_metric\",\"tool_version\":\"0.1.1\"}"
  },
  "closure_values": {},
  "output": "4e6231a4fa2bc2925490d28c0ebc84335601f75441a9c2aa9d27b6b867525692"
}
```

</details>

<details>

<summary>Call 163: store.parquet.ParquetStore.query</summary>

Source: `.\store\parquet.py`, line 247.

```json
{
  "call": 163,
  "parent_call": 89,
  "function": "store.parquet.ParquetStore.query",
  "source": ".\\store\\parquet.py",
  "line": 247,
  "inputs": {
    "tool": "query_metric",
    "args": {
      "window": {
        "start": "2026-03-14T14:00:00Z",
        "end": "2026-03-14T14:05:00Z"
      },
      "limit": 2,
      "cursor": null,
      "service": "frontend",
      "metric": "latency_p95_ms",
      "operation": null,
      "step_seconds": 60,
      "aggregation": "avg"
    },
    "self": "<store.parquet.ParquetStore>"
  },
  "closure_values": {},
  "output": [
    [
      "kind",
      "start_ns",
      "end_ns",
      "value",
      "absolute_error_bound",
      "unit"
    ],
    [
      [
        "summary",
        1773496800000000000,
        1773497100000000000,
        120.0,
        40.0,
        "ms"
      ],
      [
        "bucket",
        1773496800000000000,
        1773496860000000000,
        120.0,
        40.0,
        "ms"
      ],
      [
        "bucket",
        1773496860000000000,
        1773496920000000000,
        120.0,
        40.0,
        "ms"
      ],
      [
        "bucket",
        1773496920000000000,
        1773496980000000000,
        120.0,
        40.0,
        "ms"
      ],
      [
        "bucket",
        1773496980000000000,
        1773497040000000000,
        120.0,
        40.0,
        "ms"
      ],
      [
        "bucket",
        1773497040000000000,
        1773497100000000000,
        1920.0,
        640.0,
        "ms"
      ]
    ],
    []
  ]
}
```

</details>

<details>

<summary>Call 164: store.parquet.ParquetStore._window</summary>

Source: `.\store\parquet.py`, line 119.

```json
{
  "call": 164,
  "parent_call": 163,
  "function": "store.parquet.ParquetStore._window",
  "source": ".\\store\\parquet.py",
  "line": 119,
  "inputs": {
    "window": {
      "start": "2026-03-14T14:00:00Z",
      "end": "2026-03-14T14:05:00Z"
    },
    "aligned": false,
    "self": "<store.parquet.ParquetStore>"
  },
  "closure_values": {},
  "output": [
    1773496800000000000,
    1773497100000000000
  ]
}
```

</details>

<details>

<summary>Call 165: contracts.models.utc_ns</summary>

Source: `.\contracts\models.py`, line 21.

```json
{
  "call": 165,
  "parent_call": 164,
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

<summary>Call 172: contracts.models.utc_ns</summary>

Source: `.\contracts\models.py`, line 21.

```json
{
  "call": 172,
  "parent_call": 164,
  "function": "contracts.models.utc_ns",
  "source": ".\\contracts\\models.py",
  "line": 21,
  "inputs": {
    "value": "2026-03-14T14:05:00Z"
  },
  "closure_values": {},
  "output": 1773497100000000000
}
```

</details>

<details>

<summary>Call 179: contracts.models.utc_ns</summary>

Source: `.\contracts\models.py`, line 21.

```json
{
  "call": 179,
  "parent_call": 164,
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

<summary>Call 186: contracts.models.utc_ns</summary>

Source: `.\contracts\models.py`, line 21.

```json
{
  "call": 186,
  "parent_call": 164,
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

<summary>Call 194: store.parquet.ParquetStore._window</summary>

Source: `.\store\parquet.py`, line 119.

```json
{
  "call": 194,
  "parent_call": 163,
  "function": "store.parquet.ParquetStore._window",
  "source": ".\\store\\parquet.py",
  "line": 119,
  "inputs": {
    "window": {
      "start": "2026-03-14T14:00:00Z",
      "end": "2026-03-14T14:05:00Z"
    },
    "aligned": true,
    "self": "<store.parquet.ParquetStore>"
  },
  "closure_values": {},
  "output": [
    1773496800000000000,
    1773497100000000000
  ]
}
```

</details>

<details>

<summary>Call 195: contracts.models.utc_ns</summary>

Source: `.\contracts\models.py`, line 21.

```json
{
  "call": 195,
  "parent_call": 194,
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

<summary>Call 202: contracts.models.utc_ns</summary>

Source: `.\contracts\models.py`, line 21.

```json
{
  "call": 202,
  "parent_call": 194,
  "function": "contracts.models.utc_ns",
  "source": ".\\contracts\\models.py",
  "line": 21,
  "inputs": {
    "value": "2026-03-14T14:05:00Z"
  },
  "closure_values": {},
  "output": 1773497100000000000
}
```

</details>

<details>

<summary>Call 209: contracts.models.utc_ns</summary>

Source: `.\contracts\models.py`, line 21.

```json
{
  "call": 209,
  "parent_call": 194,
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

<summary>Call 216: contracts.models.utc_ns</summary>

Source: `.\contracts\models.py`, line 21.

```json
{
  "call": 216,
  "parent_call": 194,
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

<summary>Call 223: store.parquet.ParquetStore._gaps</summary>

Source: `.\store\parquet.py`, line 134.

```json
{
  "call": 223,
  "parent_call": 163,
  "function": "store.parquet.ParquetStore._gaps",
  "source": ".\\store\\parquet.py",
  "line": 134,
  "inputs": {
    "service": "frontend",
    "operation": null,
    "start": 1773496800000000000,
    "end": 1773497100000000000,
    "metric": "latency_p95_ms",
    "self": "<store.parquet.ParquetStore>"
  },
  "closure_values": {},
  "output": false
}
```

</details>

<details>

<summary>Call 224: store.parquet.ParquetStore._missing_buckets</summary>

Source: `.\store\parquet.py`, line 144.

```json
{
  "call": 224,
  "parent_call": 223,
  "function": "store.parquet.ParquetStore._missing_buckets",
  "source": ".\\store\\parquet.py",
  "line": 144,
  "inputs": {
    "service": "frontend",
    "operation": null,
    "start": 1773496800000000000,
    "end": 1773497100000000000,
    "metric": "latency_p95_ms",
    "self": "<store.parquet.ParquetStore>"
  },
  "closure_values": {},
  "output": 0
}
```

</details>

<details>

<summary>Call 558: store.parquet.ParquetStore.query.&lt;locals&gt;.point</summary>

Source: `.\store\parquet.py`, line 305.

```json
{
  "call": 558,
  "parent_call": 163,
  "function": "store.parquet.ParquetStore.query.<locals>.point",
  "source": ".\\store\\parquet.py",
  "line": 305,
  "inputs": {
    "kind": "summary",
    "left": 1773496800000000000,
    "right": 1773497100000000000,
    "self": "<store.parquet.ParquetStore>"
  },
  "closure_values": {
    "args": {
      "window": {
        "start": "2026-03-14T14:00:00Z",
        "end": "2026-03-14T14:05:00Z"
      },
      "limit": 2,
      "cursor": null,
      "service": "frontend",
      "metric": "latency_p95_ms",
      "operation": null,
      "step_seconds": 60,
      "aggregation": "avg"
    },
    "self": "<store.parquet.ParquetStore>",
    "service": "frontend",
    "unit": "ms"
  },
  "output": [
    "summary",
    1773496800000000000,
    1773497100000000000,
    120.0,
    40.0,
    "ms"
  ]
}
```

</details>

<details>

<summary>Call 559: store.parquet.ParquetStore._metric_value</summary>

Source: `.\store\parquet.py`, line 189.

```json
{
  "call": 559,
  "parent_call": 558,
  "function": "store.parquet.ParquetStore._metric_value",
  "source": ".\\store\\parquet.py",
  "line": 189,
  "inputs": {
    "service": "frontend",
    "metric": "latency_p95_ms",
    "operation": null,
    "start": 1773496800000000000,
    "end": 1773497100000000000,
    "aggregation": "avg",
    "self": "<store.parquet.ParquetStore>"
  },
  "closure_values": {},
  "output": [
    120.0,
    40.0
  ]
}
```

</details>

<details>

<summary>Call 2034: telemetry.histograms.percentile</summary>

Source: `.\telemetry\histograms.py`, line 26.

```json
{
  "call": 2034,
  "parent_call": 559,
  "function": "telemetry.histograms.percentile",
  "source": ".\\telemetry\\histograms.py",
  "line": 26,
  "inputs": {
    "counts": [
      0,
      0,
      45,
      55,
      8,
      182,
      0,
      0,
      0,
      10,
      0,
      0,
      0,
      0,
      0
    ],
    "bounds": [
      5.0,
      10.0,
      20.0,
      40.0,
      80.0,
      160.0,
      320.0,
      640.0,
      1280.0,
      2560.0,
      5120.0,
      10240.0,
      20480.0,
      60000.0
    ],
    "q": 0.95
  },
  "closure_values": {},
  "output": [
    120.0,
    40.0
  ]
}
```

</details>

<details>

<summary>Call 2035: telemetry.histograms.validate_bounds</summary>

Source: `.\telemetry\histograms.py`, line 7.

```json
{
  "call": 2035,
  "parent_call": 2034,
  "function": "telemetry.histograms.validate_bounds",
  "source": ".\\telemetry\\histograms.py",
  "line": 7,
  "inputs": {
    "bounds": [
      5.0,
      10.0,
      20.0,
      40.0,
      80.0,
      160.0,
      320.0,
      640.0,
      1280.0,
      2560.0,
      5120.0,
      10240.0,
      20480.0,
      60000.0
    ]
  },
  "closure_values": {},
  "output": null
}
```

</details>

<details>

<summary>Call 2106: store.parquet.ParquetStore.query.&lt;locals&gt;.point</summary>

Source: `.\store\parquet.py`, line 305.

```json
{
  "call": 2106,
  "parent_call": 163,
  "function": "store.parquet.ParquetStore.query.<locals>.point",
  "source": ".\\store\\parquet.py",
  "line": 305,
  "inputs": {
    "kind": "bucket",
    "left": 1773496800000000000,
    "right": 1773496860000000000,
    "self": "<store.parquet.ParquetStore>"
  },
  "closure_values": {
    "args": {
      "window": {
        "start": "2026-03-14T14:00:00Z",
        "end": "2026-03-14T14:05:00Z"
      },
      "limit": 2,
      "cursor": null,
      "service": "frontend",
      "metric": "latency_p95_ms",
      "operation": null,
      "step_seconds": 60,
      "aggregation": "avg"
    },
    "self": "<store.parquet.ParquetStore>",
    "service": "frontend",
    "unit": "ms"
  },
  "output": [
    "bucket",
    1773496800000000000,
    1773496860000000000,
    120.0,
    40.0,
    "ms"
  ]
}
```

</details>

<details>

<summary>Call 2107: store.parquet.ParquetStore._metric_value</summary>

Source: `.\store\parquet.py`, line 189.

```json
{
  "call": 2107,
  "parent_call": 2106,
  "function": "store.parquet.ParquetStore._metric_value",
  "source": ".\\store\\parquet.py",
  "line": 189,
  "inputs": {
    "service": "frontend",
    "metric": "latency_p95_ms",
    "operation": null,
    "start": 1773496800000000000,
    "end": 1773496860000000000,
    "aggregation": "avg",
    "self": "<store.parquet.ParquetStore>"
  },
  "closure_values": {},
  "output": [
    120.0,
    40.0
  ]
}
```

</details>

<details>

<summary>Call 2430: telemetry.histograms.percentile</summary>

Source: `.\telemetry\histograms.py`, line 26.

```json
{
  "call": 2430,
  "parent_call": 2107,
  "function": "telemetry.histograms.percentile",
  "source": ".\\telemetry\\histograms.py",
  "line": 26,
  "inputs": {
    "counts": [
      0,
      0,
      6,
      14,
      2,
      38,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0
    ],
    "bounds": [
      5.0,
      10.0,
      20.0,
      40.0,
      80.0,
      160.0,
      320.0,
      640.0,
      1280.0,
      2560.0,
      5120.0,
      10240.0,
      20480.0,
      60000.0
    ],
    "q": 0.95
  },
  "closure_values": {},
  "output": [
    120.0,
    40.0
  ]
}
```

</details>

<details>

<summary>Call 2431: telemetry.histograms.validate_bounds</summary>

Source: `.\telemetry\histograms.py`, line 7.

```json
{
  "call": 2431,
  "parent_call": 2430,
  "function": "telemetry.histograms.validate_bounds",
  "source": ".\\telemetry\\histograms.py",
  "line": 7,
  "inputs": {
    "bounds": [
      5.0,
      10.0,
      20.0,
      40.0,
      80.0,
      160.0,
      320.0,
      640.0,
      1280.0,
      2560.0,
      5120.0,
      10240.0,
      20480.0,
      60000.0
    ]
  },
  "closure_values": {},
  "output": null
}
```

</details>

<details>

<summary>Call 2503: store.parquet.ParquetStore.query.&lt;locals&gt;.point</summary>

Source: `.\store\parquet.py`, line 305.

```json
{
  "call": 2503,
  "parent_call": 163,
  "function": "store.parquet.ParquetStore.query.<locals>.point",
  "source": ".\\store\\parquet.py",
  "line": 305,
  "inputs": {
    "kind": "bucket",
    "left": 1773496860000000000,
    "right": 1773496920000000000,
    "self": "<store.parquet.ParquetStore>"
  },
  "closure_values": {
    "args": {
      "window": {
        "start": "2026-03-14T14:00:00Z",
        "end": "2026-03-14T14:05:00Z"
      },
      "limit": 2,
      "cursor": null,
      "service": "frontend",
      "metric": "latency_p95_ms",
      "operation": null,
      "step_seconds": 60,
      "aggregation": "avg"
    },
    "self": "<store.parquet.ParquetStore>",
    "service": "frontend",
    "unit": "ms"
  },
  "output": [
    "bucket",
    1773496860000000000,
    1773496920000000000,
    120.0,
    40.0,
    "ms"
  ]
}
```

</details>

<details>

<summary>Call 2504: store.parquet.ParquetStore._metric_value</summary>

Source: `.\store\parquet.py`, line 189.

```json
{
  "call": 2504,
  "parent_call": 2503,
  "function": "store.parquet.ParquetStore._metric_value",
  "source": ".\\store\\parquet.py",
  "line": 189,
  "inputs": {
    "service": "frontend",
    "metric": "latency_p95_ms",
    "operation": null,
    "start": 1773496860000000000,
    "end": 1773496920000000000,
    "aggregation": "avg",
    "self": "<store.parquet.ParquetStore>"
  },
  "closure_values": {},
  "output": [
    120.0,
    40.0
  ]
}
```

</details>

<details>

<summary>Call 2827: telemetry.histograms.percentile</summary>

Source: `.\telemetry\histograms.py`, line 26.

```json
{
  "call": 2827,
  "parent_call": 2504,
  "function": "telemetry.histograms.percentile",
  "source": ".\\telemetry\\histograms.py",
  "line": 26,
  "inputs": {
    "counts": [
      0,
      0,
      7,
      13,
      1,
      39,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0
    ],
    "bounds": [
      5.0,
      10.0,
      20.0,
      40.0,
      80.0,
      160.0,
      320.0,
      640.0,
      1280.0,
      2560.0,
      5120.0,
      10240.0,
      20480.0,
      60000.0
    ],
    "q": 0.95
  },
  "closure_values": {},
  "output": [
    120.0,
    40.0
  ]
}
```

</details>

<details>

<summary>Call 2828: telemetry.histograms.validate_bounds</summary>

Source: `.\telemetry\histograms.py`, line 7.

```json
{
  "call": 2828,
  "parent_call": 2827,
  "function": "telemetry.histograms.validate_bounds",
  "source": ".\\telemetry\\histograms.py",
  "line": 7,
  "inputs": {
    "bounds": [
      5.0,
      10.0,
      20.0,
      40.0,
      80.0,
      160.0,
      320.0,
      640.0,
      1280.0,
      2560.0,
      5120.0,
      10240.0,
      20480.0,
      60000.0
    ]
  },
  "closure_values": {},
  "output": null
}
```

</details>

<details>

<summary>Call 2900: store.parquet.ParquetStore.query.&lt;locals&gt;.point</summary>

Source: `.\store\parquet.py`, line 305.

```json
{
  "call": 2900,
  "parent_call": 163,
  "function": "store.parquet.ParquetStore.query.<locals>.point",
  "source": ".\\store\\parquet.py",
  "line": 305,
  "inputs": {
    "kind": "bucket",
    "left": 1773496920000000000,
    "right": 1773496980000000000,
    "self": "<store.parquet.ParquetStore>"
  },
  "closure_values": {
    "args": {
      "window": {
        "start": "2026-03-14T14:00:00Z",
        "end": "2026-03-14T14:05:00Z"
      },
      "limit": 2,
      "cursor": null,
      "service": "frontend",
      "metric": "latency_p95_ms",
      "operation": null,
      "step_seconds": 60,
      "aggregation": "avg"
    },
    "self": "<store.parquet.ParquetStore>",
    "service": "frontend",
    "unit": "ms"
  },
  "output": [
    "bucket",
    1773496920000000000,
    1773496980000000000,
    120.0,
    40.0,
    "ms"
  ]
}
```

</details>

<details>

<summary>Call 2901: store.parquet.ParquetStore._metric_value</summary>

Source: `.\store\parquet.py`, line 189.

```json
{
  "call": 2901,
  "parent_call": 2900,
  "function": "store.parquet.ParquetStore._metric_value",
  "source": ".\\store\\parquet.py",
  "line": 189,
  "inputs": {
    "service": "frontend",
    "metric": "latency_p95_ms",
    "operation": null,
    "start": 1773496920000000000,
    "end": 1773496980000000000,
    "aggregation": "avg",
    "self": "<store.parquet.ParquetStore>"
  },
  "closure_values": {},
  "output": [
    120.0,
    40.0
  ]
}
```

</details>

<details>

<summary>Call 3224: telemetry.histograms.percentile</summary>

Source: `.\telemetry\histograms.py`, line 26.

```json
{
  "call": 3224,
  "parent_call": 2901,
  "function": "telemetry.histograms.percentile",
  "source": ".\\telemetry\\histograms.py",
  "line": 26,
  "inputs": {
    "counts": [
      0,
      0,
      13,
      7,
      3,
      37,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0
    ],
    "bounds": [
      5.0,
      10.0,
      20.0,
      40.0,
      80.0,
      160.0,
      320.0,
      640.0,
      1280.0,
      2560.0,
      5120.0,
      10240.0,
      20480.0,
      60000.0
    ],
    "q": 0.95
  },
  "closure_values": {},
  "output": [
    120.0,
    40.0
  ]
}
```

</details>

<details>

<summary>Call 3225: telemetry.histograms.validate_bounds</summary>

Source: `.\telemetry\histograms.py`, line 7.

```json
{
  "call": 3225,
  "parent_call": 3224,
  "function": "telemetry.histograms.validate_bounds",
  "source": ".\\telemetry\\histograms.py",
  "line": 7,
  "inputs": {
    "bounds": [
      5.0,
      10.0,
      20.0,
      40.0,
      80.0,
      160.0,
      320.0,
      640.0,
      1280.0,
      2560.0,
      5120.0,
      10240.0,
      20480.0,
      60000.0
    ]
  },
  "closure_values": {},
  "output": null
}
```

</details>

<details>

<summary>Call 3297: store.parquet.ParquetStore.query.&lt;locals&gt;.point</summary>

Source: `.\store\parquet.py`, line 305.

```json
{
  "call": 3297,
  "parent_call": 163,
  "function": "store.parquet.ParquetStore.query.<locals>.point",
  "source": ".\\store\\parquet.py",
  "line": 305,
  "inputs": {
    "kind": "bucket",
    "left": 1773496980000000000,
    "right": 1773497040000000000,
    "self": "<store.parquet.ParquetStore>"
  },
  "closure_values": {
    "args": {
      "window": {
        "start": "2026-03-14T14:00:00Z",
        "end": "2026-03-14T14:05:00Z"
      },
      "limit": 2,
      "cursor": null,
      "service": "frontend",
      "metric": "latency_p95_ms",
      "operation": null,
      "step_seconds": 60,
      "aggregation": "avg"
    },
    "self": "<store.parquet.ParquetStore>",
    "service": "frontend",
    "unit": "ms"
  },
  "output": [
    "bucket",
    1773496980000000000,
    1773497040000000000,
    120.0,
    40.0,
    "ms"
  ]
}
```

</details>

<details>

<summary>Call 3298: store.parquet.ParquetStore._metric_value</summary>

Source: `.\store\parquet.py`, line 189.

```json
{
  "call": 3298,
  "parent_call": 3297,
  "function": "store.parquet.ParquetStore._metric_value",
  "source": ".\\store\\parquet.py",
  "line": 189,
  "inputs": {
    "service": "frontend",
    "metric": "latency_p95_ms",
    "operation": null,
    "start": 1773496980000000000,
    "end": 1773497040000000000,
    "aggregation": "avg",
    "self": "<store.parquet.ParquetStore>"
  },
  "closure_values": {},
  "output": [
    120.0,
    40.0
  ]
}
```

</details>

<details>

<summary>Call 3621: telemetry.histograms.percentile</summary>

Source: `.\telemetry\histograms.py`, line 26.

```json
{
  "call": 3621,
  "parent_call": 3298,
  "function": "telemetry.histograms.percentile",
  "source": ".\\telemetry\\histograms.py",
  "line": 26,
  "inputs": {
    "counts": [
      0,
      0,
      10,
      10,
      1,
      39,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0
    ],
    "bounds": [
      5.0,
      10.0,
      20.0,
      40.0,
      80.0,
      160.0,
      320.0,
      640.0,
      1280.0,
      2560.0,
      5120.0,
      10240.0,
      20480.0,
      60000.0
    ],
    "q": 0.95
  },
  "closure_values": {},
  "output": [
    120.0,
    40.0
  ]
}
```

</details>

<details>

<summary>Call 3622: telemetry.histograms.validate_bounds</summary>

Source: `.\telemetry\histograms.py`, line 7.

```json
{
  "call": 3622,
  "parent_call": 3621,
  "function": "telemetry.histograms.validate_bounds",
  "source": ".\\telemetry\\histograms.py",
  "line": 7,
  "inputs": {
    "bounds": [
      5.0,
      10.0,
      20.0,
      40.0,
      80.0,
      160.0,
      320.0,
      640.0,
      1280.0,
      2560.0,
      5120.0,
      10240.0,
      20480.0,
      60000.0
    ]
  },
  "closure_values": {},
  "output": null
}
```

</details>

<details>

<summary>Call 3694: store.parquet.ParquetStore.query.&lt;locals&gt;.point</summary>

Source: `.\store\parquet.py`, line 305.

```json
{
  "call": 3694,
  "parent_call": 163,
  "function": "store.parquet.ParquetStore.query.<locals>.point",
  "source": ".\\store\\parquet.py",
  "line": 305,
  "inputs": {
    "kind": "bucket",
    "left": 1773497040000000000,
    "right": 1773497100000000000,
    "self": "<store.parquet.ParquetStore>"
  },
  "closure_values": {
    "args": {
      "window": {
        "start": "2026-03-14T14:00:00Z",
        "end": "2026-03-14T14:05:00Z"
      },
      "limit": 2,
      "cursor": null,
      "service": "frontend",
      "metric": "latency_p95_ms",
      "operation": null,
      "step_seconds": 60,
      "aggregation": "avg"
    },
    "self": "<store.parquet.ParquetStore>",
    "service": "frontend",
    "unit": "ms"
  },
  "output": [
    "bucket",
    1773497040000000000,
    1773497100000000000,
    1920.0,
    640.0,
    "ms"
  ]
}
```

</details>

<details>

<summary>Call 3695: store.parquet.ParquetStore._metric_value</summary>

Source: `.\store\parquet.py`, line 189.

```json
{
  "call": 3695,
  "parent_call": 3694,
  "function": "store.parquet.ParquetStore._metric_value",
  "source": ".\\store\\parquet.py",
  "line": 189,
  "inputs": {
    "service": "frontend",
    "metric": "latency_p95_ms",
    "operation": null,
    "start": 1773497040000000000,
    "end": 1773497100000000000,
    "aggregation": "avg",
    "self": "<store.parquet.ParquetStore>"
  },
  "closure_values": {},
  "output": [
    1920.0,
    640.0
  ]
}
```

</details>

<details>

<summary>Call 4018: telemetry.histograms.percentile</summary>

Source: `.\telemetry\histograms.py`, line 26.

```json
{
  "call": 4018,
  "parent_call": 3695,
  "function": "telemetry.histograms.percentile",
  "source": ".\\telemetry\\histograms.py",
  "line": 26,
  "inputs": {
    "counts": [
      0,
      0,
      9,
      11,
      1,
      29,
      0,
      0,
      0,
      10,
      0,
      0,
      0,
      0,
      0
    ],
    "bounds": [
      5.0,
      10.0,
      20.0,
      40.0,
      80.0,
      160.0,
      320.0,
      640.0,
      1280.0,
      2560.0,
      5120.0,
      10240.0,
      20480.0,
      60000.0
    ],
    "q": 0.95
  },
  "closure_values": {},
  "output": [
    1920.0,
    640.0
  ]
}
```

</details>

<details>

<summary>Call 4019: telemetry.histograms.validate_bounds</summary>

Source: `.\telemetry\histograms.py`, line 7.

```json
{
  "call": 4019,
  "parent_call": 4018,
  "function": "telemetry.histograms.validate_bounds",
  "source": ".\\telemetry\\histograms.py",
  "line": 7,
  "inputs": {
    "bounds": [
      5.0,
      10.0,
      20.0,
      40.0,
      80.0,
      160.0,
      320.0,
      640.0,
      1280.0,
      2560.0,
      5120.0,
      10240.0,
      20480.0,
      60000.0
    ]
  },
  "closure_values": {},
  "output": null
}
```

</details>

<details>

<summary>Call 4103: mcp_servers.telemetry.engine.ToolEngine.call.&lt;locals&gt;.envelope</summary>

Source: `.\mcp_servers\telemetry\engine.py`, line 79.

```json
{
  "call": 4103,
  "parent_call": 89,
  "function": "mcp_servers.telemetry.engine.ToolEngine.call.<locals>.envelope",
  "source": ".\\mcp_servers\\telemetry\\engine.py",
  "line": 79,
  "inputs": {
    "self": "<mcp_servers.telemetry.engine.ToolEngine>"
  },
  "closure_values": {
    "all_rows": [
      [
        "summary",
        1773496800000000000,
        1773497100000000000,
        120.0,
        40.0,
        "ms"
      ],
      [
        "bucket",
        1773496800000000000,
        1773496860000000000,
        120.0,
        40.0,
        "ms"
      ],
      [
        "bucket",
        1773496860000000000,
        1773496920000000000,
        120.0,
        40.0,
        "ms"
      ],
      [
        "bucket",
        1773496920000000000,
        1773496980000000000,
        120.0,
        40.0,
        "ms"
      ],
      [
        "bucket",
        1773496980000000000,
        1773497040000000000,
        120.0,
        40.0,
        "ms"
      ],
      [
        "bucket",
        1773497040000000000,
        1773497100000000000,
        1920.0,
        640.0,
        "ms"
      ]
    ],
    "columns": [
      "kind",
      "start_ns",
      "end_ns",
      "value",
      "absolute_error_bound",
      "unit"
    ],
    "digest": "4e6231a4fa2bc2925490d28c0ebc84335601f75441a9c2aa9d27b6b867525692",
    "offset": 0,
    "query_id": "q4e6231a4",
    "selected": [
      [
        "M1",
        "summary",
        1773496800000000000,
        1773497100000000000,
        120.0,
        40.0,
        "ms"
      ]
    ],
    "self": "<mcp_servers.telemetry.engine.ToolEngine>",
    "warnings": []
  },
  "output": {
    "data": {
      "columns": [
        "handle",
        "kind",
        "start_ns",
        "end_ns",
        "value",
        "absolute_error_bound",
        "unit"
      ],
      "rows": [
        [
          "M1",
          "summary",
          1773496800000000000,
          1773497100000000000,
          120.0,
          40.0,
          "ms"
        ]
      ]
    },
    "total_matches": 6,
    "returned": 1,
    "truncated": true,
    "next_cursor": "4e6231a4fa2bc2925490d28c0ebc84335601f75441a9c2aa9d27b6b867525692:1",
    "query_id": "q4e6231a4",
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

<summary>Call 4106: pydantic.main.BaseModel.__init__</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 253.

```json
{
  "call": 4106,
  "parent_call": 4103,
  "function": "pydantic.main.BaseModel.__init__",
  "source": ".\\.venv\\Lib\\site-packages\\pydantic\\main.py",
  "line": 253,
  "inputs": {
    "data": {
      "columns": [
        "handle",
        "kind",
        "start_ns",
        "end_ns",
        "value",
        "absolute_error_bound",
        "unit"
      ],
      "rows": [
        [
          "M1",
          "summary",
          1773496800000000000,
          1773497100000000000,
          120.0,
          40.0,
          "ms"
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
      "kind",
      "start_ns",
      "end_ns",
      "value",
      "absolute_error_bound",
      "unit"
    ],
    "rows": [
      [
        "M1",
        "summary",
        1773496800000000000,
        1773497100000000000,
        120.0,
        40.0,
        "ms"
      ]
    ]
  }
}
```

</details>

<details>

<summary>Call 4108: contracts.models.TableData.rectangular</summary>

Source: `.\contracts\models.py`, line 256.

```json
{
  "call": 4108,
  "parent_call": 4107,
  "function": "contracts.models.TableData.rectangular",
  "source": ".\\contracts\\models.py",
  "line": 256,
  "inputs": {
    "self": {
      "columns": [
        "handle",
        "kind",
        "start_ns",
        "end_ns",
        "value",
        "absolute_error_bound",
        "unit"
      ],
      "rows": [
        [
          "M1",
          "summary",
          1773496800000000000,
          1773497100000000000,
          120.0,
          40.0,
          "ms"
        ]
      ]
    }
  },
  "closure_values": {},
  "output": {
    "columns": [
      "handle",
      "kind",
      "start_ns",
      "end_ns",
      "value",
      "absolute_error_bound",
      "unit"
    ],
    "rows": [
      [
        "M1",
        "summary",
        1773496800000000000,
        1773497100000000000,
        120.0,
        40.0,
        "ms"
      ]
    ]
  }
}
```

</details>

<details>

<summary>Call 4117: pydantic.main.BaseModel.__init__</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 253.

```json
{
  "call": 4117,
  "parent_call": 4103,
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

<summary>Call 4119: pydantic.main.BaseModel.__init__</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 253.

```json
{
  "call": 4119,
  "parent_call": 4103,
  "function": "pydantic.main.BaseModel.__init__",
  "source": ".\\.venv\\Lib\\site-packages\\pydantic\\main.py",
  "line": 253,
  "inputs": {
    "data": {
      "data": {
        "columns": [
          "handle",
          "kind",
          "start_ns",
          "end_ns",
          "value",
          "absolute_error_bound",
          "unit"
        ],
        "rows": [
          [
            "M1",
            "summary",
            1773496800000000000,
            1773497100000000000,
            120.0,
            40.0,
            "ms"
          ]
        ]
      },
      "total_matches": 6,
      "returned": 1,
      "truncated": true,
      "next_cursor": "4e6231a4fa2bc2925490d28c0ebc84335601f75441a9c2aa9d27b6b867525692:1",
      "query_id": "q4e6231a4",
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
        "kind",
        "start_ns",
        "end_ns",
        "value",
        "absolute_error_bound",
        "unit"
      ],
      "rows": [
        [
          "M1",
          "summary",
          1773496800000000000,
          1773497100000000000,
          120.0,
          40.0,
          "ms"
        ]
      ]
    },
    "total_matches": 6,
    "returned": 1,
    "truncated": true,
    "next_cursor": "4e6231a4fa2bc2925490d28c0ebc84335601f75441a9c2aa9d27b6b867525692:1",
    "query_id": "q4e6231a4",
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

<summary>Call 4121: contracts.models.TableData.rectangular</summary>

Source: `.\contracts\models.py`, line 256.

```json
{
  "call": 4121,
  "parent_call": 4120,
  "function": "contracts.models.TableData.rectangular",
  "source": ".\\contracts\\models.py",
  "line": 256,
  "inputs": {
    "self": {
      "columns": [
        "handle",
        "kind",
        "start_ns",
        "end_ns",
        "value",
        "absolute_error_bound",
        "unit"
      ],
      "rows": [
        [
          "M1",
          "summary",
          1773496800000000000,
          1773497100000000000,
          120.0,
          40.0,
          "ms"
        ]
      ]
    }
  },
  "closure_values": {},
  "output": {
    "columns": [
      "handle",
      "kind",
      "start_ns",
      "end_ns",
      "value",
      "absolute_error_bound",
      "unit"
    ],
    "rows": [
      [
        "M1",
        "summary",
        1773496800000000000,
        1773497100000000000,
        120.0,
        40.0,
        "ms"
      ]
    ]
  }
}
```

</details>

<details>

<summary>Call 4129: contracts.models.ToolResult.consistent</summary>

Source: `.\contracts\models.py`, line 286.

```json
{
  "call": 4129,
  "parent_call": 4120,
  "function": "contracts.models.ToolResult.consistent",
  "source": ".\\contracts\\models.py",
  "line": 286,
  "inputs": {
    "self": {
      "data": {
        "columns": [
          "handle",
          "kind",
          "start_ns",
          "end_ns",
          "value",
          "absolute_error_bound",
          "unit"
        ],
        "rows": [
          [
            "M1",
            "summary",
            1773496800000000000,
            1773497100000000000,
            120.0,
            40.0,
            "ms"
          ]
        ]
      },
      "total_matches": 6,
      "returned": 1,
      "truncated": true,
      "next_cursor": "4e6231a4fa2bc2925490d28c0ebc84335601f75441a9c2aa9d27b6b867525692:1",
      "query_id": "q4e6231a4",
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
        "kind",
        "start_ns",
        "end_ns",
        "value",
        "absolute_error_bound",
        "unit"
      ],
      "rows": [
        [
          "M1",
          "summary",
          1773496800000000000,
          1773497100000000000,
          120.0,
          40.0,
          "ms"
        ]
      ]
    },
    "total_matches": 6,
    "returned": 1,
    "truncated": true,
    "next_cursor": "4e6231a4fa2bc2925490d28c0ebc84335601f75441a9c2aa9d27b6b867525692:1",
    "query_id": "q4e6231a4",
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

<summary>Call 4132: pydantic.main.BaseModel.model_dump</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 427.

```json
{
  "call": 4132,
  "parent_call": 4103,
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
          "kind",
          "start_ns",
          "end_ns",
          "value",
          "absolute_error_bound",
          "unit"
        ],
        "rows": [
          [
            "M1",
            "summary",
            1773496800000000000,
            1773497100000000000,
            120.0,
            40.0,
            "ms"
          ]
        ]
      },
      "total_matches": 6,
      "returned": 1,
      "truncated": true,
      "next_cursor": "4e6231a4fa2bc2925490d28c0ebc84335601f75441a9c2aa9d27b6b867525692:1",
      "query_id": "q4e6231a4",
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
        "kind",
        "start_ns",
        "end_ns",
        "value",
        "absolute_error_bound",
        "unit"
      ],
      "rows": [
        [
          "M1",
          "summary",
          1773496800000000000,
          1773497100000000000,
          120.0,
          40.0,
          "ms"
        ]
      ]
    },
    "total_matches": 6,
    "returned": 1,
    "truncated": true,
    "next_cursor": "4e6231a4fa2bc2925490d28c0ebc84335601f75441a9c2aa9d27b6b867525692:1",
    "query_id": "q4e6231a4",
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

<summary>Call 4134: store.evidence.compact_json</summary>

Source: `.\store\evidence.py`, line 70.

```json
{
  "call": 4134,
  "parent_call": 89,
  "function": "store.evidence.compact_json",
  "source": ".\\store\\evidence.py",
  "line": 70,
  "inputs": {
    "value": {
      "data": {
        "columns": [
          "handle",
          "kind",
          "start_ns",
          "end_ns",
          "value",
          "absolute_error_bound",
          "unit"
        ],
        "rows": [
          [
            "M1",
            "summary",
            1773496800000000000,
            1773497100000000000,
            120.0,
            40.0,
            "ms"
          ]
        ]
      },
      "total_matches": 6,
      "returned": 1,
      "truncated": true,
      "next_cursor": "4e6231a4fa2bc2925490d28c0ebc84335601f75441a9c2aa9d27b6b867525692:1",
      "query_id": "q4e6231a4",
      "source": {
        "backend": "parquet",
        "dataset_id": "856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb",
        "tool_version": "0.1.1"
      },
      "warnings": []
    }
  },
  "closure_values": {},
  "output": "{\"data\":{\"columns\":[\"handle\",\"kind\",\"start_ns\",\"end_ns\",\"value\",\"absolute_error_bound\",\"unit\"],\"rows\":[[\"M1\",\"summary\",1773496800000000000,1773497100000000000,120.0,40.0,\"ms\"]]},\"total_matches\":6,\"returned\":1,\"truncated\":true,\"next_cursor\":\"4e6231a4fa2bc2925490d28c0ebc84335601f75441a9c2aa9d27b6b867525692:1\",\"query_id\":\"q4e6231a4\",\"source\":{\"backend\":\"parquet\",\"dataset_id\":\"856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb\",\"tool_version\":\"0.1.1\"},\"warnings\":[]}"
}
```

</details>

<details>

<summary>Call 4142: mcp_servers.telemetry.engine.ToolEngine.__init__.&lt;locals&gt;.&lt;lambda&gt;</summary>

Source: `.\mcp_servers\telemetry\engine.py`, line 44.

```json
{
  "call": 4142,
  "parent_call": 89,
  "function": "mcp_servers.telemetry.engine.ToolEngine.__init__.<locals>.<lambda>",
  "source": ".\\mcp_servers\\telemetry\\engine.py",
  "line": 44,
  "inputs": {
    "text": "{\"data\":{\"columns\":[\"handle\",\"kind\",\"start_ns\",\"end_ns\",\"value\",\"absolute_error_bound\",\"unit\"],\"rows\":[[\"M1\",\"summary\",1773496800000000000,1773497100000000000,120.0,40.0,\"ms\"]]},\"total_matches\":6,\"returned\":1,\"truncated\":true,\"next_cursor\":\"4e6231a4fa2bc2925490d28c0ebc84335601f75441a9c2aa9d27b6b867525692:1\",\"query_id\":\"q4e6231a4\",\"source\":{\"backend\":\"parquet\",\"dataset_id\":\"856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb\",\"tool_version\":\"0.1.1\"},\"warnings\":[]}"
  },
  "closure_values": {},
  "output": 480
}
```

</details>

<details>

<summary>Call 4146: mcp_servers.telemetry.engine.ToolEngine.call.&lt;locals&gt;.envelope</summary>

Source: `.\mcp_servers\telemetry\engine.py`, line 79.

```json
{
  "call": 4146,
  "parent_call": 89,
  "function": "mcp_servers.telemetry.engine.ToolEngine.call.<locals>.envelope",
  "source": ".\\mcp_servers\\telemetry\\engine.py",
  "line": 79,
  "inputs": {
    "self": "<mcp_servers.telemetry.engine.ToolEngine>"
  },
  "closure_values": {
    "all_rows": [
      [
        "summary",
        1773496800000000000,
        1773497100000000000,
        120.0,
        40.0,
        "ms"
      ],
      [
        "bucket",
        1773496800000000000,
        1773496860000000000,
        120.0,
        40.0,
        "ms"
      ],
      [
        "bucket",
        1773496860000000000,
        1773496920000000000,
        120.0,
        40.0,
        "ms"
      ],
      [
        "bucket",
        1773496920000000000,
        1773496980000000000,
        120.0,
        40.0,
        "ms"
      ],
      [
        "bucket",
        1773496980000000000,
        1773497040000000000,
        120.0,
        40.0,
        "ms"
      ],
      [
        "bucket",
        1773497040000000000,
        1773497100000000000,
        1920.0,
        640.0,
        "ms"
      ]
    ],
    "columns": [
      "kind",
      "start_ns",
      "end_ns",
      "value",
      "absolute_error_bound",
      "unit"
    ],
    "digest": "4e6231a4fa2bc2925490d28c0ebc84335601f75441a9c2aa9d27b6b867525692",
    "offset": 0,
    "query_id": "q4e6231a4",
    "selected": [
      [
        "M1",
        "summary",
        1773496800000000000,
        1773497100000000000,
        120.0,
        40.0,
        "ms"
      ],
      [
        "M2",
        "bucket",
        1773496800000000000,
        1773496860000000000,
        120.0,
        40.0,
        "ms"
      ]
    ],
    "self": "<mcp_servers.telemetry.engine.ToolEngine>",
    "warnings": []
  },
  "output": {
    "data": {
      "columns": [
        "handle",
        "kind",
        "start_ns",
        "end_ns",
        "value",
        "absolute_error_bound",
        "unit"
      ],
      "rows": [
        [
          "M1",
          "summary",
          1773496800000000000,
          1773497100000000000,
          120.0,
          40.0,
          "ms"
        ],
        [
          "M2",
          "bucket",
          1773496800000000000,
          1773496860000000000,
          120.0,
          40.0,
          "ms"
        ]
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
}
```

</details>

<details>

<summary>Call 4149: pydantic.main.BaseModel.__init__</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 253.

```json
{
  "call": 4149,
  "parent_call": 4146,
  "function": "pydantic.main.BaseModel.__init__",
  "source": ".\\.venv\\Lib\\site-packages\\pydantic\\main.py",
  "line": 253,
  "inputs": {
    "data": {
      "columns": [
        "handle",
        "kind",
        "start_ns",
        "end_ns",
        "value",
        "absolute_error_bound",
        "unit"
      ],
      "rows": [
        [
          "M1",
          "summary",
          1773496800000000000,
          1773497100000000000,
          120.0,
          40.0,
          "ms"
        ],
        [
          "M2",
          "bucket",
          1773496800000000000,
          1773496860000000000,
          120.0,
          40.0,
          "ms"
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
      "kind",
      "start_ns",
      "end_ns",
      "value",
      "absolute_error_bound",
      "unit"
    ],
    "rows": [
      [
        "M1",
        "summary",
        1773496800000000000,
        1773497100000000000,
        120.0,
        40.0,
        "ms"
      ],
      [
        "M2",
        "bucket",
        1773496800000000000,
        1773496860000000000,
        120.0,
        40.0,
        "ms"
      ]
    ]
  }
}
```

</details>

<details>

<summary>Call 4151: contracts.models.TableData.rectangular</summary>

Source: `.\contracts\models.py`, line 256.

```json
{
  "call": 4151,
  "parent_call": 4150,
  "function": "contracts.models.TableData.rectangular",
  "source": ".\\contracts\\models.py",
  "line": 256,
  "inputs": {
    "self": {
      "columns": [
        "handle",
        "kind",
        "start_ns",
        "end_ns",
        "value",
        "absolute_error_bound",
        "unit"
      ],
      "rows": [
        [
          "M1",
          "summary",
          1773496800000000000,
          1773497100000000000,
          120.0,
          40.0,
          "ms"
        ],
        [
          "M2",
          "bucket",
          1773496800000000000,
          1773496860000000000,
          120.0,
          40.0,
          "ms"
        ]
      ]
    }
  },
  "closure_values": {},
  "output": {
    "columns": [
      "handle",
      "kind",
      "start_ns",
      "end_ns",
      "value",
      "absolute_error_bound",
      "unit"
    ],
    "rows": [
      [
        "M1",
        "summary",
        1773496800000000000,
        1773497100000000000,
        120.0,
        40.0,
        "ms"
      ],
      [
        "M2",
        "bucket",
        1773496800000000000,
        1773496860000000000,
        120.0,
        40.0,
        "ms"
      ]
    ]
  }
}
```

</details>

<details>

<summary>Call 4163: pydantic.main.BaseModel.__init__</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 253.

```json
{
  "call": 4163,
  "parent_call": 4146,
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

<summary>Call 4165: pydantic.main.BaseModel.__init__</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 253.

```json
{
  "call": 4165,
  "parent_call": 4146,
  "function": "pydantic.main.BaseModel.__init__",
  "source": ".\\.venv\\Lib\\site-packages\\pydantic\\main.py",
  "line": 253,
  "inputs": {
    "data": {
      "data": {
        "columns": [
          "handle",
          "kind",
          "start_ns",
          "end_ns",
          "value",
          "absolute_error_bound",
          "unit"
        ],
        "rows": [
          [
            "M1",
            "summary",
            1773496800000000000,
            1773497100000000000,
            120.0,
            40.0,
            "ms"
          ],
          [
            "M2",
            "bucket",
            1773496800000000000,
            1773496860000000000,
            120.0,
            40.0,
            "ms"
          ]
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
    },
    "self": {}
  },
  "closure_values": {},
  "output": null,
  "constructed_object": {
    "data": {
      "columns": [
        "handle",
        "kind",
        "start_ns",
        "end_ns",
        "value",
        "absolute_error_bound",
        "unit"
      ],
      "rows": [
        [
          "M1",
          "summary",
          1773496800000000000,
          1773497100000000000,
          120.0,
          40.0,
          "ms"
        ],
        [
          "M2",
          "bucket",
          1773496800000000000,
          1773496860000000000,
          120.0,
          40.0,
          "ms"
        ]
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
}
```

</details>

<details>

<summary>Call 4167: contracts.models.TableData.rectangular</summary>

Source: `.\contracts\models.py`, line 256.

```json
{
  "call": 4167,
  "parent_call": 4166,
  "function": "contracts.models.TableData.rectangular",
  "source": ".\\contracts\\models.py",
  "line": 256,
  "inputs": {
    "self": {
      "columns": [
        "handle",
        "kind",
        "start_ns",
        "end_ns",
        "value",
        "absolute_error_bound",
        "unit"
      ],
      "rows": [
        [
          "M1",
          "summary",
          1773496800000000000,
          1773497100000000000,
          120.0,
          40.0,
          "ms"
        ],
        [
          "M2",
          "bucket",
          1773496800000000000,
          1773496860000000000,
          120.0,
          40.0,
          "ms"
        ]
      ]
    }
  },
  "closure_values": {},
  "output": {
    "columns": [
      "handle",
      "kind",
      "start_ns",
      "end_ns",
      "value",
      "absolute_error_bound",
      "unit"
    ],
    "rows": [
      [
        "M1",
        "summary",
        1773496800000000000,
        1773497100000000000,
        120.0,
        40.0,
        "ms"
      ],
      [
        "M2",
        "bucket",
        1773496800000000000,
        1773496860000000000,
        120.0,
        40.0,
        "ms"
      ]
    ]
  }
}
```

</details>

<details>

<summary>Call 4178: contracts.models.ToolResult.consistent</summary>

Source: `.\contracts\models.py`, line 286.

```json
{
  "call": 4178,
  "parent_call": 4166,
  "function": "contracts.models.ToolResult.consistent",
  "source": ".\\contracts\\models.py",
  "line": 286,
  "inputs": {
    "self": {
      "data": {
        "columns": [
          "handle",
          "kind",
          "start_ns",
          "end_ns",
          "value",
          "absolute_error_bound",
          "unit"
        ],
        "rows": [
          [
            "M1",
            "summary",
            1773496800000000000,
            1773497100000000000,
            120.0,
            40.0,
            "ms"
          ],
          [
            "M2",
            "bucket",
            1773496800000000000,
            1773496860000000000,
            120.0,
            40.0,
            "ms"
          ]
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
  },
  "closure_values": {},
  "output": {
    "data": {
      "columns": [
        "handle",
        "kind",
        "start_ns",
        "end_ns",
        "value",
        "absolute_error_bound",
        "unit"
      ],
      "rows": [
        [
          "M1",
          "summary",
          1773496800000000000,
          1773497100000000000,
          120.0,
          40.0,
          "ms"
        ],
        [
          "M2",
          "bucket",
          1773496800000000000,
          1773496860000000000,
          120.0,
          40.0,
          "ms"
        ]
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
}
```

</details>

<details>

<summary>Call 4181: pydantic.main.BaseModel.model_dump</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 427.

```json
{
  "call": 4181,
  "parent_call": 4146,
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
          "kind",
          "start_ns",
          "end_ns",
          "value",
          "absolute_error_bound",
          "unit"
        ],
        "rows": [
          [
            "M1",
            "summary",
            1773496800000000000,
            1773497100000000000,
            120.0,
            40.0,
            "ms"
          ],
          [
            "M2",
            "bucket",
            1773496800000000000,
            1773496860000000000,
            120.0,
            40.0,
            "ms"
          ]
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
  },
  "closure_values": {},
  "output": {
    "data": {
      "columns": [
        "handle",
        "kind",
        "start_ns",
        "end_ns",
        "value",
        "absolute_error_bound",
        "unit"
      ],
      "rows": [
        [
          "M1",
          "summary",
          1773496800000000000,
          1773497100000000000,
          120.0,
          40.0,
          "ms"
        ],
        [
          "M2",
          "bucket",
          1773496800000000000,
          1773496860000000000,
          120.0,
          40.0,
          "ms"
        ]
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
}
```

</details>

<details>

<summary>Call 4183: store.evidence.compact_json</summary>

Source: `.\store\evidence.py`, line 70.

```json
{
  "call": 4183,
  "parent_call": 89,
  "function": "store.evidence.compact_json",
  "source": ".\\store\\evidence.py",
  "line": 70,
  "inputs": {
    "value": {
      "data": {
        "columns": [
          "handle",
          "kind",
          "start_ns",
          "end_ns",
          "value",
          "absolute_error_bound",
          "unit"
        ],
        "rows": [
          [
            "M1",
            "summary",
            1773496800000000000,
            1773497100000000000,
            120.0,
            40.0,
            "ms"
          ],
          [
            "M2",
            "bucket",
            1773496800000000000,
            1773496860000000000,
            120.0,
            40.0,
            "ms"
          ]
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
  },
  "closure_values": {},
  "output": "{\"data\":{\"columns\":[\"handle\",\"kind\",\"start_ns\",\"end_ns\",\"value\",\"absolute_error_bound\",\"unit\"],\"rows\":[[\"M1\",\"summary\",1773496800000000000,1773497100000000000,120.0,40.0,\"ms\"],[\"M2\",\"bucket\",1773496800000000000,1773496860000000000,120.0,40.0,\"ms\"]]},\"total_matches\":6,\"returned\":2,\"truncated\":true,\"next_cursor\":\"4e6231a4fa2bc2925490d28c0ebc84335601f75441a9c2aa9d27b6b867525692:2\",\"query_id\":\"q4e6231a4\",\"source\":{\"backend\":\"parquet\",\"dataset_id\":\"856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb\",\"tool_version\":\"0.1.1\"},\"warnings\":[]}"
}
```

</details>

<details>

<summary>Call 4191: mcp_servers.telemetry.engine.ToolEngine.__init__.&lt;locals&gt;.&lt;lambda&gt;</summary>

Source: `.\mcp_servers\telemetry\engine.py`, line 44.

```json
{
  "call": 4191,
  "parent_call": 89,
  "function": "mcp_servers.telemetry.engine.ToolEngine.__init__.<locals>.<lambda>",
  "source": ".\\mcp_servers\\telemetry\\engine.py",
  "line": 44,
  "inputs": {
    "text": "{\"data\":{\"columns\":[\"handle\",\"kind\",\"start_ns\",\"end_ns\",\"value\",\"absolute_error_bound\",\"unit\"],\"rows\":[[\"M1\",\"summary\",1773496800000000000,1773497100000000000,120.0,40.0,\"ms\"],[\"M2\",\"bucket\",1773496800000000000,1773496860000000000,120.0,40.0,\"ms\"]]},\"total_matches\":6,\"returned\":2,\"truncated\":true,\"next_cursor\":\"4e6231a4fa2bc2925490d28c0ebc84335601f75441a9c2aa9d27b6b867525692:2\",\"query_id\":\"q4e6231a4\",\"source\":{\"backend\":\"parquet\",\"dataset_id\":\"856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb\",\"tool_version\":\"0.1.1\"},\"warnings\":[]}"
  },
  "closure_values": {},
  "output": 552
}
```

</details>

<details>

<summary>Call 4194: mcp_servers.telemetry.engine.ToolEngine.call.&lt;locals&gt;.envelope</summary>

Source: `.\mcp_servers\telemetry\engine.py`, line 79.

```json
{
  "call": 4194,
  "parent_call": 89,
  "function": "mcp_servers.telemetry.engine.ToolEngine.call.<locals>.envelope",
  "source": ".\\mcp_servers\\telemetry\\engine.py",
  "line": 79,
  "inputs": {
    "self": "<mcp_servers.telemetry.engine.ToolEngine>"
  },
  "closure_values": {
    "all_rows": [
      [
        "summary",
        1773496800000000000,
        1773497100000000000,
        120.0,
        40.0,
        "ms"
      ],
      [
        "bucket",
        1773496800000000000,
        1773496860000000000,
        120.0,
        40.0,
        "ms"
      ],
      [
        "bucket",
        1773496860000000000,
        1773496920000000000,
        120.0,
        40.0,
        "ms"
      ],
      [
        "bucket",
        1773496920000000000,
        1773496980000000000,
        120.0,
        40.0,
        "ms"
      ],
      [
        "bucket",
        1773496980000000000,
        1773497040000000000,
        120.0,
        40.0,
        "ms"
      ],
      [
        "bucket",
        1773497040000000000,
        1773497100000000000,
        1920.0,
        640.0,
        "ms"
      ]
    ],
    "columns": [
      "kind",
      "start_ns",
      "end_ns",
      "value",
      "absolute_error_bound",
      "unit"
    ],
    "digest": "4e6231a4fa2bc2925490d28c0ebc84335601f75441a9c2aa9d27b6b867525692",
    "offset": 0,
    "query_id": "q4e6231a4",
    "selected": [
      [
        "M1",
        "summary",
        1773496800000000000,
        1773497100000000000,
        120.0,
        40.0,
        "ms"
      ],
      [
        "M2",
        "bucket",
        1773496800000000000,
        1773496860000000000,
        120.0,
        40.0,
        "ms"
      ]
    ],
    "self": "<mcp_servers.telemetry.engine.ToolEngine>",
    "warnings": []
  },
  "output": {
    "data": {
      "columns": [
        "handle",
        "kind",
        "start_ns",
        "end_ns",
        "value",
        "absolute_error_bound",
        "unit"
      ],
      "rows": [
        [
          "M1",
          "summary",
          1773496800000000000,
          1773497100000000000,
          120.0,
          40.0,
          "ms"
        ],
        [
          "M2",
          "bucket",
          1773496800000000000,
          1773496860000000000,
          120.0,
          40.0,
          "ms"
        ]
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
}
```

</details>

<details>

<summary>Call 4197: pydantic.main.BaseModel.__init__</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 253.

```json
{
  "call": 4197,
  "parent_call": 4194,
  "function": "pydantic.main.BaseModel.__init__",
  "source": ".\\.venv\\Lib\\site-packages\\pydantic\\main.py",
  "line": 253,
  "inputs": {
    "data": {
      "columns": [
        "handle",
        "kind",
        "start_ns",
        "end_ns",
        "value",
        "absolute_error_bound",
        "unit"
      ],
      "rows": [
        [
          "M1",
          "summary",
          1773496800000000000,
          1773497100000000000,
          120.0,
          40.0,
          "ms"
        ],
        [
          "M2",
          "bucket",
          1773496800000000000,
          1773496860000000000,
          120.0,
          40.0,
          "ms"
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
      "kind",
      "start_ns",
      "end_ns",
      "value",
      "absolute_error_bound",
      "unit"
    ],
    "rows": [
      [
        "M1",
        "summary",
        1773496800000000000,
        1773497100000000000,
        120.0,
        40.0,
        "ms"
      ],
      [
        "M2",
        "bucket",
        1773496800000000000,
        1773496860000000000,
        120.0,
        40.0,
        "ms"
      ]
    ]
  }
}
```

</details>

<details>

<summary>Call 4199: contracts.models.TableData.rectangular</summary>

Source: `.\contracts\models.py`, line 256.

```json
{
  "call": 4199,
  "parent_call": 4198,
  "function": "contracts.models.TableData.rectangular",
  "source": ".\\contracts\\models.py",
  "line": 256,
  "inputs": {
    "self": {
      "columns": [
        "handle",
        "kind",
        "start_ns",
        "end_ns",
        "value",
        "absolute_error_bound",
        "unit"
      ],
      "rows": [
        [
          "M1",
          "summary",
          1773496800000000000,
          1773497100000000000,
          120.0,
          40.0,
          "ms"
        ],
        [
          "M2",
          "bucket",
          1773496800000000000,
          1773496860000000000,
          120.0,
          40.0,
          "ms"
        ]
      ]
    }
  },
  "closure_values": {},
  "output": {
    "columns": [
      "handle",
      "kind",
      "start_ns",
      "end_ns",
      "value",
      "absolute_error_bound",
      "unit"
    ],
    "rows": [
      [
        "M1",
        "summary",
        1773496800000000000,
        1773497100000000000,
        120.0,
        40.0,
        "ms"
      ],
      [
        "M2",
        "bucket",
        1773496800000000000,
        1773496860000000000,
        120.0,
        40.0,
        "ms"
      ]
    ]
  }
}
```

</details>

<details>

<summary>Call 4211: pydantic.main.BaseModel.__init__</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 253.

```json
{
  "call": 4211,
  "parent_call": 4194,
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

<summary>Call 4213: pydantic.main.BaseModel.__init__</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 253.

```json
{
  "call": 4213,
  "parent_call": 4194,
  "function": "pydantic.main.BaseModel.__init__",
  "source": ".\\.venv\\Lib\\site-packages\\pydantic\\main.py",
  "line": 253,
  "inputs": {
    "data": {
      "data": {
        "columns": [
          "handle",
          "kind",
          "start_ns",
          "end_ns",
          "value",
          "absolute_error_bound",
          "unit"
        ],
        "rows": [
          [
            "M1",
            "summary",
            1773496800000000000,
            1773497100000000000,
            120.0,
            40.0,
            "ms"
          ],
          [
            "M2",
            "bucket",
            1773496800000000000,
            1773496860000000000,
            120.0,
            40.0,
            "ms"
          ]
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
    },
    "self": {}
  },
  "closure_values": {},
  "output": null,
  "constructed_object": {
    "data": {
      "columns": [
        "handle",
        "kind",
        "start_ns",
        "end_ns",
        "value",
        "absolute_error_bound",
        "unit"
      ],
      "rows": [
        [
          "M1",
          "summary",
          1773496800000000000,
          1773497100000000000,
          120.0,
          40.0,
          "ms"
        ],
        [
          "M2",
          "bucket",
          1773496800000000000,
          1773496860000000000,
          120.0,
          40.0,
          "ms"
        ]
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
}
```

</details>

<details>

<summary>Call 4215: contracts.models.TableData.rectangular</summary>

Source: `.\contracts\models.py`, line 256.

```json
{
  "call": 4215,
  "parent_call": 4214,
  "function": "contracts.models.TableData.rectangular",
  "source": ".\\contracts\\models.py",
  "line": 256,
  "inputs": {
    "self": {
      "columns": [
        "handle",
        "kind",
        "start_ns",
        "end_ns",
        "value",
        "absolute_error_bound",
        "unit"
      ],
      "rows": [
        [
          "M1",
          "summary",
          1773496800000000000,
          1773497100000000000,
          120.0,
          40.0,
          "ms"
        ],
        [
          "M2",
          "bucket",
          1773496800000000000,
          1773496860000000000,
          120.0,
          40.0,
          "ms"
        ]
      ]
    }
  },
  "closure_values": {},
  "output": {
    "columns": [
      "handle",
      "kind",
      "start_ns",
      "end_ns",
      "value",
      "absolute_error_bound",
      "unit"
    ],
    "rows": [
      [
        "M1",
        "summary",
        1773496800000000000,
        1773497100000000000,
        120.0,
        40.0,
        "ms"
      ],
      [
        "M2",
        "bucket",
        1773496800000000000,
        1773496860000000000,
        120.0,
        40.0,
        "ms"
      ]
    ]
  }
}
```

</details>

<details>

<summary>Call 4226: contracts.models.ToolResult.consistent</summary>

Source: `.\contracts\models.py`, line 286.

```json
{
  "call": 4226,
  "parent_call": 4214,
  "function": "contracts.models.ToolResult.consistent",
  "source": ".\\contracts\\models.py",
  "line": 286,
  "inputs": {
    "self": {
      "data": {
        "columns": [
          "handle",
          "kind",
          "start_ns",
          "end_ns",
          "value",
          "absolute_error_bound",
          "unit"
        ],
        "rows": [
          [
            "M1",
            "summary",
            1773496800000000000,
            1773497100000000000,
            120.0,
            40.0,
            "ms"
          ],
          [
            "M2",
            "bucket",
            1773496800000000000,
            1773496860000000000,
            120.0,
            40.0,
            "ms"
          ]
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
  },
  "closure_values": {},
  "output": {
    "data": {
      "columns": [
        "handle",
        "kind",
        "start_ns",
        "end_ns",
        "value",
        "absolute_error_bound",
        "unit"
      ],
      "rows": [
        [
          "M1",
          "summary",
          1773496800000000000,
          1773497100000000000,
          120.0,
          40.0,
          "ms"
        ],
        [
          "M2",
          "bucket",
          1773496800000000000,
          1773496860000000000,
          120.0,
          40.0,
          "ms"
        ]
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
}
```

</details>

<details>

<summary>Call 4229: pydantic.main.BaseModel.model_dump</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 427.

```json
{
  "call": 4229,
  "parent_call": 4194,
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
          "kind",
          "start_ns",
          "end_ns",
          "value",
          "absolute_error_bound",
          "unit"
        ],
        "rows": [
          [
            "M1",
            "summary",
            1773496800000000000,
            1773497100000000000,
            120.0,
            40.0,
            "ms"
          ],
          [
            "M2",
            "bucket",
            1773496800000000000,
            1773496860000000000,
            120.0,
            40.0,
            "ms"
          ]
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
  },
  "closure_values": {},
  "output": {
    "data": {
      "columns": [
        "handle",
        "kind",
        "start_ns",
        "end_ns",
        "value",
        "absolute_error_bound",
        "unit"
      ],
      "rows": [
        [
          "M1",
          "summary",
          1773496800000000000,
          1773497100000000000,
          120.0,
          40.0,
          "ms"
        ],
        [
          "M2",
          "bucket",
          1773496800000000000,
          1773496860000000000,
          120.0,
          40.0,
          "ms"
        ]
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
}
```

</details>

<details>

<summary>Call 4231: store.evidence.compact_json</summary>

Source: `.\store\evidence.py`, line 70.

```json
{
  "call": 4231,
  "parent_call": 89,
  "function": "store.evidence.compact_json",
  "source": ".\\store\\evidence.py",
  "line": 70,
  "inputs": {
    "value": {
      "data": {
        "columns": [
          "handle",
          "kind",
          "start_ns",
          "end_ns",
          "value",
          "absolute_error_bound",
          "unit"
        ],
        "rows": [
          [
            "M1",
            "summary",
            1773496800000000000,
            1773497100000000000,
            120.0,
            40.0,
            "ms"
          ],
          [
            "M2",
            "bucket",
            1773496800000000000,
            1773496860000000000,
            120.0,
            40.0,
            "ms"
          ]
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
  },
  "closure_values": {},
  "output": "{\"data\":{\"columns\":[\"handle\",\"kind\",\"start_ns\",\"end_ns\",\"value\",\"absolute_error_bound\",\"unit\"],\"rows\":[[\"M1\",\"summary\",1773496800000000000,1773497100000000000,120.0,40.0,\"ms\"],[\"M2\",\"bucket\",1773496800000000000,1773496860000000000,120.0,40.0,\"ms\"]]},\"total_matches\":6,\"returned\":2,\"truncated\":true,\"next_cursor\":\"4e6231a4fa2bc2925490d28c0ebc84335601f75441a9c2aa9d27b6b867525692:2\",\"query_id\":\"q4e6231a4\",\"source\":{\"backend\":\"parquet\",\"dataset_id\":\"856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb\",\"tool_version\":\"0.1.1\"},\"warnings\":[]}"
}
```

</details>

<details>

<summary>Call 4239: mcp_servers.telemetry.engine.ToolEngine.__init__.&lt;locals&gt;.&lt;lambda&gt;</summary>

Source: `.\mcp_servers\telemetry\engine.py`, line 44.

```json
{
  "call": 4239,
  "parent_call": 89,
  "function": "mcp_servers.telemetry.engine.ToolEngine.__init__.<locals>.<lambda>",
  "source": ".\\mcp_servers\\telemetry\\engine.py",
  "line": 44,
  "inputs": {
    "text": "{\"data\":{\"columns\":[\"handle\",\"kind\",\"start_ns\",\"end_ns\",\"value\",\"absolute_error_bound\",\"unit\"],\"rows\":[[\"M1\",\"summary\",1773496800000000000,1773497100000000000,120.0,40.0,\"ms\"],[\"M2\",\"bucket\",1773496800000000000,1773496860000000000,120.0,40.0,\"ms\"]]},\"total_matches\":6,\"returned\":2,\"truncated\":true,\"next_cursor\":\"4e6231a4fa2bc2925490d28c0ebc84335601f75441a9c2aa9d27b6b867525692:2\",\"query_id\":\"q4e6231a4\",\"source\":{\"backend\":\"parquet\",\"dataset_id\":\"856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb\",\"tool_version\":\"0.1.1\"},\"warnings\":[]}"
  },
  "closure_values": {},
  "output": 552
}
```

</details>

<details>

<summary>Call 4242: mcp.server.fastmcp.utilities.func_metadata.FuncMetadata.convert_result</summary>

Source: `.\.venv\Lib\site-packages\mcp\server\fastmcp\utilities\func_metadata.py`, line 97.

```json
{
  "call": 4242,
  "parent_call": 51,
  "function": "mcp.server.fastmcp.utilities.func_metadata.FuncMetadata.convert_result",
  "source": ".\\.venv\\Lib\\site-packages\\mcp\\server\\fastmcp\\utilities\\func_metadata.py",
  "line": 97,
  "inputs": {
    "result": {
      "data": {
        "columns": [
          "handle",
          "kind",
          "start_ns",
          "end_ns",
          "value",
          "absolute_error_bound",
          "unit"
        ],
        "rows": [
          [
            "M1",
            "summary",
            1773496800000000000,
            1773497100000000000,
            120.0,
            40.0,
            "ms"
          ],
          [
            "M2",
            "bucket",
            1773496800000000000,
            1773496860000000000,
            120.0,
            40.0,
            "ms"
          ]
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
    },
    "self": "<mcp.server.fastmcp.utilities.func_metadata.FuncMetadata>"
  },
  "closure_values": {},
  "output": [
    [
      {
        "type": "text",
        "text": "{\n  \"data\": {\n    \"columns\": [\n      \"handle\",\n      \"kind\",\n      \"start_ns\",\n      \"end_ns\",\n      \"value\",\n      \"absolute_error_bound\",\n      \"unit\"\n    ],\n    \"rows\": [\n      [\n        \"M1\",\n        \"summary\",\n        1773496800000000000,\n        1773497100000000000,\n        120.0,\n        40.0,\n        \"ms\"\n      ],\n      [\n        \"M2\",\n        \"bucket\",\n        1773496800000000000,\n        1773496860000000000,\n        120.0,\n        40.0,\n        \"ms\"\n      ]\n    ]\n  },\n  \"total_matches\": 6,\n  \"returned\": 2,\n  \"truncated\": true,\n  \"next_cursor\": \"4e6231a4fa2bc2925490d28c0ebc84335601f75441a9c2aa9d27b6b867525692:2\",\n  \"query_id\": \"q4e6231a4\",\n  \"source\": {\n    \"backend\": \"parquet\",\n    \"dataset_id\": \"856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb\",\n    \"tool_version\": \"0.1.1\"\n  },\n  \"warnings\": []\n}",
        "annotations": null,
        "meta": null
      }
    ],
    {
      "data": {
        "columns": [
          "handle",
          "kind",
          "start_ns",
          "end_ns",
          "value",
          "absolute_error_bound",
          "unit"
        ],
        "rows": [
          [
            "M1",
            "summary",
            1773496800000000000,
            1773497100000000000,
            120.0,
            40.0,
            "ms"
          ],
          [
            "M2",
            "bucket",
            1773496800000000000,
            1773496860000000000,
            120.0,
            40.0,
            "ms"
          ]
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
  ]
}
```

</details>

<details>

<summary>Call 4244: mcp.server.fastmcp.utilities.func_metadata._convert_to_content</summary>

Source: `.\.venv\Lib\site-packages\mcp\server\fastmcp\utilities\func_metadata.py`, line 499.

```json
{
  "call": 4244,
  "parent_call": 4242,
  "function": "mcp.server.fastmcp.utilities.func_metadata._convert_to_content",
  "source": ".\\.venv\\Lib\\site-packages\\mcp\\server\\fastmcp\\utilities\\func_metadata.py",
  "line": 499,
  "inputs": {
    "result": {
      "data": {
        "columns": [
          "handle",
          "kind",
          "start_ns",
          "end_ns",
          "value",
          "absolute_error_bound",
          "unit"
        ],
        "rows": [
          [
            "M1",
            "summary",
            1773496800000000000,
            1773497100000000000,
            120.0,
            40.0,
            "ms"
          ],
          [
            "M2",
            "bucket",
            1773496800000000000,
            1773496860000000000,
            120.0,
            40.0,
            "ms"
          ]
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
  },
  "closure_values": {},
  "output": [
    {
      "type": "text",
      "text": "{\n  \"data\": {\n    \"columns\": [\n      \"handle\",\n      \"kind\",\n      \"start_ns\",\n      \"end_ns\",\n      \"value\",\n      \"absolute_error_bound\",\n      \"unit\"\n    ],\n    \"rows\": [\n      [\n        \"M1\",\n        \"summary\",\n        1773496800000000000,\n        1773497100000000000,\n        120.0,\n        40.0,\n        \"ms\"\n      ],\n      [\n        \"M2\",\n        \"bucket\",\n        1773496800000000000,\n        1773496860000000000,\n        120.0,\n        40.0,\n        \"ms\"\n      ]\n    ]\n  },\n  \"total_matches\": 6,\n  \"returned\": 2,\n  \"truncated\": true,\n  \"next_cursor\": \"4e6231a4fa2bc2925490d28c0ebc84335601f75441a9c2aa9d27b6b867525692:2\",\n  \"query_id\": \"q4e6231a4\",\n  \"source\": {\n    \"backend\": \"parquet\",\n    \"dataset_id\": \"856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb\",\n    \"tool_version\": \"0.1.1\"\n  },\n  \"warnings\": []\n}",
      "annotations": null,
      "meta": null
    }
  ]
}
```

</details>

<details>

<summary>Call 4252: pydantic.main.BaseModel.__init__</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 253.

```json
{
  "call": 4252,
  "parent_call": 4244,
  "function": "pydantic.main.BaseModel.__init__",
  "source": ".\\.venv\\Lib\\site-packages\\pydantic\\main.py",
  "line": 253,
  "inputs": {
    "data": {
      "type": "text",
      "text": "{\n  \"data\": {\n    \"columns\": [\n      \"handle\",\n      \"kind\",\n      \"start_ns\",\n      \"end_ns\",\n      \"value\",\n      \"absolute_error_bound\",\n      \"unit\"\n    ],\n    \"rows\": [\n      [\n        \"M1\",\n        \"summary\",\n        1773496800000000000,\n        1773497100000000000,\n        120.0,\n        40.0,\n        \"ms\"\n      ],\n      [\n        \"M2\",\n        \"bucket\",\n        1773496800000000000,\n        1773496860000000000,\n        120.0,\n        40.0,\n        \"ms\"\n      ]\n    ]\n  },\n  \"total_matches\": 6,\n  \"returned\": 2,\n  \"truncated\": true,\n  \"next_cursor\": \"4e6231a4fa2bc2925490d28c0ebc84335601f75441a9c2aa9d27b6b867525692:2\",\n  \"query_id\": \"q4e6231a4\",\n  \"source\": {\n    \"backend\": \"parquet\",\n    \"dataset_id\": \"856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb\",\n    \"tool_version\": \"0.1.1\"\n  },\n  \"warnings\": []\n}"
    },
    "self": "<mcp.types.TextContent>"
  },
  "closure_values": {},
  "output": null,
  "constructed_object": {
    "type": "text",
    "text": "{\n  \"data\": {\n    \"columns\": [\n      \"handle\",\n      \"kind\",\n      \"start_ns\",\n      \"end_ns\",\n      \"value\",\n      \"absolute_error_bound\",\n      \"unit\"\n    ],\n    \"rows\": [\n      [\n        \"M1\",\n        \"summary\",\n        1773496800000000000,\n        1773497100000000000,\n        120.0,\n        40.0,\n        \"ms\"\n      ],\n      [\n        \"M2\",\n        \"bucket\",\n        1773496800000000000,\n        1773496860000000000,\n        120.0,\n        40.0,\n        \"ms\"\n      ]\n    ]\n  },\n  \"total_matches\": 6,\n  \"returned\": 2,\n  \"truncated\": true,\n  \"next_cursor\": \"4e6231a4fa2bc2925490d28c0ebc84335601f75441a9c2aa9d27b6b867525692:2\",\n  \"query_id\": \"q4e6231a4\",\n  \"source\": {\n    \"backend\": \"parquet\",\n    \"dataset_id\": \"856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb\",\n    \"tool_version\": \"0.1.1\"\n  },\n  \"warnings\": []\n}",
    "annotations": null,
    "meta": null
  }
}
```

</details>

<details>

<summary>Call 4254: pydantic.main.BaseModel.model_validate</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 693.

```json
{
  "call": 4254,
  "parent_call": 4242,
  "function": "pydantic.main.BaseModel.model_validate",
  "source": ".\\.venv\\Lib\\site-packages\\pydantic\\main.py",
  "line": 693,
  "inputs": {
    "obj": {
      "data": {
        "columns": [
          "handle",
          "kind",
          "start_ns",
          "end_ns",
          "value",
          "absolute_error_bound",
          "unit"
        ],
        "rows": [
          [
            "M1",
            "summary",
            1773496800000000000,
            1773497100000000000,
            120.0,
            40.0,
            "ms"
          ],
          [
            "M2",
            "bucket",
            1773496800000000000,
            1773496860000000000,
            120.0,
            40.0,
            "ms"
          ]
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
    },
    "strict": null,
    "extra": null,
    "from_attributes": null,
    "context": null,
    "by_alias": null,
    "by_name": null,
    "cls": "<class mcp.server.fastmcp.utilities.func_metadata.query_metricDictOutput>"
  },
  "closure_values": {},
  "output": {
    "data": {
      "columns": [
        "handle",
        "kind",
        "start_ns",
        "end_ns",
        "value",
        "absolute_error_bound",
        "unit"
      ],
      "rows": [
        [
          "M1",
          "summary",
          1773496800000000000,
          1773497100000000000,
          120.0,
          40.0,
          "ms"
        ],
        [
          "M2",
          "bucket",
          1773496800000000000,
          1773496860000000000,
          120.0,
          40.0,
          "ms"
        ]
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
}
```

</details>

<details>

<summary>Call 4256: pydantic.main.BaseModel.model_dump</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 427.

```json
{
  "call": 4256,
  "parent_call": 4242,
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
          "kind",
          "start_ns",
          "end_ns",
          "value",
          "absolute_error_bound",
          "unit"
        ],
        "rows": [
          [
            "M1",
            "summary",
            1773496800000000000,
            1773497100000000000,
            120.0,
            40.0,
            "ms"
          ],
          [
            "M2",
            "bucket",
            1773496800000000000,
            1773496860000000000,
            120.0,
            40.0,
            "ms"
          ]
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
  },
  "closure_values": {},
  "output": {
    "data": {
      "columns": [
        "handle",
        "kind",
        "start_ns",
        "end_ns",
        "value",
        "absolute_error_bound",
        "unit"
      ],
      "rows": [
        [
          "M1",
          "summary",
          1773496800000000000,
          1773497100000000000,
          120.0,
          40.0,
          "ms"
        ],
        [
          "M2",
          "bucket",
          1773496800000000000,
          1773496860000000000,
          120.0,
          40.0,
          "ms"
        ]
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
}
```

</details>

<details>

<summary>Call 6705: pydantic.main.BaseModel.__init__</summary>

Source: `.\.venv\Lib\site-packages\pydantic\main.py`, line 253.

```json
{
  "call": 6705,
  "parent_call": 1,
  "function": "pydantic.main.BaseModel.__init__",
  "source": ".\\.venv\\Lib\\site-packages\\pydantic\\main.py",
  "line": 253,
  "inputs": {
    "data": {
      "content": [
        {
          "type": "text",
          "text": "{\n  \"data\": {\n    \"columns\": [\n      \"handle\",\n      \"kind\",\n      \"start_ns\",\n      \"end_ns\",\n      \"value\",\n      \"absolute_error_bound\",\n      \"unit\"\n    ],\n    \"rows\": [\n      [\n        \"M1\",\n        \"summary\",\n        1773496800000000000,\n        1773497100000000000,\n        120.0,\n        40.0,\n        \"ms\"\n      ],\n      [\n        \"M2\",\n        \"bucket\",\n        1773496800000000000,\n        1773496860000000000,\n        120.0,\n        40.0,\n        \"ms\"\n      ]\n    ]\n  },\n  \"total_matches\": 6,\n  \"returned\": 2,\n  \"truncated\": true,\n  \"next_cursor\": \"4e6231a4fa2bc2925490d28c0ebc84335601f75441a9c2aa9d27b6b867525692:2\",\n  \"query_id\": \"q4e6231a4\",\n  \"source\": {\n    \"backend\": \"parquet\",\n    \"dataset_id\": \"856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb\",\n    \"tool_version\": \"0.1.1\"\n  },\n  \"warnings\": []\n}",
          "annotations": null,
          "meta": null
        }
      ],
      "structuredContent": {
        "data": {
          "columns": [
            "handle",
            "kind",
            "start_ns",
            "end_ns",
            "value",
            "absolute_error_bound",
            "unit"
          ],
          "rows": [
            [
              "M1",
              "summary",
              1773496800000000000,
              1773497100000000000,
              120.0,
              40.0,
              "ms"
            ],
            [
              "M2",
              "bucket",
              1773496800000000000,
              1773496860000000000,
              120.0,
              40.0,
              "ms"
            ]
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
        "text": "{\n  \"data\": {\n    \"columns\": [\n      \"handle\",\n      \"kind\",\n      \"start_ns\",\n      \"end_ns\",\n      \"value\",\n      \"absolute_error_bound\",\n      \"unit\"\n    ],\n    \"rows\": [\n      [\n        \"M1\",\n        \"summary\",\n        1773496800000000000,\n        1773497100000000000,\n        120.0,\n        40.0,\n        \"ms\"\n      ],\n      [\n        \"M2\",\n        \"bucket\",\n        1773496800000000000,\n        1773496860000000000,\n        120.0,\n        40.0,\n        \"ms\"\n      ]\n    ]\n  },\n  \"total_matches\": 6,\n  \"returned\": 2,\n  \"truncated\": true,\n  \"next_cursor\": \"4e6231a4fa2bc2925490d28c0ebc84335601f75441a9c2aa9d27b6b867525692:2\",\n  \"query_id\": \"q4e6231a4\",\n  \"source\": {\n    \"backend\": \"parquet\",\n    \"dataset_id\": \"856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb\",\n    \"tool_version\": \"0.1.1\"\n  },\n  \"warnings\": []\n}",
        "annotations": null,
        "meta": null
      }
    ],
    "structuredContent": {
      "data": {
        "columns": [
          "handle",
          "kind",
          "start_ns",
          "end_ns",
          "value",
          "absolute_error_bound",
          "unit"
        ],
        "rows": [
          [
            "M1",
            "summary",
            1773496800000000000,
            1773497100000000000,
            120.0,
            40.0,
            "ms"
          ],
          [
            "M2",
            "bucket",
            1773496800000000000,
            1773496860000000000,
            120.0,
            40.0,
            "ms"
          ]
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
    },
    "isError": false
  }
}
```

</details>
