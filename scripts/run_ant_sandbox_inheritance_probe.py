from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from alife_biosphere.ant_sandbox import build_showcase_config
from alife_biosphere.ant_sandbox import summarize_inheritance_dynamics
from alife_biosphere.ant_sandbox.simulation import run_simulation


SEEDS = (7, 11, 13)


def _case_config(seed: int, mode: str):
    base = build_showcase_config(seed=seed, ticks=1800)
    if mode == "mutate":
        ants = replace(base.ants, inheritance_mode="mutate", mutation_rate=0.35, mutation_step=0.06)
    elif mode == "resample":
        ants = replace(base.ants, inheritance_mode="resample", mutation_rate=0.0, mutation_step=0.0)
    else:
        ants = replace(base.ants, inheritance_mode="clone", mutation_rate=0.0, mutation_step=0.0)
    return replace(base, ants=ants)


def main() -> None:
    output_dir = ROOT / "outputs" / "ant_sandbox_inheritance_probe"
    output_dir.mkdir(parents=True, exist_ok=True)
    case_rows: list[dict[str, object]] = []
    for mode in ("clone", "mutate", "resample"):
        for seed in SEEDS:
            config = _case_config(seed, mode)
            result = run_simulation(config)
            inheritance = summarize_inheritance_dynamics(result)
            case_rows.append(
                {
                    "mode": mode,
                    "seed": seed,
                    "births": sum(1 for event in result.events if event.event_type == "ant_birth"),
                    "deaths": sum(1 for event in result.events if event.event_type == "ant_death"),
                    "pickups": sum(1 for event in result.events if event.event_type == "food_pickup"),
                    "unloads": sum(1 for event in result.events if event.event_type == "food_unload"),
                    "alive": result.world.alive_count(),
                    "food_remaining": result.world.food_remaining(),
                    **inheritance,
                }
            )
    summary: dict[str, object] = {"cases": case_rows, "by_mode": {}}
    for mode in ("clone", "mutate", "resample"):
        rows = [row for row in case_rows if row["mode"] == mode]
        summary["by_mode"][mode] = {
            "case_count": len(rows),
            "mean_births": round(sum(int(row["births"]) for row in rows) / max(1, len(rows)), 4),
            "mean_deaths": round(sum(int(row["deaths"]) for row in rows) / max(1, len(rows)), 4),
            "mean_unloads": round(sum(int(row["unloads"]) for row in rows) / max(1, len(rows)), 4),
            "mean_alive": round(sum(int(row["alive"]) for row in rows) / max(1, len(rows)), 4),
            "mean_mutated_births": round(sum(int(row["mutated_births"]) for row in rows) / max(1, len(rows)), 4),
            "mean_max_generation": round(sum(int(row["max_generation"]) for row in rows) / max(1, len(rows)), 4),
        }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(summary["by_mode"])


if __name__ == "__main__":
    main()
