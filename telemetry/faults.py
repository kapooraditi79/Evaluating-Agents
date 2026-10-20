"""Private injection mechanisms have exactly one diagnosis-level mapping."""

from contracts.models import Diagnosis

FAULT_DIAGNOSES = {
    "latency": Diagnosis.SLOW_DEPENDENCY,
    "errors": Diagnosis.ELEVATED_ERRORS,
    "cpu_saturation": Diagnosis.RESOURCE_SATURATION,
    "memory_leak": Diagnosis.MEMORY_LEAK_RESTARTS,
    "dependency_down": Diagnosis.DEPENDENCY_UNAVAILABLE,
    "bad_deploy": Diagnosis.BAD_RELEASE,
    "retries": Diagnosis.RETRY_AMPLIFICATION,
    "n_plus_one": Diagnosis.QUERY_AMPLIFICATION,
}
