from __future__ import annotations

import hashlib
import random
from pathlib import Path
from typing import Literal, Self

import yaml
from pydantic import Field, model_validator

from contracts.models import Contract, utc_ns

ROOT = Path(__file__).resolve().parents[1]


def stream(seed: int, name: str) -> random.Random:
    return random.Random(int.from_bytes(hashlib.sha256(f"{seed}:{name}".encode()).digest()))


class Environment(Contract):
    duration_seconds: int = Field(default=600, ge=60, le=86400)
    bucket_seconds: int = Field(default=10, ge=1)
    request_interval_seconds: int = Field(default=1, ge=1)
    trace_sampling_rate: float = Field(default=1, gt=0, le=1)
    log_keep_rate: float = Field(default=1, ge=0, le=1)
    start: str = "2026-03-14T14:00:00Z"
    histogram_bounds_ms: list[float] = Field(
        default_factory=lambda: [
            5,
            10,
            20,
            40,
            80,
            160,
            320,
            640,
            1280,
            2560,
            5120,
            10240,
            20480,
            60000,
        ]
    )
    response_token_cap: int = Field(default=1500, ge=400)

    @model_validator(mode="after")
    def valid_time(self) -> Self:
        if self.duration_seconds % self.bucket_seconds:
            raise ValueError("duration must contain whole buckets")
        if utc_ns(self.start) % (self.bucket_seconds * 1_000_000_000):
            raise ValueError("start must align to epoch buckets")
        if self.bucket_seconds % self.request_interval_seconds:
            raise ValueError("request interval must divide native bucket size")
        bounds = self.histogram_bounds_ms
        if (
            not bounds
            or bounds[0] <= 0
            or any(b <= a for a, b in zip(bounds, bounds[1:], strict=False))
        ):
            raise ValueError("histogram bounds must be positive and increasing")
        return self


class Edge(Contract):
    service: str
    critical: bool


class Service(Contract):
    base_ms: float = Field(gt=0)
    dependencies: list[Edge]


class Topology(Contract):
    services: dict[str, Service]
    operations: dict[str, list[Edge]]

    @model_validator(mode="after")
    def acyclic(self) -> Self:
        if "frontend" not in self.services or "POST /checkout" not in self.operations:
            raise ValueError("frontend and POST /checkout are required")
        if self.services["frontend"].dependencies:
            raise ValueError("frontend dependencies must be declared per user operation")

        def visit(name: str, ancestors: set[str]) -> None:
            if name not in self.services or name in ancestors:
                raise ValueError("unknown service or dependency cycle")
            for edge in self.services[name].dependencies:
                if edge.service == "frontend":
                    raise ValueError("dependencies cannot call the entrypoint frontend")
                visit(edge.service, ancestors | {name})

        for name in self.services:
            visit(name, set())
        for edges in self.operations.values():
            if not edges or any(edge.service == "frontend" for edge in edges):
                raise ValueError("operations must call non-frontend services")
            for edge in edges:
                visit(edge.service, set())
        return self


Mechanism = Literal[
    "latency",
    "errors",
    "cpu_saturation",
    "memory_leak",
    "dependency_down",
    "bad_deploy",
    "retries",
    "n_plus_one",
]


class Fault(Contract):
    service: str
    mechanism: Mechanism
    onset_fraction: float = Field(default=0.45, ge=0.1, le=0.8)
    end_fraction: float = Field(default=1, gt=0.1, le=1)
    region: Literal["east", "west"] | None = None

    @model_validator(mode="after")
    def ordered(self) -> Self:
        if self.end_fraction <= self.onset_fraction:
            raise ValueError("end must follow onset")
        return self


def load_environment(path: Path | None = None) -> Environment:
    return Environment.model_validate(
        yaml.safe_load((path or ROOT / "configs/environment.yaml").read_text(encoding="utf-8"))
    )


def load_topology(path: Path | None = None) -> Topology:
    return Topology.model_validate(
        yaml.safe_load((path or ROOT / "configs/topology.yaml").read_text(encoding="utf-8"))
    )
