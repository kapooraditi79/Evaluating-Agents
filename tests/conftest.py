from pathlib import Path

import pytest

from telemetry.config import Fault, load_environment
from telemetry.generator import generate


@pytest.fixture(scope="session")
def config():
    return load_environment().model_copy(update={"duration_seconds": 180})


@pytest.fixture(scope="session")
def bundles(tmp_path_factory, config):
    root = tmp_path_factory.mktemp("bundles")
    return {
        "healthy": generate(root / "h", seed=22, environment=config),
        "slow": generate(
            root / "s",
            seed=22,
            environment=config,
            faults=[Fault(service="payment", mechanism="latency")],
        ),
        "errors": generate(
            root / "e",
            seed=22,
            environment=config,
            faults=[Fault(service="payment", mechanism="errors")],
        ),
    }


@pytest.fixture
def engine(bundles):
    from mcp_servers.telemetry.engine import ToolEngine
    from store import ParquetStore

    return ToolEngine(ParquetStore(bundles["errors"].public))


def hashes(root: Path) -> dict[str, bytes]:
    return {p.name: p.read_bytes() for p in root.iterdir() if p.is_file()}
