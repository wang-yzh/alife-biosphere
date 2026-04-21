from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from alife_biosphere.config import SimulationConfig, WorldConfig
from alife_biosphere.reporting import summarize_disturbance_recovery, summarize_source_sink_roles
from alife_biosphere.simulation import run_simulation


def _base_world(seed: int) -> WorldConfig:
    return WorldConfig(
        seed=seed,
        ticks=40,
        founder_count=10,
        disturbance_interval=8,
        disturbance_resource_shock=2.0,
        disturbance_hazard_pulse=0.12,
        senescence_age=24,
        max_age=50,
    )


def main() -> None:
    seeds = [7, 11, 13, 17, 19]
    results = []
    per_run = []
    for seed in seeds:
        result = run_simulation(SimulationConfig(world=_base_world(seed)))
        results.append(result)
        per_run.append(
            {
                "seed": seed,
                "summary": result.summary(),
                "recovery_summary": summarize_disturbance_recovery(result, recolonization_window=8),
            }
        )

    aggregate = summarize_source_sink_roles(results, recolonization_window=8)
    output_dir = ROOT / "outputs" / "source_sink_probe"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "per_run_summary.json").write_text(
        json.dumps(per_run, indent=2),
        encoding="utf-8",
    )
    (output_dir / "aggregate_summary.json").write_text(
        json.dumps(aggregate, indent=2),
        encoding="utf-8",
    )
    print({"seeds": seeds, "run_count": len(results)})
    print(aggregate)


if __name__ == "__main__":
    main()
