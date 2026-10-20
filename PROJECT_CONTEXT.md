# OTel Root-Cause Investigator — Project Context v2.1

**Status:** living design document, v2.1 (supersedes the v1 brief on the Desktop, which is left untouched). What changed since v2: section 15.
**Date:** 2026-10-20
**Working mode:** mentor mode. No code is written until the owner says so. Decisions below are marked
`DECIDED` (owner said so), `AGREED` (owner and Person A both said yes), `PENDING (A)` (owner decided, waiting for Person A),
`PROPOSED` (assistant recommendation awaiting a yes/no) or `OPEN` (needs an answer).

---

## 1. What the project is

### One-paragraph definition
A local, read-only **LLM investigator** that diagnoses incidents in a microservice application from
telemetry (traces, metrics, logs). It reaches the telemetry through **MCP tools**, follows
**Agent Skills** (reusable investigation procedures), runs on a **small open-source model on a consumer GPU**,
and is judged by an **evaluation harness** that knows the injected ground truth. The harness measures
correctness, evidence grounding, calibration/abstention, robustness (decoys, missing telemetry,
prompt injection) and cost. **OpenTelemetry is used twice:** as the format of the shop's telemetry the agent
investigates, and (phased, D13) as the format in which the agent's own runs are recorded.

### The research question (this is what makes it more than a demo)
> On a 6 GB GPU with a small open model, how much of the investigation quality comes from
> **the model**, how much from **tool design (MCP)**, and how much from **procedure (Skills)**?
> Which failure modes survive all three?

Everything is built so that this can be answered by a controlled ablation: model x tools x skills.

### What it is not
- Not a production SRE product and not a novelty claim (Datadog, Dynatrace and the Aegis benchmark exist).
- Not remediation: every tool is read-only.
- Not evidence about real production systems. Results are about a controlled lab.
- OpenTelemetry records data; it does not compute any score. Scoring is plain Python.

### Success criteria for the MVP (today)
1. One command runs the full pipeline: scenario -> agent -> validated answer -> score -> results table.
2. At least 3 conditions compared with numbers on a fixed, versioned scenario set.
3. Every run leaves a complete, replayable run record (artifact files and a results row first; an OpenTelemetry trace tree per run as soon as the first end-to-end run works).
4. A written failure taxonomy of the agent's mistakes, with examples.
5. A new developer can reproduce a run from the README.

---

## 2. Learning goals mapped to where they are learned

| Goal (from the owner) | Where it is practised | Feature IDs |
|---|---|---|
| Understand agent architecture, not a black box | Own agent loop: state, limits, tool-call parsing, stop rules | F-A2..F-A7, F-A11 |
| Write MCP servers | Telemetry MCP server with bounded, validated, read-only tools | F-M1..F-M6 |
| Write effective Agent Skills | 3 investigation skills, with/without ablation, gotchas from real failures | F-S1..F-S5 |
| Evaluate output (correctness, grounding, hallucination, tool errors) | Scorer, evidence verifier, calibration, failure taxonomy | F-E1..F-E11 |
| Observability of agent runs | OpenTelemetry trace tree per run, linked evaluation trace, viewer | F-A5, F-A10, F-E11, F-X5 |
| LLM vs deterministic logic | Rule baseline vs agent; deterministic verifier vs LLM judge | F-E2, F-E5 |
| Data workflow thinking | Telemetry generation -> store -> serve -> investigate -> score | section 5 |
| Fault injection | Fault catalog and scenario archetypes | F-D3..F-D9 |

---

## 3. Decision log

