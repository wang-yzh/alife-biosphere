# Alife Biosphere Build Plan v2

## Purpose

This document is the current build plan for the ecology-first direction of
`alife_biosphere`.

It supersedes `build_plan_v1.md` as the active milestone order.

The main change is simple:

```text
Do not treat inheritance, signaling, trust, or archive systems as the main
line before the ecosystem itself can survive, turn over, and leave history.
```

## 1. Current Starting Point

The project already has an M0 executable scaffold with:

- deterministic config and RNG
- bounded habitats
- founder initialization
- basic event emission
- smoke simulation
- passing basic tests

That is enough to begin building real ecology.

## 2. Milestone Order

## M1. Ecology kernel

Scope:

- habitat graph
- movement and migration costs
- occupancy pressure
- habitat families
- hazard and crowding damage
- life stages and death reasons
- reproduction readiness
- ecological probe outputs

Required result:

- a small world with visibly uneven habitat use and interpretable turnover

## M2. Reproduction and lineage

Scope:

- offspring creation
- parent-child recording
- lineage identity
- founder and bottleneck tracking
- reproduction cost balancing

Required result:

- populations can renew themselves without collapsing into fixed founders or
  instant explosion

## M3. Disturbance and recovery

Scope:

- local crashes
- regional stress
- resource depressions
- recolonization windows
- rescue and failure summaries

Required result:

- some seeds show real loss and non-trivial recovery without hidden resets

## M4. Habitat history and ecological memory

Scope:

- depletion traces
- occupancy-dependent habitat change
- recovery lag
- bounded habitat modification

Required result:

- later outcomes depend partly on what previously happened in each habitat

## M5. Niche formation and long-run ecology probes

Scope:

- longer-run probe scripts
- coexistence diagnostics
- lineage spread and local dominance summaries
- habitat-family usage summaries

Required result:

- the world can show persistent differentiation rather than immediate collapse
  to one generic strategy

## M6. Optional complexity modules

Candidate modules:

- compact inheritance
- signaling
- antagonists
- archive systems
- richer group scaffolding

Promotion rule:

- only add these if M1-M5 reveal a concrete ecological bottleneck that the new
  mechanism is meant to address

## 3. Mandatory Control Families

### Topology controls

- baseline hand-designed graph
- more modular graph
- more corridor-heavy graph

### Resource controls

- abundant baseline
- tighter carrying capacity
- stronger frontier/wild asymmetry

### Disturbance controls

- no disturbance
- local disturbance
- asynchronous multi-site disturbance

### Reproduction-cost controls

- cheaper reproduction
- baseline reproduction
- costlier reproduction

## 4. Promotion Gates

Advance only when the current milestone produces at least one phenomenon that a
human observer can directly recognize, not only a metric change.

Examples:

- M1 should show uneven habitat use
- M2 should show real turnover
- M3 should show loss and recolonization
- M4 should show habitat history
- M5 should show partial coexistence or durable differentiation

If a milestone cannot produce a clear visible phenomenon, the next layer should
not be added yet.

## 5. What Has Been De-Prioritized

Relative to `build_plan_v1.md`, the following are no longer main-line
requirements:

- early trust scaffolding
- early group scaffolding
- early signaling
- early archive systems
- early antagonist roles

They remain valid future modules.
They are no longer permitted to substitute for a thin ecology.

## 6. Practical Interpretation

The project should now be built as:

```text
watchable sandbox
  -> real ecology
  -> historical ecology
  -> optional higher-order mechanisms
```

That is the shortest route to a sustained artificial ecosystem.
