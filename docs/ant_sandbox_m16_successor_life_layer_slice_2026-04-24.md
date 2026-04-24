# Ant Sandbox M16 Successor Life Layer Slice 2026-04-24

## Purpose

This slice introduces the first non-ant life layer:

```text
decomposer patches
```

The goal is not to make a second protagonist species.

The goal is to prove that ant-created substrate can support another life
process.

## What Changed

The branch now includes:

- decomposer patch state in the world
- decomposer emergence from corpse substrate
- decomposer feeding on corpse and residue
- decomposer decay when substrate is exhausted
- weak decomposer spread to nearby high-residue cells
- enriched residue deposition from decomposer activity

The new successor layer is:

- non-mobile
- local
- weak
- checkpointed
- observer-visible
- comparison-visible
- counted by open-endedness dependency metrics

## New Event Surface

The branch now emits:

- `decomposer_emerge`
- `decomposer_feed`
- `decomposer_spread`
- `decomposer_decay`
- `residue_enriched`

This is the first implemented dependency chain:

```text
ant death -> corpse -> decomposer -> enriched residue
```

## Current Signal

Current showcase probe after the successor slice:

```text
alive=33
corpse_count=0
decomposer_patch_count=2
residue_cell_count=83
enriched_residue_cell_count=13
decomposer_emerges=51
decomposer_feeds=1733
decomposer_decays=49
```

Interpretation:

```text
the successor layer is not decorative:
it repeatedly emerges from corpse substrate,
processes that substrate,
and leaves a distinct enriched residue footprint
```

That is exactly the minimum dependency proof M16 was meant to establish.

## Observer And Metrics Impact

The observer now shows:

- corpses
- decomposer patches
- enriched residue cells

Branch comparison now reports:

- decomposer patch counts
- decomposer event counts
- enriched residue cell counts

Open-endedness metrics now upgrade ecological dependency from:

```text
requires_m16
```

to:

```text
available
```

for the first implemented dependency edge:

```text
corpse -> decomposer
```

## Verification

Targeted successor-life verification:

```text
uv run pytest tests/test_ant_sandbox_successor_life.py tests/test_ant_sandbox_open_endedness_metrics.py tests/test_ant_sandbox_observer.py tests/test_ant_sandbox_branch_comparison.py tests/test_ant_sandbox_niche_substrate.py
24 passed in 18.17s
```

Full suite after M16:

```text
uv run pytest
78 passed
```

## Why This Slice Matters

This is the first point where the project contains more than one life process.

Not because a second actor was added by hand for spectacle,
but because the first actor created a substrate that could support the second.

That is the correct direction for open evolution.

## Current Limits

This slice still keeps the successor layer deliberately small:

- no mobile scavenger
- no fungus network
- no plant layer
- no mutation in the successor layer
- no direct ant-decomposer coadaptation yet

That is intentional.

The first success is dependency, not diversity explosion.

## Next Step

The next milestone should no longer be:

```text
can we add one more mechanism?
```

It should be:

```text
can forked worlds with ants + decomposers diverge into meaningfully different
multi-niche ecological histories?
```

That is the start of `M17 multi-niche open evolution run`.
