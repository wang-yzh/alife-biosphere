from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from alife_biosphere.ant_sandbox import build_showcase_config
from alife_biosphere.ant_sandbox import initialize_world
from alife_biosphere.ant_sandbox import summarize_food_source_competition
from alife_biosphere.ant_sandbox.simulation import run_simulation


def main() -> None:
    config = build_showcase_config()
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
    birth_events = [event for event in result.events if event.event_type == "ant_birth"]
    death_events = [event for event in result.events if event.event_type == "ant_death"]
    derived = {
        "births": len(birth_events),
        "deaths": len(death_events),
        "death_reasons": {
            reason: sum(1 for event in death_events if event.payload.get("reason") == reason)
            for reason in sorted({event.payload.get("reason", "unknown") for event in death_events})
        },
        "births_by_colony": {
            colony_id: sum(1 for event in birth_events if event.payload.get("colony_id") == colony_id)
            for colony_id in world.colonies
        },
        "deaths_by_colony": {
            colony_id: sum(1 for event in death_events if event.payload.get("colony_id") == colony_id)
            for colony_id in world.colonies
        },
        "final_population_by_colony": {
            colony_id: world.alive_count_for_colony(colony_id)
            for colony_id in world.colonies
        },
        "pickups": sum(1 for event in result.events if event.event_type == "food_pickup"),
        "unloads": sum(1 for event in result.events if event.event_type == "food_unload"),
        "feeds": sum(1 for event in result.events if event.event_type == "nest_feed"),
        "upkeep_consumed": sum(event.payload["consumed"] for event in result.events if event.event_type == "nest_upkeep"),
        "food_reseeds": sum(1 for event in result.events if event.event_type == "food_patch_reseed"),
        "food_regrows": sum(1 for event in result.events if event.event_type == "food_patch_regrow"),
        "contested_sources": sum(1 for event in result.events if event.event_type == "food_source_contested"),
        "hostility_contacts": sum(summary["hostility_contacts"] for summary in tick_summaries),
        "contest_entries": sum(summary["contest_entries"] for summary in tick_summaries),
        "contestant_ticks": sum(summary["contesting_ants"] for summary in tick_summaries),
        "avoidance_turns": sum(summary["avoidance_turns"] for summary in tick_summaries),
        "hungry_ant_ticks": sum(summary["hungry_ants"] for summary in tick_summaries),
        "combat_starts": sum(1 for event in result.events if event.event_type == "combat_start"),
        "combat_ends": sum(1 for event in result.events if event.event_type == "combat_end"),
        "combat_pairs": sum(summary["combat_pairs"] for summary in tick_summaries),
        "colony_pickups": {
            colony_id: sum(
                1
                for event in result.events
                if event.event_type == "food_pickup"
                and event.organism_id is not None
                and event.organism_id.startswith(f"{colony_id}_")
            )
            for colony_id in world.colonies
        },
        "colony_unloads": {
            colony_id: sum(
                1
                for event in result.events
                if event.event_type == "food_unload"
                and event.organism_id is not None
                and event.organism_id.startswith(f"{colony_id}_")
            )
            for colony_id in world.colonies
        },
        "nest_food": world.delivered_food_total(),
        "colony_food": {colony_id: colony.nest.stored_food for colony_id, colony in world.colonies.items()},
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
