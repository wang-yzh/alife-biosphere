# Ant Sandbox M4 Role Slice 2026-04-21

## Purpose

This note records the first role-differentiation slice for the ant-sandbox
branch.

It answers:

```text
Can we now extract long-run behavior summaries and see multiple behavior
clusters instead of treating the colony as one undifferentiated mass?
```

## What Changed

Added in this pass:

- `src/alife_biosphere/ant_sandbox/reporting.py`
- per-ant behavior summaries over long runs
- deterministic lightweight clustering into three behavior groups
- `scripts/run_ant_sandbox_role_probe.py`

## What The Summary Measures

For each ant, the current summary records:

- moves
- pickups
- unloads
- alive ticks
- carrying ticks
- near-nest ticks
- far-field ticks
- total travel distance

These are then clustered into first-pass role-like groups.

## What To Run

```text
/Users/qlqwpy/Documents/游乐园/.venv/bin/python -m pytest
/Users/qlqwpy/Documents/游乐园/.venv/bin/python scripts/run_ant_sandbox_role_probe.py
```

## What This Supports

This slice supports the narrower claim that the branch can now examine
behavior-role structure instead of only colony totals.

It does not yet prove robust emergent division of labor, but it does make that
question testable.

## What It Does Not Support Yet

This slice does not yet support claims about:

- stable role structure across many seeds
- strongly interpretable biological role categories
- role shifts under disturbance

## Next Practical Step

The next useful extension is:

- compare role structure across many seeds
- compare role structure with and without pheromones
- render role colors directly in the sandbox observer
