from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from alife_biosphere.config import SimulationConfig, WorldConfig
from alife_biosphere.io import write_config, write_events, write_summary
from alife_biosphere.reporting import summarize_disturbance_recovery
from alife_biosphere.reporting import summarize_habitat_memory
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
    output_dir = ROOT / "outputs" / "ecology_probe"
    output_dir.mkdir(parents=True, exist_ok=True)
    write_config(output_dir / "config.json", config)
    write_summary(output_dir / "summary.json", result)
    write_events(output_dir / "events.json", result)
    summary_events = [event.to_dict() for event in result.events if event.event_type == "tick_summary"]
    recovery_summary = summarize_disturbance_recovery(result, recolonization_window=8)
    habitat_memory_summary = summarize_habitat_memory(result)
    derived = {
        "final_tick_summary": summary_events[-1]["payload"],
        "birth_events": sum(1 for event in result.events if event.event_type == "birth"),
        "death_events": sum(1 for event in result.events if event.event_type == "death"),
        "disturbance_events": sum(1 for event in result.events if event.event_type == "disturbance"),
        "move_events": sum(1 for event in result.events if event.event_type == "move"),
        "recovery_summary": recovery_summary,
        "habitat_memory_summary": habitat_memory_summary,
    }
    (output_dir / "derived_summary.json").write_text(
        json.dumps(derived, indent=2),
        encoding="utf-8",
    )
    (output_dir / "disturbance_recovery_summary.json").write_text(
        json.dumps(recovery_summary, indent=2),
        encoding="utf-8",
    )
    (output_dir / "habitat_memory_summary.json").write_text(
        json.dumps(habitat_memory_summary, indent=2),
        encoding="utf-8",
    )
    print(result.summary())
    print(derived)


if __name__ == "__main__":
    main()
