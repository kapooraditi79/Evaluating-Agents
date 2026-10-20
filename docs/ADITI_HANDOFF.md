# Person A integration handoff after G0

Based on PROJECT_CONTEXT v2.1 and origin/main commit `01b4b20`. The update was
fast-forwarded locally. The previous local context and packaging files are preserved
in `data/merge-backup-01b4b20/` (ignored developer backups).

## Confirmations for contract review

Person A's implementation supports the following. These confirmations do not record
Person B's approval or declare the candidate contract frozen.

| Item | Implementation and qualification |
|---|---|
| D13, three stores | Only a selected `public/<id>` is read. Store initialization rejects paths inside `runs/` and `private/`, case-insensitively, before opening the manifest or telemetry. Leakage audits reject nested reserved stores without reading them. All nine tools reject path arguments. Existing link/junction checks remain. This is an application boundary, not an OS sandbox. |
| D15, fault types | All eight mechanisms map to exactly one closed diagnosis; `unknown` is an allowed answer. See [the full mapping and ambiguity cases](fault-diagnoses.md). Mechanisms remain private. |
| D17, query IDs | SHA-256 of dataset, tool version, tool name and normalized result arguments; limit/cursor excluded. Start with `q` plus eight hex digits; a new collision extends the prefix deterministically for the recorded session order. All pages share an ID; handles use positions in the whole sorted result. Verifier helpers are in `store/evidence.py`. |
| C2, aggregation | Epoch-aligned `[start,end)` native buckets; handler START determines membership; latency is handler duration. Merge histogram counts before estimating percentiles. Error rate is a ratio of paired sums. Gauges support temporal avg/max. Zero requests and missing cells differ; gaps warn. Partial native metric buckets are rejected because histograms cannot be sliced within a bucket. |
| C3, roles | Cause lists support multiple primaries. A trigger is harmless alone; the retry policy becomes a trigger only when downstream failure actually causes amplification. Scoring remains Person B's work. |
| C3, leakage | Forbidden terms are checked in public text, attributes, names and Parquet metadata, including decoded JSON. Only explicitly planted adversarial log bodies have an exception. |
| C3, shortcut audit | The 16-case starter suite's latest-ERROR rule gets 12.5% fault-service accuracy and 6.25% overall. This single small audit does not establish general shortcut resistance. |
| D19, templates | Alert/report choice and relative reference time are balanced across labels in each split; best lookup accuracy is 50%. Alert numbers come from telemetry, including healthy transient blips. This is a finite-suite audit, not proof about all classifiers or future datasets. |
| F-D12 | Three complete bundles, pagination exchange and a schema-only two-cause truth are in [fixtures/v0.1.1](../fixtures/v0.1.1/reference_index.json). |

Histogram bounds, gauge sampling, trigger semantics, evidence canonicalization and
the public schema extensions are described in [contracts/README.md](../contracts/README.md).
Default bounds have a largest finite-bin absolute error bound of **19,760 ms**;
each percentile reports its own bound. Overflow has no finite bound and returns
null with a warning. Set verifier tolerance from the returned bound, not a fixed
small tolerance.

`no_fault` concerns sustained actionable trouble in the monitored checkout operation.
It does not mean every background component is healthy. A brief alert blip can be
real without an injected sustained cause. This interpretation needs to match the scorer.

## Real definitions versus G0 stubs

All nine **tool names are identical**. Tool order and all descriptions differ.
The stubs remain available for reproducing the historical pilot; their arguments
are not compatible with the real server without changes to the caller and grader.

Complete exports and the machine-readable comparison:

* [Real MCP tools/list](tooling/tools-report.definitions.json), including `$defs`,
  output schemas and read-only annotations.
* [Real model function schemas](tooling/tools-report.functions.json).
* [G0 stub snapshot](tooling/g0-stub-tools.json).
* [Report](tooling/tools-report.json): inventories every nested argument's type,
  local/effective requiredness, nullability, defaults and constraints; 158 differences
  including descriptions and MCP metadata. Raw exports preserve cosmetic schema titles.
