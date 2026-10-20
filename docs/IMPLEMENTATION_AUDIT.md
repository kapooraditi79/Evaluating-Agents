# Person A implementation audit

The user requested an audit of the implemented components before connecting Aditi's
agent. This review covered executable data semantics, shared interfaces, evidence
identity, leakage checks, artifact publication and real MCP transport.

The original 32 passing tests were insufficient: a new independent regression run
reproduced 21 failing checks out of 22 cases. Several checks describe the same root
issue; this is not a claim of 21 distinct bugs. Those reproduced failures are fixed.
Additional edge cases were found and covered while making the corrections.

## Findings and corrections

| Area | Original gap | Correction |
|---|---|---|
| Ground truth | Optional email errors could be labeled as a checkout root cause | Record only effects propagated to POST /checkout; unrelated injections are decoys |
| Simulation | A locally failed handler still called its dependencies | Fail fast locally and stop on failed critical dependencies; retries stop after success |
| Trigger semantics | A retry policy alone was rejected rather than shown harmless | Permit the policy alone; it becomes a trigger only when actual extra failed-call attempts occur |
| Timing | Private onset/end times truncated fractional seconds | Use matching integer-nanosecond activation windows and truth timestamps |
| Reproducibility | An active trace in the developer process could contaminate generated trace IDs | Isolate simulated roots from ambient OTel context |
| Resources | One-region saturation produced globally saturated gauges | Aggregate equal-size east/west replicas before temporal average/max |
| Data quality | Invalid metric values, contradictory populations and duplicate keys were accepted | Validate values, units, gauge maxima, histogram populations and unique keys |
| Histogram helpers | Negative durations and invalid quantiles could produce meaningless results | Validate finite increasing bounds, nonnegative observations and valid counts/quantiles |
| Metric gaps | Available operations and CPU rows could hide missing error counts/histograms | Check each required service/operation/series; pair error and request observations |
| Service discovery | Losing a service's metric rows could make the service unknown | Discover services across all available telemetry tables |
| Evidence | Omitted zero-duration defaults differed from explicit zero; unused switches changed identities | Normalize defaults and hash only result-affecting arguments |
| Trace summary | An optional ERROR span could make the whole trace appear failed | Separate root-request status from matching-span status |
| Errors | Backend RuntimeError escaped; malformed Unicode cursor became QUERY_FAILED | Log unexpected failures and return typed errors; validate ASCII cursor offsets |
| Leakage | JSON escapes and Arrow field metadata were not fully inspected | Decode JSON and inspect decoded schema/field metadata; block link/junction traversal |
| Publication | A failed audit could leave a public dataset on disk | Validate/audit in owned staging directories, then publish complete datasets |
| Adversarial cases | Log loss could remove the planted attack while leaving the intended test | Plant into retained logs and mark the case privately |
| Suite outputs | Reusing a changed configuration could overwrite an existing reference index | Reject nonempty reference/suite output directories |
| Reproducibility metadata | Suite identity omitted private answer contents and implementation versions | Include truth hashes and generator/tool versions; use portable relative paths |

## Verification

Run the documented commands from the repository root:

```powershell
.\.venv\Scripts\python -m pytest
.\.venv\Scripts\python -m ruff check .
.\.venv\Scripts\python -m ruff format --check .
```

Tests cover the regressions, original functionality, checked-in exchange replay,
schema exports, deterministic generation and discovery/calls of all nine tools
through an actual stdio MCP connection. The server is tested with warnings treated
as errors. No GPU or model output was used to validate these components.

Latest local verification: **108 tests passed**, including Aditi's 28 G0 tests;
Ruff lint and formatting passed;
dependency consistency passed (`pip check`); no whitespace errors in tracked changes.

The corrected 16-case starter suite remains exactly balanced on template choice
and relative reference time within each split: best categorical lookup accuracy
is 50%. The latest-ERROR shortcut scores 12.5% on fault-service cases (8 fault
cases) and 6.25% overall (16 cases). These narrow, small-sample audits do not prove
general shortcut resistance or benchmark difficulty.

## v2.1 and G0 integration follow-up

Pulled origin/main `01b4b20`, including PROJECT_CONTEXT v2.1 and G0. The combined
environment installs both packages and both test suites. Its shared pytest pin is
9.0.3; requests/jsonschema retain G0's pins. The previous local context and settings
have verified backups in ignored data/merge-backup-01b4b20.

The store now rejects runs/private ancestors before reading files, and public
audits reject nested reserved stores without traversing them. Tests exercise valid
looking datasets under each reserved store and calls to all nine tools.

Shorter descriptions save 860 characters without changing argument schemas. Actual
stdio discovery is exported with complete stub differences and clearly labeled
character-based token estimates. See [the integration handoff](ADITI_HANDOFF.md).
Real model-facing schemas: 9,738 characters/bytes, approximately 2,705 tokens using
Aditi's 3.6 characters/token heuristic. Exact tokenizer counts remain unmeasured.

## Current artifacts and compatibility

* Wire schema: 0.1.0. Closed diagnosis vocabulary is unchanged.
* Tool and generator implementation revisions: 0.1.1.
* Current shared fixtures: fixtures/v0.1.1.
* Corrected starter suite and audit: data/suite-v011 (generated, gitignored).
* Old fixtures/v0.1 and data/suite-v01 are historical and were not overwritten.
* Source tool_version changes query identities intentionally. Never replay an old
  citation under a different implementation version without an explicit comparison.
* Ground truth is scoped to the question's monitored operation. A background fault
  can exist while no_fault is true for checkout. Aditi must use these semantics.
* find_traces now supplies both status (root request) and matching_status (matched
  spans). This tool-specific column clarification must be included in joint review.

## Still outside this audit's completion claim

* Integration with Aditi's actual model, answer schema, scorer and evidence verifier.
* An exact tokenizer and measured context/response budget; the current envelope
  byte cap is conservative and is not reported as measured tokens.
* Trustworthy log-loss detection: counts alone cannot distinguish silence from loss.
  Adding a producer/collector coverage signal requires a jointly reviewed contract.
* Wider baselines, hard-tier discrimination, statistical comparisons and a realism
  transfer test on the real Demo. Those experiments cannot be replaced by unit tests.
* Human joint approval of the contract candidate. This audit does not impersonate
  Aditi's review or claim the complete two-person project is finished.
