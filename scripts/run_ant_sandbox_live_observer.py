from __future__ import annotations

import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from alife_biosphere.ant_sandbox import AntAgentConfig, AntSandboxConfig
from alife_biosphere.ant_sandbox.observer import _frame_payload, write_ant_live_observer_html
from alife_biosphere.ant_sandbox.simulation import step_world
from alife_biosphere.ant_sandbox.world import initialize_world


def _initial_frame(world) -> dict[str, int]:
    return {
        "ticks": 0,
        "alive": world.alive_count(),
        "carrying": world.carrying_count(),
        "nest_food": world.delivered_food_total(),
        "food_remaining": world.food_remaining(),
        "events": 0,
        "moves": 0,
        "pickups": 0,
        "unloads": 0,
        "births": 0,
        "deaths": 0,
        "food_trail_cells": 0,
        "home_trail_cells": 0,
    }


def _state_payload(config: AntSandboxConfig, world, frame: dict[str, object], complete: bool) -> dict[str, object]:
    return {
        "title": "Ant Sandbox Live World",
        "width": config.width,
        "height": config.height,
        "total_ticks": config.ticks,
        "nest": {"x": world.nest.x, "y": world.nest.y, "radius": world.nest.radius},
        "frames": [frame],
        "live": True,
        "complete": complete,
    }


def _write_atomic(path: Path, text: str) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def main() -> None:
    config = AntSandboxConfig(
        ticks=240,
        ants=AntAgentConfig(
            pheromone_enabled=True,
            max_age=200,
            max_population=44,
            spawn_food_cost=3,
            spawn_interval=6,
        ),
    )
    output_dir = ROOT / "outputs" / "ant_sandbox_live_observer"
    output_dir.mkdir(parents=True, exist_ok=True)
    world = initialize_world(config)
    initial_frame = _frame_payload(world, _initial_frame(world), 0)
    initial_payload = _state_payload(config, world, initial_frame, complete=False)
    write_ant_live_observer_html(output_dir / "live_observer.html", initial_payload)
    _write_atomic(output_dir / "state.json", json.dumps(initial_payload, indent=2))
    print({"html": str(output_dir / "live_observer.html"), "ticks": config.ticks})
    time.sleep(0.5)
    for tick in range(1, config.ticks + 1):
        summary = step_world(world, config, tick)
        frame = _frame_payload(world, summary, tick)
        payload = _state_payload(config, world, frame, complete=False)
        write_ant_live_observer_html(output_dir / "live_observer.html", payload)
        _write_atomic(output_dir / "state.json", json.dumps(payload, indent=2))
        time.sleep(0.35)
    final_payload = _state_payload(config, world, frame, complete=True)
    write_ant_live_observer_html(output_dir / "live_observer.html", final_payload)
    _write_atomic(output_dir / "state.json", json.dumps(final_payload, indent=2))
    print("Ant sandbox live observer complete.")


if __name__ == "__main__":
    main()
