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
- first successor life layer through corpse-dependent decomposer patches
- multi-niche open evolution campaign orchestration across root and fork branches
- stabilized showcase economy with lower late-stage starvation pressure

The current visible world also includes:

- three colonies: `Wei`, `Shu`, `Wu`
- a larger `128 x 96` showcase map
- terrain types such as `dense_grass`, `sand`, and `rock`
- wall-heavy showcase layouts for routing stress tests

Latest showcase lifecycle snapshot:

- `births=50`
- `deaths=46`
- `death_reasons={'old_age': 20, 'starvation': 26}`
- `final_population_by_colony={'wei': 15, 'shu': 9, 'wu': 12}`
- `pickups=1117`
- `unloads=1086`

For the current branch-level status page, see:

- [ant_sandbox_status_v1.md](docs/ant_sandbox_status_v1.md)
- [ant_sandbox_handoff_plan_v1.md](docs/ant_sandbox_handoff_plan_v1.md)
- [ant_sandbox_open_evolution_engineering_plan_v1.md](docs/ant_sandbox_open_evolution_engineering_plan_v1.md)
- [ant_sandbox_open_evolution_engineering_plan_v2.md](docs/ant_sandbox_open_evolution_engineering_plan_v2.md)

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

- [outputs/ant_sandbox_observer/observer.html](outputs/ant_sandbox_observer/observer.html)

This is the best entry point if you want to inspect colony traffic, food
competition, terrain routing, wall behavior, and lifecycle turnover.

### Live Observer

Generate the live file-refresh observer:

```bash
python scripts/run_ant_sandbox_live_observer.py
```

Open:

- [outputs/ant_sandbox_live_observer/live_observer.html](outputs/ant_sandbox_live_observer/live_observer.html)

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

- [outputs/ant_sandbox_infinite_experiment](outputs/ant_sandbox_infinite_experiment)

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

- [outputs/ant_sandbox_checkpoint_observer](outputs/ant_sandbox_checkpoint_observer)

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

- [outputs/ant_sandbox_branch_comparison](outputs/ant_sandbox_branch_comparison)

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

- [outputs/ant_sandbox_open_endedness](outputs/ant_sandbox_open_endedness)

### Multi-Niche Open Evolution Campaign

Run a root branch plus fork family, then emit observers, comparison, and metrics:

```bash
python scripts/run_ant_sandbox_multi_niche_open_evolution.py --campaign-id m17_smoke --root-tick 40 --fork-additional-ticks 20 --fork-seeds 11 29
```

Outputs are written under:

- [outputs/ant_sandbox_multi_niche_open_evolution](outputs/ant_sandbox_multi_niche_open_evolution)

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

- [outputs/ant_sandbox_probe](outputs/ant_sandbox_probe)
- [outputs/ant_sandbox_inheritance_probe](outputs/ant_sandbox_inheritance_probe)
- [outputs/ant_sandbox_pheromone_probe](outputs/ant_sandbox_pheromone_probe)
- [outputs/ant_sandbox_persistence_probe](outputs/ant_sandbox_persistence_probe)
- [outputs/ant_sandbox_validation_matrix](outputs/ant_sandbox_validation_matrix)

## Repository Map

Core ant sandbox implementation:

- [config.py](src/alife_biosphere/ant_sandbox/config.py)
- [world.py](src/alife_biosphere/ant_sandbox/world.py)
- [simulation.py](src/alife_biosphere/ant_sandbox/simulation.py)
- [observer.py](src/alife_biosphere/ant_sandbox/observer.py)
- [reporting.py](src/alife_biosphere/ant_sandbox/reporting.py)
- [validation.py](src/alife_biosphere/ant_sandbox/validation.py)
- [showcase.py](src/alife_biosphere/ant_sandbox/showcase.py)
- [checkpoint.py](src/alife_biosphere/ant_sandbox/checkpoint.py)
- [comparison.py](src/alife_biosphere/ant_sandbox/comparison.py)
- [open_endedness.py](src/alife_biosphere/ant_sandbox/open_endedness.py)
- [campaign.py](src/alife_biosphere/ant_sandbox/campaign.py)