| ID | Decision | Status | Rationale / notes |
|---|---|---|---|
| D1 | The agent under test is an **open-source local model**, not Claude Code | DECIDED | Owner's choice. A weaker model also avoids saturating the benchmark, so tool and skill effects stay visible. Claude may still be used as a development helper. |
| D2 | Serve the model through a **local server** (Ollama now; llama.cpp `llama-server` possible), behind a small model-client interface | PROPOSED | Ollama 0.40.6 is installed and works. Its native `/api/chat` is used by the G0 runner because it reports timings. |
| D3 | Choose the model by **measurement (gate G0)**, from two families: (a) dense <=8B at 4-bit, fully in VRAM; (b) ~20-30B **MoE** with expert tensors offloaded to CPU RAM | PROPOSED | See section 4. Only `qwen2.5-coder:7b` is installed *and* tool-capable; a second candidate is still to be shortlisted by the owner. |
| D4 | **AirLLM** is an experiment (F-A9), not the default runtime | PROPOSED | Its 4 GB claim is about peak memory. The sources found publish no decode-speed numbers, and layer streaming repeats weight transfers per token. Measure before committing. |
| D5 | Telemetry source: simulator first, real OpenTelemetry Demo as a transfer test | OPEN | See table below. Aegis was assessed and needs a Kubernetes stack and has undocumented data schemas, so it is a reference, not a dependency. |
| D6 | Own **agent runtime** (loop, MCP client, skill loader) | PROPOSED | The open model lives outside Claude Code, and building the harness is the learning goal. |
| D7 | Tools sit behind a **backend-agnostic `TelemetryStore`** interface | PROPOSED | Same MCP tools can later point at the real demo's Prometheus/Jaeger/OpenSearch. |
| D8 | The final answer is submitted through a **`submit_answer` tool** with a schema | PROPOSED | Interacts with D14 (tool-call format policy). |
| D9 | **Read-only** tools only; no remediation | PROPOSED | Diagnosis and remediation are separate problems. |
| D10 | Stack: Python 3.12, pydantic v2 contracts, pytest, ruff, parquet via pyarrow | PROPOSED | Installed here: Python 3.12.8, `mcp` 1.9.1, `opentelemetry-sdk` 1.37, pandas, pyarrow, pydantic 2.11, requests, jsonschema. |
| D11 | Git: trunk-based, short branches, the two people review each other | PROPOSED | The folder is now a git repository (one commit so far). The `.gitignore` excludes `reference/`, `runs/`, `data/`. |
| D12 | Working mode: assistant is a mentor; code only on request | DECIDED | Owner's instruction. |
| D13 | **OpenTelemetry for agent runs and evaluation, phased.** P0: results table + artifact files. P1: each run recorded as a **trace tree** (`invoke_agent` > `chat` / `execute_tool`). P2: evaluation results as `gen_ai.evaluation.result` events on a separate `evaluate` trace linked to the run | DECIDED | Owner wants a trace tree to inspect a failing run. OpenTelemetry records; it does not score. The GenAI conventions are all in "Development" status and live in the `semantic-conventions-genai` repository, so attribute names are kept in one module and the version is pinned. |
| D14 | **Tool-call format policy:** (a) strict, only structured calls count; (b) recovered, bare JSON in the reply is parsed under documented rules, strict reported separately; (c) constrained, every turn is a JSON action enforced by the server's structured-output feature | OPEN | Pilot evidence (section 4): 7 of 7 tool calls were correct JSON written as plain text, which Ollama did not parse. Must be decided before the gate set is frozen. A parser that acts on any JSON must not fire on a quoted log line. |
| D15 | **Service and fault type are scored separately** (plus fault type given correct service, and a fault-type confusion matrix). Fault type is chosen from a **closed, diagnosis-level list** (with `unknown`) | DECIDED (scoring); PENDING (A) (vocabulary, and mapping from each injection to one diagnosis) | Separates "cannot locate" from "cannot explain". Injection names (`latency_injection`...) would leak how the data is made. |
| D16 | The agent receives only `reference_time` and `data_range`, **not** a baseline or incident window | DECIDED; AGREED with A on `reference_time` | The agent chooses its own baseline, so `query_metric` must accept the whole range at a coarse step. |
| D17 | **Evidence references:** short handles (`S3` span, `L12` log, `M4` metric, `T2` trace), cited as `query_id:handle`. `query_id` = hash of (dataset_id, tool_version, tool, canonical arguments that define the result set); `limit` and `cursor` excluded; 6+ hex chars; deterministic collision rule; handles numbered over the whole ordered result, not per page | DECIDED (B); PENDING (A) | The verifier recomputes the id from logged arguments and may re-run the logged call. |
| D18 | Model experiments run on **Person B's machine** (RTX 4050 6 GB, 24 GB RAM). Person A's machine (RTX 3050 4 GB, 16 GB) does non-GPU work | AGREED | Hardware is recorded in every run record; speeds from two machines are not comparable. |
| D19 | Question wording is **mixed** across faulty and healthy cases (two templates: alert, neutral report). A false-alarm alert must be backed by real data. `reference_time` follows the same distribution for faulty and healthy cases | AGREED (A proposed the mixing); details PENDING (A) | Question style must not reveal whether a fault exists. Test: template and `reference_time` cannot predict `no_fault`. |

### D5 — where the telemetry comes from (owner to decide)

| Option | Time to first usable data | Scenario volume | Realism | Main risk |
|---|---|---|---|---|
| A. Simulator (OTel SDK spans, virtual time) | Short once designed | Hundreds, seeded | Low-medium | "Works on my simulator" |
| B. Real OpenTelemetry Demo (Docker) | Hours: stack + backends + traffic | ~15 fixed flags, minutes each | High | Too few scenarios for statistics |
| C. A first, B as a transfer test | A first | A for volume, B for a small realism check | Both | More total work |

The assistant leans to C but the choice changes the two-person split, so it is the first decision to settle.
OpenTelemetry itself is the standard and SDKs that *produce* telemetry plus a Collector that routes it.
It does not store or query anything, so option B still needs backends (Prometheus, Jaeger, OpenSearch).

---

## 4. Constraints and feasibility (read this before promising scope)

### Hardware (measured on this machine)
RTX 4050 Laptop with 6 GB VRAM, 24 GB RAM, 16 logical CPUs, Docker limited to about 11.5 GB, Windows 11, about 67 GB free disk.

### What fits in 6 GB (rough rules of thumb, verify per model)
- An 8B-class model at 4-bit is roughly 5 GB of weights, which leaves little room for the KV cache.
  The KV cache is also VRAM: an 8B model with grouped-query attention uses on the order of 100+ KB per token
  (about 2 GB at 16k tokens in fp16). Expect a usable context of only a few thousand tokens in VRAM
  unless the cache is quantized or spilled. **Tool outputs must therefore be small.**
- A ~20B model does not fit in 6 GB. One calculator lists gpt-oss-20b at about 11-14 GB at 4-bit
  (21B parameters, 3.6B active). A mixture-of-experts model can still run with the expert tensors kept in CPU RAM;
  llama.cpp has flags for this (`--n-cpu-moe`, or `-ot ".ffn_.*_exps.=CPU"`). Unsloth's docs include a 6 GB worked example
  with a different MoE model at 28 tokens/s. That is someone else's number, not a prediction for this machine.
- **Why MoE matters here:** only the active parameters are computed per token, so a "20B-class" model can be usable
  without streaming weights from disk.

### AirLLM
It loads one layer at a time, so peak VRAM is about one layer. The sources found report that memory claim but no reproducible
tokens-per-second table, and note that cold layers cross storage and PCIe repeatedly during generation.
So for an agent that needs thousands of generated tokens per investigation, the feasibility question is purely about
throughput, and nobody has measured it for this machine. **That is experiment F-A9, run on 3 scenarios, after the main pipeline works.**

### Compute budget (use the formula, not the example)
```
runs            = scenarios x conditions x repeats
tokens_per_run  = steps x output_tokens_per_step          (prefill time is extra)
hours           = runs x tokens_per_run / tokens_per_second / 3600
```
Worked example with **assumed** numbers (replace them with gate-G0 measurements):
- 20 tok/s, 10 steps x 250 tokens = 2,500 tokens -> about 2 minutes of decoding per run, plus prefill.
- 10 scenarios x 3 conditions x 1 repeat = 30 runs -> about 1-2 hours of GPU time.
- If a method took 3 s/token (an assumption, not a measurement), 2,500 tokens = 2 hours per run, 30 runs = 60 hours.

