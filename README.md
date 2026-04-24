# Alife Biosphere

`alife_biosphere` is currently being developed as an instinct-first ant sandbox
with a simple open lifecycle.

The active branch work is no longer centered on the old habitat-graph ecology
prototype. The current project world is a terrain-aware outdoor sandbox where:

- ants move in local 2D space
- multiple colonies share the same map
- food sources have persistent identity and depletion
- pheromone trails shape route formation
- walls and terrain create routing pressure
- replay observers let you inspect the world visually

The current showcase direction is:

```text
surface ecology -> food competition -> multi-colony overlap ->
death and reproduction -> inheritance contract -> inherited instinct
variation -> checkpointed long-run branching -> niche substrate ->
successor life -> open-ended evolution
```

## Current Branch State

The active sandbox branch has already passed its first core gates under the
current probe setup:

- local spatial movement instead of abstract habitat hops
- working foraging loop
- pheromone usefulness over pheromone-off baselines
- colony persistence under bounded pressure
- role-like behavior clustering
- disturbance recovery
- simple lifecycle with starvation and old-age death
- nest-food-driven reproduction with parent and lineage tracking
- `Genome v1` scaffolding with explicit genome ids and generation tracking
- bounded point mutation plus `clone / mutate / resample` ablation controls
- checkpoint / resume / fork runtime for long-run experiment branches
- checkpoint-aware observer for saved and forked branches
- branch comparison ledger for shared checkpoint families
- corpse and residue substrate for future derived niches
- open-endedness metrics layer with explicit status labels and no single score

The current visible world also includes:

- three colonies: `Wei`, `Shu`, `Wu`
- a larger `128 x 96` showcase map
- terrain types such as `dense_grass`, `sand`, and `rock`
- wall-heavy showcase layouts for routing stress tests

Latest showcase lifecycle snapshot:

- `births=52`
- `deaths=51`
- `death_reasons={'old_age': 9, 'starvation': 42}`
- `final_population_by_colony={'wei': 11, 'shu': 12, 'wu': 10}`
- `pickups=1049`
- `unloads=1009`

For the current branch-level status page, see:

- [ant_sandbox_status_v1.md](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/docs/ant_sandbox_status_v1.md)
- [ant_sandbox_handoff_plan_v1.md](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/docs/ant_sandbox_handoff_plan_v1.md)
- [ant_sandbox_open_evolution_engineering_plan_v1.md](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/docs/ant_sandbox_open_evolution_engineering_plan_v1.md)

## Quick Start

Requirements:

- Python `>=3.11`

Install:

```bash
python -m pip install -e ".[dev]"
```

Run tests:

```bash
python -m pytest
```

## Run The Sandbox

### Replay Observer

Generate the current showcase replay:

```bash
python scripts/run_ant_sandbox_observer.py
```

Open:

- [outputs/ant_sandbox_observer/observer.html](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/outputs/ant_sandbox_observer/observer.html)

This is the best entry point if you want to inspect colony traffic, food
competition, terrain routing, wall behavior, and lifecycle turnover.

### Live Observer

Generate the live file-refresh observer:

```bash
python scripts/run_ant_sandbox_live_observer.py
```

Open:

- [outputs/ant_sandbox_live_observer/live_observer.html](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/outputs/ant_sandbox_live_observer/live_observer.html)

This is useful for monitoring a single run while it is advancing.

### Infinite Experiment Runner

Start a checkpointed long run:

```bash
python scripts/run_ant_sandbox_infinite_experiment.py --branch-id root --target-tick 1800 --checkpoint-every 300
```

Resume from a saved checkpoint:

```bash
python scripts/run_ant_sandbox_infinite_experiment.py --checkpoint outputs/ant_sandbox_infinite_experiment/root/checkpoint_final.json --additional-ticks 900
```

Fork a branch from a saved checkpoint:

```bash
python scripts/run_ant_sandbox_infinite_experiment.py --checkpoint outputs/ant_sandbox_infinite_experiment/root/checkpoint_final.json --branch-id root_seed_99 --seed 99 --additional-ticks 900
```

Outputs are written under:

- [outputs/ant_sandbox_infinite_experiment](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/outputs/ant_sandbox_infinite_experiment)

### Checkpoint Observer

Open a saved branch directly:

```bash
python scripts/run_ant_sandbox_checkpoint_observer.py --checkpoint outputs/ant_sandbox_infinite_experiment/root/checkpoint_final.json
```

