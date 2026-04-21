from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from alife_biosphere.config import SimulationConfig, WorldConfig
from alife_biosphere.observer import build_observer_payload, write_observer_html
from alife_biosphere.simulation import run_simulation


def main() -> None:
    config = SimulationConfig(
        world=WorldConfig(
            ticks=40,
            founder_count=10,
            disturbance_interval=8,
            disturbance_resource_shock=2.0,
            disturbance_hazard_pulse=0.12,
            senescence_age=24,
            max_age=50,
        )
    )
    result = run_simulation(config)
    payload = build_observer_payload(
        config,
        result,
        title="Alife Biosphere Sandbox Observer",
    )
    output_dir = ROOT / "outputs" / "observer"
    output_dir.mkdir(parents=True, exist_ok=True)
    write_observer_html(output_dir / "observer.html", config, result, title="Alife Biosphere Sandbox Observer")
    (output_dir / "observer_data.json").write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )
    print({"ticks": payload["ticks"], "habitats": len(payload["habitats"]), "html": str(output_dir / "observer.html")})


if __name__ == "__main__":
    main()