Consequences:
1. **One GPU is a shared resource.** Runs serialize on Person B's machine (D18).
2. Today's experiment is small: roughly 10-15 scenarios x 3 conditions x 1 repeat. Repeats and larger suites are tomorrow.
3. Step and token budgets per run are first-class config, not afterthoughts.

### G0 pilot findings (exploratory, 2026-10-20)
Tooling: `evaluation/g0/` (stub tool schemas, 8 pilot cases, four-level grader, runner, 28 unit tests). Model: `qwen2.5-coder:7b`
(Q4_K_M, 7.6B parameters), temperature 0, seed 7, context 4096. **8 cases, one model, one seed: a first look, not a verdict.**

| Finding | Evidence | Consequence |
|---|---|---|
| Format, not understanding, caused most failures | 7 of 7 tool calls were correct JSON written into the reply text; Ollama did not parse them. Strict score 1/8; 6/8 if bare JSON is accepted | Decide D14 before freezing the gate set |
| Real decision errors exist underneath | "check latency" guessed a service instead of discovering one; "what does p95 mean?" triggered a `search_logs` call | Restraint and discovery need testing and probably a skill |
| It copied a 32-character trace id exactly and computed a relative time window correctly | cases p7, p3 | Short handles are likely fine; keep testing |
| The nine stub tool schemas cost most of ~2,000 prompt tokens | mean prompt 2,053, max 2,270 tokens, with a ~100-token system prompt | Half of the default 4,096 context is gone before any work. Keep tool descriptions short; track the tool-list token size as a number |
| Already spilling onto the CPU at the default context | `ollama ps`: 82% GPU / 18% CPU at 4096 | Usable context is the key number for tool-output caps (not yet measured) |
| Speed | mean 27 tokens/s generation on short outputs | Re-measure with long prompts and outputs |

### What "build the entire project today" realistically means
All **P0** features and a good part of **P1** are plausible for two people. **P2** and the real-demo adapter are not.
The estimates in section 8 are guesses and will be corrected after the first integration.

---

## 5. Architecture

```
            OFFLINE (Person A)                                   ONLINE (Person B)
 +--------------------------------+                 +-------------------------------------------+
 | Scenario generator             |                 | Agent runtime                             |
 |  seed -> faults, decoys,       |                 |  system prompt + skill index (Level 1)    |
 |  degradations, ground truth    |                 |  loop: model -> tool call -> result       |
 +---------------+----------------+                 |  limits: steps, tokens, wall time         |
                 |                                  |  tools: MCP tools + load_skill +          |
                 v                                  |         submit_answer                     |
 +--------------------------------+                 +----------+---------------+----------------+
 | Telemetry (OTel SDK spans,     |   public only               |               |
 | logs, metrics) -> parquet      +------------+                | MCP (stdio)   | local model API
 +--------------------------------+            v                v               v
 +--------------------------------+   +-----------------+  +-------------+  +------------------+
 | private/ ground truth (JSON)   |   | TelemetryStore  |<-+ MCP server  |  | Local model      |
 +----------------+---------------+   | (backend iface) |  | (read-only) |  | Ollama/llama.cpp |
                  |                   +-----------------+  +-------------+  +------------------+
                  |                                                  
                  |            +----------------------------------------------------------+
                  +----------->| Evaluation harness (Person B)                            |
                               |  validate answer schema -> score vs truth -> verify      |
                               |  evidence against the run's tool results -> aggregate    |
                               +----------------------------------------------------------+

 Three stores that never mix:  public/ (shop telemetry the agent may query)
                               runs/   (the agent's own run records and OpenTelemetry traces)
                               private/ (ground truth + evaluation traces and scores)
```

### Data workflow, stage by stage
| Stage | Input | Output | Owner | Failure to guard against |
|---|---|---|---|---|
| 1 Generate | seed, archetype | telemetry files + ground truth + manifest | A | label leakage into public files |
| 2 Store | telemetry files | queryable `TelemetryStore` | A | silent empty results |
| 3 Serve | store | MCP tools with bounded, typed output | A | context overflow, unvalidated queries |
| 4 Investigate | manifest question + tools + skills | run record (artifacts, later a trace tree) + submitted answer | B | malformed tool calls, loops, runaway cost |
| 5 Validate | answer | schema-valid answer or a counted error | B | accepting free-text guesses |
| 6 Score | answer + truth | metrics per run | B | circular evaluation |
| 7 Verify | answer + run record | evidence verdicts | B | fabricated IDs and numbers |
| 8 Aggregate | run records | tables, CIs, taxonomy | B | reporting one accuracy number |

### Agent runtime behaviour (spec)
- Loop: build messages -> call model -> parse tool call (policy D14) -> execute -> append bounded result -> repeat.
- Hard limits per run: `max_steps`, `max_tool_calls`, `max_context_tokens`, `max_wall_seconds`. Hitting a limit ends the run with a recorded `stop_reason`.
- Malformed tool call: one repair attempt (re-prompt with the validation error), then count a `tool_call_error` and continue or stop by policy. The gate measures the **first attempt**; "valid after repair" is reported separately.
- Tool results are truncated to a fixed token cap with an explicit `truncated: true` marker.
- Skills use progressive disclosure, as in the Agent Skills spec: Level 1 = name + description always in the system prompt; Level 2 = `SKILL.md` body returned by `load_skill`; Level 3 = files returned by `read_skill_file` when the skill says when to read them.
- Every run records enough to be replayed: per-step request and response artifacts, and (P1) a trace tree (C6).
- The model never sees ground truth, scenario ids with meaning, or archetype names.

---

## 6. Contracts (the interface between the two people)

