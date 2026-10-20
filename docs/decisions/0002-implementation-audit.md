# Audit corrections, implementation revision 0.1.1

The user requested an audit before integration. The first independent regression
run reproduced 21 failed checks (22 cases total); the original 32 passing tests
had not exercised these boundaries. See tests/test_audit_regressions.py.

The wire schema remains 0.1.0. This revision tightens the already agreed semantics;
it adds no required manifest, telemetry or MCP fields. Tool implementation version
is now 0.1.1 and generator_version is 0.1.1. Query IDs intentionally change with
the tool version. The diagnosis list is unchanged. Joint contract review is pending.

Corrections:

* Fault windows use exact integer nanoseconds, including fractional seconds.
* Root traces cannot inherit the developer process's active trace context.
* A failed handler does not execute children; critical failures stop further work;
  retries stop after success and require an actual failed critical call to activate.
* Ground truth uses effects propagated to the monitored POST /checkout operation.
  Unrelated or unobserved injections are private decoys. A retry policy on its own
  is harmless and has no primary cause. Optional calls can still propagate delay.
* Overlapping mechanisms on the same service/scope are rejected instead of having
  order-dependent effects. Independent services and disjoint scopes remain supported.
* Service gauges average equal-size east/west replicas before temporal averaging
  and max aggregation. Regional saturation no longer looks like global saturation.
* The brief alert blip is applied to both classes; reports have no automatic blip.
* Metric gaps are checked per service/operation and required metric/histogram.
  Error rates use only paired request/error observations. Coverage checks all required
  metric cells. Missing resource metrics no longer make a known service disappear.
* Malformed counts, gauges, units, result row widths, negative histogram values,
  invalid quantiles, duplicate keys and contradictory counts are rejected.
* JSON escapes and Arrow field metadata are decoded for leakage checks. Link/junction
  traversal is rejected. Dataset publication happens only after staged leakage checks.
* Unexpected backend failures are logged and returned as QUERY_FAILED; malformed
  cursors remain input errors. Response-budget configuration is validated.
* Prompt injections are planted after log loss and recorded privately, ensuring an
  injection case actually exposes the attack text to the investigator.
* Suite/reference indexes refuse nonempty output roots. Suite hashes cover private
  truth hashes and implementation versions; paths use portable '/' separators.

Historical fixtures/v0.1 and data/suite-v01 are retained, not rewritten. Use corrected
fixtures/v0.1.1 and data/suite-v011. Earlier results must not be pooled with this revision.

Outstanding experiment work is separate from these bugs: exact model tokenizer
measurement, integration with Aditi, trustworthy log-loss coverage signals, broader
shortcut baselines/hard-tier validation and real Demo transfer are not claimed complete.
