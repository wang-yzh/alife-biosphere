from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from alife_biosphere.ant_sandbox import AntSandboxConfig
from alife_biosphere.ant_sandbox import initialize_world
from alife_biosphere.ant_sandbox import summarize_food_source_competition
from alife_biosphere.ant_sandbox.simulation import run_simulation


def main() -> None:
    config = AntSandboxConfig()
    result = run_simulation(config)
    world = result.world
    output_dir = ROOT / "outputs" / "ant_sandbox_probe"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "config.json").write_text(json.dumps(config.to_dict(), indent=2), encoding="utf-8")
    (output_dir / "summary.json").write_text(json.dumps(result.summary(), indent=2), encoding="utf-8")
    (output_dir / "events.json").write_text(
        json.dumps([event.to_dict() for event in result.events], indent=2),
        encoding="utf-8",
    )
    (output_dir / "world.json").write_text(json.dumps(world.to_dict(), indent=2), encoding="utf-8")
    tick_summaries = [event.payload for event in result.events if event.event_type == "tick_summary"]
    derived = {
        "pickups": sum(1 for event in result.events if event.event_type == "food_pickup"),
        "unloads": sum(1 for event in result.events if event.event_type == "food_unload"),
        "feeds": sum(1 for event in result.events if event.event_type == "nest_feed"),
        "upkeep_consumed": sum(event.payload["consumed"] for event in result.events if event.event_type == "nest_upkeep"),
        "food_reseeds": sum(1 for event in result.events if event.event_type == "food_patch_reseed"),
        "contested_sources": sum(1 for event in result.events if event.event_type == "food_source_contested"),
        "nest_food": world.nest.stored_food,
        "food_remaining": world.food_remaining(),
        "final_summary": tick_summaries[-1] if tick_summaries else {},
    }
    (output_dir / "derived_summary.json").write_text(json.dumps(derived, indent=2), encoding="utf-8")
    (output_dir / "food_source_competition_summary.json").write_text(
        json.dumps(summarize_food_source_competition(result), indent=2),
        encoding="utf-8",
    )
    print(result.summary())
    print(derived)


if __name__ == "__main__":
    main()