Contracts live in `contracts/` as pydantic models plus JSON Schema exports, are versioned (`schema_version`),
and **any change needs both people to approve**. Everything else may change freely behind them.
Items marked **†** were proposed to Person A and are awaiting confirmation before v0.1 is frozen.

### C1 Scenario manifest (public)
`{id, question, reference_time, data_range{start,end}, source{type:"parquet"|"otel-demo", path|endpoints}, schema_version}`
- `question` has two templates (D19): an **alert** ("Alert fired at T: p95 latency of frontend 'OP' is X ms (normally about Y ms). Find the root cause.") and a **neutral report** ("A user reports that 'OP' felt slow or flaky around T. Is there a real problem in the system? If so, find the root cause; if not, say so."). The template is independent of whether a fault exists.
- It must contain no fault names, archetype names, or hints, and the word "incident" does not appear.
- Numbers in an alert must be consistent with the telemetry, also for false alarms.
- `reference_time` is the alert time or the reported time, in UTC. The manifest does **not** give baseline or incident windows (D16).

### C2 Telemetry schema (public)
| Table | Columns |
|---|---|
| spans | trace_id, span_id, parent_span_id, service, operation, start_ns, end_ns, duration_ms, status (OK/ERROR), status_message, attributes (JSON: service.version, app.region, ...) |
| logs | ts_ns, service, severity, body, trace_id (nullable), span_id (nullable) |
| metrics | ts_ns, service, operation (nullable), metric, value, unit |

Semantics to document and test: UTC; ISO-8601 with `Z` in files, integer nanoseconds in tables; IDs are lowercase hex;
metrics are computed from all requests *before* trace sampling; logs carry trace ids even when the trace itself was not sampled;
metric names are fixed (request_count, error_count, latency_p50/p95/p99_ms, cpu_utilization, memory_mb).
**† Aggregation rules:** buckets are start-inclusive, end-exclusive, aligned to the epoch; a bucket's timestamp is its start; a request belongs to a bucket by
its start time; latency is the server-side duration of that service's handler; **percentiles are not composable**, so the store keeps mergeable per-bucket
histograms (explicit bin bounds, like an OpenTelemetry histogram) and estimates a percentile for any window from them, documenting the bin bounds and the
worst-case error; error rate = sum(error_count) / sum(request_count), never an average of rates; gauges (cpu, memory) are offered as average **and** max;
a bucket with `request_count = 0` differs from a missing bucket (a gap, which raises a warning).
Fast-failing spans exist (a failing span can be shorter than a healthy one), so `find_traces` supports a status filter combined with a service filter.

### C3 Ground truth (private)
`{id, root_causes[{service, fault_type, role: primary|trigger, propagation_path, onset_time, end_time, scope}], affected_services, decoys[], no_fault, symptom, injection_mechanism, degradations, features, tier, generator_version, seed}`
- `fault_type` uses the closed diagnosis-level vocabulary (D15); `injection_mechanism` is private and may use simulator names.
- `propagation_path` is ordered (e.g. payment -> checkout -> frontend). `scope` is all / region / version / endpoint plus its value.
- **† Roles:** a *trigger* is harmless alone and harmful only because of the primary (flaky dependency + aggressive retries). Scorer credit: primary = full, trigger only = half, several primaries = recall.
- Leakage means exposing injected labels or ground truth; realistic diagnostic text (`OOMKilled`, `connection refused`) is allowed. **†** Test: forbidden terms (injected, fault, chaos, decoy, scenario, archetype, seed, ground truth) must not appear in any public text, attribute, file name or file metadata. Planted prompt-injection log lines are allowed adversarial content, not leakage. The MCP server and every tool must be unable to read `private/`; a test proves it.
- **†** A shortcut audit: a keyword rule such as "blame the service with the latest ERROR log" must score poorly, or the benchmark is gameable.

### C4 MCP tool contracts
Result envelope for every tool (compact columnar tables, `{"columns": [...], "rows": [[...]]}`):
```
{data, total_matches, returned, truncated, next_cursor, query_id,
 source{backend, dataset_id, tool_version}, warnings[{code, message}]}
```
"No matches" is a normal result (`total_matches = 0`); "query failed" is a separate typed error. Never return an empty result for a failed query.
Rules: explicit time range required; limits and defaults documented; validate service names, timestamps and limits; never accept free-form backend queries; read-only; deterministic.
Initial response cap: **1,500 tokens, provisional and configurable** until Person B reports the usable context of the chosen model.
Evidence references follow D17. Sort order must be total (e.g. start_ns, then span_id) so the same query always yields the same handles.
`query_metric` must accept the whole `data_range` at a coarse step (e.g. 60 s) so the agent can find the change point itself (D16).
Tool-list size matters: the nine stub schemas cost most of ~2,000 prompt tokens (section 4), so descriptions stay short and the token size of `tools/list` is reported.

| Tool | Purpose | Key parameters |
|---|---|---|
| `list_services` | services and telemetry available | window |
| `query_metric` | bounded time series + summary | service, metric, window, step, operation? |
| `compare_windows` | incident vs baseline change | service, metric, incident window, baseline window |
| `find_traces` | trace summaries matching filters | service?, operation?, window, status?, min_duration_ms?, region?, limit, cursor |
| `get_trace` | ordered span tree for one trace | trace_id |
| `breakdown` | grouped stats by an attribute | window, group_by (service/operation/status/version/region), metric |
| `search_logs` | capped, de-duplicated excerpts + counts | service?, window, severity?, contains?, trace_id?, limit, cursor |
| `get_dependencies` | observed caller->callee edges with rates | window |
| `check_coverage` | sampling rate, metric gaps, log-volume anomalies | window, service? |
| (agent-side) `load_skill`, `read_skill_file`, `submit_answer` | not MCP; provided by the runtime | |

The stand-in schemas used by the G0 test are in `evaluation/g0/stub_tools.py`. Person A owns the real definitions and should diff against them.

Open design question (discuss before building): should there also be a composite `get_overview` triage tool?
It would make the agent stronger and the benchmark weaker, because it embodies the rule baseline. Treat "primitive tools vs composite tools" as experiment E-TOOLS.

