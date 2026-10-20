import pytest
from pydantic import ValidationError

from contracts.models import Cause, Diagnosis, GroundTruth, Window, export_schemas, iso_time, utc_ns


def test_utc_and_ordering():
    assert utc_ns("2026-03-14T14:00:00Z") % 1_000_000_000 == 0
    with pytest.raises(ValueError):
        utc_ns("2026-03-14T14:00:00")
    with pytest.raises(ValidationError):
        Window(start="2026-03-14T15:00:00Z", end="2026-03-14T14:00:00Z")
    timestamp = "2026-03-14T14:00:00.123456789Z"
    assert iso_time(utc_ns(timestamp)) == timestamp


def test_exported_schema_snapshot(tmp_path):
    from pathlib import Path

    export_schemas(tmp_path)
    for file in tmp_path.glob("*.json"):
        assert file.read_bytes() == (Path("contracts/schemas") / file.name).read_bytes()


def test_closed_diagnoses_and_cause_roles():
    base = dict(
        service="payment",
        propagation_path=["payment", "checkout", "frontend"],
        onset_time="2026-03-14T14:00:00Z",
    )
    with pytest.raises(ValidationError):
        Cause(**base, fault_type="latency_injection")
    trigger = Cause(**base, fault_type=Diagnosis.RETRY_AMPLIFICATION, role="trigger")
    with pytest.raises(ValidationError):
        GroundTruth(id="x", root_causes=[trigger], no_fault=False, symptom={}, seed=1)
