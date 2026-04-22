from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from alife_biosphere.ant_sandbox import AntAgentConfig, AntSandboxConfig, FoodPatchConfig, NestConfig
from alife_biosphere.ant_sandbox.simulation import run_simulation


def main() -> None:
    config = AntSandboxConfig(
        ticks=420,
        nest=NestConfig(initial_stored_food=240, colony_upkeep_per_ant_tick=0.0),
        food_patches=(
            FoodPatchConfig(
                "food_a",
                x=38,
                y=14,
                radius=3,
                amount=120,
                max_amount=120,
                regrowth_rate=1,
                relocate_on_depletion=False,
            ),
            FoodPatchConfig(
                "food_b",
                x=48,
                y=35,
                radius=4,
                amount=180,
                max_amount=180,
                regrowth_rate=1,
                relocate_on_depletion=False,
            ),
        ),
        ants=AntAgentConfig(
            max_age=260,
            max_population=44,
            spawn_food_cost=1,
            spawn_interval=6,
            pheromone_enabled=True,
            hunger_return_threshold=5.0,
            nest_feed_amount=4.0,
        ),
    )
    result = run_simulation(config)
    output_dir = ROOT / "outputs" / "ant_sandbox_persistence_probe"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "config.json").write_text(json.dumps(config.to_dict(), indent=2), encoding="utf-8")
    (output_dir / "summary.json").write_text(json.dumps(result.summary(), indent=2), encoding="utf-8")
    (output_dir / "events.json").write_text(
        json.dumps([event.to_dict() for event in result.events], indent=2),
        encoding="utf-8",
    )
    tick_summaries = [event.payload for event in result.events if event.event_type == "tick_summary"]
    derived = {
        "births": sum(1 for event in result.events if event.event_type == "ant_birth"),
        "deaths": sum(1 for event in result.events if event.event_type == "ant_death"),
        "pickups": sum(1 for event in result.events if event.event_type == "food_pickup"),
        "unloads": sum(1 for event in result.events if event.event_type == "food_unload"),
        "feeds": sum(1 for event in result.events if event.event_type == "nest_feed"),
        "upkeep_consumed": sum(event.payload["consumed"] for event in result.events if event.event_type == "nest_upkeep"),
        "food_reseeds": sum(1 for event in result.events if event.event_type == "food_patch_reseed"),
        "alive_min": min(summary["alive"] for summary in tick_summaries),
        "alive_max": max(summary["alive"] for summary in tick_summaries),
        "final_summary": tick_summaries[-1] if tick_summaries else {},
    }
    (output_dir / "derived_summary.json").write_text(json.dumps(derived, indent=2), encoding="utf-8")
    print(result.summary())
    print(derived)


if __name__ == "__main__":
    main()