### C5 Answer schema (submitted via `submit_answer`) — draft, Person B to finalize
`{status: root_cause_found|inconclusive|no_problem, root_causes[{service, fault_type, region?, confidence, evidence}] (ranked), alternatives_considered[{hypothesis, why_rejected}], limitations[], next_check?}`
- `fault_type` is chosen from the closed vocabulary (D15) and scored separately from `service`.
- Still to decide (owner): confidence scale (categorical vs numeric), evidence as bare refs vs `{ref, claim}`, an optional `onset_estimate` (scored against the true onset), how an answer that fails the schema after repair is scored, and a cap on the number of causes.

### C6 Run record: artifacts now, OpenTelemetry trace tree next (D13)
**Phase 1 (P0):** per run, a folder of artifact files (per-step request and response, grading, timing) and one row in a results table.
The G0 runner already writes this shape (`runs/g0/<model>/iteration-N/<case>/...`).
**Phase 2 (P1):** the same information as spans, one trace per (scenario, condition, repeat), written by the OpenTelemetry SDK through a small file exporter (one JSON line per finished span).

| Span | Kind | Key attributes |
|---|---|---|
| `invoke_agent rca-investigator` (root) | INTERNAL | `gen_ai.operation.name=invoke_agent`, `gen_ai.agent.name`, `gen_ai.request.model`, `gen_ai.request.seed`, `gen_ai.request.temperature`, summed `gen_ai.usage.input_tokens` / `output_tokens`; ours: `rca.scenario_id`, `rca.condition`, `rca.suite_hash`, `rca.skill_versions`, `rca.tool_set_hash`, `rca.limits`, `rca.hardware`, `rca.git_sha`, `rca.stop_reason` |
| `chat {model}` | CLIENT | `gen_ai.operation.name=chat`, `gen_ai.provider.name`, `gen_ai.request.model`, `gen_ai.usage.*`, `gen_ai.response.finish_reasons`; ours: `rca.artifact` (path to the request/response files) |
| `execute_tool {name}` | INTERNAL | operation and tool-name attributes **to be verified against the specification** (the page was not fully read); ours: `rca.query_id`, `rca.result_tokens`, `rca.truncated`, `rca.total_matches`; `error.type` on failure |
| `skill.load {name}` | INTERNAL | `rca.skill`, `rca.skill_version`, `rca.level` |
| `validate_answer` | INTERNAL | `rca.schema_ok`, `rca.repair_attempts` |
| `evaluate` (a **separate trace** with a span **link** to the run trace) | INTERNAL | events `gen_ai.evaluation.result` with names `service_correct`, `fault_type_correct`, `abstention_correct`, `evidence_verified` (score value, label, explanation) |

Rules:
1. Spans hold structure, timing and counts. Prompts, responses and tool results stay in artifact files, referenced by `rca.artifact`.
2. A finished span cannot be changed, and scoring happens after the run, so evaluation results go on the separate linked `evaluate` trace.
3. Ground truth and scores never appear on any span of the run trace, and the three stores (`public/`, `runs/`, `private/`) never mix.
4. All attribute names live in one module (`observability/names.py`); the semantic-convention version is pinned, because everything is "Development".
5. Spans are read back with plain pandas; OpenTelemetry computes no metric.

---

## 7. Feature specification

Priority: **P0** = MVP today, **P1** = today if time allows, **P2** = later. Each feature has an acceptance criterion (AC).

### Data and faults (Person A)
| ID | P | Feature | AC |
|---|---|---|---|
| F-D1 | P0 | Topology of >=10 services with OTel-Demo names, 3 user-facing operations, critical vs non-critical edges | Diagram + test that a failure in a non-critical callee does not fail its caller |
| F-D2 | P0 | Telemetry generator emitting C2 via the real OTel SDK for spans | Same seed gives identical output; schema test passes |
| F-D3 | P0 | Fault catalog v1: latency, errors, CPU saturation, memory leak (sawtooth + restarts), dependency down, bad deploy | One signature test per fault (what it changes, what it must not change) |
| F-D4 | P0 | Ground truth + public/private split | Leakage test (C3): no truth term appears in `public/` |
| F-D5 | P0 | Archetypes: single fault, deep-dependency fault, healthy control, decoy-only false alarm | Generator produces each, with a symptom (or none) verified |
| F-D6 | P1 | Retry storm (cause + trigger), query amplification (N+1), region-scoped fault, dual fault | Each is invisible or misleading to the rule baseline by design; documented |
| F-D7 | P1 | Degraded observability: low trace sampling, metric gaps, log loss | `check_coverage` can detect each |
| F-D8 | P1 | Prompt-injection text planted in logs | Scored separately as an injection-robustness metric |
| F-D9 | P1 | Difficulty features and tiers; benchmark discrimination report; shortcut audit | Rule-baseline and keyword-baseline accuracy reported per tier; target headroom decided after seeing data |
| F-D10 | P2 | Real OpenTelemetry Demo adapter (transfer test) | Same MCP tools answer on the real stack |
| F-D11 | P1 | Versioned suite with fixed dev/test split decided *before* tuning | `suite.json` with hash recorded in every run |
| F-D12 | P0 | Shared reference set: 3 scenario bundles (slow payment, fast-failing error, healthy control) + a pagination example + a schema-only two-cause ground truth | Each with manifest, telemetry sample, private answer, tool response; used as contract-test fixtures |
| F-D13 | P1 | Question templates and distribution tests (D19) | Template and `reference_time` do not predict `no_fault` |

