from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from alife_biosphere.ant_sandbox import AntSandboxConfig
from alife_biosphere.ant_sandbox import AntAgentConfig
from alife_biosphere.ant_sandbox.simulation import run_simulation


def _run(enabled: bool) -> dict[str, object]:
    config = AntSandboxConfig(
        ants=AntAgentConfig(pheromone_enabled=enabled),
    )
    result = run_simulation(config)
    return {
        "enabled": enabled,
        "summary": result.summary(),
        "pickups": sum(1 for event in result.events if event.event_type == "food_pickup"),
        "unloads": sum(1 for event in result.events if event.event_type == "food_unload"),
        "trail_deposits": sum(1 for event in result.events if event.event_type == "trail_deposit"),
    }


def main() -> None:
    on = _run(True)
    off = _run(False)
    output_dir = ROOT / "outputs" / "ant_sandbox_pheromone_probe"
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = {"pheromone_on": on, "pheromone_off": off}
    (output_dir / "summary.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(payload)


if __name__ == "__main__":
    main()
