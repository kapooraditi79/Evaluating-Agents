# Session handoff — read this first (written 2026-10-25)

For: Person B (the owner), and for any new Claude session opened in this folder.
Companion files: `PROJECT_CONTEXT.md` (the full spec, v2.1) and `docs/ADITI_HANDOFF.md` (Person A's handoff).
This file is the short story. The spec is the reference. If they disagree, ask the owner.

---

## 0. RULES FOR CLAUDE IN A NEW SESSION (follow these exactly)

The owner is Person B. They are building this project **to learn**. On 2026-10-20 they told me directly:
"you are spewing code, I am left to wonder what you did, there is no learning for me here."

1. **The owner writes the code.** Do not generate files or large blocks. A tiny snippet, or a fix to a bug in their file, is fine when asked.
2. **One concept per message.** Plain language. A concrete example before any code. No walls of text.
3. **Ask before telling.** Ask for a prediction, then let them run it, then compare. Ask "why" questions.
4. **They decide what goes in each file and how it works.** You review, point out bugs, and ask design questions.
5. **Short messages.** If they say "overwhelming", cut scope and decide small things for them, but still don't write the project for them.
6. When they say "do the code": they mean a small piece, not the whole feature. Keep it small and explain after.
7. Review their code by reading the file. Don't assume what it contains. Check what is actually on disk.
8. Never claim a test passed unless you ran it. Separate "the pipeline works" from "the model is correct".
9. Do not merge into `main`, force-push, or declare contracts frozen. Both collaborators must review contracts.

(The same rule is saved in Claude's memory for this folder and in `CLAUDE.md`.)

---

## 1. What are we doing?

We are building a **local, read-only LLM investigator** that finds the root cause of incidents in a microservice shop
by reading telemetry (traces, metrics, logs). It runs on a **small open model on a 6 GB GPU**.
Then we build an **evaluation harness** that knows the true injected fault and scores the agent.

**The research question** (this is what makes it a project and not a demo):
> On a 6 GB GPU with a small model, how much of the investigation quality comes from
> the **model**, how much from **tool design (MCP)**, and how much from **procedure (Skills)**?
> Which failure modes survive all three?

We answer it with an **ablation**: change one thing at a time (model, tools, skills) and compare scores.

**Learning goals:** how agents work (the loop), how to write MCP tools, how to write Agent Skills,
how to evaluate agents (correctness, evidence, honesty, robustness), observability of agent runs.

**Not:** a product, not remediation (tools are read-only), not evidence about real production systems.

---

## 2. The two people

| | Person A | Person B (you) |
|---|---|---|
| Owns | Fake shop telemetry generator, ground truth, `TelemetryStore`, the MCP server (9 tools) | Model serving, **agent loop**, skills, **scorer**, evidence verifier, experiments |
| Machine | RTX 3050 4 GB, 16 GB RAM (no model runs) | **RTX 4050 6 GB, 24 GB RAM (all model experiments)** |
| Status | **Done**, on branch `person-a/telemetry-integration` | In progress: learning ladder, then integration |

The only coupling is the **contracts** (C1-C6) plus the MCP protocol. Contract changes need both people's approval.

---

## 3. Architecture (simple version)

```
OFFLINE (A)                                  ONLINE (B)
 generator -> telemetry files (public/)      agent loop  <->  local model (Ollama)
          -> ground truth (private/)               |
                                                   v   MCP tools (read-only)
 TelemetryStore  <---- MCP server (9 tools) <------+
                                                   |
 private/ ground truth ----------------------> scorer: compare answer to truth,
                                               verify cited evidence, aggregate
```

Three stores that **never mix**:
- `public/` — telemetry the agent may query
- `runs/` — the agent's own run records
- `private/` — ground truth and scores (the agent must never read it; A has a test for it)

**The 9 tools:** `list_services`, `query_metric`, `find_traces`, `get_trace`, `search_logs`,
`compare_windows`, `get_dependencies`, `check_coverage`, `breakdown`.
Tool names are the same as the G0 stubs, but **arguments differ** (see section 6).

**The agent loop** (this is what you are learning to build):
```
messages = [user question]
repeat:
    reply = model(messages); append reply
    if reply has no tool_calls: done
    for each tool call: run it, append {"role": "tool", "content": result}
    stop if limits hit (max steps, max tool calls, time)
```
The model has no memory. `messages` is the agent's entire memory.

**Final answer:** the agent must call a `submit_answer` tool with a schema (status, ranked root causes with
service + fault type + confidence + evidence, limitations). Status is one of `root_cause_found`, `inconclusive`, `no_problem`.

---

## 4. Decisions made (complete list)

### Project-level (PROJECT_CONTEXT.md decision log)
| ID | Decision | Status |
|---|---|---|
| D1 | Agent under test is an **open-source local model**, not Claude Code | DECIDED |
| D2 | Serve through a local server (Ollama; llama.cpp possible) behind a small client interface | proposed |
| D3 | Choose the model **by measurement (gate G0)**, not reputation | proposed |
| D4 | AirLLM is an experiment only, not the default | proposed |
| D5 | Telemetry: simulator first (Person A built it); real OTel Demo as a later transfer test | OPEN |
| D6 | Write our **own agent runtime** (loop, MCP client, skill loader) | proposed |
| D7 | Tools sit behind a backend-agnostic `TelemetryStore` interface | proposed |
| D8 | Final answer via a `submit_answer` tool with a schema | proposed |
| D9 | **Read-only** tools only | proposed |
| D10 | Python 3.12, pydantic v2, pytest, ruff, parquet | proposed |
| D11 | Git: trunk-based, short branches, the two people review each other | proposed |
| D12 | Mentor mode: assistant guides, code only on request (reinforced: see section 0) | DECIDED |
| D13 | **OpenTelemetry for the agent's own runs, phased:** P0 results table + artifact files; P1 a trace tree per run; P2 evaluation events on a separate linked trace. OTel records, it never scores | DECIDED |
| D14 | **Tool-call format policy** (see below) | **now decided: strict** |
| D15 | **Service and fault type scored separately.** Fault type from a closed, diagnosis-level list (with `unknown`). Person A confirmed the mapping (`docs/fault-diagnoses.md`) | DECIDED |
| D16 | The agent gets only `reference_time` and `data_range`, **not** the incident window | DECIDED |
| D17 | **Evidence references** are short handles cited as `query_id:handle` (e.g. `S3`, `L12`). A built the helpers in `store/evidence.py` | DECIDED (B); A implemented |
| D18 | All model experiments run on Person B's machine (RTX 4050) | AGREED |
| D19 | Question wording mixes "alert" and "neutral report" templates so the wording cannot reveal whether a fault exists | AGREED |

### Decisions made in this mentoring session (2026-10-20)
1. **D14 = strict.** Only a real `tool_calls` field counts. If a model writes tool-call JSON as plain text, that is a model failure, not something we silently fix. (The owner chose this. The earlier plan "strict and recovered reported side by side" is still a valid *measurement*, but the agent itself is strict.)
2. **Evidence for D14:** `qwen2.5-coder:7b` wrote correct call JSON into `content` with no `tool_calls`, across 7 prompt variants, and even called `get_time` for "hi, how are you?". Cause: Ollama only parses calls wrapped in `<tool_call>` tags; this model did not wrap them. A prompt did not fix it.
3. **Model for the learning steps: `llama3.1:8b`** (pulled by the owner). It returned a real `tool_calls` on the first try. `qwen2.5:7b` and `qwen3:8b` were the other candidates. Final model choice still comes from the gate (G0) with a frozen 30-case set.
4. **Learning mode:** the owner learns by building a ladder of small steps (section 7). G0 code is kept; the 600 lines of agent code I wrote were deleted at the owner's request.
5. **Loop design agreed:** result messages use role `tool` (not `assistant`); the model's own reply is appended before the result; the loop is done when a reply has **no `tool_calls`**; hard limit on tool calls (the owner chose 5 for the demo); an **unknown tool name** is sent back to the model as a `tool` message and counted (not a crash); `run_agent` returns text **plus a `stop_reason`** and counts (`tool_calls_used`, `unknown_tool_calls`) instead of a bare string.
6. **Finding (also in G0 pilot):** the model calls a tool even when none is needed ("hi" -> `get_time`). Restraint is a testable weakness and will need a skill and/or gate cases.
7. **Nested arguments** (`{"query": {...}}`) are Person A's design. The owner thinks nested is better and reusable. Treat "the model handles nested well" as a **hypothesis to measure**, not a fact.

### G0 pilot findings (exploratory; 8 cases, 1 model, 1 seed — a first look, not a verdict)
- 7 of 7 tool calls were correct JSON but arrived as text, so strict score was 1/8 (6/8 if text-JSON accepted).
- Stub tool definitions cost about 2,000 of 4,096 context tokens.
- At 4096 context the model already spilled 18% to CPU. Speed about 27 tokens/s on short outputs.

### Gate G0 rule (fixed before measuring)
A call is valid only if it passes four levels (parseable, tool exists, schema-valid, semantically sensible); a correct decision **not** to call counts as success.
Pass if **>= 27/30** frozen gate prompts pass **and** zero invalid tool names. First attempt only. Threshold never changed after seeing results.
The 8 pilot cases are for exploring only and must not be reused in the frozen set.

---

## 5. Where things are (checked 2026-10-25)

- Branch: `integration` (checked out from `origin/person-a/telemetry-integration`, commit `0091db0`, plus A's docs commit `9997525`).
- `main` is untouched. Do not merge into it.
- **Your learning files** (`step1_chat.py`, `step2_tool.py`, `step3_loop.py`) are committed on branch **`b/learning-steps`**, not on `integration`. Bring them over with:
  `git checkout b/learning-steps -- step1_chat.py step2_tool.py step3_loop.py`
- `evaluation/g0/pilot_cases.json` shows as **modified** on `integration` (157 lines added, 63 removed). Nobody knows why yet. It may be A's version or a line-ending change. **Check with `git diff` before committing it.**
- `answer.json` is untracked and unexplained. Don't commit it until you know what it is.
- Folder map: `contracts/` (schemas), `store/` (data access), `mcp_servers/telemetry/` (the server; `engine.py` has `ToolEngine.call(tool, arguments)`), `telemetry/` (generator), `fixtures/v0.1.1/` (3 datasets + 4 example exchanges: slow_payment, fast_failure, healthy, pagination), `docs/tooling/` (real vs stub tool schemas), `evaluation/g0/` (the G0 quiz kit), `tests/`, `reference/` (old throwaway prototype, do not use).
- Tests: your G0 tests (28) passed earlier on `main`. A's tests are not yet run by you. **Do not claim they pass until you run them.**

---

## 6. Real tools vs G0 stubs (what breaks)

- Stubs use **flat** arguments: `{"service": "payment", "start": "...", "end": "..."}`.
- Real calls are **nested**: `{"query": {"service": "payment", "metric": "memory_mb", "window": {"start": "...", "end": "..."}, "step_seconds": 60}}`.
- Every real tool needs `query` (object) and `query.window` with `start` and `end`.
- The G0 grader checks flat arguments, so it will fail correct nested calls. The grader and the cases need adapting (item 4 of A's integration list).
- The real server validates arguments with pydantic (`model_validate`) and returns typed errors like `INVALID_ARGUMENT` as normal results. Think of it as the server's version of your "unknown tool" guard.
- Real windows must be ordered UTC `Z` timestamps inside the dataset; metric windows must align to native buckets.
- Full list of differences: `docs/ADITI_HANDOFF.md`, `docs/tooling/tools-report.json`.

---

## 7. The learning ladder (the owner builds each step)

| # | Build | Teaches | Status |
|---|---|---|---|
| 1 | One LLM call by hand to Ollama | A call is messages in, message out | DONE (`step1_chat.py`) |
| 2 | One tool by hand (`get_time` + schema) | A tool call is the model *asking* you to run something | DONE (`step2_tool.py`) |
| 3 | The loop | An agent is a `while` loop around a model | DONE (`step3_loop.py`, reviewed and fixed) |
| 4 | Break it on purpose, add limits and stop reasons | Why guard code exists | DONE (unknown tool, max calls, "hi" test) |
| 5 | **Call A's engine / MCP server with `list_services`** | What a real tool returns; MCP vs plain function | **NEXT** |
| 6 | Connect the loop to the MCP server | How the halves fit | |
| 7 | Write one Skill, fixing an *observed* failure | What a skill is for | |
| 8 | Score a run against ground truth | How evaluation works | |

Then the project work: adapt G0 cases + grader to nested schemas, freeze the 30-case gate, run G0 on `llama3.1:8b`
(and the qwen models for comparison), measure usable context, choose the model.

---

## 8. YOUR NEXT STEPS (in order)

**Step 5, small and concrete:**
1. Bring your step files onto this branch (command in section 5).
2. Create `step5_engine.py`. It should:
   - import `ParquetStore` (`store/parquet.py`) and `ToolEngine` (`mcp_servers/telemetry/engine.py`);
   - point the store at **one** `fixtures/v0.1.1/public/<hash>/` folder (it must be a `public/<dataset_id>` path);
   - build `ToolEngine(store)`;
   - call `engine.call("list_services", {"window": {"start": ..., "end": ...}})` (get the window from that folder's `manifest.json`);
   - print the result.
   - See `tests/conftest.py:39` for the same setup in A's tests.
3. **Before running, predict:** is the result a plain list, or a structured object? Then compare.
4. Try on purpose: a bad window (start after end), an unknown tool name, a missing `window`. Read the error each time.

**Then:**
5. Read `docs/ADITI_HANDOFF.md` fully and `docs/tooling/` (real vs stub tools).
6. Run A's tests in a virtual environment, report exactly what passed.
7. Find out what the `pilot_cases.json` change is.
8. Connect your step 3 loop to the real server for `list_services` only, then one more tool.

---

## 9. Reading list: evaluating agents (what you asked for)

**Start here, in this order.** I'm giving titles and authors from memory, so search for them and check the dates.

1. **Anthropic, "Building effective agents"** (short). The agent loop, workflows vs agents, and why simple wins.
2. **Anthropic, "Writing effective tools for agents"**. Tool names, descriptions, response size, helpful errors. This is the guide behind our tool design.
3. **Anthropic, "Demystifying evals for AI agents"**. Graders, tasks, trials, transcripts. Read this for the *vocabulary* of agent evaluation.
4. **Hamel Husain, "Your AI product needs evals"** and his follow-ups on error analysis. Practical: look at real failures first, then build metrics.
5. **Eugene Yan, articles on evaluating LLM applications**. Clear on grading methods and their limits.

**Then, to understand the core ideas:**
- **tau-bench (Sierra)**: introduces *pass^k*, which asks whether an agent succeeds **every** time across k repeats, not just once. Relevant to your repeat runs.
- **Berkeley Function Calling Leaderboard (BFCL)**: how tool-calling accuracy is graded. Compare with your G0 four-level grader.
- **SWE-bench**: a classic example of grading by running tests, not by judging text.
- **"Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" (Zheng et al., 2023)**: the biases of model-based judges. Why we keep deterministic checks and treat an LLM judge as a late, validated extra (F-E10).
- **Root-cause-analysis benchmarks**, for your domain: Aegis (referenced in `PROJECT_CONTEXT.md`), and OpenRCA / RCAEval. Look at how they define ground truth and score.
- **Statistics:** Wilson score interval (for small pass/fail counts), bootstrap confidence intervals, McNemar's test for paired comparisons. Any good short intro will do.
- **OpenTelemetry GenAI semantic conventions** (`semantic-conventions-genai` repo): for the run-tracing phase. Status is "Development", so attribute names may change.

**The ideas to take away (in your own words, later):**
1. **Task / trial / grader / transcript.** A task is one scenario. A trial is one run. A grader scores it. The transcript is the full record.
2. **Deterministic grader first.** Ground truth is known, so score by code, not by another model.
3. **Outcome vs process.** Did it find the right service? And did it check the baseline, test alternatives, cite real evidence?
4. **Grounding.** Every claim must cite a handle that exists in the run's tool results (D17). A correct answer with fake evidence is a failure.
5. **Calibration and abstention.** Does "high confidence" mean usually right? Does it say "no problem" on a healthy system?
6. **Robustness.** Decoys, missing telemetry, prompt injection in logs.
7. **Benchmark quality.** A rule baseline must not score 100%, or the benchmark does not test the agent. (The old prototype's rule baseline scored 85%, which is why harder faults were added.)
8. **Never report one accuracy number.** Report a table with N and an interval.
9. **Pre-registration.** Fix thresholds and the dev/test split *before* measuring, so you cannot tune to the test.

---

## 10. Open questions for the owner (from the spec, still unanswered)
1. D5: simulator only for now, real OTel Demo later? (Likely yes. Confirm.)
2. D3: which models to compare at the gate beyond `llama3.1:8b` and `qwen2.5-coder:7b`?
3. C5 answer schema: confidence scale (categorical vs numeric), evidence as bare refs or `{ref, claim}`, optional `onset_estimate`, scoring of invalid answers, cap on causes.
4. May one frontier-model run be used only to calibrate benchmark difficulty, never as the system under test?
5. The one sentence you want to be able to say when this is finished.