### MCP and store (Person A)
| ID | P | Feature | AC |
|---|---|---|---|
| F-M1 | P0 | `TelemetryStore` interface + parquet implementation, with mergeable histograms for latency | Unit tests; empty vs error distinguished; percentiles recomputable for any window |
| F-M2 | P0 | MCP server (stdio, official Python SDK) with `list_services`, `query_metric`, `find_traces`, `get_trace`, `search_logs` | Works from a plain MCP client with no LLM |
| F-M3 | P0 | Result envelope, caps, validation, typed errors, handles and `query_id` (D17) | Contract tests; no tool output exceeds its token cap; same query gives same handles |
| F-M4 | P1 | `compare_windows`, `breakdown`, `get_dependencies`, `check_coverage` | Golden-output tests |
| F-M5 | P1 | Tool output size benchmark, including the token size of `tools/list` | Report of tokens per tool call on real scenarios |
| F-M6 | P2 | E-TOOLS experiment support: composite `get_overview` behind a flag | Toggle without code change |

### Agent runtime (Person B)
| ID | P | Feature | AC |
|---|---|---|---|
| F-A1 | P0 | **Gate G0.** Pilot kit built (`evaluation/g0`, section 4). Remaining: decide D14, write and freeze the 30-case gate file, measure usable context and long-prompt speed, test a second model | Table of measured numbers, committed; thresholds untouched after measuring |
| F-A2 | P0 | Agent loop with hard limits and recorded stop reasons | Fake-model test covers every stop reason |
| F-A3 | P0 | MCP client (stdio) with tool discovery | Lists and calls tools against A's server or a stub |
| F-A4 | P0 | `submit_answer` with schema validation and one repair attempt | Invalid answers are counted, never silently fixed |
| F-A5 | P0 | **Run record (phase 1):** per-step artifact files + one results row per run | A run can be replayed from its artifacts alone |
| F-A6 | P1 | Skill loader: Level 1 index, `load_skill`, `read_skill_file` | Skill ablation switch works |
| F-A7 | P1 | Hypothesis scratchpad in state | Visible in the run record |
| F-A8 | P2 | Skeptic pass / sub-agents | Only if it beats the single agent |
| F-A9 | P2 | AirLLM throughput experiment on 3 scenarios | Measured tokens/s and feasibility verdict |
| F-A10 | P1 | **Run trace (phase 2, D13):** instrument the loop with the OpenTelemetry SDK; `invoke_agent` root, `chat` / `execute_tool` / `skill.load` / `validate_answer` children; file exporter | Trace tree readable for any run; names in one module; no ground truth on any span |
| F-A11 | P0 | Tool-call format policy implemented as decided in D14, with strict and recovered rates both reported | Quoted JSON in a model's text never triggers a call (test) |

### Skills (Person B writes, Person A reviews domain correctness)
| ID | P | Feature | AC |
|---|---|---|---|
| F-S1 | P1 | `investigate-latency` | Meets the spec checks below; ablation run |
| F-S2 | P1 | `investigate-error-spike` | Same |
| F-S3 | P2 | `correlate-dependency` | Same |
| F-S4 | P1 | Skill lint script: valid frontmatter, description says what + when, body < 500 lines | Runs in the test suite |
| F-S5 | P1 | Gotchas come from observed failures only | Each gotcha links to a failing run id |

Skill authoring rules (from the Agent Skills best-practice guides): start from real failures not generic advice;
add only what the model would get wrong without it; give a default rather than a menu; keep a gotchas section;
use a validation loop; test with and without the skill and keep it only if it helps.
A weak local model needs shorter, more prescriptive skills than a frontier model: this is a finding to measure, not assume.
Skill evaluation follows the Agent Skills evaluation guide: test cases with expected output, assertions added after the first outputs,
with/without comparison in `iteration-N/` folders with `timing.json`, and human review of transcripts.

### Evaluation (Person B)
| ID | P | Feature | AC |
|---|---|---|---|
| F-E1 | P0 | Scorer: service top-1/top-3, **fault type scored separately**, fault type given correct service, recall of primaries, abstention, false positives on healthy cases, fault-type confusion matrix | Unit tests with hand-made answers |
| F-E2 | P0 | Rule-based baseline | Reproducible numbers per archetype |
| F-E3 | P0 | Experiment runner: conditions x scenarios x repeats, resumable, results table | Interrupt and resume loses nothing |
| F-E4 | P0 | Results table with per-archetype and per-tier breakdown | Generated by one command |
| F-E5 | P1 | **Evidence verifier**: every cited `query_id:handle` must exist in the run's tool results and match | Deterministic, no LLM; may re-run the logged call |
| F-E6 | P1 | Calibration: confidence vs correctness; abstention quality | Reliability table |
| F-E7 | P1 | Process metrics: baseline compared, alternatives checked, tool errors, steps | Computed from the run record / trace |
| F-E8 | P1 | Paired comparison: bootstrap CIs, McNemar on per-scenario outcomes | Reported with N |
| F-E9 | P1 | Failure taxonomy labelling sheet | >=10 labelled failures |
| F-E10 | P2 | LLM judge for reasoning quality | Only if validated against human labels |
| F-E11 | P2 | **Evaluation events (D13):** emit `gen_ai.evaluation.result` on a separate `evaluate` trace linked to the run trace | Scores for service, fault type, abstention, evidence on every run; stored outside every agent-visible store |

### Engineering (both)
| ID | P | Feature | AC |
|---|---|---|---|
| F-X1 | P0 | Repo skeleton, `pyproject.toml`, ruff, pytest, pinned dependencies | `python -m pytest` green (done for G0: 28 tests) |
| F-X2 | P0 | `contracts/` package with versioned schemas | Both approve changes |
| F-X3 | P0 | Config files (YAML) for model, limits, suite, conditions | No magic numbers in code |
| F-X4 | P1 | Decision records in `docs/decisions/` | One file per decision |
| F-X5 | P2 | Trace tree viewer for a run (CLI first) | A human can follow a failing run in under a minute |
| F-X6 | P0 | README with a one-command reproduction | A fresh clone reproduces one run |

---

## 8. Two-person split

