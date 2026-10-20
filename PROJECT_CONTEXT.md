# OTel Root-Cause Investigator — Project Context v2

**Status:** living design document, v2 (supersedes the v1 brief on the Desktop, which is left untouched)
**Date:** 2026-10-20
**Working mode:** mentor mode. No code is written until the owner says so. Decisions below are marked
`DECIDED` (owner said so), `PROPOSED` (assistant recommendation awaiting a yes/no) or `OPEN` (needs an answer).

---

## 1. What the project is

### One-paragraph definition
A local, read-only **LLM investigator** that diagnoses incidents in a microservice application from
telemetry (traces, metrics, logs). It reaches the telemetry through **MCP tools**, follows
**Agent Skills** (reusable investigation procedures), runs on a **small open-source model on a consumer GPU**,
and is judged by an **evaluation harness** that knows the injected ground truth. The harness measures
correctness, evidence grounding, calibration/abstention, robustness (decoys, missing telemetry,
prompt injection) and cost.

### The research question (this is what makes it more than a demo)
> On a 6 GB GPU with a small open model, how much of the investigation quality comes from
> **the model**, how much from **tool design (MCP)**, and how much from **procedure (Skills)**?
> Which failure modes survive all three?

Everything is built so that this can be answered by a controlled ablation: model x tools x skills.

### What it is not
- Not a production SRE product and not a novelty claim (Datadog, Dynatrace and the Aegis benchmark exist).
- Not remediation: every tool is read-only.
- Not evidence about real production systems. Results are about a controlled lab.

### Success criteria for the MVP (today)
1. One command runs the full pipeline: scenario -> agent -> validated answer -> score -> results table.
2. At least 3 conditions compared with numbers on a fixed, versioned scenario set.
3. Every run leaves a complete, replayable trajectory log.
4. A written failure taxonomy of the agent's mistakes, with examples.
5. A new developer can reproduce a run from the README.

---

## 2. Learning goals mapped to where they are learned

| Goal (from the owner) | Where it is practised | Feature IDs |
|---|---|---|
| Understand agent architecture, not a black box | Own agent loop: state, limits, tool-call parsing, stop rules | F-A2..F-A7 |
| Write MCP servers | Telemetry MCP server with bounded, validated, read-only tools | F-M1..F-M6 |
| Write effective Agent Skills | 3 investigation skills, with/without ablation, gotchas from real failures | F-S1..F-S5 |
| Evaluate output (correctness, grounding, hallucination, tool errors) | Scorer, evidence verifier, calibration, failure taxonomy | F-E1..F-E10 |
| Observability of agent runs | Trajectory JSONL, replay, trace viewer | F-A5, F-X5 |
| LLM vs deterministic logic | Rule baseline vs agent; deterministic verifier vs LLM judge | F-E2, F-E5 |
| Data workflow thinking | Telemetry generation -> store -> serve -> investigate -> score | section 5 |
| Fault injection | Fault catalog and scenario archetypes | F-D3..F-D9 |

---

## 3. Decision log

