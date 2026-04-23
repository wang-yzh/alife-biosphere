# Ant Sandbox M10A Lifecycle Slice 2026-04-24

## Purpose

This slice starts the first simple open-lifecycle layer for the active
ant-sandbox branch.

The branch is no longer only asking:

```text
Can three colonies forage, route, and compete on one map?
```

It is now also asking:

```text
Can that world sustain births and deaths without mutation or scripted caste?
```

## What Changed

The current branch now supports:

- starvation death
- old-age death
- nest-food-driven reproduction
- parent-linked births
- lineage bookkeeping across generations

Each new ant now records:

- `parent_id`
- `lineage_id`
- `birth_tick`

The child copies the parent instinct fields exactly in this slice:

- `range_bias`
- `trail_affinity`
- `harvest_drive`

## What Is Intentionally Not Added Yet

This slice does not add:

- mutation
- genome mechanics
- recombination
- combat consequences
- culture or learning systems

That is intentional.
The branch needs a clean inheritance contract before it starts changing the
contents of inheritance.

## Observer And Probe Impact

The observer now exposes lifecycle state directly:

- per-colony alive counts
- per-colony births
- per-colony deaths
- selected-ant energy
- selected-ant starvation ticks
- selected-ant parent and lineage fields

The probe output now reports:

- `births`
- `deaths`
- `death_reasons`
- `births_by_colony`
- `deaths_by_colony`
- `final_population_by_colony`

## Current Signal

Latest showcase lifecycle probe:

- `births=52`
- `deaths=51`
- `death_reasons={'old_age': 9, 'starvation': 42}`
- `births_by_colony={'wei': 16, 'shu': 17, 'wu': 19}`
- `deaths_by_colony={'wei': 16, 'shu': 16, 'wu': 19}`
- `final_population_by_colony={'wei': 11, 'shu': 12, 'wu': 10}`
- `pickups=1049`
- `unloads=1009`

The current interpretation is:

```text
the sandbox has crossed from behavior demo into bounded ecological turnover,
but it is not yet an inherited-variation system
```

## Verification

Current verification result:

- `48 passed in 33.79s`

## Why This Slice Matters

This is the first slice where the three-colony sandbox can be read as a real
ongoing ecology rather than only a replay of fixed agents.

Food return now influences reproduction.
Starvation and age now remove individuals.
Parent and lineage identity now survive across births.

That creates the minimum base needed for the next step:

```text
formal inheritance first, mutation later
```