Continue replay from a saved branch:

```bash
python scripts/run_ant_sandbox_checkpoint_observer.py --checkpoint outputs/ant_sandbox_infinite_experiment/root/checkpoint_final.json --target-tick 2400
```

Outputs are written under:

- [outputs/ant_sandbox_checkpoint_observer](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/outputs/ant_sandbox_checkpoint_observer)

### Branch Comparison

Compare multiple saved branches:

```bash
python scripts/run_ant_sandbox_branch_comparison.py --checkpoints outputs/ant_sandbox_infinite_experiment/root/checkpoint_final.json outputs/ant_sandbox_infinite_experiment/root_seed_11/checkpoint_final.json outputs/ant_sandbox_infinite_experiment/root_seed_99/checkpoint_final.json
```

Or scan a directory of saved branches:

```bash
python scripts/run_ant_sandbox_branch_comparison.py --input-dir outputs/ant_sandbox_infinite_experiment
```

Outputs are written under:

- [outputs/ant_sandbox_branch_comparison](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/outputs/ant_sandbox_branch_comparison)

### Open-Endedness Metrics

Generate metrics from a comparison report:

```bash
python scripts/run_ant_sandbox_open_endedness_metrics.py --comparison outputs/ant_sandbox_branch_comparison_smoke/comparison.json
```

Or build from checkpoints by letting the metrics layer reuse comparison first:

```bash
python scripts/run_ant_sandbox_open_endedness_metrics.py --input-dir outputs/ant_sandbox_infinite_experiment
```

Outputs are written under:

- [outputs/ant_sandbox_open_endedness](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/outputs/ant_sandbox_open_endedness)

## Run Probes

General showcase probe:

```bash
python scripts/run_ant_sandbox_probe.py
```

This probe now reports both behavior and lifecycle summaries, including:

- `births`
- `deaths`
- `death_reasons`
- `births_by_colony`
- `deaths_by_colony`
- `final_population_by_colony`

Inheritance ablation probe:

```bash
python scripts/run_ant_sandbox_inheritance_probe.py
```

Pheromone comparison:

```bash
python scripts/run_ant_sandbox_pheromone_probe.py
```

Persistence probe:

```bash
python scripts/run_ant_sandbox_persistence_probe.py
```

Role clustering probe:

```bash
python scripts/run_ant_sandbox_role_probe.py
```

Disturbance recovery probe:

```bash
python scripts/run_ant_sandbox_disturbance_probe.py
```

Validation matrix:

```bash
python scripts/run_ant_sandbox_validation_matrix.py
```

Probe outputs are written under:

- [outputs/ant_sandbox_probe](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/outputs/ant_sandbox_probe)
- [outputs/ant_sandbox_inheritance_probe](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/outputs/ant_sandbox_inheritance_probe)
- [outputs/ant_sandbox_pheromone_probe](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/outputs/ant_sandbox_pheromone_probe)
- [outputs/ant_sandbox_persistence_probe](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/outputs/ant_sandbox_persistence_probe)
- [outputs/ant_sandbox_validation_matrix](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/outputs/ant_sandbox_validation_matrix)

## Repository Map

Core ant sandbox implementation:

- [config.py](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/src/alife_biosphere/ant_sandbox/config.py)
- [world.py](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/src/alife_biosphere/ant_sandbox/world.py)
- [simulation.py](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/src/alife_biosphere/ant_sandbox/simulation.py)
- [observer.py](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/src/alife_biosphere/ant_sandbox/observer.py)
- [reporting.py](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/src/alife_biosphere/ant_sandbox/reporting.py)
- [validation.py](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/src/alife_biosphere/ant_sandbox/validation.py)
- [showcase.py](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/src/alife_biosphere/ant_sandbox/showcase.py)
- [checkpoint.py](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/src/alife_biosphere/ant_sandbox/checkpoint.py)
- [comparison.py](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/src/alife_biosphere/ant_sandbox/comparison.py)
- [open_endedness.py](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/src/alife_biosphere/ant_sandbox/open_endedness.py)

Main runnable scripts:

