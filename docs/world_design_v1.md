# Artificial Life Biosphere Design v1

## Status Note

This is a mechanism-rich predecessor to the current ecology-first design.

It remains useful as supporting design material, especially for later optional
mechanisms, but `world_design_v2.md` is now the current authoritative design
for planning and implementation.

## 1. Status

This document upgrades `world_design_v0.md`.

`v0` remains the baseline design note.
`v1` is the current authoritative design because later literature and the
existing M0 scaffold together force several mechanisms into the core.

The key shift from `v0` to `v1` is:

```text
The world should not only preserve organism history.
It should preserve organism history, group history, habitat history,
and disturbance history.
```

## 2. What Changed Since v0

Four topics moved from "future extensions" to "core requirements":

1. selective dual inheritance
2. deceptive and trust-sensitive signaling
3. bottlenecks, catastrophe, and rescue dynamics
4. topology-sensitive parasite and migration structure

This change is driven by:

- `literature_gap_review_v0.md`
- `literature_to_mechanism_matrix_v0.md`
- `founder_effects_and_lineage_turnover_review_v0.md`
- `literature_secondary_gaps_v1.md`

## 3. Updated Research Questions

`v1` keeps the original question:

> How can lived experience become heritable structure inside a persistent
> population?

But it now treats that as only one of four linked questions:

1. How does lifetime experience become vertical inheritance?
2. How does shared experience become cultural inheritance without collapsing
   into free copying?
3. Under what conditions does a kin group become a meaningful selectable unit?
4. What kind of disturbance regime creates resilience without killing long-run
   innovation?

## 4. Updated Ontology

```text
Biosphere
  -> HabitatGraph
  -> Organisms
  -> KinGroups
  -> Species / Clades
  -> CulturalArchive
  -> InteractionNetwork
  -> LineageGraph
  -> DisturbanceEngine
  -> EventLog
```

## 4.1 Organism

The core state remains bounded and intentionally compact:

```text
Organism =
  genome
  phenotype
  controller
  lifetime_memory
  inherited_priors
  energy
  matter
  integrity
  information
  age
  lineage_id
  species_id
  habitat_id
  group_id
  trust_profile
```

`group_id` and `trust_profile` are the two most important additions.

## 4.2 KinGroup

`v1` introduces a first-class group record:

```text
KinGroup =
  group_id
  lineage_anchor
  member_ids
  shared_resource_pool
  role_profile
  local_signal_codebook
  founder_width
  bottleneck_history
```

Why it is needed:

- division of labor
- offspring-group investment
- adaptive sacrifice
- local coordination
- founder and bottleneck history

Important caution:

- a group is not automatically a higher-level individual
- higher-level individuality must be inferred from persistence, dependence, and
  conflict suppression

## 4.3 Habitat

The habitat structure extends `v0`:

```text
Habitat =
  capacity
  climate_state
  resource_vector
  hazard_vector
  protocol_bank
  memory_field
  recent_occupancy
  depletion_trace
  signal_trace
  parasite_pressure
  refuge_score
```

New interpretation:

- `memory_field` stores ecological inheritance
- `recent_occupancy` and `depletion_trace` support state-dependent climate
- `signal_trace` and `parasite_pressure` support trust and antagonist dynamics
- `refuge_score` makes rescue structure measurable

## 4.4 InteractionNetwork

The world must be able to reconstruct:

- cooperation edges
- conflict edges
- parasitic edges
- signaling edges
- teaching / archive edges

Without this network layer, many later claims will remain hand-wavy.

## 4.5 DisturbanceEngine

The world now includes an explicit disturbance subsystem:

- local crashes
- regional stress
- parasite blooms
- resource collapses
- founder events
- recolonization windows

This is not cosmetic.
It is the mechanism that lets us study resilience, bottlenecks, and rescue.

## 5. Core Design Rules In v1

## 5.1 No single global objective

Unchanged from `v0`.

Organisms still respond to local survival and reproduction pressures.
Metrics remain research-facing only.

## 5.2 Culture is not free copying

All cultural transfer must be:

- bounded
- source-attributed
- validation-sensitive
- forgettable

The archive should behave like a biased and lossy opportunity structure, not a
downloadable skill tree.

## 5.3 Communication is allowed to fail

Signals can be:

- honest
- deceptive
- ambiguous
- covert
- stale

This is a design requirement, not a pathology reserve.

## 5.4 Rescue must emerge from structure

Recovery should emerge from:

- refuge availability
- migration opportunities
- retained variation
- ecological memory
- prior bottleneck history

It should not come from invisible safety rules.

## 5.5 Space is part of the mechanism

Graph topology changes:

- kin clustering
- local parasite pressure
- rescue flow
- colonization difficulty
- dispersal bottlenecks

Therefore topology must become an explicit experiment variable later.

## 6. Development, Learning, And Inheritance

## 6.1 Development

The juvenile stage is now interpreted as costly plasticity.

Juveniles should experience:

- lower hazard than frontier habitats
- high protocol exposure
- limited archive visibility
- strong phenotype shaping
- non-zero development cost

New developmental records:

- developmental habitat sequence
- phenotype divergence from founder expression
- plasticity cost paid
- maturation success

## 6.2 Vertical inheritance

Vertical inheritance remains compact.

Allowed:

- action priors
- bias templates
- protocol fragments
- developmental marks

Disallowed:

- full lifetime replay
- free archive cloning
- exact adult controller copies by default

## 6.3 Cultural inheritance

`v1` requires a critical social learning pipeline:

```text
observe / copy
  -> provisional capsule
  -> validation episode
  -> retain / modify / discard
```

This is the minimum needed to avoid nonadaptive cultural overload.

## 6.4 Forgetting

Forgetting is mandatory.

It should remove:

- stale capsules
- repeatedly failing copied routines
- obsolete trust estimates

Without forgetting, the archive becomes a graveyard of frozen noise.

## 7. Communication And Trust

## 7.1 Minimal signal alphabet

The first version should use only low-bandwidth primitives:

- `ping`
- `trail`
- `warn`
- `tag`

These are not words.
They are local coordination hints.

## 7.2 Trust profile

Each organism maintains compact trust estimates for:

- kin
- in-group
- out-group
- archive source reliability
- recent signal class reliability

Trust changes through interaction history.
It is not a fixed reputation label.

## 7.3 Signal verification

Reliability should come from trade-offs and verification opportunities, not
only from energy cost.

Receivers should be able to:

- follow a signal
- ignore a signal
- partially verify a signal
- downgrade trust after failure

## 7.4 Deception events

The system should log:

- misleading trail use
- false warning use
- signal jamming
- deceptive tag mimicry

These are scientific events, not just anomalies.

## 8. Disturbance, Bottlenecks, And Rescue

## 8.1 Lineage history fields

Each lineage or founder branch should track:

- founder size
- last bottleneck width
- cumulative severe bottlenecks
- source habitat
- time since last collapse
- inferred rescue source

## 8.2 Disturbance classes

Default disturbance families:

- `local_crash`
- `resource_collapse`
- `parasite_bloom`
- `signal_pollution`
- `regional_stress`

These should be asynchronous by default.

## 8.3 Rescue sources

Rescue should be classified when possible as:

- standing variation
- new mutation
- inherited prior
- cultural import
- refuge migration
- ecological-memory reuse

If we do not classify rescue, we will not know what the world is actually
selecting for.

## 8.4 Refuge rules

At least two refuge-capable habitats should exist in the default world.

Constraints:

- they should not fail synchronously under default settings
- at least one migration path from frontier to refuge should remain open
- refuge occupancy pressure should matter; refuges cannot be infinite safety

## 9. Spatial Topology

The minimal implementation may still use one hand-designed graph.
But `v1` freezes a later requirement: topology must become a treatment.

Target graph families:

- modular terrestrial-like graphs
- dendritic / river-like graphs

Why:

- host-parasite theory and recent network work both show that topology changes
  virulence, relatedness, and rescue behavior

## 10. Updated Numerical Layer

`v1` inherits all bounded resource variables from `v0` and adds bounded
interaction variables.

## 10.1 Group variables

- `shared_resource_pool` in `[0, 150]`
- `group_signal_load` in `[0, 50]`
- `group_cohesion` in `[0, 1]`

`group_cohesion` should be derived from recent cooperative and conflict events.

## 10.2 Archive variables

- `archive_visibility_limit = 3 to 7`
- `archive_validation_cost = energy 0.8 + information 0.4`
- `archive_copy_noise = low but non-zero`
- `archive_retention_decay = 0.01 to 0.03 per tick when unused`

## 10.3 Signaling variables

- `signal_emit_cost = energy 0.15`
- `signal_verify_cost = energy 0.25 + information 0.2`
- `signal_lifetime = 2 to 8 ticks`

## 10.4 Disturbance variables

Recommended starting defaults:

- `local_disturbance_rate = 0.015 per habitat per tick`
- `regional_disturbance_rate = 0.002 per tick`
- `disturbance_severity = bounded in [0.1, 0.6]`
- `minimum_refuge_fraction = 0.2 of habitats`
- `founder_bottleneck_width = 2 to 6`

These are starting values for probes, not final truths.

## 11. Updated Metrics

## 11.1 Group metrics

- group persistence
- fission / fusion rate
- role asymmetry score
- within-group conflict rate
- group-level reproduction success

## 11.2 Trust and signal metrics

- signal reliability
- deception rate
- verification success
- covert-signal usefulness
- trust drift

## 11.3 Bottleneck and rescue metrics

- bottleneck frequency
- median bottleneck width
- rescue probability
- rebound delay
- minimum post-shock population
- rescue-source composition

## 11.4 Spatial and antagonist metrics

- parasite occupancy by habitat
- parasite extinction rate
- graph-position survival bias
- refuge-to-frontier rescue flow
- local relatedness proxy

## 12. Updated Hypotheses

`v0` hypotheses remain active.
`v1` adds:

### H5. Critical social learning beats unconditional copying

Validated copying should outperform unconditional archive copying in at least
some changing environments.

### H6. Asynchronous disturbances with refuge structure preserve deeper lineages

Local crashes plus migration paths should support longer persistence than
uniform synchronized shocks.

### H7. Moderate bottlenecks trade short-run survival for long-run robustness

Some bottlenecked lineages should become more drift-robust even while becoming
more extinction-prone in the short term.

### H8. Topology changes antagonist evolution

Different habitat graph families should generate different parasite and trust
regimes.

## 13. Immediate Design Consequences

Compared with `v0`, the following are no longer optional:

1. `group_id` must enter the core data model early.
2. habitat state needs occupancy and depletion traces.
3. disturbance hooks must exist before full coevolution.
4. event logs must support interaction-network reconstruction.
5. signaling must appear before unrestricted archive design.

## 14. Immediate Next Spec Needed

Because an M0 scaffold already exists, the next most valuable design freeze is:

```text
docs/m1_biosphere_kernel_spec.md
```

That spec should freeze:

- graph edges
- migration rules
- carrying-capacity pressure
- death causes
- disturbance scheduling
- event schema expansion

## 15. Current Minimal Build Target

The immediate target after `v1` is:

> a small graph biosphere with habitat memory traces, local disturbances,
> bounded refuge structure, organisms carrying `group_id` and `trust_profile`,
> latent protocols, and rich event logging, but without full cultural archive
> recombination yet

That is the smallest substrate that still respects the literature gathered so
far.