* [Description-only before/after comparison](tooling/description-changes.json): no
  tool arguments were changed while shortening descriptions.

Shared changes for **every tool**:

* Stubs accept flat arguments. Real MCP calls require `{"query": {...}}`.
  `query` is a required object; `query.window` is a required object with required
  string `start` and `end`. Replace flat `start`/`end` with this window.
* Real windows must be valid ordered UTC `Z` timestamps within the dataset. Up to
  nine fractional digits are accepted; the G0 semantic checker currently accepts
  whole seconds only. Metric and coverage windows must also align to native buckets.
* Every real query has optional `limit`: integer, default 20, minimum 1, maximum 100;
  and optional `cursor`: string or null, default null. Only the stubs for
  `find_traces` and `search_logs` had these; their limits had no default and cursors
  could not explicitly be null. Cursor contents are validated against the result set.
* All real **inner query objects** forbid unknown fields. The SDK's outer function
  schema does not advertise `additionalProperties:false`, unlike the flat stubs.
* Optional real service, operation and filter strings permit explicit null where
  noted below. The corresponding optional stub strings permit omission but not null.
  Required service/metric/ID strings remain required and non-null.
* MCP definitions additionally advertise read-only/deterministic annotations and
  a generic object output schema. These are absent from the stubs and are omitted
  from the model-facing function projection. The envelope is documented separately.

The table covers the remaining changes beyond that shared wrapper/window/paging:

| Tool | Stub to real argument differences |
|---|---|
| `list_services` | Stub start/end were optional. The real window and both endpoints are required. No further filters. |
| `query_metric` | Required service:string and metric:string enum remain. Real metric adds `error_rate` to the seven stub choices. Optional operation becomes nullable, default null. `step_seconds` remains optional integer but now defaults to 60, allows 1..86400 instead of 10..600, and must be a multiple of native bucket width at runtime. Adds optional aggregation:string `avg` or `max`, default `avg`, used for gauges. |
| `compare_windows` | Replace required incident_start/end with required window.start/end; replace required baseline_start/end with required baseline_window.start/end. Required service and metric remain, with `error_rate` added. Adds optional nullable operation, step_seconds and aggregation as for query_metric. The inherited step is validated but does not affect the returned summaries or query ID; removing it is a proposed joint contract simplification. |
| `find_traces` | Optional service, operation and status become nullable, default null; status still accepts OK/ERROR. min_duration_ms remains optional nonnegative number, now explicitly defaults to 0.0 and rejects nonfinite values. Removes region:string enum us/eu/ap. Adds optional attributes:object of string values, default empty at runtime; supported keys are `app.region` and `service.version`. Filter a region with `{"attributes":{"app.region":"east"}}`. |
| `get_trace` | trace_id remains required string, now with pattern `^[0-9a-f]{32}$`. Adds required window plus optional paging. A retained span must start in the window; then the entire trace is returned, possibly over pages. |
| `breakdown` | group_by remains required string with the same five choices. metric becomes optional, defaults to request_count, and supports only request_count/error_count/latency_p95_ms, instead of all seven stub metrics. Removes optional service filter. Counts and latency describe retained handler spans, not the complete metric population. |
| `search_logs` | Optional service, severity, contains and trace_id become nullable, default null. Severity retains INFO/WARN/ERROR (enum order changes only). contains now has maxLength 200; matching remains case-insensitive literal text. trace_id gains the lowercase 32-hex pattern. |
| `get_dependencies` | No extra filters beyond the common window/paging. Stub description promised error rates. Real columns are caller, callee, observed_calls and calls_per_second, plus handle; there is no edge-error-rate column. |
| `check_coverage` | Optional service becomes nullable, default null. Returns sampling, missing metric buckets and retained log counts. It warns LOG_COVERAGE_UNKNOWN; it does not claim that unusual log volume proves log loss. |

Service and region catalogs also differ, although the service JSON Schema is a string
in both versions. The real topology has **11 services**:
frontend, checkout, cart, payment, shipping, quote, currency, email, productcatalog,
recommendation and ad. The stubs list 12: they include redis, postgres and
product-catalog, omit quote, and use a different product-catalog spelling. Real
regions are east/west, rather than the stub's us/eu/ap. Discover services from the
selected dataset rather than copying the stub catalog.

