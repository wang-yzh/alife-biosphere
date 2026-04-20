# Alife Biosphere Build Plan v1

## Status Note

This is a mechanism-heavy planning line centered on inheritance, signaling,
trust, archive structure, and related higher-order systems.

It remains useful as a supporting reference, but it is no longer the current
project plan after the ecology-first realignment on 2026-04-21.

Use these documents for the current plan:

- `ecology_north_star_v1.md`
- `build_plan_v2.md`
- `observable_phenomena_and_failure_modes_v1.md`
- `m1_ecology_kernel_spec_v2.md`

## Purpose

This document upgrades `build_plan_v0.md` after:

- the second literature pass
- the current M0 scaffold already present in the repository

`v0` assumed that group logic, disturbance, and trust-sensitive communication
could arrive later.
`v1` moves them earlier because delaying them would hard-code the wrong world.

Kernel-specific implementation reference:

```text
docs/m1_biosphere_kernel_spec.md
```

## 1. Current Starting Point

The repository already has an M0 executable scaffold.

That means `v1` is not planning from zero.
It is planning from:

- deterministic config and RNG
- bounded habitats
- founder organism initialization
- basic event emission
- smoke simulation
- passing tests

This is good.
It lets us move directly into mechanism-bearing milestones.

## 2. Revised Milestone Order

## M1. Biosphere kernel with graph and disturbance support

Scope:

- habitat graph edges
- movement and migration rules
- carrying-capacity pressure
- habitat memory traces
- disturbance scheduling hooks
- refuge designation

Required outputs:

- graph-aware world state
- reproducible disturbance schedule
- updated event schema for movement and habitat pressure

Exit criteria:

- graph updates are deterministic under seed
- refuge fraction stays above configured minimum in default probes
- habitat pressure produces non-trivial occupancy differences

## M2. Lifecycle plus group scaffolding

Scope:

- reproduction preparation
- death causes
- life-stage records
- `group_id`
- founder history
- bottleneck metadata
- `trust_profile` scaffold

Required outputs:

- organism state extension
- group registration events
- founder and bottleneck logging

Exit criteria:

- organisms can survive, die, and prepare reproduction
- group membership changes are logged
- founder history survives serialization

## M3. Lineage, rescue, and interaction logging

Scope:

- lineage graph
- rescue-event detection
- interaction-network reconstruction
- disturbance summaries

Required outputs:

- lineage summaries
- rescue summaries
- interaction-edge extraction from events

Exit criteria:

- births and deaths reconcile with lineage counts
- rescue events can be identified from logs
- interaction graphs can be reconstructed for a probe run

## M4. Latent protocols, signaling, and somatic learning

Scope:

- protocol banks
- low-bandwidth signaling
- trust-sensitive signal interpretation
- short-term memory
- costly protocol discovery

Required outputs:

- signal event family
- protocol probe
- signaling ablation

Exit criteria:

- signaling measurably changes coordination outcomes
- deceptive signaling can occur and be logged
- learning remains costly

## M5. Vertical inheritance and critical social learning

Scope:

- compact inherited capsules
- provisional copied capsules
- validation, retention, discard logic
- forgetting path

Required outputs:

- inheritance probe
- no-copy vs unconditional-copy vs validated-copy ablation

Exit criteria:

- validated copying outperforms unconditional copying in at least one treatment
- inherited priors help offspring without trivializing habitats
- stale copied information remains observable as a failure mode

## M6. Disturbance and rescue experiments

Scope:

- local crashes
- regional stress
- refuge migration
- founder bottleneck treatments
- rescue-source classification

Required outputs:

- rescue probe
- bottleneck probe
- rebound summaries

Exit criteria:

- U-shaped decline-and-rebound trajectories appear in at least some seeds
- rescue sources can be assigned from logs in simple cases
- asynchronous disturbances preserve more lineage depth than synchronized
  controls in at least one setting

## M7. Cultural archive with bounded access

Scope:

- archive storage
- visibility limits
- source attribution
- access gating
- overload controls

Required outputs:

- archive probe
- overload probe
- trust-sensitive archive access

Exit criteria:

- archive improves resilience only when validation exists
- overload can be induced in controls
- trust history affects archive outcomes

## M8. Antagonists and parasite ecology

Scope:

- parasite / thief / mimic / jammer roles
- graph-dependent antagonist spread
- defense and deception logging

Required outputs:

- antagonist probe
- topology-dependent parasite summaries

Exit criteria:

- antagonist pressure changes diversity or complexity metrics
- parasite relations are reconstructable from event and network data

## M9. Habitat coevolution

Scope:

- bounded habitat diversification
- occupancy-dependent habitat change
- graph-aware environmental branching

Required outputs:

- coevolution probe
- comparison against static graph treatments

Exit criteria:

- habitat novelty appears without global collapse
- rescue structure still functions after diversification

## 3. New Mandatory Controls

### Communication controls

- no signaling
- honest-only signaling
- deception enabled
- covert signaling enabled

### Disturbance controls

- no disturbance
- synchronized disturbance
- asynchronous disturbance
- asynchronous disturbance with refuges removed

### Social-learning controls

- no copying
- unconditional copying
- validated copying
- validated copying with stale archive

### Topology controls

- one baseline hand-designed graph
- one modular graph
- one dendritic graph

## 4. New Required Probe Scripts

After `v1`, the probe suite should include:

- `run_signal_probe.py`
- `run_bottleneck_probe.py`
- `run_rescue_probe.py`
- `run_topology_probe.py`

The old smoke run stays useful, but it is no longer enough evidence.

## 5. Immediate Next Build Slice

The next coding slice should produce:

1. graph-aware habitat state
2. disturbance scheduler
3. organism records with `group_id`
4. trust-profile scaffold
5. expanded event schema for movement, pressure, and founder history

This slice is still small enough to implement cleanly, but it prevents us from
building a substrate that later has to be rewritten.
