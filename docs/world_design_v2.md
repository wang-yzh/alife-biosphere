# Artificial Life Biosphere Design v2

## 1. Status

This document is the current authoritative design for the ecology-first
direction of `alife_biosphere`.

`world_design_v1.md` remains useful as a mechanism-rich predecessor, but `v2`
is now the design contract for current planning.

## 2. Design Shift

The key shift from `v1` to `v2` is:

```text
The project should first prove that a persistent ecology can form.
Only then should it decide which advanced inheritance or communication
mechanisms are worth introducing.
```

This means the world is no longer defined primarily by:

- multiple inheritance channels
- trust-sensitive signaling
- archive structure
- early group scaffolding

It is defined first by:

- habitat differences
- resource pressure
- movement and recolonization
- birth, death, and turnover
- disturbance and recovery
- lineage and habitat history

## 3. Primary Research Questions

The project now treats these as the core questions:

1. Can a small artificial world sustain non-trivial ecological structure over
   long runs?
2. Can different habitats support different local population outcomes?
3. Can disturbance create real loss without collapsing the world into either
   trivial reset or permanent death?
4. Can lineages accumulate, split, and disappear in ways that matter
   ecologically?
5. Can habitats retain state shaped by prior occupancy and depletion?

Advanced inheritance, signaling, trust, and archive design remain important,
but they are now subordinate questions.

## 4. Current Ontology

```text
Biosphere
  -> HabitatGraph
  -> Habitats
  -> Organisms
  -> Lineages
  -> DisturbanceEngine
  -> EventLog
  -> DerivedViews
```

## 4.1 Organism

The organism should stay compact and ecologically legible:

```text
Organism =
  genome
  controller
  energy
  matter
  integrity
  age
  lineage_id
  parent_id
  habitat_id
  life_stage
  alive
```

Possible later additions:

- lifetime memory
- inherited priors
- signaling state
- role or group metadata

These are not required to define the first real ecology.

## 4.2 Habitat

Habitats are first-class ecological regions, not cosmetic map tiles:

```text
Habitat =
  habitat_id
  habitat_family
  capacity
  resource_level
  max_resource_level
  hazard_level
  climate_state
  neighbors
  occupancy_pressure
  recent_occupancy
  depletion_trace
  refuge_score
```

Possible later additions:

- memory_field
- signal_trace
- parasite_pressure
- protocol_bank

Those become worthwhile only if simpler habitat history is already meaningful.

## 4.3 Lineage

Lineage must exist as a real state/history concept much earlier than archive or
group theory.

Minimum meaning:

- births know their parent
- descendants retain lineage identity
- founder and bottleneck history are reconstructable

## 4.4 DisturbanceEngine

Disturbance is core because resilience cannot be inferred from calm worlds
alone.

Minimum disturbance family:

- local crash
- regional stress
- resource depression
- recolonization window

Disturbance should expose structure, not act as hidden balancing logic.

## 4.5 DerivedViews

Several things should initially be derived analyses rather than first-class
entities:

- niche clusters
- species labels
- interaction networks
- group candidates

This avoids prematurely hard-coding social or taxonomic structure that should
first emerge from the ecology.

## 5. Core Design Rules

## Rule 1. Ecology before mechanism stack

Do not add advanced mechanisms to compensate for a thin world.

## Rule 2. No single global objective

Selection pressure should remain local, ecological, and state-dependent.

## Rule 3. Costs before capabilities

Movement, reproduction, occupancy, and survival costs must exist before richer
coordination or learning features.

## Rule 4. History before interpretation

The system must log enough raw events that lineage, disturbance, and habitat
history can be reconstructed without story inflation.

## Rule 5. Derived structure before hard-coded classes

Infer groups, niches, and species-like patterns from trajectories before making
them mandatory objects.

## Rule 6. Disturbance without hidden rescue

Recovery should come from refuge structure, migration, retained variation, and
habitat state, not from invisible safety rails.

## Rule 7. Watchability matters

The world should be interpretable by direct observation as well as by metrics.
If it only looks interesting in a spreadsheet, the design is too indirect.

## 6. Optional Later Layers

These remain on the table, but they are not current requirements:

- compact inheritance channels
- critical social learning
- signaling and deception
- archive systems
- antagonists and parasites
- richer group-level structure

Each should be added only if the ecology-first world has already produced a
clear bottleneck or missing phenomenon that the new mechanism addresses.

## 7. Near-Term Implication

The next build stages should focus on:

- graph-aware habitat structure
- full organism lifecycle with reproduction
- lineage tracking
- disturbance and recovery
- habitat modification by occupancy and depletion

That is the shortest path to a real artificial ecosystem.
