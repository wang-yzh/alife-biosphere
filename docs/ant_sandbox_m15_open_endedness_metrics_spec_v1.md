# Ant Sandbox M15 Open-Endedness Metrics Spec v1

## Purpose

M15 defines how this project will measure early open-endedness.

The goal is not to create one universal score.

The goal is to track whether branches accumulate new stepping stones:

```text
new stable structures
new resource dependencies
new spatial patterns
new lineage histories
new exploitable substrates
```

## Core Warning

Open-endedness is not:

- max food return
- max population
- max mutation count
- longest survival alone
- most combat wins

Those can be useful metrics, but none of them prove expanding ecological
possibility.

## Required Metric Families

M15 should include five metric families:

1. branch divergence
2. niche occupancy
3. stepping-stone persistence
4. ecological dependency
5. novelty without collapse

## Branch Divergence

Question:

```text
Do forks from the same checkpoint develop different ecological histories?
```

Metrics:

- final colony population vector
- food class use vector
- residue map signature
- corpse distribution signature
- trail corridor signature
- lineage depth vector
- generation distribution
- branch-to-branch distance over these signatures

Interpretation:

- divergence is necessary but not sufficient
- random collapse is divergence but not open-endedness

## Niche Occupancy

Question:

```text
Which ecological opportunities are being used?
```

Metrics:

- active food classes
- occupied resource patches
- used corridor count
- substrate-bearing cells
- corpse-use events after M16
- residue-use events after M16
- successor organism occupied zones after M16

Interpretation:

- more occupied niches can be positive
- but unstable noise should not be counted as a durable niche

## Stepping-Stone Persistence

Question:

```text
Does a new structure last long enough to support later structures?
```

Candidate structures:

- persistent trail corridors
- long-lived residue zones
- repeated food routes
- stable colony territory partitions
- recurring corpse fields
- successor organism patches after M16

Metrics:

- first tick observed
- last tick observed
- active duration
- recurrence count
- dependent event count

Interpretation:

- a stepping stone should persist or recur
- one-tick novelty is not enough

## Ecological Dependency

Question:

```text
Does one process depend on another process created earlier?
```

Dependency examples:

- decomposer exists because ants died
- fungus grows because trails or residues persist
- scavenger route follows battle or starvation zones
- plant spread depends on ant transport

Metrics:

- dependency edge count
- maximum dependency depth
- events by dependency type
- branch differences in dependency graph

Output shape:

```text
dependency_graph:
  corpse -> decomposer
  residue -> fungus
  ant_transport -> seed_patch
```

Interpretation:

- dependency depth is closer to open-endedness than raw performance

## Novelty Without Collapse

Question:

```text
Does novelty coexist with sustained ecology?
```

Metrics:

- alive counts remain bounded
- at least one colony persists
- at least one resource loop persists
- new structure appears without total ecosystem collapse
- branch remains checkpointable and observable

Interpretation:

- collapse can be informative
- but repeated collapse is not open-ended evolution

## Proposed Output

Add:

```text
outputs/ant_sandbox_open_endedness/
  metrics.json
  metrics.md
```

The first implementation may be generated from branch comparison outputs rather
than directly from simulation.

## Metric Status Labels

Each metric should carry a status:

- `available`
- `proxy`
- `requires_m14`
- `requires_m16`
- `not_implemented`

This prevents documents from implying that future metrics already exist.

## Tests

Required tests:

- metrics load branch comparison data
- metric status labels are present
- dependency metrics remain `requires_m16` before successor life exists
- no single scalar open-endedness score is emitted

Targeted test path:

```text
tests/test_ant_sandbox_open_endedness_metrics.py
```

## Acceptance Criteria

M15 is complete when:

- branch comparison can be converted into open-endedness metric families
- each metric is labeled by implementation status
- reports separate divergence, persistence, dependency, and collapse
- documentation explicitly avoids one-score fitness claims

## Failure Modes

Stop if:

- output ranks branches as winner and loser only
- metrics treat population growth as open-endedness
- metrics count every random new cell as novelty
- metrics do not distinguish durable structures from transient noise

## Execution Note

M15 should begin after M13 and at least the first M14 substrate.

It can define future metrics earlier, but implementation should label them
clearly when they depend on M16.
