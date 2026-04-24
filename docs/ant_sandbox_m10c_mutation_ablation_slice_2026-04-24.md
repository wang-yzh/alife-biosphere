# Ant Sandbox M10C Mutation Ablation Slice 2026-04-24

## Purpose

This slice turns the new genome contract into an actual experimental control
surface.

The branch is no longer only asking:

```text
Can we name the inherited structure?
```

It is now also asking:

```text
What changes when inheritance is cloned, mutated, or broken?
```

## What Changed

The active branch now supports three explicit inheritance modes:

- `clone`
- `mutate`
- `resample`

Mode meanings:

- `clone`: child copies parent instinct genome exactly
- `mutate`: child copies parent genome and may receive one bounded point mutation
- `resample`: child keeps the genealogical parent link but receives a fresh founder-like instinct sample instead of copied traits

Current mutation scope is intentionally small:

- at most one mutated trait per birth
- trait set limited to `range_bias`, `trail_affinity`, `harvest_drive`
- bounded step size
- no recombination
- no module duplication
- no epigenetic layer

## New Measurement Surface

The branch now reports:

- `inheritance_mode`
- `mutation_rate`
- `mutation_step`
- `mutated_births`
- `max_generation`
- `alive_generation_distribution`
- `births_by_generation`
- `mean_traits_by_colony`
- `mean_traits_by_generation`

## New Probes

The branch now includes:

- `scripts/run_ant_sandbox_inheritance_probe.py`
- `scripts/run_ant_sandbox_inheritance_observer.py`

The inheritance probe runs `clone / mutate / resample` over seeds:

```text
7, 11, 13
```

## Current Signal

Current inheritance probe means:

- `clone`: `mean_unloads=1032.3333`, `mean_alive=34.3333`
- `mutate`: `mean_unloads=1097.6667`, `mean_alive=40.6667`, `mean_mutated_births=19.6667`
- `resample`: `mean_unloads=1103.6667`, `mean_alive=36.6667`

Current interpretation:

```text
the sandbox can now compare inheritance regimes directly,
but it is still too early to call any trait trend an adaptive law
```

## Verification

Verification for this slice:

- targeted tests: `29 passed in 34.18s`
- full suite: `51 passed in 34.09s`

## Why This Slice Matters

This is the first point where the branch can separate three different stories:

- stable inheritance
- inheritance plus bounded novelty
- reproduction without trait copying

Without that separation, later mutation results would be anecdotal.

## Next Step

The correct next move is not bigger mutation operators.

It is:

```text
longer-run comparison
+ better evolutionary metrics
+ observer support for mutation-bearing lineages
```
