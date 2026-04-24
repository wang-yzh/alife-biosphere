# Ant Sandbox M11 Infinite Experiment Runtime Slice 2026-04-24

## Purpose

This slice changes the sandbox from a fixed-length replay generator into a
runtime that can support open-ended experiments.

The goal is not to claim open-ended evolution yet.

The goal is to make this possible:

```text
run -> pause -> archive -> resume -> fork -> compare descendants
```

Without that runtime layer, every long-run evolutionary claim would be fragile:
the run could not be interrupted, audited, reproduced from a mid-point, or
branched into alternate futures.

## What Changed

The branch now has a JSON checkpoint contract:

- `metadata`: run id, branch id, parent run id, parent branch id, parent
  checkpoint, fork tick, saved tick, format version
- `config`: full `AntSandboxConfig`
- `world`: full runtime state, including ants, food patches, colonies, terrain,
  pheromone fields, stale field, occupied cells, genome ids, and events

The branch now supports:

- saving a checkpoint at any tick
- loading a checkpoint back into a live `AntSandboxWorld`
- resuming from `world.tick + 1`
- forking from a checkpoint with new branch metadata
- changing future stochastic seed and inheritance parameters on a fork

## New Code Surface

New runtime module:

- `src/alife_biosphere/ant_sandbox/checkpoint.py`

New public helpers:

- `write_checkpoint(path, config, world, metadata)`
- `load_checkpoint(path)`
- `run_world_until(world, config, target_tick)`

New command-line runner:

- `scripts/run_ant_sandbox_infinite_experiment.py`

Example new run:

```bash
python scripts/run_ant_sandbox_infinite_experiment.py \
  --branch-id root \
  --target-tick 1800 \
  --checkpoint-every 300
```

Example resume:

```bash
python scripts/run_ant_sandbox_infinite_experiment.py \
  --checkpoint outputs/ant_sandbox_infinite_experiment/root/checkpoint_final.json \
  --additional-ticks 900
```

Example fork:

```bash
python scripts/run_ant_sandbox_infinite_experiment.py \
  --checkpoint outputs/ant_sandbox_infinite_experiment/root/checkpoint_final.json \
  --branch-id root_seed_99 \
  --seed 99 \
  --additional-ticks 900
```

Outputs are written under:

```text
outputs/ant_sandbox_infinite_experiment/<branch-id>/
```

Each run writes:

- `checkpoint_final.json`
- `status.json`
- `config.json`
- `world.json`
- `events.json`
- periodic checkpoint files under `checkpoints/`

## Verification Standard

The critical invariant is:

```text
run 60 ticks continuously
==
run 30 ticks, checkpoint, reload, resume to 60 ticks
```

The new tests verify:

- config serialization round-trip
- world serialization round-trip after simulation
- checkpoint resume equivalence against uninterrupted execution
- fork metadata preservation

Targeted verification:

```text
uv run pytest tests/test_ant_sandbox_checkpoint.py
```

Current result:

```text
4 passed
```

## Why This Matters For Open Evolution

Open-ended evolution is not mainly "more mutation".

For this project, the required substrate is:

- long-lived runs
- archived historical states
- restartable worlds
- branchable alternate futures
- provenance linking branches back to parent ticks
- later comparison of which branches discover new niches or collapse

This slice creates that substrate.

The next evolutionary layer can now be built on top of actual experiment
lineages instead of short isolated runs.

## Current Limits

This slice does not yet implement:

- background daemon execution
- UI controls for pausing or forking
- observer replay directly from a checkpoint branch
- branch comparison dashboards
- automated novelty or niche-discovery scoring

Those should be later layers.

The correct next step is not to add a daemon immediately.

It is:

```text
make checkpointed branches visible and comparable
```
