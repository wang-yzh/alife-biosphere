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
        ticks=300,
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
        disturbance_tick=150,
        disturbance_food_shift=True,
        disturbance_food_shift_dx=-8,
        disturbance_food_shift_dy=6,
        disturbance_kill_radius=4,
        ants=AntAgentConfig(
            max_age=240,
            max_population=44,
            spawn_food_cost=2,
            spawn_interval=6,
            pheromone_enabled=True,
            hunger_return_threshold=5.0,
            nest_feed_amount=4.0,
        ),
    )
    result = run_simulation(config)
    tick_summaries = [event.payload for event in result.events if event.event_type == "tick_summary"]
    pre = tick_summaries[110:150]
    post = tick_summaries[200:240]
    pre_unloads = sum(item["unloads"] for item in pre)
    post_unloads = sum(item["unloads"] for item in post)
    recovery_ratio = 0.0 if pre_unloads == 0 else round(post_unloads / pre_unloads, 4)
    derived = {
        "pre_unloads": pre_unloads,
        "post_unloads": post_unloads,
        "recovery_ratio": recovery_ratio,
        "disturbance_events": sum(1 for event in result.events if event.event_type == "disturbance"),
        "food_shift_events": sum(1 for event in result.events if event.event_type == "food_shift"),
    }
    output_dir = ROOT / "outputs" / "ant_sandbox_disturbance_probe"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "config.json").write_text(json.dumps(config.to_dict(), indent=2), encoding="utf-8")
    (output_dir / "summary.json").write_text(json.dumps(result.summary(), indent=2), encoding="utf-8")
    (output_dir / "events.json").write_text(
        json.dumps([event.to_dict() for event in result.events], indent=2),
        encoding="utf-8",
    )
    (output_dir / "derived_summary.json").write_text(json.dumps(derived, indent=2), encoding="utf-8")
    print(result.summary())
    print(derived)


if __name__ == "__main__":
    main()
