# Contracts v0.1

This snapshot implements the conversation agreements between Person A and Aditi.
Wire schema is 0.1.0; current generator and tool implementation version is 0.1.1.
See [audit corrections](../docs/decisions/0002-implementation-audit.md).
It is ready for joint review; it does not claim that a human review has happened.
Changes to shared contracts require both collaborators' approval. Person B owns
the final answer and trajectory schemas; this package deliberately does not invent
those schemas on her behalf. She should import `Diagnosis` for her closed answer enum.

## Public manifest

`Manifest`: opaque content-addressed `id`, `schema_version`, question, `data_range`,
`reference_time`, source, native `bucket_seconds`, and configured trace retention.
Source path is exactly `.`: the manifest never authorizes arbitrary file access.
Actual cause onset and baseline windows are absent. All ISO dates require `Z`;
Parquet timestamps are integer UTC epoch nanoseconds. ISO inputs support up to
nine fractional digits without rounding; span timestamps retain nanosecond precision.

The template and relative reference-time distribution are exactly balanced across
labels **within each development/test split**. This is a finite-suite metadata audit,
not a proof that arbitrary classifiers cannot exploit other artifacts. All alerts
can include the same real, brief frontend latency blip, regardless of case label;
reports have no automatic blip. Question values come from the same
histogram estimates the tools expose. A brief transient is defined as no sustained
actionable problem, so these cases have `no_fault=true`.

## Telemetry tables

The fields in `models.py` and exported JSON Schemas are authoritative.

* `spans.parquet`: C2 span fields; attributes are canonical JSON strings on disk,
  dictionaries after decoding. Duration means server-side handler time, including
  synchronous child calls, not independent network transit time.
* `logs.parquet`: C2 fields plus JSON `attributes`. Links survive trace sampling.
* `metrics.parquet`: C2 fields plus nullable `max_value`. Counts are per bucket,
  never cumulative counters. Gauge `value` is the mean of one-second samples;
  `max_value` is their maximum. Each one-second service sample is the mean of two
  equal-size east/west replicas. CPU unit is ratio [0,1]; memory unit is MB. This
  averaging happens before temporal aggregation, including for regional faults.
* `histograms.parquet`: bucket time, service, operation, `bounds_ms`, `counts`.
  These additional public sufficient statistics are required for merging latency.

Buckets are `[start,end)`, epoch aligned, timestamped by bucket START. Requests
belong to buckets by handler START, even if they finish later. Counts and histograms
come from **all** generated handlers before whole-trace retention. All reachable
service/operation combinations get zero-count buckets where no requests occur.
Empty latency has null value, not zero. Missing buckets are not synthesized as zero.

### Aggregation

Metric query endpoints must align to the native bucket width; arbitrary partial
native buckets receive `UNALIGNED_WINDOW`. Step is a positive multiple of native
width, aligned to epoch; first/last output buckets can be shorter than the requested
step but contain only whole native buckets. This prevents pretending a histogram
can be sliced within a bucket. Raw trace/log windows do not require alignment.

* Counts: sum native counts. Server handler counts are not unique user requests.
* Error rate: `sum(error_count)/sum(request_count)` over paired bucket/operation
  observations only; unmatched counts are excluded with a gap warning. Null for no
  paired requests. This prevents different missing populations biasing the ratio.
* Gauge average: mean of native averages, valid because all native buckets are
  equally long and equally sampled. Gauge maximum: max native `max_value`.
* Percentile: sum native histogram counts, then estimate the nearest-rank percentile.
  Do not average precomputed percentiles. Service-wide latency mixes its handler
  operations; use the operation filter for meaningful endpoint-specific comparisons.
* Gaps: checked per service, operation and required count/histogram/gauge series.
  Warn `METRIC_GAP`; summary covers available observations and can be incomplete.
  `check_coverage` counts native buckets missing any required cell, not just CPU.
* `compare_windows`: returns both summaries; count totals are not normalized for
  unequal window durations. `breakdown` explicitly uses retained spans and warns.

Default explicit bounds (ms):
`5,10,20,40,80,160,320,640,1280,2560,5120,10240,20480,60000`.
These are configurable but must be identical within one dataset.
Like OTel explicit histograms, bins have inclusive upper bounds: `[0,5]`, `(5,10]`,
..., `(20480,60000]`, `(60000,+inf)`. Counts have `len(bounds)+1` entries.
The estimate is the selected finite bin midpoint. Absolute error relative to the
raw nearest-rank percentile is at most half that bin's width; each response point
reports `absolute_error_bound`. Worst finite-bin bound with defaults is **19,760 ms**;
the coarse high-latency tail is intentional and must not be presented as precise.
Overflow returns null with a warning; there is no finite worst-case overflow error.
This estimates the empirical percentile, not a population confidence interval.

## Private truth and diagnoses

`root_causes` is a list. Each cause contains service, closed `fault_type`, role,
propagation path (cause outward to callers), onset/end, scope and optional private
`injection_mechanism`. Null end means it persists through the observation horizon,
not that telemetry proves the problem continues forever.

