import json
from pathlib import Path

from mcp_servers.telemetry.engine import ToolEngine
from store import ParquetStore

# One dataset: the "slow payment" alert. Must be a public/<dataset_id> folder.
folder = Path("fixtures/v0.1.1/public/856bbd1c9d78ceea0776082722d05b9a01ad7db621e320170986b52bedc9c5fb")

manifest = json.loads((folder / "manifest.json").read_text())
window = manifest["data_range"]  # {"start": ..., "end": ...}

engine = ToolEngine(ParquetStore(folder))

result = engine.call("list_services", {"window": window})
print(result)
