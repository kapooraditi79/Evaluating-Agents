# Closed diagnosis vocabulary

The answer uses only these nine diagnosis labels. Injection mechanism names are
private implementation details and never appear as answer labels.

| Private mechanism | Ground-truth diagnosis | Intended evidence |
|---|---|---|
| latency | slow_dependency | Handler delay; upstream wait; no matching resource spike |
| errors | elevated_errors | Increased failures, including short rejected requests |
| cpu_saturation | resource_saturation | High CPU plus slower handlers |
| memory_leak | memory_leak_restarts | Growing memory, resets and restart-related errors |
| dependency_down | dependency_unavailable | Connection refusal and upstream errors |
| bad_deploy | bad_release | Failures confined to version 1.1.0 after its appearance |
| retries | retry_amplification | Repeated child attempts only when downstream fails |
| n_plus_one | query_amplification | Extra child calls even when downstream succeeds |
| no known mechanism / insufficient evidence | unknown | Agent cannot substantiate a more specific diagnosis |

`telemetry.faults.FAULT_DIAGNOSES` is total and one-to-one for the eight implemented
mechanisms. `unknown` is an allowed answer label; known injected mechanisms retain
their canonical truth label even when observability is degraded. Aditi scores
abstention separately; an unknown answer is not automatically a correct fault type.

`slow_dependency` names the service whose slow handler blocks an ancestor; it does
not mean the agent should blame the waiting ancestor. `resource_saturation` currently
means CPU saturation; it does not claim to identify every resource bottleneck.

## What telemetry cannot uniquely identify

* Generic handler errors and an unavailable dependency can look identical without
  informative logs/status messages or downstream coverage. Error rate alone cannot
  distinguish `elevated_errors`, `dependency_unavailable`, and `bad_release`.
* CPU-induced delay and other handler delay become hard to distinguish if resource
  metrics are missing. High CPU by itself is correlation, not proof of causation.
* A memory leak cannot be established from latency and errors alone. Missing memory
  history or restart observations can make `memory_leak_restarts` indistinguishable
  from generic saturation or temporary unavailability.
* A release-related failure can resemble generic errors when version attributes
  are absent. A simultaneous release and failure is evidence, not universal causal proof.
* Retries and repeated application queries can have the same call graph when
  attempts/status evidence is missing. Retry amplification needs repeated attempts
  associated with failed downstream calls; N+1 repeats successful work too.
* Different low-level mechanisms can deliberately generate equivalent observations.
  This lab measures diagnosis from available evidence, not recovery of hidden code.

Service localization and fault classification must therefore score separately. The
model should state limitations or use `unknown` rather than invent a mechanism.
These are diagnosis categories, not claims of identifiability in every scenario.

## Current realism limits

Sequential synchronous calls, fixed traffic cadence, simple resource trajectories,
synthetic background email failures, and mostly direct fault signatures keep this
first environment small. Passing the latest-error shortcut audit does not establish
that the benchmark defeats all shortcuts. A wider rule baseline and realistic hard
cases are still required before claiming benchmark discrimination (gate G1).