Main runnable scripts:

- [run_ant_sandbox_observer.py](scripts/run_ant_sandbox_observer.py)
- [run_ant_sandbox_live_observer.py](scripts/run_ant_sandbox_live_observer.py)
- [run_ant_sandbox_probe.py](scripts/run_ant_sandbox_probe.py)
- [run_ant_sandbox_validation_matrix.py](scripts/run_ant_sandbox_validation_matrix.py)
- [run_ant_sandbox_infinite_experiment.py](scripts/run_ant_sandbox_infinite_experiment.py)
- [run_ant_sandbox_checkpoint_observer.py](scripts/run_ant_sandbox_checkpoint_observer.py)
- [run_ant_sandbox_branch_comparison.py](scripts/run_ant_sandbox_branch_comparison.py)
- [run_ant_sandbox_open_endedness_metrics.py](scripts/run_ant_sandbox_open_endedness_metrics.py)
- [run_ant_sandbox_multi_niche_open_evolution.py](scripts/run_ant_sandbox_multi_niche_open_evolution.py)

## Documentation

Shortest re-entry path for the current ant sandbox line:

1. [docs/README.md](docs/README.md)
2. [docs/ant_sandbox_status_v1.md](docs/ant_sandbox_status_v1.md)
3. [docs/ant_sandbox_handoff_plan_v1.md](docs/ant_sandbox_handoff_plan_v1.md)
4. [docs/ant_sandbox_open_evolution_engineering_plan_v2.md](docs/ant_sandbox_open_evolution_engineering_plan_v2.md)
5. [docs/ant_sandbox_open_evolution_engineering_plan_v1.md](docs/ant_sandbox_open_evolution_engineering_plan_v1.md)
6. [docs/ant_sandbox_m17_multi_niche_open_evolution_slice_2026-04-25.md](docs/ant_sandbox_m17_multi_niche_open_evolution_slice_2026-04-25.md)
7. [docs/ant_sandbox_m18_economic_stabilization_slice_2026-04-25.md](docs/ant_sandbox_m18_economic_stabilization_slice_2026-04-25.md)
8. [docs/ant_sandbox_m16_successor_life_layer_slice_2026-04-24.md](docs/ant_sandbox_m16_successor_life_layer_slice_2026-04-24.md)
9. [docs/ant_sandbox_m15_open_endedness_metrics_slice_2026-04-24.md](docs/ant_sandbox_m15_open_endedness_metrics_slice_2026-04-24.md)
10. [docs/ant_sandbox_m14_niche_substrate_slice_2026-04-24.md](docs/ant_sandbox_m14_niche_substrate_slice_2026-04-24.md)
11. [docs/ant_sandbox_m13_branch_comparison_slice_2026-04-24.md](docs/ant_sandbox_m13_branch_comparison_slice_2026-04-24.md)
12. [docs/ant_sandbox_m12_checkpoint_observer_slice_2026-04-24.md](docs/ant_sandbox_m12_checkpoint_observer_slice_2026-04-24.md)

If you need the full document catalog:

- [docs/document_catalog_v1.md](docs/document_catalog_v1.md)

## Near-Term Roadmap

The current near-term work is not culture, learning, or heavy social systems.

It is:

- M18 economic stabilization
- M19 fungus layer
- M20 dual dependency-chain campaign
- M17 is now in place as the forked multi-niche campaign layer
- conflict as optional later pressure rather than the current branch center

## Legacy Note

This repository still contains the earlier ecology-graph line, observer, and
probe scripts. They remain useful as historical scaffolding, but they are not
the current product direction on the active ant-sandbox branch.

Development workflow files:

- [CONTRIBUTING.md](CONTRIBUTING.md)
- [.github/workflows/ci.yml](.github/workflows/ci.yml)
- [.github/pull_request_template.md](.github/pull_request_template.md)
