# Ant Sandbox M1 Foraging Slice 2026-04-21

## Purpose

This note records the first real behavior slice for the ant-sandbox branch.

It answers:

```text
Has the branch moved beyond world initialization into an actual ant-like
foraging loop?
```

## Short Answer

Yes, in a minimal deterministic form.

The branch now supports:

- local movement on a grid
- food pickup
- return-to-nest behavior when carrying food
- unload-at-nest behavior

## What Changed

Added in this pass:

- `src/alife_biosphere/ant_sandbox/simulation.py`
- `scripts/run_ant_sandbox_probe.py`
- `tests/test_ant_sandbox_simulation.py`

Behavior now exists for:

- local wandering
- food sensing within a limited radius
- carrying state
- food return to nest
- nest food accumulation

## What To Run

```text
/Users/qlqwpy/Documents/游乐园/.venv/bin/python -m pytest
/Users/qlqwpy/Documents/游乐园/.venv/bin/python scripts/run_ant_sandbox_probe.py
```

## What This Supports

This slice supports the narrower claim that the new branch is no longer only a
substrate skeleton.

It now contains the first real colony task loop:

```text
find food -> pick up -> carry -> return to nest -> unload
```

## What It Does Not Support Yet

This slice does not yet support claims about:

- pheromone effectiveness
- robust colony persistence
- role differentiation
- disturbance recovery in the ant-sandbox sense

## Next Practical Step

The next main-line target is:

- trace field / pheromone layer
- comparison of pheromone-on versus pheromone-off performance
