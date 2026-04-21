# Ant Sandbox M5 Disturbance Slice 2026-04-22

## Purpose

This note records the first disturbance-recovery slice for the ant-sandbox
branch.

It answers:

```text
Can the colony absorb a spatial disturbance and still recover part of its
foraging function?
```

## What Changed

Added in this pass:

- food-shift disturbance
- local mortality pulse near the nest
- `scripts/run_ant_sandbox_disturbance_probe.py`

## What To Run

```text
/Users/qlqwpy/Documents/游乐园/.venv/bin/python -m pytest
/Users/qlqwpy/Documents/游乐园/.venv/bin/python scripts/run_ant_sandbox_disturbance_probe.py
```

## Current Recovery Measure

The current probe compares:

- pre-disturbance unloads
- post-disturbance unloads

and derives a first `recovery_ratio`.

## What This Supports

This slice supports the narrower claim that the ant-sandbox branch can now test
functional recovery in local space, rather than only graph-level collapse.

## What It Does Not Support Yet

This slice does not yet support claims about:

- strong recovery guarantees across many seeds
- optimal disturbance design
- role-specific response to disturbance

## Next Practical Step

The next useful extensions are:

- compare recovery with and without pheromones
- render disturbance directly in the ant sandbox observer
- measure recovery over multiple time windows
