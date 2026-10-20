"""Versioned balanced suite and explicitly limited shortcut audits; no model scoring."""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from contracts.models import TOOL_VERSION, Cause, Diagnosis, GroundTruth
from mcp_servers.telemetry.engine import ToolEngine
from store.parquet import ParquetStore
from telemetry.config import Environment, Fault, load_environment
from telemetry.generator import GENERATOR_VERSION, Bundle, _json, generate


def require_empty_output(destination: Path) -> None:
    if destination.exists() and any(destination.iterdir()):
        raise FileExistsError("reference/suite output must be empty; choose a new directory")


def build_references(destination: Path, environment: Environment | None = None) -> list[Bundle]:
    require_empty_output(destination)
    config = environment or load_environment()
    bundles = [
        generate(
            destination,
            seed=101,
            faults=[Fault(service="payment", mechanism="latency")],
            environment=config,
            template="alert",
        ),
        generate(
            destination,
            seed=102,
            faults=[Fault(service="payment", mechanism="errors")],
            environment=config,
            template="report",
        ),
        generate(destination, seed=103, environment=config, template="alert"),
    ]
    labels = ("slow_payment", "fast_failure", "healthy")
    index: dict[str, Any] = {}
    for label, bundle in zip(labels, bundles, strict=True):
        engine = ToolEngine(ParquetStore(bundle.public), cap=config.response_token_cap)
        window = bundle.manifest.data_range.model_dump()
        query = {"window": window, "service": "payment", "metric": "latency_p95_ms"}
        result = engine.call("query_metric", query)
        _json(
            destination / "examples" / f"{label}.json",
            {"tool": "query_metric", "arguments": query, "response": result},
        )
        index[label] = {
            "public": bundle.public.relative_to(destination).as_posix(),
            "private": bundle.private.relative_to(destination).as_posix(),
        }
    store = ParquetStore(bundles[1].public)
    engine = ToolEngine(store, cap=config.response_token_cap)
    arguments = {
        "window": store.manifest.data_range.model_dump(),
        "service": "payment",
        "status": "ERROR",
        "limit": 1,
    }
    page1 = engine.call("find_traces", arguments)
    page2_args = {**arguments, "cursor": page1["next_cursor"]}
    page2 = engine.call("find_traces", page2_args)
    _json(
        destination / "examples/pagination.json",
        {
            "tool": "find_traces",
            "pages": [
                {"arguments": arguments, "response": page1},
                {"arguments": page2_args, "response": page2},
            ],
        },
    )
    two_cause = GroundTruth(
        id="schema-example-only",
        no_fault=False,
        seed=0,
        root_causes=[
            Cause(
                service="payment",
                fault_type=Diagnosis.DEPENDENCY_UNAVAILABLE,
                propagation_path=["payment", "checkout", "frontend"],
                onset_time="2026-03-14T14:04:30Z",
                injection_mechanism="dependency_down",
            ),
            Cause(
                service="checkout",
                fault_type=Diagnosis.RETRY_AMPLIFICATION,
                role="trigger",
                propagation_path=["checkout", "frontend"],
                onset_time="2026-03-14T14:04:30Z",
                injection_mechanism="retries",
            ),
        ],
        symptom={"operation": "POST /checkout", "kind": "errors"},
    )
    _json(destination / "private/two_cause_schema_example.json", two_cause.model_dump())
    _json(destination / "reference_index.json", index)
    return bundles


def balanced_plan() -> list[dict[str, Any]]:
    """Exact template x reference fraction balance WITHIN each split and each label."""
    plan = []
    mechanisms = [
        "latency",
        "errors",
        "cpu_saturation",
        "memory_leak",
        "dependency_down",
        "bad_deploy",
    ]
    services = ["payment", "quote", "cart", "currency", "shipping", "checkout"]
    fault_index = 0
    for split in ("dev", "test"):
        for template in ("report", "alert"):
            for fraction in (0.6, 0.75):
                for faulty in (False, True):
                    mechanism = mechanisms[fault_index % len(mechanisms)] if faulty else None
                    if faulty:
                        fault_index += 1
                    plan.append(
                        {
                            "split": split,
                            "template": template,
                            "reference_fraction": fraction,
                            "faulty": faulty,
                            "mechanism": mechanism,
                            "service": services[(fault_index - 1) % len(services)]
                            if faulty
                            else None,
                            "seed": 500 + len(plan),
                        }
                    )
    return plan


def balance_audit(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Categorical lookup classifier's best accuracy from the TWO metadata features jointly."""
    counts: dict[str, dict[tuple[str, float], Counter]] = defaultdict(lambda: defaultdict(Counter))
    for record in records:
        counts[record["split"]][record["template"], record["reference_fraction"]][
            record["faulty"]
        ] += 1
    accuracy = {
        split: sum(max(c.values()) for c in groups.values())
        / sum(sum(c.values()) for c in groups.values())
        for split, groups in counts.items()
    }
    return {
        "best_metadata_lookup_accuracy": accuracy,
        "passed": bool(accuracy) and all(value == 0.5 for value in accuracy.values()),
        "scope": (
            "exact balance of template and relative reference time; not proof against all leakage"
        ),
    }


def build_suite(destination: Path, environment: Environment | None = None) -> dict[str, Any]:
    require_empty_output(destination)
    config = environment or load_environment()
    records = []
    correct, fault_correct, fault_count = 0, 0, 0
    for item in balanced_plan():
        bundle = generate(
            destination,
            seed=item["seed"],
            environment=config,
            faults=[Fault(service=item["service"], mechanism=item["mechanism"])]
            if item["faulty"]
            else [],
            template=item["template"],
            reference_fraction=item["reference_fraction"],
            decoy_only=not item["faulty"] and item["template"] == "report",
        )
        store = ParquetStore(bundle.public)
        if item["faulty"] == bundle.truth.no_fault:
            raise ValueError("suite generation did not produce the intended case label")
        errors = sorted(
            (r for r in store.tables["logs"] if r["severity"] == "ERROR"),
            key=lambda r: (r["ts_ns"], r["service"], r["span_id"] or ""),
        )
        guess = errors[-1]["service"] if errors else None
        primary_services = {c.service for c in bundle.truth.root_causes if c.role == "primary"}
        hit = guess in primary_services if primary_services else guess is None
        correct += hit
        if item["faulty"]:
            fault_count += 1
            fault_correct += guess in primary_services
        records.append(
            {
                **item,
                "dataset_id": bundle.manifest.id,
                "public": bundle.public.relative_to(destination).as_posix(),
                "private": bundle.private.relative_to(destination).as_posix(),
                "truth_hash": hashlib.sha256(
                    json.dumps(bundle.truth.model_dump(), sort_keys=True).encode()
                ).hexdigest(),
            }
        )
    suite = {
        "schema_version": "0.1.0",
        "generator_version": GENERATOR_VERSION,
        "tool_version": TOOL_VERSION,
        "records": records,
    }
    suite_hash = hashlib.sha256(json.dumps(suite, sort_keys=True).encode()).hexdigest()
    suite["suite_hash"] = suite_hash
    _json(destination / "suite.json", suite)
    report = {
        "n": len(records),
        "metadata": balance_audit(records),
        "latest_error_shortcut": {
            "overall_accuracy": correct / len(records),
            "fault_service_accuracy": fault_correct / fault_count,
            "passed": fault_correct / fault_count <= 0.25,
        },
        "limitations": [
            "only one keyword shortcut tested",
            "background email failures are a controlled distractor",
            "hard-tier rule baseline discrimination is not established",
        ],
    }
    _json(destination / "audit.json", report)
    return report
