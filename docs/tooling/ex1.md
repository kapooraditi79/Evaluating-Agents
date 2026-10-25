AI client chooses query_metric
│
│ INPUT:
│ service="frontend", metric="latency_p95_ms"
│ window=14:00–14:05, limit=2
▼
MCP SDK: validate arguments
│
│ OUTPUT:
│ QueryMetric object, including defaults:
│ operation=None, step_seconds=60, aggregation="avg"
▼
server.py: query_metric(query)
│
├─ query.model_dump()
│ OUTPUT: dictionary containing those validated inputs
│
▼
engine.py: ToolEngine.call("query_metric", dictionary)
│
├─ QueryMetric.model_validate(dictionary)
│ └─ Window.ordered()
│ ├─ utc_ns(start) → 1773496800000000000
│ └─ utc_ns(end) → 1773497100000000000
│ OUTPUT: validated QueryMetric object
│
├─ evidence.py: canonical_query(...)
│ ├─ model_dump(exclude={"limit", "cursor"})
│ ├─ Window.model_validate(...)
│ ├─ utc_ns(...) → iso_time(...) for both timestamps
│ └─ json.dumps(...)
│ OUTPUT: standardized JSON string identifying the request
│
├─ QueryIds.get(canonical_string)
│ └─ digest_query(...) → SHA-256 fingerprint
│ OUTPUT: "q4e6231a4"
│
├─ digest_query(canonical_string)
│ OUTPUT: full fingerprint used in pagination cursors
│
▼
parquet.py: ParquetStore.query("query_metric", query_object)
│
├─ \_window(...) → integer start/end timestamps
├─ \_window(aligned=True) → same timestamps, alignment checked
│
├─ \_gaps(...)
│ └─ \_missing_buckets(...) → 0
│ OUTPUT: False; no missing-bucket warning
│
├─ point("summary", start, end)
│ └─ \_metric_value(...)
│ └─ percentile(merged_counts, bounds, 0.95)
│ └─ validate_bounds(...) → None: valid
│ OUTPUT: (120.0, 40.0)
│ OUTPUT: summary row: p95=120 ms, error bound=40 ms
│
├─ point("bucket", ...) × 5
│ Each repeats \_metric_value → percentile → validate_bounds
│ OUTPUT: bucket values [120, 120, 120, 120, 1920] ms
│
│ RETURN TO ENGINE:
│ columns + all SIX rows + warnings=[]
▼
engine.py: build the response
│
├─ Add handles M1 and M2 to the first two rows
│
├─ envelope()
│ ├─ TableData(...) → rectangular()
│ ├─ ToolSource(...)
│ ├─ ToolResult(...) → rectangular() → consistent()
│ └─ model_dump()
│ OUTPUT: result dictionary
│
├─ compact_json(result)
│ OUTPUT: compact JSON string
│
├─ count(JSON)
│ OUTPUT: 552 bytes for the two-row response
│
│ RETURN:
│ query_id="q4e6231a4"
│ returned=2, total_matches=6
│ rows=M1 summary + M2 first bucket
│ next_cursor="<full fingerprint></full>:2"
▼
MCP SDK: convert and validate the result
│ OUTPUT: structuredContent=result, isError=False
▼
AI client receives the response