| ID | Decision | Status | Rationale / notes |
|---|---|---|---|
| D1 | The agent under test is an **open-source local model**, not Claude Code | DECIDED | Owner's choice. A weaker model also avoids saturating the benchmark, so tool and skill effects stay visible. Claude may still be used as a development helper. |
| D2 | Serve the model through an **OpenAI-compatible local server** (Ollama or llama.cpp `llama-server`) | PROPOSED | Standard interface, tool-calling support, easy to swap models. |
| D3 | Choose the model by **measurement (gate G0)**, from two families: (a) dense <=8B at 4-bit, fully in VRAM; (b) ~20-30B **MoE** with expert tensors offloaded to CPU RAM | PROPOSED | See section 4. Names are from memory; verify what is current before testing. |
| D4 | **AirLLM** is an experiment (F-A9), not the default runtime | PROPOSED | Its 4 GB claim is about peak memory. The sources found publish no decode-speed numbers, and layer streaming repeats weight transfers per token. Measure before committing. |
| D5 | Telemetry source: simulator first, real OpenTelemetry Demo as a transfer test | OPEN | See table below. |
| D6 | Own **agent runtime** (loop, MCP client, skill loader) | PROPOSED | The open model lives outside Claude Code, and building the harness is the learning goal. |
| D7 | Tools sit behind a **backend-agnostic `TelemetryStore`** interface | PROPOSED | Same MCP tools can later point at the real demo's Prometheus/Jaeger/OpenSearch. |
| D8 | The final answer is submitted through a **`submit_answer` tool** with a schema | PROPOSED | Weak models parse structured tool calls better than free text. |
| D9 | **Read-only** tools only; no remediation | PROPOSED | Diagnosis and remediation are separate problems. |
| D10 | Stack: Python 3.12, pydantic v2 contracts, pytest, ruff, parquet via pyarrow | PROPOSED | Already installed on this machine: Python 3.12.8, `mcp` 1.9.1, `opentelemetry-sdk` 1.37, pandas, pyarrow, pydantic 2.11. |
| D11 | `git init` in THE HARNESS; trunk-based, short branches, the two people review each other | OPEN | Needs the owner's yes. |
| D12 | Working mode: assistant is a mentor; code only on request | DECIDED | Owner's instruction. |

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
RTX 4050 with 6 GB VRAM, 24 GB RAM, 16 logical CPUs, Docker limited to about 11.5 GB, Windows 11.

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
1. **One GPU is a shared resource.** Runs serialize. The two people must agree who runs experiments (OPEN Q4).
2. Today's experiment is small: roughly 10-15 scenarios x 3 conditions x 1 repeat. Repeats and larger suites are tomorrow.
3. Step and token budgets per run are first-class config, not afterthoughts.

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
 | logs, metrics) -> parquet      +------------+                | MCP (stdio)   | OpenAI-compatible API
 +--------------------------------+            v                v               v
 +--------------------------------+   +-----------------+  +-------------+  +------------------+
 | private/ ground truth (JSON)   |   | TelemetryStore  |<-+ MCP server  |  | Local model      |
 +----------------+---------------+   | (backend iface) |  | (read-only) |  | Ollama/llama.cpp |
                  |                   +-----------------+  +-------------+  +------------------+
                  |                                                  
                  |            +----------------------------------------------------------+
                  +----------->| Evaluation harness (Person B)                            |
                               |  validate answer schema -> score vs truth -> verify      |
                               |  evidence against the tool-call log -> aggregate -> report|
                               +----------------------------------------------------------+
