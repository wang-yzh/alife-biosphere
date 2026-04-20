from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from alife_biosphere.config import SimulationConfig
from alife_biosphere.io import write_config, write_events, write_summary
from alife_biosphere.simulation import run_simulation


def main() -> None:
    config = SimulationConfig()
    result = run_simulation(config)
    output_dir = ROOT / "outputs" / "smoke"
    output_dir.mkdir(parents=True, exist_ok=True)
    write_config(output_dir / "config.json", config)
    write_summary(output_dir / "summary.json", result)
    write_events(output_dir / "events.json", result)
    print(result.summary())


if __name__ == "__main__":
    main()
