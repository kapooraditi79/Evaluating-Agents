# OTel Root-Cause Investigator — Person A

A local incident-data generator, Parquet query layer and read-only MCP server.
This is the environment half of the project. Aditi builds the model investigator,
skills and evaluation harness. No GPU, model download or Docker is needed here.

The checked-in [shared fixtures](fixtures/README.md) are ready to inspect; you do
not have to generate new data before talking to Aditi. Start with the
[contract guide](contracts/README.md), [service graph](docs/topology.md), and one
[sample tool exchange](fixtures/v0.1.1/examples/slow_payment.json).

The current implementation is revision **0.1.1**, with wire schema **0.1.0**.
Read the [implementation audit](docs/IMPLEMENTATION_AUDIT.md) for reproduced gaps,
corrections and remaining work. Earlier fixtures/v0.1 are historical artifacts.
The [G0 integration handoff](docs/ADITI_HANDOFF.md) confirms the v2.1 items, lists
every stub-to-real tool difference, and reports definition sizes and token estimates.

## Start here on Windows

From this repository in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -e '.[dev]'
.\.venv\Scripts\python -m pytest
.\.venv\Scripts\python -m telemetry.cli references --output data/references
```

Dependencies are pinned in pyproject.toml; requirements-lock.txt records the tested
Windows/Python 3.12 environment including transitives. To reproduce that environment,
install `-r requirements-lock.txt` before the editable install. Run commands from
the repository root so the YAML configuration files are available.

The references command generates three complete bundles and tool exchanges. Output
directories are immutable: rerunning into the same destination fails explicitly.
Choose a new output directory when regenerating; nothing is silently overwritten.

```text
data/references/
  public/<opaque-content-id>/
    manifest.json
    spans.parquet
    logs.parquet
    metrics.parquet
    histograms.parquet
  private/<opaque-content-id>/truth.json
  private/two_cause_schema_example.json
  examples/slow_payment.json
  examples/fast_failure.json
  examples/healthy.json
  examples/pagination.json
  reference_index.json
```

Only one selected `public/<id>` directory is exposed to an investigator.
The index, examples, private files, suite records and source code reveal labels
and belong to developers/evaluators, not the agent's context or tools.

## Test a real MCP connection without an LLM

```powershell
$referenceIndex = Get-Content data/references/reference_index.json -Raw | ConvertFrom-Json
$publicPath = Join-Path 'data/references' $referenceIndex.fast_failure.public
.\.venv\Scripts\python -m telemetry.cli smoke --public-dir "$publicPath"
```

This launches the official MCP SDK server over stdio, discovers nine tools and calls
`list_services`. The automated integration test also calls metric, trace and log tools.

For Aditi's MCP client, launch:

```powershell
.\.venv\Scripts\python -m mcp_servers.telemetry.server --public-dir "$publicPath"
```

Use `sys.executable` or the full `.venv` Python path when launching from Python;
pass arguments as a list so paths containing spaces work. Each MCP tool accepts
`{"query": {...}}`; the exported JSON Schema describes the inner query.

## What each component does

| Folder | Responsibility |
|---|---|
| contracts/ | Strict Pydantic models and JSON Schemas shared with Aditi |
| configs/ | Normal topology, traffic, buckets, histogram bounds and provisional output budget |
| telemetry/ | Virtual time, seeded behavior, real SDK spans, faults, public/private writing, audits |
| store/ | Fixed-file reader, validated aggregation, deterministic result-set identity |
| mcp_servers/telemetry/ | Nine typed read-only tools, bounded pagination and stdio server |
| evaluation/g0/ | Aditi's exploratory model tool-call pilot, using its original stub schemas |
| tests/ | Contracts, fault signatures, leakage, aggregation, paging and real MCP integration |

Default graph has 11 services and three user operations. Calls run sequentially;
critical failures propagate, optional email/ad failures do not fail their caller.
Six initial faults are latency, errors, CPU saturation, memory leak/restarts,
unavailable dependency, and bad release. Retry and N+1 mechanisms are also available
through the Python API. A retry policy is harmless alone and is labeled a trigger
only when it actually amplifies a failed critical downstream call. Failed handlers
do not execute children, and critical child failures stop further handler work.

## Generate a versioned suite and audits

```powershell
.\.venv\Scripts\python -m telemetry.cli suite --output data/suite-v011
Get-Content data/suite-v011/audit.json
.\.venv\Scripts\python -m ruff check .
.\.venv\Scripts\python -m ruff format --check .
```

The fixed 16-case plan has eight development and eight test records. Each split
balances alert/report templates and early/late reference positions across labels.
The suite includes healthy controls and unrelated-anomaly false alarms. It records
a suite hash covering implementation versions and private answer hashes, and audits
the latest-ERROR-log shortcut. These audits do not replace
Aditi's rule baseline, model experiments or statistical analysis. This first suite
is a smoke benchmark; reserve a newly versioned test set before substantive tuning.

Custom Python example:

```python
from pathlib import Path
from telemetry.config import Fault, load_environment
from telemetry.generator import generate

bundle = generate(
    Path('data/custom'), seed=42,
    environment=load_environment(),
    faults=[Fault(service='payment', mechanism='latency', region='east')],
)
print(bundle.public)
```

`trace_sampling_rate`, `log_keep_rate`, `metric_gap=True`, and `injection_log=True`
exercise degraded observability/adversarial logs. `check_coverage` detects known
sampling and metric gaps; it honestly reports log coverage unknown because a small
log count alone cannot prove loss. Full log-loss detection and harder benchmark
quality reports remain follow-up work.

## Contract handoff

Read [contracts v0.1](contracts/README.md) and
[closed diagnoses and ambiguity](docs/fault-diagnoses.md).
Regenerate JSON Schemas with `python -m telemetry.cli schemas`.
Aditi should use `Diagnosis` for the answer enum and `store.evidence.canonical_query`
for her evidence verifier. The reference exchanges demonstrate paging and citations.
Human joint review is still required before calling this contract frozen.

The initial 1500-token target uses a stricter 1500-byte serialized-envelope budget
until Aditi supplies the actual tokenizer. Do not report this as measured tokens.
Forward either MCP structured content or its text equivalent to the model once.

## Current limits

Aditi's G0 pilot is included; the full investigation runtime/scorer is still pending.
Synthetic faults,
limited service diversity in the first suite, brief alert blips, coarse tail bins,
and fixed traffic cadence constrain realism. The full rule-baseline discrimination
gate, advanced hard-suite design, real Demo transfer adapter, and production claims
are not completed by generating these fixtures. Application-level private-data
restrictions are tested; the process is not an OS sandbox against arbitrary code.
