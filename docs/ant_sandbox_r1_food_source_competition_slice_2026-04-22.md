# Ant Sandbox R1 Food Source Competition Slice 2026-04-22

## Purpose

This slice begins the first long-horizon route step:

```text
resource competition
```

The branch is still single-colony.
So this pass does not yet implement colony-vs-colony war.
It makes food sources themselves become contested ecological objects.

## What Changed

Each food source now tracks:

- `nearby_ants`
- `carrying_nearby`
- `recent_pickups`
- `competition_pressure`
- `contested_ticks`
- `depletion_count`

The simulation now emits:

- `food_source_contested`
- `food_source_depleted`

when source pressure crosses clear thresholds.

## Observer Change

The observer now renders source pressure visually.

Food sources can show:

- stronger hot-source halo
- stronger border emphasis
- amount plus nearby-ant count

This makes it possible to see which source is being fought over even before
multi-colony mechanics exist.

## Probe Change

`run_ant_sandbox_probe.py` now writes:

- `food_source_competition_summary.json`

with per-source competition summaries and top competition hotspots.

## Current Default Result

In the current default probe run:

- `food_pickups = 33`
- `food_unloads = 28`
- `contested_sources = 20`

and the final world retains source-specific pressure differences rather than
treating all food as one global pool.

## Why This Matters

This is the first step toward future features such as:

- multi-nest food competition
- territorial overlap
- conflict
- stronger death ecology

because those later systems need source pressure to exist first.
