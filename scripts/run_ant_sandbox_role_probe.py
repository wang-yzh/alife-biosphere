from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from alife_biosphere.ant_sandbox import AntAgentConfig, AntSandboxConfig
from alife_biosphere.ant_sandbox.reporting import summarize_behavior_roles
from alife_biosphere.ant_sandbox.simulation import run_simulation


def main() -> None:
    config = AntSandboxConfig(
        ticks=420,
        ants=AntAgentConfig(
            max_age=200,
            max_population=44,
            spawn_food_cost=3,
            spawn_interval=6,
            pheromone_enabled=True,
        ),
    )
    result = run_simulation(config)
    role_summary = summarize_behavior_roles(config, result, cluster_count=3)
    output_dir = ROOT / "outputs" / "ant_sandbox_role_probe"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "config.json").write_text(json.dumps(config.to_dict(), indent=2), encoding="utf-8")
    (output_dir / "summary.json").write_text(json.dumps(result.summary(), indent=2), encoding="utf-8")
    (output_dir / "role_summary.json").write_text(json.dumps(role_summary, indent=2), encoding="utf-8")
    print(result.summary())
    print(role_summary["cluster_summaries"])


if __name__ == "__main__":
    main()
