import json

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from contracts.models import Diagnosis, utc_ns
from store import ParquetStore
from telemetry.config import Fault, load_topology
from telemetry.faults import FAULT_DIAGNOSES
from telemetry.generator import ADVERSARIAL_BODY, generate
from telemetry.leakage import audit_public


def test_deterministic_parquet_and_private_truth(tmp_path, config, bundles):
    repeated = generate(
        tmp_path,
        seed=22,
        environment=config,
        faults=[Fault(service="payment", mechanism="latency")],
    )
    original = bundles["slow"]
    assert repeated.manifest == original.manifest
    for path in original.public.iterdir():
        assert path.read_bytes() == (repeated.public / path.name).read_bytes()
    assert repeated.truth == original.truth


def test_topology_and_operation_count():
    graph = load_topology()
    assert len(graph.services) >= 10
    assert len(graph.operations) == 3


def test_sampling_preserves_metrics_and_log_links(tmp_path, config, bundles):
    full = ParquetStore(bundles["errors"].public)
    sampled = generate(
        tmp_path,
        seed=22,
        environment=config.model_copy(update={"trace_sampling_rate": 0.1}),
        faults=[Fault(service="payment", mechanism="errors")],
    )
    partial = ParquetStore(sampled.public)
    assert partial.tables["metrics"] == full.tables["metrics"]
    assert partial.tables["histograms"] == full.tables["histograms"]
    assert partial.tables["logs"] == full.tables["logs"]
    retained = {r["trace_id"] for r in partial.tables["spans"]}
    assert any(r["trace_id"] and r["trace_id"] not in retained for r in partial.tables["logs"])


@pytest.mark.parametrize(
    "mechanism",
    ["latency", "errors", "cpu_saturation", "memory_leak", "dependency_down", "bad_deploy"],
)
def test_fault_signatures(tmp_path, config, mechanism):
    bundle = generate(
        tmp_path,
        seed=17,
        environment=config,
        faults=[Fault(service="payment", mechanism=mechanism)],
    )
    store = ParquetStore(bundle.public)
    rows = [r for r in store.tables["spans"] if r["service"] == "payment"]
    onset = utc_ns(bundle.truth.root_causes[0].onset_time)
    before = [r for r in rows if r["start_ns"] < onset]
    after = [r for r in rows if r["start_ns"] >= onset]
    assert before and after and all(r["status"] == "OK" for r in before)
    assert bundle.truth.root_causes[0].fault_type == FAULT_DIAGNOSES[mechanism]
    assert all(r["status"] == "OK" for r in store.tables["spans"] if r["service"] == "cart")
    if mechanism == "latency":
        assert min(r["duration_ms"] for r in after) > 1800
    elif mechanism in {"errors", "dependency_down"}:
        assert all(r["status"] == "ERROR" and r["duration_ms"] <= 3 for r in after)
        expected = "connection refused" if mechanism == "dependency_down" else "request rejected"
        assert all(r["status_message"] == expected for r in after)
    elif mechanism == "cpu_saturation":
        assert any(
            r["metric"] == "cpu_utilization" and r["value"] > 0.9 for r in store.tables["metrics"]
        )
        assert all(r["status"] == "OK" and r["duration_ms"] > 800 for r in after)
    elif mechanism == "memory_leak":
        memory = [
            r["value"]
            for r in store.tables["metrics"]
            if r["service"] == "payment" and r["metric"] == "memory_mb"
        ]
        assert max(memory) > 500
        assert any(b < a for a, b in zip(memory, memory[1:], strict=False))
        assert any("restarting" in r["body"] for r in store.tables["logs"])
    else:
        assert any(r["status"] == "ERROR" for r in after)
        assert all(
            r["attributes"]["service.version"] == "1.1.0" for r in after if r["status"] == "ERROR"
        )


def test_noncritical_failure_does_not_fail_caller(tmp_path, config):
    bundle = generate(
        tmp_path,
        seed=1,
        environment=config,
        faults=[Fault(service="email", mechanism="dependency_down")],
    )
    rows = ParquetStore(bundle.public).tables["spans"]
    assert any(r["status"] == "ERROR" for r in rows if r["service"] == "email")
    assert all(r["status"] == "OK" for r in rows if r["service"] in {"checkout", "frontend"})


def test_private_injection_mapping_is_total():
    assert len(FAULT_DIAGNOSES) == 8
    assert set(FAULT_DIAGNOSES.values()) == set(Diagnosis) - {Diagnosis.UNKNOWN}


def test_retries_amplification_region_and_multiple_primaries(tmp_path, config):
    primary = Fault(service="payment", mechanism="errors")
    base = generate(tmp_path / "base", environment=config, faults=[primary])
    amplified = generate(
        tmp_path / "retry",
        environment=config,
        faults=[primary, Fault(service="checkout", mechanism="retries")],
    )

    def errors(bundle):
        return sum(
            r["service"] == "payment" and r["status"] == "ERROR"
            for r in ParquetStore(bundle.public).tables["spans"]
        )

    assert errors(amplified) == 3 * errors(base)
    assert [c.role for c in amplified.truth.root_causes] == ["primary", "trigger"]
    regional = generate(
        tmp_path / "regional",
        environment=config,
        faults=[
            Fault(service="payment", mechanism="latency", region="east"),
            Fault(service="quote", mechanism="errors"),
        ],
    )
    assert len(regional.truth.root_causes) == 2
    assert all(c.role == "primary" for c in regional.truth.root_causes)
    payment = [
        r for r in ParquetStore(regional.public).tables["spans"] if r["service"] == "payment"
    ]
    assert all(r["duration_ms"] < 40 for r in payment if r["attributes"]["app.region"] == "west")
    assert any(r["duration_ms"] > 1800 for r in payment if r["attributes"]["app.region"] == "east")


def test_query_amplification_repeats_successful_calls(tmp_path, config, bundles):
    bundle = generate(
        tmp_path, environment=config, faults=[Fault(service="checkout", mechanism="n_plus_one")]
    )
    rows = ParquetStore(bundle.public).tables["spans"]
    assert all(r["status"] == "OK" for r in rows)
    per_trace = {}
    for row in rows:
        if row["service"] == "payment":
            per_trace[row["trace_id"]] = per_trace.get(row["trace_id"], 0) + 1
    assert set(per_trace.values()) == {1, 5}


def test_leakage_audit_attributes_metadata_and_explicit_exception(tmp_path, config):
    bundle = generate(tmp_path, environment=config, injection_log=True)
    assert audit_public(bundle.public)  # adversarial text is NOT silently exempted
    assert not audit_public(bundle.public, frozenset({ADVERSARIAL_BODY}))
    file = bundle.public / "logs.parquet"
    table = pq.read_table(file)
    rows = table.to_pylist()
    rows[0]["attributes"] = json.dumps({"seed": 22})
    pq.write_table(pa.Table.from_pylist(rows, schema=table.schema), file)
    assert audit_public(bundle.public, frozenset({ADVERSARIAL_BODY}))
    clean = pq.read_table(file).replace_schema_metadata({b"note": b"ground truth"})
    pq.write_table(clean, file)
    assert any("metadata" in issue for issue in audit_public(bundle.public))
