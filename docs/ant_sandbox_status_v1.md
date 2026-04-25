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
| `M10B genome contract` | `pass` | the branch now wraps inherited instinct traits in an explicit genome structure with `genome_id`, `parent_genome_id`, `generation`, and mutation bookkeeping, while keeping mutation disabled |
| `M10C mutation and ablation controls` | `pass` | the branch now supports bounded point mutation plus `clone / mutate / resample` comparison runs, with generation-level summaries and mutation event bookkeeping |
| `M11 infinite experiment runtime` | `pass` | the branch can checkpoint, reload, resume, and fork a live sandbox world with provenance metadata |
| `M12 checkpoint observer` | `pass` | the branch can open a saved checkpoint as a branch-aware observer and can optionally continue replay from that checkpoint to a later target tick |
| `M13 branch comparison ledger` | `pass` | the branch can group related checkpoints into branch families and emit JSON plus Markdown reports with provenance, outcome metrics, spatial signatures, and pairwise deltas |
| `M14 niche substrate` | `pass` | the branch now generates corpse and residue substrates from ant death, trail use, nest unloads, and nest feeding, and those substrates survive checkpoints and appear in observer plus branch comparison outputs |
| `M15 open-endedness metrics` | `pass` | the branch now converts checkpoint-family comparison outputs into five explicit metric families with status labels, while avoiding any single universal fitness score |
| `M16 successor life layer` | `pass` | the branch now supports a weak decomposer patch layer that emerges from corpse substrate, feeds locally, enriches residue, survives checkpoints, appears in the observer, and upgrades the first dependency edge to an implemented metric |
| `M17 multi-niche open evolution run` | `pass` | the branch now has a campaign workflow that runs a root branch plus fork family, emits observer artifacts for every branch, and produces comparison plus open-endedness outputs as one integrated experiment package |

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

## Current Mutation Signal

Three-mode inheritance probe over seeds `7, 11, 13`:

- `clone`: `mean_unloads=1032.3333`, `mean_alive=34.3333`, `mean_mutated_births=0.0`
- `mutate`: `mean_unloads=1097.6667`, `mean_alive=40.6667`, `mean_mutated_births=19.6667`
- `resample`: `mean_unloads=1103.6667`, `mean_alive=36.6667`, `mean_mutated_births=0.0`

Current reading:

```text
bounded mutation is now real and measurable,
but the branch is still in the first comparison stage rather than making
strong evolutionary claims
```

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
- inheritance beyond parent, lineage, and genome bookkeeping
- stronger mutation baselines and longer-run trait drift under selection pressure
- automated branch comparison for niche discovery or collapse
- stronger substrate diversity beyond corpse and residue
- successor diversity still limited to one weak decomposer layer
- long-run campaign validation still narrow in branch count and seed coverage

## Next Phase

The next active phase is no longer "prove the small sandbox works".

It is:

- branch comparison before stronger open-ended evolution claims
- open-endedness metrics that do not collapse into one fitness score
- multi-niche successor ecology beyond the first decomposer layer
- broader campaign coverage and richer dependency chains
- combat as optional later pressure rather than the current branch center

The next current planning set is:

- `ant_sandbox_handoff_plan_v1.md`
- `ant_sandbox_open_evolution_engineering_plan_v1.md`
- `ant_sandbox_m12_checkpoint_observer_slice_2026-04-24.md`
- `ant_sandbox_m12_checkpoint_observer_spec_v1.md`
- `ant_sandbox_m13_branch_comparison_slice_2026-04-24.md`
- `ant_sandbox_m13_branch_comparison_spec_v1.md`
- `ant_sandbox_m14_niche_substrate_slice_2026-04-24.md`
- `ant_sandbox_m14_niche_substrate_spec_v1.md`
- `ant_sandbox_m15_open_endedness_metrics_slice_2026-04-24.md`
- `ant_sandbox_m15_open_endedness_metrics_spec_v1.md`
- `ant_sandbox_m16_successor_life_layer_slice_2026-04-24.md`
- `ant_sandbox_m16_successor_life_layer_spec_v1.md`
- `ant_sandbox_m17_multi_niche_open_evolution_slice_2026-04-25.md`
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
- explicit genome ids and generation tracking
- bounded mutation and ablation controls
- checkpoint / resume / fork runtime

That is enough to treat it as the real project world, not just a sketch.
