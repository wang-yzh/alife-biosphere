# Repository Architecture v0

## Status Note

This is a historical pre-scaffold planning note.

It was written before the M0 executable scaffold existed, so it no longer
matches the repository exactly.

Use these documents for the current project contract instead:

- `current_build_status_and_next_steps.md`
- `build_plan_v1.md`
- `m1_biosphere_kernel_spec.md`
- `../README.md`
- `README.md`

## Purpose

`world_design_v0.md` defines what the biosphere should mean.
`build_plan_v0.md` defines milestone order.

This document fills the missing middle layer:

```text
What files should exist first,
what each module owns,
and what the minimum implementation slice should look like.
```

The goal is to prevent the project from drifting into either:

- pure concept writing with no executable core, or
- premature feature growth with no stable architecture.

## Guiding Rule

The first implementation should favor:

- explicit state over hidden magic
- deterministic stepping over background processes
- append-only logs over mutable summaries
- small typed records over large implicit objects

## Initial Repository Layout

```text
alife_biosphere/
  README.md
  pyproject.toml
  src/
    alife_biosphere/
      __init__.py
      config.py
      rng.py
      world.py
      habitat.py
      organism.py
      genome.py
      controller.py
      events.py
      simulation.py
      io.py
  tests/
    test_config.py
    test_rng.py
    test_world_invariants.py
    test_simulation_smoke.py
  scripts/
    run_smoke.py
  outputs/
    .gitkeep
  docs/
    world_design_v0.md
    build_plan_v0.md
    repository_architecture_v0.md
```

## Module Ownership

### `config.py`

Owns typed configuration objects only.

Must define:

- world config
- habitat config
- organism config
- simulation config

Must support:

- conversion to plain dictionaries
- round-trip serialization
- seeded reproducibility

Must not contain simulation logic.

### `rng.py`

Owns deterministic random-number construction.

Must provide:

- one canonical way to create seeded RNG instances
- child seed derivation from parent seed plus labels

This avoids ad hoc random state scattered across modules.

### `world.py`

Owns the top-level biosphere state.

Minimum responsibilities:

- global tick
- habitat collection
- organism collection
- pending births
- deaths resolved this tick
- event emission hooks

`World` should be a plain state container with light helper methods.

### `habitat.py`

Owns habitat state and local update rules.

Minimum fields:

- `habitat_id`
- `capacity`
- `resource_level`
- `hazard_level`
- `climate_state`
- `occupants`

Minimum behavior:

- bounded regeneration
- bounded climate drift
- occupancy pressure signal

### `organism.py`

Owns organism state and lifecycle bookkeeping.

Minimum fields:

- `organism_id`
- `lineage_id`
- `habitat_id`
- `energy`
- `matter`
- `integrity`
- `information`
- `age`
- `alive`

Minimum behavior:

- metabolism
- aging
- action application
- death threshold detection

### `genome.py`

Owns inherited structural parameters.

Version zero should keep this intentionally small.

Possible fields:

- controller size
- metabolism multiplier
- exploration bias
- consolidation bias

The first genome is not meant to be biologically realistic.
It is a bounded inherited parameter packet.

### `controller.py`

Owns action selection.

For version zero, keep it simple:

- fixed small policy
- random-but-seeded choice with genome biases
- no large learning machinery yet

The purpose is to exercise the lifecycle and logging pipeline before richer
behavior is added.

### `events.py`

Owns append-only event records.

Every event should be a typed record with:

- tick
- event type
- organism id
- habitat id
- payload

Version zero event types:

- `birth`
- `death`
- `move`
- `harvest`
- `tick_summary`

### `simulation.py`

Owns the deterministic stepping loop.

This module should:

- create a world from config
- run one tick
- run N ticks
- collect emitted events

This is the main integration point for tests and probe scripts.

### `io.py`

Owns serialization helpers.

Version zero only needs:

- config save/load
- event log write
- small summary write

Avoid mixing this into simulation code.

## Minimum Data Model

The smallest useful state is:

```text
World
  tick: int
  habitats: dict[str, Habitat]
  organisms: dict[str, Organism]
  events: list[Event]
```

```text
Habitat
  habitat_id: str
  capacity: int
  resource_level: float
  hazard_level: float
  climate_state: float
  occupants: tuple[str, ...]
```

```text
Organism
  organism_id: str
  lineage_id: str
  habitat_id: str
  genome: Genome
  energy: float
  matter: float
  integrity: float
  information: float
  age: int
  alive: bool
```

```text
Event
  tick: int
  event_type: str
  organism_id: str | None
  habitat_id: str | None
  payload: dict[str, object]
```

## M0 Implementation Contract

The first runnable milestone should not yet implement:

- inheritance packets
- cultural archive
- habitat coevolution
- protocol discovery
- learned priors

It should implement only enough to prove:

1. we can create a bounded world
2. organisms can live inside it for multiple ticks
3. seeded runs are reproducible
4. logs can be written and inspected

## First Smoke Scenario

The first smoke run should use:

- 3 habitats
- 8 organisms
- 20 ticks
- deterministic seed
- event logging enabled

Success means:

- no crash
- no negative resources
- at least one organism survives five ticks
- event log is written
- repeating the same seed produces the same summary

## Testing Contract

Before adding richer mechanisms, these tests must exist:

### `test_config.py`

- config round-trip preserves values
- invalid ranges raise errors

### `test_rng.py`

- same seed gives same child seeds
- different labels produce different child seeds

### `test_world_invariants.py`

- habitat resources stay bounded
- integrity never rises above max
- dead organisms remain dead

### `test_simulation_smoke.py`

- smoke run completes
- event log is non-empty
- run summary is deterministic

## What This Document Intentionally Leaves Open

This document does not yet freeze:

- the final genome representation
- the final learning mechanism
- social interaction details
- cultural archive access rules
- niche/species inference

Those belong to later milestones.

For now, the job is to produce a small clean kernel that later inheritance and
ecology layers can trust.
