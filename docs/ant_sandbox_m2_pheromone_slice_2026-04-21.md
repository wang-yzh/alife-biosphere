# Ant Sandbox M2 Pheromone Slice 2026-04-21

## Purpose

This note records the first pheromone / trace-field slice for the ant-sandbox
branch.

It answers:

```text
Does the sandbox now contain an actual trace layer,
and does enabling it improve the foraging loop?
```

## Short Answer

Yes, in a first bounded form.

The branch now has:

- food trail deposition from returning ants
- home trail deposition from outbound ants
- decay of both trail fields
- trail-aware movement for foragers
- a direct `pheromone_on` vs `pheromone_off` comparison probe

## What Changed

Added or changed in this pass:

- trail fields in `AntSandboxWorld`
- trail deposition events
- trail decay
- trail-aware steering in `src/alife_biosphere/ant_sandbox/simulation.py`
- `scripts/run_ant_sandbox_pheromone_probe.py`

## What To Run

```text
/Users/qlqwpy/Documents/游乐园/.venv/bin/python -m pytest
/Users/qlqwpy/Documents/游乐园/.venv/bin/python scripts/run_ant_sandbox_pheromone_probe.py
```

## Current Observed Comparison

At the time of writing:

```text
pheromone_on:
  nest_food = 10
  pickups = 10
  unloads = 10

pheromone_off:
  nest_food = 7
  pickups = 8
  unloads = 7
```

That is enough to support a first claim that enabling the trace field improves
foraging throughput in the current default sandbox.

## What This Supports

This slice supports the narrower claim that:

- the sandbox is no longer relying only on direct food sensing
- environmental traces now matter for colony performance
- `pheromone_on` can outperform `pheromone_off` in the current default setup

## What It Does Not Support

This slice does not yet support claims about:

- robust pheromone superiority across many seeds and layouts
- optimal trail strategy
- pheromone-driven role differentiation
- large-scale colony traffic organization

## Next Practical Step

The next useful extension is:

- more robust pheromone comparison across many seeds
- stronger visual rendering of trails in the sandbox observer
- colony persistence under longer runs