```

### Data workflow, stage by stage
| Stage | Input | Output | Owner | Failure to guard against |
|---|---|---|---|---|
| 1 Generate | seed, archetype | telemetry files + ground truth + manifest | A | label leakage into public files |
| 2 Store | telemetry files | queryable `TelemetryStore` | A | silent empty results |
| 3 Serve | store | MCP tools with bounded, typed output | A | context overflow, unvalidated queries |
| 4 Investigate | manifest question + tools + skills | trajectory + submitted answer | B | malformed tool calls, loops, runaway cost |
| 5 Validate | answer | schema-valid answer or a counted error | B | accepting free-text guesses |
| 6 Score | answer + truth | metrics per run | B | circular evaluation |
| 7 Verify | answer + tool-call log | evidence verdicts | B | fabricated IDs and numbers |
| 8 Aggregate | run records | tables, CIs, taxonomy | B | reporting one accuracy number |

### Agent runtime behaviour (spec)
- Loop: build messages -> call model -> parse tool call -> execute -> append bounded result -> repeat.
- Hard limits per run: `max_steps`, `max_tool_calls`, `max_context_tokens`, `max_wall_seconds`. Hitting a limit ends the run with a recorded `stop_reason`.
- Malformed tool call: one repair attempt (re-prompt with the validation error), then count a `tool_call_error` and continue or stop by policy.
- Tool results are truncated to a fixed token cap with an explicit `truncated: true` marker.
- Skills use progressive disclosure, as in the Agent Skills spec: Level 1 = name + description always in the system prompt; Level 2 = `SKILL.md` body returned by `load_skill`; Level 3 = files returned by `read_skill_file` when the skill says when to read them.
- The model never sees ground truth, scenario ids with meaning, or archetype names.

---

## 6. Contracts (the interface between the two people)

Contracts live in `contracts/` as pydantic models plus JSON Schema exports, are versioned (`schema_version`),
and **any change needs both people to approve**. Everything else may change freely behind them.

### C1 Scenario manifest (public)
`{id, question, data_range{start,end}, source{type:"parquet"|"otel-demo", path|endpoints}, schema_version}`
It must contain no fault names, archetype names, or hints.

### C2 Telemetry schema (public)
| Table | Columns |
|---|---|
| spans | trace_id, span_id, parent_span_id, service, operation, start_ns, end_ns, duration_ms, status (OK/ERROR), status_message, attributes (JSON: service.version, app.region, ...) |
| logs | ts_ns, service, severity, body, trace_id (nullable), span_id (nullable) |
| metrics | ts_ns, service, operation (nullable), metric, value, unit |

Semantics to document and test: UTC nanoseconds; IDs are lowercase hex; metrics are computed from all requests *before* trace sampling;
logs carry trace ids even when the trace itself was not sampled; metric names are fixed (request_count, error_count, latency_p50/p95/p99_ms, cpu_utilization, memory_mb).

### C3 Ground truth (private)
`{id, root_causes[{service, fault_type, role: primary|trigger, onset, end, scope}], decoys[], no_fault, symptom, degradations, features, tier, generator_version, seed}`

### C4 MCP tool contracts
Result envelope for every tool: `{data, total_matches, truncated, query_id, source, warnings[]}`.
Rules: explicit time range required; limits and defaults documented; validate service names, timestamps and limits;
distinguish "no matches" from "query failed"; never accept free-form backend queries; read-only.

| Tool | Purpose | Key parameters |
|---|---|---|
| `list_services` | services and telemetry available | window |
| `query_metric` | bounded time series + summary | service, metric, window, step, operation? |
| `compare_windows` | incident vs baseline change | service, metric, incident window, baseline window |
| `find_traces` | trace summaries matching filters | service?, operation?, window, status?, min_duration_ms?, attribute filter?, limit |
| `get_trace` | ordered span tree for one trace | trace_id |
| `breakdown` | grouped stats by an attribute | window, group_by (service/operation/status/version/region), metric |
| `search_logs` | capped, de-duplicated excerpts + counts | service?, window, severity?, contains?, trace_id?, limit |
| `get_dependencies` | observed caller->callee edges with rates | window |
| `check_coverage` | sampling rate, metric gaps, log-volume anomalies | window, service? |
| (agent-side) `load_skill`, `read_skill_file`, `submit_answer` | not MCP; provided by the runtime | |

Open design question (discuss before building): should there also be a composite `get_overview` triage tool?
It would make the agent stronger and the benchmark weaker, because it embodies the rule baseline. Treat "primitive tools vs composite tools" as experiment E-TOOLS.

### C5 Answer schema (submitted via `submit_answer`)
`{status: root_cause_found|inconclusive|no_problem, root_causes[{service, fault_type?, region?, confidence: low|medium|high, evidence_ids[]}] (ranked), alternatives_considered[{hypothesis, why_rejected}], limitations[], next_check?}`

### C6 Trajectory log (JSONL, one object per event)
Events: `run_start` (model name + quantization + server version, seed, suite hash, skill versions, tool-set hash, git sha, limits),
`model_call` (tokens in/out, latency), `tool_call`, `tool_result` (size, truncated), `skill_load`, `error` (typed), `final_answer`, `run_end` (stop_reason).

---

## 7. Feature specification

Priority: **P0** = MVP today, **P1** = today if time allows, **P2** = later. Each feature has an acceptance criterion (AC).

### Data and faults (Person A)
| ID | P | Feature | AC |
|---|---|---|---|
| F-D1 | P0 | Topology of >=10 services with OTel-Demo names, 3 user-facing operations, critical vs non-critical edges | Diagram + test that a failure in a non-critical callee does not fail its caller |
| F-D2 | P0 | Telemetry generator emitting C2 via the real OTel SDK for spans | Same seed gives identical output; schema test passes |
| F-D3 | P0 | Fault catalog v1: latency, errors, CPU saturation, memory leak (sawtooth + restarts), dependency down, bad deploy | One signature test per fault (what it changes, what it must not change) |
| F-D4 | P0 | Ground truth + public/private split | Leakage test: no truth term appears in `public/` |
| F-D5 | P0 | Archetypes: single fault, deep-dependency fault, healthy control, decoy-only false alarm | Generator produces each, with a symptom (or none) verified |
| F-D6 | P1 | Retry storm (cause + trigger), query amplification (N+1), region-scoped fault, dual fault | Each is invisible or misleading to the rule baseline by design; documented |
| F-D7 | P1 | Degraded observability: low trace sampling, metric gaps, log loss | `check_coverage` can detect each |
| F-D8 | P1 | Prompt-injection text planted in logs | Scored separately as an injection-robustness metric |
| F-D9 | P1 | Difficulty features and tiers; benchmark discrimination report | Rule-baseline accuracy reported per tier; target headroom decided after seeing data |
| F-D10 | P2 | Real OpenTelemetry Demo adapter (transfer test) | Same MCP tools answer on the real stack |
| F-D11 | P1 | Versioned suite with fixed dev/test split decided *before* tuning | `suite.json` with hash recorded in every run |

### MCP and store (Person A)
| ID | P | Feature | AC |
|---|---|---|---|
| F-M1 | P0 | `TelemetryStore` interface + parquet implementation | Unit tests; empty vs error distinguished |
| F-M2 | P0 | MCP server (stdio, official Python SDK) with `list_services`, `query_metric`, `find_traces`, `get_trace`, `search_logs` | Works from a plain MCP client with no LLM |
| F-M3 | P0 | Result envelope, caps, validation, typed errors | Contract tests; no tool output exceeds its token cap |
| F-M4 | P1 | `compare_windows`, `breakdown`, `get_dependencies`, `check_coverage` | Golden-output tests |
| F-M5 | P1 | Tool output size benchmark | Report of tokens per tool call on real scenarios |
| F-M6 | P2 | E-TOOLS experiment support: composite `get_overview` behind a flag | Toggle without code change |

### Agent runtime (Person B)
| ID | P | Feature | AC |
|---|---|---|---|
| F-A1 | P0 | **Gate G0** script: tool-call validity rate, tokens/s, max usable context for each candidate model | Table of measured numbers, committed |
| F-A2 | P0 | Agent loop with hard limits and recorded stop reasons | Fake-model test covers every stop reason |
| F-A3 | P0 | MCP client (stdio) with tool discovery | Lists and calls tools against A's server or a stub |
| F-A4 | P0 | `submit_answer` with schema validation and one repair attempt | Invalid answers are counted, never silently fixed |
| F-A5 | P0 | Trajectory logging (C6) | A run can be replayed from its log alone |
| F-A6 | P1 | Skill loader: Level 1 index, `load_skill`, `read_skill_file` | Skill ablation switch works |
| F-A7 | P1 | Hypothesis scratchpad in state | Visible in the log |
| F-A8 | P2 | Skeptic pass / sub-agents | Only if it beats the single agent |
| F-A9 | P2 | AirLLM throughput experiment on 3 scenarios | Measured tokens/s and feasibility verdict |

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

### Evaluation (Person B)
| ID | P | Feature | AC |
|---|---|---|---|
| F-E1 | P0 | Scorer: top-1/top-3 service, recall of primaries, abstention, false positives on healthy cases | Unit tests with hand-made answers |
| F-E2 | P0 | Rule-based baseline | Reproducible numbers per archetype |
| F-E3 | P0 | Experiment runner: conditions x scenarios x repeats, resumable, JSONL results | Interrupt and resume loses nothing |
| F-E4 | P0 | Results table with per-archetype and per-tier breakdown | Generated by one command |
| F-E5 | P1 | **Evidence verifier**: every cited id/number must exist in the tool-call log and match | Deterministic, no LLM |
| F-E6 | P1 | Calibration: confidence vs correctness; abstention quality | Reliability table |
| F-E7 | P1 | Process metrics: baseline compared, alternatives checked, tool errors, steps | Computed from trajectory |
| F-E8 | P1 | Paired comparison: bootstrap CIs, McNemar on per-scenario outcomes | Reported with N |
| F-E9 | P1 | Failure taxonomy labelling sheet | >=10 labelled failures |
| F-E10 | P2 | LLM judge for reasoning quality | Only if validated against human labels |

### Engineering (both)
| ID | P | Feature | AC |
|---|---|---|---|
| F-X1 | P0 | Repo skeleton, `pyproject.toml`, ruff, pytest, pinned dependencies | `make test` (or equivalent) green |
| F-X2 | P0 | `contracts/` package with versioned schemas | Both approve changes |
| F-X3 | P0 | Config files (YAML) for model, limits, suite, conditions | No magic numbers in code |
| F-X4 | P1 | Decision records in `docs/decisions/` | One file per decision |
| F-X5 | P1 | Trace viewer for a trajectory (CLI or HTML) | Human can follow a run |
| F-X6 | P0 | README with a one-command reproduction | A fresh clone reproduces one run |

---

## 8. Two-person split

### Ownership
| | Person A: Environment, data, MCP | Person B: Agent, skills, evaluation |
|---|---|---|
| Owns | scenario generator, telemetry, ground truth, `TelemetryStore`, MCP server | model serving + gate G0, agent runtime, skills, scorer, verifier, experiments, reports |
| Publishes | `fixtures/` (3 sample scenarios) in the first block, then the suite | `FakeModel` and a stub MCP client so A can test end to end |
| Is blocked by | only the contracts | only the contracts (works against A's fixtures) |
| Reviews | B's skills for domain correctness | A's tools for how a model actually uses them |

The only coupling is **C1-C6 plus the MCP protocol**. Either person can be stubbed by the other, so neither waits.

### Collaboration rules
- Contract changes: pull request touching `contracts/` needs both approvals.
- Small branches, merged within the day; the other person reviews.
- One shared decision log. If it is not in the log, it was not decided.
- GPU etiquette: runs are queued; record who is using it (OPEN Q4).

### Plan for today (durations are the assistant's guesses; correct them after block 2)
| Block | Who | Content | Exit condition |
|---|---|---|---|
| 0 | both | Settle D5, D3, D11; freeze C1-C6; repo skeleton; the mentor walks through the architecture with questions (section 11) | Contracts committed, both can explain the data workflow |
| 1 | A | F-D1..D5, F-M1; publish fixtures early | 3 fixtures readable through `TelemetryStore` |
| 1 | B | F-A1 (gate G0), F-A2, F-A4, F-A5 against a stub | A model is chosen by measured numbers; fake-model run completes |
| 2 | A | F-M2, F-M3 (then F-M4) | Plain MCP client can call every P0 tool |
| 2 | B | F-A3, F-E1, F-E2, F-A6 | Agent completes one real scenario end to end |
| 3 | both | Integration run on 3 scenarios; fix what breaks; first rule-baseline table | First end-to-end row in the results table |
| 4 | A | F-D6, F-D7 (hard scenarios), F-D9 | Baseline-vs-benchmark discrimination report |
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
Service accuracy (top-1, top-3, recall for multi-fault); fault-type accuracy; scope accuracy;
evidence correctness and unsupported-claim rate (from the verifier); abstention quality and false-positive rate on healthy and decoy-only cases;
calibration; tool-call error rate; steps and tokens; wall time; injection robustness; run-to-run consistency when repeated.
Never report a single accuracy number.

### Statistics
Per-scenario paired outcomes; bootstrap confidence intervals; state N every time; no claim of improvement when intervals overlap heavily.
Dev/test split fixed before tuning; skills and prompts are tuned on dev only; test is run once per condition.

### Threats to validity (write these in the README)
Simulator realism; fault names appearing in log text; the model having memorized OpenTelemetry-Demo fault scenarios;
small N; one machine and one quantization; prompt sensitivity; decoys that are easier or harder than real ones;
rejection sampling that favours detectable faults.

---

## 10. Engineering practices

### Repository layout (target)
```
THE HARNESS/
  PROJECT_CONTEXT.md
  README.md
  pyproject.toml            pinned dependencies, ruff + pytest config
  contracts/                pydantic models + exported JSON Schemas (versioned)
  configs/                  model.yaml, limits.yaml, suite.yaml, conditions.yaml
  telemetry/                generator, faults, scenarios            (Person A)
  store/                    TelemetryStore interface + parquet impl (Person A)
  mcp_servers/telemetry/    MCP server                              (Person A)
  agent/                    runtime, model client, MCP client, skill loader (Person B)
  skills/                   one folder per skill with SKILL.md      (Person B)
  evaluation/               scorer, verifier, baselines, runner, reports (Person B)
  tests/                    unit/, contract/, integration/, golden/
  docs/decisions/           one decision record per file
  data/                     generated, gitignored; suite hash recorded
  runs/                     trajectories and results, gitignored
  reference/                read-only prototype, not imported
