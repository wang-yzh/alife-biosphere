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

This pass also upgrades the default showcase layout into a clearer competition
field with three source roles:

- `food_near`
- `food_gap`
- `food_far`

The goal is not perfect balance yet.
The goal is to make ants choose among distinct sources instead of converging on
one undifferentiated food pool.

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

- `food_pickups = 70`
- `food_unloads = 64`
- `contested_sources = 77`

In the current default `240`-tick showcase run:

- `food_near` is heavily contested and can fully deplete
- `food_gap` also receives meaningful traffic
- `food_far` is visible but still lightly used in this early layout

This means the branch has crossed from “one source happens to be active” into
“multiple named sources participate in the same surface economy”.

and the final world retains source-specific pressure differences rather than
treating all food as one global pool.

## Nest Traffic Note

During this competition pass, outbound ants after unloading were also adjusted
so they do not reform the same pathological nest-side right-cluster.

The current logic now combines:

- short outbound task commitment
- nest-edge fan-out after unloading
- local density avoidance near the nest

This keeps source competition from collapsing into a single stuck nest-edge
blob.

## Why This Matters

This is the first step toward future features such as:

- multi-nest food competition
- territorial overlap
- conflict
- stronger death ecology

because those later systems need source pressure to exist first.
