# Alife Biosphere

`alife_biosphere` is currently being developed as an instinct-first ant sandbox.

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
surface ecology -> food competition -> multi-colony overlap -> conflict ->
death consequences -> inherited instinct variation -> long-run evolution
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

The current visible world also includes:

- three colonies: `Wei`, `Shu`, `Wu`
- a larger `128 x 96` showcase map
- terrain types such as `dense_grass`, `sand`, and `rock`
- wall-heavy showcase layouts for routing stress tests

For the current branch-level status page, see:

- [ant_sandbox_status_v1.md](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/docs/ant_sandbox_status_v1.md)

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
competition, terrain routing, and wall behavior.

### Live Observer

Generate the live file-refresh observer:

```bash
python scripts/run_ant_sandbox_live_observer.py
```

Open:

- [outputs/ant_sandbox_live_observer/live_observer.html](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/outputs/ant_sandbox_live_observer/live_observer.html)

This is useful for monitoring a single run while it is advancing.

## Run Probes

General showcase probe:

```bash
python scripts/run_ant_sandbox_probe.py
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

Main runnable scripts:

- [run_ant_sandbox_observer.py](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/scripts/run_ant_sandbox_observer.py)
- [run_ant_sandbox_live_observer.py](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/scripts/run_ant_sandbox_live_observer.py)
- [run_ant_sandbox_probe.py](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/scripts/run_ant_sandbox_probe.py)
- [run_ant_sandbox_validation_matrix.py](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/scripts/run_ant_sandbox_validation_matrix.py)

## Documentation

Shortest re-entry path for the current ant sandbox line:

1. [docs/README.md](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/docs/README.md)
2. [docs/ant_sandbox_status_v1.md](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/docs/ant_sandbox_status_v1.md)
3. [docs/ant_sandbox_world_design_v2.md](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/docs/ant_sandbox_world_design_v2.md)
4. [docs/ant_sandbox_build_plan_v2.md](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/docs/ant_sandbox_build_plan_v2.md)
5. [docs/ant_sandbox_m7_scale_up_spec_v1.md](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/docs/ant_sandbox_m7_scale_up_spec_v1.md)
6. [docs/ant_sandbox_long_horizon_construction_route_v1.md](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/docs/ant_sandbox_long_horizon_construction_route_v1.md)

If you need the full document catalog:

- [docs/document_catalog_v1.md](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/docs/document_catalog_v1.md)

## Near-Term Roadmap

The current near-term work is not culture or heavy social systems.

It is:

- stronger multi-source resource competition
- clearer multi-colony overlap
- better obstacle routing under pressure
- conflict after competition is already legible
- stronger death consequences before inheritance
- inherited instinct variation only after those pressures matter

## Legacy Note

This repository still contains the earlier ecology-graph line, observer, and
probe scripts. They remain useful as historical scaffolding, but they are not
the current product direction on the active ant-sandbox branch.

Development workflow files:

- [CONTRIBUTING.md](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/CONTRIBUTING.md)
- [.github/workflows/ci.yml](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/.github/workflows/ci.yml)
- [.github/pull_request_template.md](/Users/qlqwpy/Documents/游乐园/alife_biosphere_working_copy_20260420_230919/.github/pull_request_template.md)
