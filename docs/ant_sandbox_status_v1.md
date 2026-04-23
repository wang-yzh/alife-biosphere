# Ant Sandbox Status v1

## Purpose

This document is the branch-level status page for the current ant-sandbox
branch.

It does not replace the detailed slice notes.
It compresses them into one answer:

```text
Which sandbox milestones are now actually passing,
and which are still provisional?
```

## Current Validation Basis

The current status is based on:

- `M1` foraging probe
- `M2` pheromone comparison
- `M3` persistence probe
- `M4` role clustering summary
- `M5` disturbance recovery probe
- current showcase lifecycle probe with three colonies, terrain, walls, and
  simple reproduction / death enabled

and a multi-seed validation matrix over:

```text
7, 11, 13
```

## Current Status

| Metric | Status | Reason |
| --- | --- | --- |
| `M1 spatial realism` | `pass` | the branch now runs on a local grid with local movement and local sensing rather than a habitat graph |
| `M2 foraging loop` | `pass` | the branch now repeatedly produces `food_pickup` and `food_unload` with net nest food return |
| `M3 pheromone effectiveness` | `pass` | in the current default sandbox, pheromone-on outperforms pheromone-off on food return across the current validation seeds |
| `M4 colony persistence` | `pass` | the branch now shows births, deaths, and bounded alive counts in longer runs without total collapse under the current persistence configuration |
| `M5 role differentiation` | `pass` | the branch now produces multiple role-like behavior clusters from trace summaries |
| `M6 disturbance recovery` | `pass` | the branch now recovers a substantial fraction of prior function after local-space disturbance in the current probe setup |
| `M10A simple lifecycle` | `pass` | the branch now supports starvation and old-age death plus nest-food-driven reproduction with parent and lineage bookkeeping, without mutation |

## Current Lifecycle Snapshot

Latest showcase lifecycle probe:

- `births=52`
- `deaths=51`
- `death_reasons={'old_age': 9, 'starvation': 42}`
- `births_by_colony={'wei': 16, 'shu': 17, 'wu': 19}`
- `deaths_by_colony={'wei': 16, 'shu': 16, 'wu': 19}`
- `final_population_by_colony={'wei': 11, 'shu': 12, 'wu': 10}`
- `pickups=1049`
- `unloads=1009`

## Important Caution

These are current branch-level passes, not final claims of robustness.

The current status should be read as:

```text
the sandbox now passes these gates in its present default and probe settings,
not yet under broad adversarial validation
```

## What Is Still Provisional

Still provisional:

- wider multi-seed robustness
- wider food layout robustness
- stronger role interpretation
- disturbance recovery under harder settings
- observer integration of longer-run lifecycle overlays
- inheritance beyond parent and lineage bookkeeping
- mutation and trait drift under selection pressure

## Next Phase

The next active phase is no longer "prove the small sandbox works".

It is:

- longer-run three-colony lifecycle balance
- stronger resource pressure and turnover under scarcity
- inheritance contract before mutation
- mutation only after lineage and comparison metrics are stable
- combat as optional later pressure rather than the current branch center

The next current planning set is:

- `ant_sandbox_world_design_v2.md`
- `ant_sandbox_build_plan_v2.md`
- `ant_sandbox_m7_scale_up_spec_v1.md`

## Current Working Interpretation

The branch is no longer just a substrate experiment.
It is now a real early ant sandbox with:

- local space
- foraging loops
- trace-mediated improvement
- bounded persistence
- behavior clustering
- local-space recovery
- starvation and old-age death
- nest-food-driven reproduction
- parent and lineage tracking across births

That is enough to treat it as the real project world, not just a sketch.