- [run_ant_sandbox_observer.py](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/scripts/run_ant_sandbox_observer.py)
- [run_ant_sandbox_live_observer.py](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/scripts/run_ant_sandbox_live_observer.py)
- [run_ant_sandbox_probe.py](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/scripts/run_ant_sandbox_probe.py)
- [run_ant_sandbox_validation_matrix.py](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/scripts/run_ant_sandbox_validation_matrix.py)
- [run_ant_sandbox_infinite_experiment.py](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/scripts/run_ant_sandbox_infinite_experiment.py)
- [run_ant_sandbox_checkpoint_observer.py](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/scripts/run_ant_sandbox_checkpoint_observer.py)
- [run_ant_sandbox_branch_comparison.py](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/scripts/run_ant_sandbox_branch_comparison.py)
- [run_ant_sandbox_open_endedness_metrics.py](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/scripts/run_ant_sandbox_open_endedness_metrics.py)

## Documentation

Shortest re-entry path for the current ant sandbox line:

1. [docs/README.md](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/docs/README.md)
2. [docs/ant_sandbox_status_v1.md](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/docs/ant_sandbox_status_v1.md)
3. [docs/ant_sandbox_handoff_plan_v1.md](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/docs/ant_sandbox_handoff_plan_v1.md)
4. [docs/ant_sandbox_open_evolution_engineering_plan_v1.md](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/docs/ant_sandbox_open_evolution_engineering_plan_v1.md)
5. [docs/ant_sandbox_m12_checkpoint_observer_slice_2026-04-24.md](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/docs/ant_sandbox_m12_checkpoint_observer_slice_2026-04-24.md)
6. [docs/ant_sandbox_m12_checkpoint_observer_spec_v1.md](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/docs/ant_sandbox_m12_checkpoint_observer_spec_v1.md)
7. [docs/ant_sandbox_m13_branch_comparison_slice_2026-04-24.md](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/docs/ant_sandbox_m13_branch_comparison_slice_2026-04-24.md)
8. [docs/ant_sandbox_m13_branch_comparison_spec_v1.md](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/docs/ant_sandbox_m13_branch_comparison_spec_v1.md)
9. [docs/ant_sandbox_m14_niche_substrate_slice_2026-04-24.md](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/docs/ant_sandbox_m14_niche_substrate_slice_2026-04-24.md)
10. [docs/ant_sandbox_m14_niche_substrate_spec_v1.md](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/docs/ant_sandbox_m14_niche_substrate_spec_v1.md)
11. [docs/ant_sandbox_m15_open_endedness_metrics_slice_2026-04-24.md](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/docs/ant_sandbox_m15_open_endedness_metrics_slice_2026-04-24.md)
12. [docs/ant_sandbox_m15_open_endedness_metrics_spec_v1.md](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/docs/ant_sandbox_m15_open_endedness_metrics_spec_v1.md)
13. [docs/ant_sandbox_m16_successor_life_layer_spec_v1.md](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/docs/ant_sandbox_m16_successor_life_layer_spec_v1.md)
14. [docs/ant_sandbox_m10a_lifecycle_slice_2026-04-24.md](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/docs/ant_sandbox_m10a_lifecycle_slice_2026-04-24.md)
15. [docs/ant_sandbox_m10b_genome_v1_slice_2026-04-24.md](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/docs/ant_sandbox_m10b_genome_v1_slice_2026-04-24.md)
16. [docs/ant_sandbox_m10c_mutation_ablation_slice_2026-04-24.md](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/docs/ant_sandbox_m10c_mutation_ablation_slice_2026-04-24.md)
17. [docs/ant_sandbox_m11_infinite_experiment_runtime_slice_2026-04-24.md](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/docs/ant_sandbox_m11_infinite_experiment_runtime_slice_2026-04-24.md)

If you need the full document catalog:

- [docs/document_catalog_v1.md](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/docs/document_catalog_v1.md)

## Near-Term Roadmap

The current near-term work is not culture, learning, or heavy social systems.

It is:

- M15 open-endedness metrics
- M16 first successor life layer after substrate evidence exists
- M14 is now in place as the first substrate layer for derived niches
- M15 is now in place as the open-endedness metrics layer
- conflict as optional later pressure rather than the current branch center

## Legacy Note

This repository still contains the earlier ecology-graph line, observer, and
probe scripts. They remain useful as historical scaffolding, but they are not
the current product direction on the active ant-sandbox branch.

Development workflow files:

- [CONTRIBUTING.md](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/CONTRIBUTING.md)
- [.github/workflows/ci.yml](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/.github/workflows/ci.yml)
- [.github/pull_request_template.md](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/.github/pull_request_template.md)