### Ownership
| | Person A: Environment, data, MCP | Person B: Agent, skills, evaluation |
|---|---|---|
| Owns | scenario generator, telemetry, ground truth, `TelemetryStore`, MCP server | model serving + gate G0, agent runtime, skills, scorer, verifier, run tracing, experiments, reports |
| Publishes | the shared reference set (F-D12) first, then the suite | `FakeModel` and a stub MCP client so A can test end to end |
| Is blocked by | only the contracts | only the contracts (works against hand-made fixtures until A's arrive) |
| Reviews | B's skills for domain correctness | A's tools for how a model actually uses them |

The only coupling is **C1-C6 plus the MCP protocol**. Either person can be stubbed by the other, so neither waits.
Until A's reference set exists, B tests against tiny hand-made fixtures. The stub must match what A builds, which is why the contracts are frozen first.

### Collaboration rules
- Contract changes: pull request touching `contracts/` needs both approvals.
- Small branches, merged within the day; the other person reviews.
- One shared decision log. If it is not in the log, it was not decided.
- GPU: experiments run on Person B's machine (D18); runs are queued.

### Plan for today (durations are the assistant's guesses; correct them after block 2)
| Block | Who | Content | Exit condition |
|---|---|---|---|
| 0 | both | Settle D5, D14, D15 vocabulary; confirm the pending † items; freeze C1-C6 v0.1; repo skeleton | Contracts committed, both can explain the data workflow |
| 1 | A | F-D1..D5, F-D12, F-M1 | Reference set readable through `TelemetryStore` |
| 1 | B | F-A1 (finish G0), F-A2, F-A4, F-A5, F-A11 against a stub | A model is chosen by measured numbers; fake-model run completes |
| 2 | A | F-M2, F-M3 (then F-M4) | Plain MCP client can call every P0 tool |
| 2 | B | F-A3, F-E1, F-E2, F-A6 | Agent completes one real scenario end to end |
| 3 | both | Integration run on 3 scenarios; fix what breaks; first rule-baseline table | First end-to-end row in the results table |
| 3b | B | F-A10 run traces on the working loop | A failing run can be read as a trace tree |
| 4 | A | F-D6, F-D7 (hard scenarios), F-D9, F-D13 | Baseline-vs-benchmark discrimination report |
| 4 | B | F-E3, F-E4, F-E5, skills F-S1 | Conditions matrix runnable |
| 5 | both | Experiment: conditions x 10-15 scenarios; failure taxonomy; README | Results table + taxonomy + reproduction steps |

Expect the GPU, not typing speed, to be the bottleneck in blocks 3 and 5.

---

## 9. Evaluation plan

### Conditions (ablation)
| Cond | Model | Tools | Skills | Purpose |
|---|---|---|---|---|
| C0 | none | rule baseline | none | floor |
| C1 | local model | primitive MCP tools | none | what tools alone buy |
| C2 | local model | primitive MCP tools | skills | what procedure adds |
| C3 | local model | primitive tools | skills + evidence-check step | what verification adds |
| (E-TOOLS) | same | composite `get_overview` | same | tool abstraction level |
| (E-MODEL) | second model | same | same | model effect |

### Metrics
Service accuracy (top-1, top-3, recall for multi-fault); **fault-type accuracy, reported separately** and conditional on the right service; scope accuracy;
evidence correctness and unsupported-claim rate (from the verifier); abstention quality and false-positive rate on healthy and decoy-only cases;
calibration; tool-call error rate (strict and recovered); steps and tokens; wall time; injection robustness; run-to-run consistency when repeated.
Never report a single accuracy number.

### Statistics
Per-scenario paired outcomes; bootstrap confidence intervals; state N every time; no claim of improvement when intervals overlap heavily.
Dev/test split fixed before tuning; skills and prompts are tuned on dev only; test is run once per condition.
For small gates, report the Wilson interval (27/30 passes is consistent with a true rate of roughly 74%-97%).

### Threats to validity (write these in the README)
Simulator realism; fault names appearing in log text; the model having memorized OpenTelemetry-Demo fault scenarios;
small N; one machine and one quantization; prompt sensitivity; decoys that are easier or harder than real ones;
rejection sampling that favours detectable faults; question style leaking whether a fault exists.

---

## 10. Engineering practices

### Repository layout (target)
```
THE HARNESS/
  PROJECT_CONTEXT.md
  README.md
  pyproject.toml            pytest + ruff config
  requirements.txt          pinned dependencies
  contracts/                pydantic models + exported JSON Schemas (versioned)
  configs/                  model.yaml, limits.yaml, suite.yaml, conditions.yaml
  telemetry/                generator, faults, scenarios            (Person A)
  store/                    TelemetryStore interface + parquet impl (Person A)
  mcp_servers/telemetry/    MCP server                              (Person A)
  agent/                    runtime, model client, MCP client, skill loader (Person B)
  observability/            names.py (all attribute names), file exporter, tracing helpers (Person B)
  skills/                   one folder per skill with SKILL.md      (Person B)
  evaluation/               g0/ (built), scorer, verifier, baselines, runner, reports (Person B)
  tests/                    unit/, contract/, integration/, golden/
  docs/decisions/           one decision record per file
  data/                     generated, gitignored; suite hash recorded
  runs/                     run records and traces, gitignored
  reference/                read-only prototype, gitignored, not imported
```

### Conventions
- Contracts first: write the pydantic model and a test before the code that uses it.
- Determinism: every random choice flows from an explicit seed; independent random streams for independent concerns.
- Type hints everywhere, `ruff` for lint and format, small modules, no hidden global state.
- Configuration in YAML, never hard-coded; no secrets in the repo.
- Every run record stores: model name + quantization + server version, seed, sampling settings, suite hash, skill versions, tool-set hash, git sha, limits, hardware.
- Run records are artifact files plus (P1) OpenTelemetry spans; results are a table; humans read them through a viewer (D13).
- Pre-registered thresholds are named constants that only apply to a frozen "gate" case file; pilot files never produce a verdict.
- Failures are typed and counted, never swallowed.

### Test strategy
| Layer | What it proves |
|---|---|
| Unit | each fault's signature; scorer logic; verifier logic; the G0 grader |
| Contract | MCP tool schemas and size caps; manifest has no leakage; handles are stable |
| Integration | agent + fake model + real MCP server completes a run |
| Golden | recorded tool outputs for fixed scenarios do not drift |
| Benchmark-quality | rule baseline and keyword baseline per tier (does the benchmark discriminate?) |

### Definition of done for a feature
Acceptance criterion met; tests added; contract unchanged or approved; documented in the README or decision log;
reviewed by the other person; no new magic numbers.

---

## 11. Gates and mentor checkpoints

### Go/no-go gates (thresholds are fixed *before* measuring)
| Gate | Question | Rule |
|---|---|---|
| G0 | Can the model call tools reliably enough to build on? | **DECIDED:** a call is valid only if it passes all four levels (parseable, existing tool, schema-valid, semantically sensible); a correct decision not to call counts as success. Pass if **>= 90% (27/30)** of the frozen gate prompts pass **and** there are **zero invalid tool names**. First attempt only. The threshold is not changed after seeing results. The Wilson interval is reported. What "parseable" means depends on D14 |
| G1 | Does the benchmark discriminate? | Rule baseline is clearly below 100% on the hard tier; headroom number agreed after seeing data |
| G2 | Does one scenario run end to end? | Valid submitted answer + complete run record |
| G3 | Does the experiment fit the GPU budget? | Projected hours from the formula in section 4 <= the time left |

### Questions the owner should be able to answer before each component is built
- **Data:** What exactly makes a fault "root cause" versus "symptom" in the call graph? How could a model cheat from the data alone? What would make a healthy control unfair?
- **MCP:** What is the maximum useful output of one tool call for a model with a few thousand tokens of context? When does a tool leak the answer? What should happen when the filter matches nothing?
- **Agent:** What stops an infinite loop? What does the loop do with a malformed tool call, and why is that a metric rather than a bug? What does the model need to remember across steps, and where does it live? What rule stops a quoted JSON log line from being mistaken for a tool call?
- **Skills:** What would the model get wrong without this skill? How will you know the skill helped, and what result would make you delete it?
- **Evaluation:** Why is "accuracy" not enough? What is the null hypothesis for the skill comparison? Which numbers are tuned on dev and which are untouched? Why does the evaluation result live on a separate trace rather than on the run's own span?

---

## 12. Scope

**In the MVP (today):** all P0, plus as many P1 as the GPU budget allows: at least 3 conditions on 10-15 scenarios, a rule baseline, a verifier or a manual evidence check, run traces, and a labelled failure sample.

**Not today:** real OpenTelemetry-Demo adapter (F-D10), sub-agents (F-A8), LLM judge (F-E10), evaluation events and a viewer (F-E11, F-X5), remediation, any production claim.

---

## 13. Open questions for the owner

1. **D14:** strict, recovered or constrained tool-call format? This blocks freezing the gate file.
2. **D5:** simulator first, real demo, or both?
3. **D3:** which second tool-capable model should be tried? (Shortlist from the Ollama tools list; the assistant will check details and ask before any download.)
4. **C5:** confidence scale, evidence as refs or `{ref, claim}`, `onset_estimate`, scoring of invalid answers, cap on causes.
5. **agent-eval-lab:** embed this project into it, or keep them separate with the lab as a later consumer?
6. **Ceiling reference:** may one frontier-model run be used purely to calibrate how hard the benchmark is, never as the system under test?
7. **The one sentence** you want to be able to say when this is finished.

Answered since v2: roles (owner is Person B), GPU (D18), git (repository exists), windows and references (D16, D17), scoring (D15), OpenTelemetry scope (D13).

---

## 14. About `reference/prototype_v0`
A throwaway simulator and rule baseline written before this spec. Facts that carry over: the first fault set was too easy
(rule baseline 85% top-1 on 24 scenarios), and harder failure types were sketched but not tested. Details in `reference/README.md`.

## 15. Change log
- **v2 -> v2.1 (2026-10-20):** added D13-D19; recorded the G0 pilot findings (section 4); rewrote C1, C3, C4, C5 and C6 to match what was agreed with Person A;
  C6 is now the run record and trace schema instead of a JSONL log; added F-A10, F-A11, F-E11, F-D12, F-D13 and updated F-A1, F-A5, F-E1, F-M1, F-M3, F-X5;
  replaced the generic G0 rule with the owner's pre-registered rule; refreshed open questions. No program code changed in this edit.

## Sources checked on 2026-10-20
- AirLLM mechanism and caveats: [DEV Community article](https://dev.to/arshtechpro/airllm-runs-a-70b-model-on-a-4gb-gpu-its-true-and-thats-not-the-interesting-part-hha), [Wavect analysis](https://wavect.io/blog/airllm-layer-wise-inference-low-vram/)
- gpt-oss-20b memory figures and MoE offload flags: [Unsloth gpt-oss docs](https://docs.unsloth.ai/basics/gpt-oss), [canirun.ai](https://canirun.ai/model/gpt-oss-20b/)
- Aegis RCA platform: [OperationsPAI/aegis](https://github.com/OperationsPAI/aegis), cold-start guide and RCA user guide in that repository
- Agent Skills: [best practices](https://agentskills.io/skill-creation/best-practices), [evaluating skills](https://agentskills.io/skill-creation/evaluating-skills), [overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- OpenTelemetry Demo and feature flags: [demo docs](https://opentelemetry.io/docs/demo/), [feature flags](https://opentelemetry.io/docs/demo/feature-flags/)
- OpenTelemetry GenAI semantic conventions (status: Development; moved repository): [semantic-conventions-genai](https://github.com/open-telemetry/semantic-conventions-genai) — agent spans, client inference spans and the `gen_ai.evaluation.result` event were read; the tool-execution span, MCP and metrics pages were not
- Ollama tool-capable model list: [ollama.com/search?c=tools](https://ollama.com/search?c=tools)