`find_traces` status filters the matching handler span. Returned `status` describes
the root request; `matching_status` describes matching spans. A tolerated email ERROR
can match while the root request remains OK. This distinction matters for scoring
and interpreting evidence.

Real tool order: list_services, query_metric, find_traces, get_trace, search_logs,
compare_windows, get_dependencies, check_coverage, breakdown. Stub order:
list_services, query_metric, compare_windows, find_traces, get_trace, breakdown,
search_logs, get_dependencies, check_coverage.

The current G0 runner and grader import `stub_tools.TOOLS`; semantic validation and
per-case expectations also inspect flat fields and a fixed service catalog. Simply
copying real schemas into TOOLS is insufficient: adapt nested windows/filters,
catalog checks and case expectations together. Keep the original 8-case pilot and
its measurements as historical results; register a separate real-tool run.

## Definition size and response budget

Sizes use compact ASCII JSON with sorted object keys, supplied tool order and no
transport framing. Here every character is one UTF-8 byte.

| Serialization | Characters / bytes | Approximate tokens, ceil(chars / 3.6) |
|---|---:|---:|
| Full real MCP tools/list, nine tools | 11,262 | 3,129 |
| Real model-facing function schemas, nine tools | 9,738 | 2,705 |
| Five P0 model-facing function schemas, diagnostic comparison only | 5,566 | 1,547 |
| G0 stub function schemas | 6,460 | 1,795 |

The 3.6 ratio comes from Aditi's one exploratory Qwen2.5-Coder 7B measurement:
**1,812 prompt tokens** for the stubs (1,971 with tools minus 159 without), including
chat-template tool boilerplate. That measured value differs from the 1,795-token
heuristic even for the original stubs. Real-definition counts above are estimates,
not tokenizer measurements or forecasts of total prompt size. Re-measure on the
actual Ollama model, template and final tool list, including agent-side tools.

Shorter descriptions saved 860 characters: full discovery was 12,122, model function
JSON was 10,598. All nine tools remain served. The five-tool row is a comparison,
not a change to the offered tool set or an experiment result.

The **1,500-token response target remains provisional**. Current implementation
uses a conservative 1,500-byte serialized envelope cap unless given an exact
tokenizer callback. It does not claim to measure tokens. Definitions, model prompt
framing and duplicated SDK text/structured output are outside this envelope budget;
forward only one copy of each tool result to the model.

Reproduce the export from the repository root:

```powershell
$idx = Get-Content fixtures/v0.1.1/reference_index.json -Raw | ConvertFrom-Json
$publicDir = Join-Path 'fixtures/v0.1.1' $idx.healthy.public
.\.venv\Scripts\python -m telemetry.cli tools-report --public-dir "$publicDir" --output docs/tooling/tools-report.json --stub-json docs/tooling/g0-stub-tools.json --approx-chars-per-token 3.6
```

## Shared environment and verification

`pyproject.toml` now includes the telemetry packages and `evaluation`, both telemetry
entry points, and G0's requests 2.32.5/jsonschema 4.23.0 dependencies.
`requirements.txt` delegates to `-e .[dev]` so the two install paths agree. The shared
test runner is pytest **9.0.3**, replacing G0's standalone 7.4.3 pin; both suites pass
on it. The lock file records this combined local environment. G0 code received
formatting and the equivalent datetime.UTC alias; schemas, pilot cases, thresholds
and grading behavior were preserved.

Validation: **108 tests pass**, including all 28 G0 tests. No Ollama/model experiment
was run on Person A's GPU. Ruff lint/format and dependency checks are recorded in
the implementation audit.

Next integration work: Person B adapts the runtime/grader to the actual schemas,
measures real-tool prompt/context costs, and connects answer scoring and evidence
verification. Jointly review the candidate contract and the differences above.
The existing G0 grading artifacts under runs/ are pilot-specific; end-to-end truth
and evaluation scores must follow D13's private-store rule.
