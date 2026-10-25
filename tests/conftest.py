from pathlib import Path  # Imports Path to work with filesystem paths in a platform-independent way.

import pytest  # Imports pytest, which provides fixtures and tools for running automated tests.

from telemetry.config import Fault, load_environment  # Imports Fault to describe simulated incidents and load_environment to obtain the telemetry generator's configuration.
from telemetry.generator import generate  # Imports the function that generates telemetry datasets for test scenarios.


@pytest.fixture(scope="session")  # Tells pytest to create this fixture once per test session and reuse it across tests.
def config():  # Defines a fixture that supplies the configuration used to generate test telemetry.

    return load_environment().model_copy(update={"duration_seconds": 180})  # Loads the default environment configuration, copies it, and changes the simulated duration to 180 seconds without modifying the original configuration.


@pytest.fixture(scope="session")  # Tells pytest to create these scenario datasets once per test session and reuse them.
def bundles(tmp_path_factory, config):  # Defines a fixture that generates healthy and faulty telemetry datasets; pytest automatically supplies the temporary-path factory and the config fixture.

    root = tmp_path_factory.mktemp("bundles")  # Creates a unique temporary directory where the generated datasets will be stored.

    return {  # Returns a dictionary that lets tests access each generated scenario by name.

        "healthy": generate(root / "h", seed=22, environment=config),  # Generates a healthy baseline dataset, using seed 22 for repeatable random data.

        "slow": generate(
            root / "s",  # Specifies the directory for the slow-service scenario's output.
            seed=22,  # Uses the same seed to keep random generation consistent where the generator permits.
            environment=config,  # Uses the same environment configuration as the healthy scenario.
            faults=[Fault(service="payment", mechanism="latency")],  # Injects a latency fault into the payment service to simulate slow responses.
        ),  # Finishes generating the slow-service scenario.

        "errors": generate(
            root / "e",  # Specifies the directory for the error-scenario output.
            seed=22,  # Uses the same seed to help make scenario comparisons reproducible.
            environment=config,  # Uses the same environment configuration as the other scenarios.
            faults=[Fault(service="payment", mechanism="errors")],  # Injects an error fault into the payment service to simulate failed requests.
        ),  # Finishes generating the error scenario.

    }  # Ends the dictionary containing the three generated datasets.


@pytest.fixture  # Tells pytest that tests can request this fixture; without a scope argument, it defaults to function scope.
def engine(bundles):  # Defines a fixture that supplies a telemetry tool engine connected to the generated error scenario.

    from mcp_servers.telemetry.engine import ToolEngine  # Imports the engine that implements the telemetry investigation tools.

    from store import ParquetStore  # Imports the storage adapter that reads telemetry data stored in Parquet files.

    return ToolEngine(ParquetStore(bundles["errors"].public))  # Opens the public telemetry data from the error scenario and gives that store to the tool engine.


def hashes(root: Path) -> dict[str, bytes]:  # Defines a helper that returns a dictionary mapping each immediate file's name to its raw bytes.

    return {
        p.name: p.read_bytes()  # Reads each file's exact contents and stores them under the filename.
        for p in root.iterdir()  # Iterates over the immediate contents of root; it does not recursively traverse subdirectories.
        if p.is_file()  # Includes files only, excluding directories.
    }  # Returns the filename-to-bytes dictionary, which can be used to compare files before and after an operation.
