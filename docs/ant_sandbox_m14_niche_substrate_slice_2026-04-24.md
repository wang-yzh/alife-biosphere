# Ant Sandbox M14 Niche Substrate Slice 2026-04-24

## Purpose

This slice adds the first ant-created environmental substrates:

- corpses
- residue

The goal is not to add a new species yet.

The goal is to make ant activity leave behind material that future organisms
could exploit.

## What Changed

The branch now supports:

- corpse creation on ant death
- corpse decay over time
- residue accumulation from:
  - trail movement
  - nest unloads
  - nest feeding
  - corpse breakdown
- residue decay over time
- serialization of corpse and residue state through checkpoints
- observer rendering for corpse and residue layers
- branch-comparison metrics for corpse and residue signatures

## New Data Surface

World state now includes:

- `corpses`
- `residue_field`

Summary and tick summary now include:

- `corpse_count`
- `residue_cell_count`
- `residue_total_value`

Branch comparison now includes:

- `corpse_count`
- `residue_cell_count`
- `residue_total_value`
- pairwise corpse and residue deltas

## Probe Signal

Current showcase probe after the substrate slice:

```text
ticks=1800
alive=33
food_remaining=58
corpse_count=0
residue_cell_count=82
residue_total_value=7.1104
corpse_creations=51
corpse_expirations=51
```

Interpretation:

```text
death now leaves short-lived ecological material,
and long-running colony activity leaves a persistent residue map
even after the corpses themselves have decayed away
```

That is the intended stepping-stone effect.

## Verification

Targeted substrate-related verification:

```text
uv run pytest tests/test_ant_sandbox_niche_substrate.py tests/test_ant_sandbox_observer.py tests/test_ant_sandbox_branch_comparison.py tests/test_ant_sandbox_checkpoint.py
18 passed in 17.39s
```

Full suite after M14:

```text
uv run pytest
68 passed in 46.70s
```

## Why This Slice Matters

This is the first point where the ant sandbox begins to produce a derived
environment.

Before this slice:

```text
ants consumed the world
```

After this slice:

```text
ants also leave behind a world
```

That is the minimum substrate needed before a decomposer, fungus, scavenger,
or similar successor layer can be justified.

## Current Limits

This slice does not yet implement:

- decomposer organisms
- residue-dependent growth
- corpse transport or scavenging
- food classes
- substrate-driven ant decision changes

Those should come later.

## Next Step

The next implementation milestone is:

```text
M15 open-endedness metrics
```

The correct next question is:

```text
how do we measure whether these new substrates create distinct branch futures?
```
