from __future__ import annotations

import argparse
import json
from dataclasses import replace
from datetime import datetime
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from alife_biosphere.ant_sandbox import build_showcase_config
from alife_biosphere.ant_sandbox.checkpoint import load_checkpoint, write_checkpoint
from alife_biosphere.ant_sandbox.simulation import step_world
from alife_biosphere.ant_sandbox.world import initialize_world


def _timestamp_id() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run, pause, resume, and fork the ant sandbox experiment.")
    parser.add_argument("--checkpoint", type=Path, default=None, help="Existing checkpoint to resume or fork.")
    parser.add_argument("--output-dir", type=Path, default=None, help="Directory for run artifacts.")
    parser.add_argument("--run-id", default=None, help="Run identifier for provenance metadata.")
    parser.add_argument("--branch-id", default=None, help="Branch identifier when forking from a checkpoint.")
    parser.add_argument("--note", default="", help="Short provenance note stored in checkpoints.")
    parser.add_argument("--target-tick", type=int, default=None, help="Absolute tick to run to.")
    parser.add_argument("--additional-ticks", type=int, default=None, help="Ticks to add after the loaded checkpoint.")
    parser.add_argument("--checkpoint-every", type=int, default=300, help="Write a checkpoint every N ticks.")
    parser.add_argument("--seed", type=int, default=None, help="Override future stochastic decisions after the checkpoint.")
    parser.add_argument("--inheritance-mode", choices=("clone", "mutate", "resample"), default=None)
    parser.add_argument("--mutation-rate", type=float, default=None)
    parser.add_argument("--mutation-step", type=float, default=None)
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    parent_metadata: dict[str, object] = {}
    parent_checkpoint = None

    if args.checkpoint is None:
        run_id = args.run_id or f"run_{_timestamp_id()}"
        target_tick = args.target_tick or 1800
        config = build_showcase_config(seed=args.seed or 7, ticks=target_tick)
        world = initialize_world(config)
    else:
        loaded = load_checkpoint(args.checkpoint)
        parent_metadata = loaded.metadata
        parent_checkpoint = args.checkpoint
        run_id = args.run_id or str(parent_metadata.get("run_id", f"run_{_timestamp_id()}"))
        config = loaded.config
        world = loaded.world
        if args.target_tick is not None:
            target_tick = args.target_tick
        elif args.additional_ticks is not None:
            target_tick = world.tick + args.additional_ticks
        else:
            target_tick = max(config.ticks, world.tick + 600)

    ants_config = config.ants
    if args.inheritance_mode is not None:
        ants_config = replace(ants_config, inheritance_mode=args.inheritance_mode)
    if args.mutation_rate is not None:
        ants_config = replace(ants_config, mutation_rate=args.mutation_rate)
    if args.mutation_step is not None:
        ants_config = replace(ants_config, mutation_step=args.mutation_step)
    config = replace(
        config,
        seed=config.seed if args.seed is None else args.seed,
        ticks=target_tick,
        ants=ants_config,
    )

    if target_tick < world.tick:
        raise ValueError(f"target tick {target_tick} is earlier than checkpoint tick {world.tick}")

    branch_id = args.branch_id or str(parent_metadata.get("branch_id", run_id))
    output_dir = args.output_dir or ROOT / "outputs" / "ant_sandbox_infinite_experiment" / branch_id
    checkpoint_dir = output_dir / "checkpoints"
    output_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_dir.mkdir(parents=True, exist_ok=True)

    metadata = {
        "run_id": run_id,
        "branch_id": branch_id,
        "parent_run_id": parent_metadata.get("run_id"),
        "parent_branch_id": parent_metadata.get("branch_id"),
        "parent_checkpoint": None if parent_checkpoint is None else str(parent_checkpoint),
        "forked_from_tick": None if parent_checkpoint is None else world.tick,
        "note": args.note,
    }

    start_tick = world.tick
    if start_tick == target_tick:
        write_checkpoint(checkpoint_dir / f"tick_{world.tick:06d}.json", config, world, metadata)
    for tick in range(start_tick + 1, target_tick + 1):
        step_world(world, config, tick)
        if args.checkpoint_every > 0 and (tick == target_tick or (tick - start_tick) % args.checkpoint_every == 0):
            write_checkpoint(checkpoint_dir / f"tick_{tick:06d}.json", config, world, metadata)

    final_checkpoint = write_checkpoint(output_dir / "checkpoint_final.json", config, world, metadata)
    status = {
        "run_id": run_id,
        "branch_id": branch_id,
        "start_tick": start_tick,
        "target_tick": target_tick,
        "final_tick": world.tick,
        "summary": world.summary(),
        "final_checkpoint": str(final_checkpoint),
    }
    (output_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (output_dir / "config.json").write_text(json.dumps(config.to_dict(), indent=2), encoding="utf-8")
    (output_dir / "world.json").write_text(json.dumps(world.to_dict(), indent=2), encoding="utf-8")
    (output_dir / "events.json").write_text(
        json.dumps([event.to_dict() for event in world.events], indent=2),
        encoding="utf-8",
    )
    print(status)


if __name__ == "__main__":
    main()
