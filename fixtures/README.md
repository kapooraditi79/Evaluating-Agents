# Shared reference set — current revision v0.1.1

Generated with `python -m telemetry.cli references --output fixtures/v0.1.1` using
the checked-in default configuration and pinned dependencies. This set is ~0.5 MB.

Start with `v0.1.1/reference_index.json` to locate each opaque dataset. These examples
are for developers and evaluators; never send this index to the investigator.

* Slow payment: sustained latency and upstream waiting.
* Fast failure: payment rejects requests in 2 ms; status filters find it.
* Healthy control: a real, brief frontend blip, no sustained root cause.
* `v0.1.1/examples/pagination.json`: two pages, one query ID, whole-result handles.
* `v0.1.1/private/two_cause_schema_example.json`: primary/trigger schema example only.

Each dataset has public telemetry and a separately stored private answer. Tool
exchange files in `examples/` may reveal labels in their filenames and are not
part of a public dataset. Tests replay the saved exchanges through the current tools.

The v0.1 directory is retained as a historical pre-audit snapshot. Do not mix its
results or tool versions with v0.1.1. The wire schema remains 0.1.0; generator/tool
implementation versions are recorded independently.