```

### Conventions
- Contracts first: write the pydantic model and a test before the code that uses it.
- Determinism: every random choice flows from an explicit seed; independent random streams for independent concerns.
- Type hints everywhere, `ruff` for lint and format, small modules, no hidden global state.
- Configuration in YAML, never hard-coded; no secrets in the repo.
- Every run record stores: model name + quantization + server version, seed, suite hash, skill versions, tool-set hash, git sha, limits.
- Logging is structured JSONL; humans read it through a viewer, not by scrolling.
- Failures are typed and counted, never swallowed.

### Test strategy
| Layer | What it proves |
|---|---|
| Unit | each fault's signature; scorer logic; verifier logic |
| Contract | MCP tool schemas and size caps; manifest has no leakage |
| Integration | agent + fake model + real MCP server completes a run |
| Golden | recorded tool outputs for fixed scenarios do not drift |
| Benchmark-quality | rule baseline per tier (does the benchmark discriminate?) |

### Definition of done for a feature
Acceptance criterion met; tests added; contract unchanged or approved; documented in the README or decision log;
reviewed by the other person; no new magic numbers.

---

## 11. Gates and mentor checkpoints

### Go/no-go gates (thresholds are fixed *before* measuring)
| Gate | Question | Suggested rule (owner to confirm) |
|---|---|---|
| G0 | Can the model call tools reliably enough to build on? | >=90% valid tool calls over 30 fixed prompts; report tokens/s and max usable context |
| G1 | Does the benchmark discriminate? | Rule baseline is clearly below 100% on the hard tier; headroom number agreed after seeing data |
| G2 | Does one scenario run end to end? | Valid submitted answer + complete trajectory |
| G3 | Does the experiment fit the GPU budget? | Projected hours from the formula in section 4 <= the time left |

### Questions the owner should be able to answer before each component is built
- **Data:** What exactly makes a fault "root cause" versus "symptom" in the call graph? How could a model cheat from the data alone? What would make a healthy control unfair?
- **MCP:** What is the maximum useful output of one tool call for a model with a few thousand tokens of context? When does a tool leak the answer? What should happen when the filter matches nothing?
- **Agent:** What stops an infinite loop? What does the loop do with a malformed tool call, and why is that a metric rather than a bug? What does the model need to remember across steps, and where does it live?
- **Skills:** What would the model get wrong without this skill? How will you know the skill helped, and what result would make you delete it?
- **Evaluation:** Why is "accuracy" not enough? What is the null hypothesis for the skill comparison? Which numbers are tuned on dev and which are untouched?

---

## 12. Scope

**In the MVP (today):** all P0, plus as many P1 as the GPU budget allows: at least 3 conditions on 10-15 scenarios, a rule baseline, a verifier or a manual evidence check, and a labelled failure sample.

**Not today:** real OpenTelemetry-Demo adapter (F-D10), sub-agents (F-A8), LLM judge (F-E10), UI beyond a trace viewer, remediation, any production claim.

---

## 13. Open questions for the owner

1. **Who is Person A and who is Person B?** Which role do you take?
2. **D5:** simulator first, real demo, or both? (Table in section 3.)
3. **D3:** do you accept the two-family shortlist with selection by gate G0? Which model names have you already run locally?
4. **GPU:** one machine for both people, or two? Who runs experiments?
5. **D11:** may I `git init` this folder?
6. **agent-eval-lab:** embed this project into it, or keep them separate with the lab as a later consumer?
7. **Ceiling reference:** may one frontier-model run be used purely to calibrate how hard the benchmark is, never as the system under test?
8. **The one sentence** you want to be able to say when this is finished.

---

## 14. About `reference/prototype_v0`
A throwaway simulator and rule baseline written before this spec. Facts that carry over: the first fault set was too easy
(rule baseline 85% top-1 on 24 scenarios), and harder failure types were sketched but not tested. Details in `reference/README.md`.

## Sources checked on 2026-10-20
- AirLLM mechanism and caveats: [DEV Community article](https://dev.to/arshtechpro/airllm-runs-a-70b-model-on-a-4gb-gpu-its-true-and-thats-not-the-interesting-part-hha), [Wavect analysis](https://wavect.io/blog/airllm-layer-wise-inference-low-vram/)
- gpt-oss-20b memory figures and MoE offload flags: [Unsloth gpt-oss docs](https://docs.unsloth.ai/basics/gpt-oss), [canirun.ai](https://canirun.ai/model/gpt-oss-20b/)
- Aegis RCA platform: [OperationsPAI/aegis](https://github.com/OperationsPAI/aegis)
- Agent Skills: [best practices](https://agentskills.io/skill-creation/best-practices), [overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- OpenTelemetry Demo and feature flags: [demo docs](https://opentelemetry.io/docs/demo/), [feature flags](https://opentelemetry.io/docs/demo/feature-flags/)