A **trigger** is harmless alone and harmful only in combination with the primary.
The retry policy is a trigger; the failing downstream service is the primary.
The simulator's monitored operation is POST /checkout. Causes and paths are recorded
only when their effects propagate to it; unrelated or unobserved injections are
private decoys. `no_fault` means no injected cause of that monitored operation's
problem, not that every background component is perfectly healthy. A retry policy
alone produces no primary cause. Optional calls tolerate errors but still add delay.
At least one primary is required for a nonempty cause list. Multiple independent
primaries are permitted. Planned Person B scoring: primary full credit, trigger-only
half credit, multiple primaries by recall; service and fault type score separately.

See [fault diagnosis mapping](../docs/fault-diagnoses.md) for exact labels and ambiguity.

## Tool protocol

All nine tools accept an object named `query`; e.g. MCP `call_tool("query_metric",
{"query": {"window": {...}, "service": "payment", "metric": "latency_p95_ms"}})`.
Schemas reject unknown fields, paths, free-form backend queries, invalid services,
invalid timestamps and invalid limits. Read-only tool annotations are supplied.
`get_trace` also takes an explicit window; if any retained span starts in that window,
it returns the entire trace with parent IDs, ordered by start time then span ID.
`find_traces` filters matching spans, while its `status` column describes the root
request and `matching_status` describes those matching spans. An optional email
ERROR can therefore match while the overall request is OK. Missing roots yield
UNKNOWN with an INCOMPLETE_TRACE warning.

Envelope: `data:{columns,rows}`, `total_matches`, `returned`, `truncated`, `next_cursor`,
`query_id`, source `{backend,dataset_id,tool_version}`, warnings `[{code,message}]`.
First column is always `handle`. `total_matches` counts rows in the logical result
after grouping/deduplication, before paging. Log duplicate multiplicity is a row field.
Zero matches is successful. Failure is `{error:{code,message}}`; never a fake empty table.
Invalid schema-level MCP requests can instead be standard SDK `isError` responses.

Limits are 1..100, default 20. The provisional 1500-token target currently uses
**at most 1500 serialized ASCII JSON bytes for the envelope**, deliberately conservative.
This is not an actual model-token measurement. Python `ToolEngine(token_counter=...)`
accepts an exact tokenizer callback; Aditi must supply/measure it before token claims.
The SDK may expose both text and structured content; forward **one envelope** to the
model, not both. The cap does not include MCP transport framing or tool definitions.
Rows are never silently edited; if one complete row cannot fit, `OUTPUT_TOO_LARGE`
asks the agent to narrow its query or use a larger measured budget.

## Query identity and evidence

`store.evidence.canonical_query` is the shared implementation for Aditi's verifier.
It hashes dataset content ID, tool implementation version, tool name and normalized validated
arguments, excluding `limit` and `cursor`. Defaults are expanded, windows normalized
to UTC `Z`, dictionary keys sorted, JSON serialized with compact separators.
Explicit and omitted defaults have the same identity. Unused summary step sizes and
non-gauge aggregation switches are excluded/normalized because they do not change results.

Query IDs use `q` plus eight SHA-256 hex characters. A new colliding query extends
its prefix one character at a time until unused; existing IDs do not change. The
allocation is deterministic for the recorded session order. A verifier can replay
allocation or use `verifies` to validate a logged prefix against the full hash.

Cursor is `full_query_digest:next_offset`; it is bound to one result set and contains
no filesystem paths. All pages use the same query ID. Handles use whole-result
one-based positions: `S` spans, `T` trace summaries, `L` logs, `M` metric points or
summaries, `V` services, `D` dependency edges, `C` coverage, `B` breakdowns.
Citation example: `q1234abcd:S51`. Only evidence actually returned in the agent's
log can support a citation. Metric rows include window, units and error bounds.

## Public/private boundary and leakage

The server loads exactly four fixed Parquet files and one manifest from an explicitly
selected `public/<content_id>` directory. It never loads truth, suite metadata or
reference examples or agent-run records. Paths inside `runs/` or `private/` are
rejected before any file is opened, even if they contain a valid-looking public
dataset. The leakage audit rejects nested reserved stores without reading them.
Content identity is verified at load time. Dataset ancestors,
manifest and data files cannot be symbolic links. Calls cannot select another path.
This is an application interface boundary, not an OS sandbox against arbitrary Python
code under the same account. Deploy processes with filesystem isolation if that stronger
threat model is required.

Forbidden terms are case-insensitive word/delimiter matches:
`injected, fault, chaos, decoy, scenario, archetype, seed, ground truth`.
The audit examines public text, attributes, relative filenames and Parquet metadata.
An explicitly allowlisted planted prompt-injection **body** may contain these words;
the surrounding attributes remain audited. Never point an agent at `private/`,
`reference_index.json`, `suite.json`, `examples/`, or this source repository as evidence.

## Export and review

Run `python -m telemetry.cli schemas` to export JSON Schemas. Contract tests ensure
the checked-in schemas match their Python models. See reference_index.json outside
the public datasets for the three sample bundles and pagination exchange.
