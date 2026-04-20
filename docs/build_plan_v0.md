# Alife Biosphere Build Plan v0

## Status Note

This is a historical milestone plan.

It remains useful for provenance and for comparing earlier assumptions against
the later `v1` milestone order, but it is not the current build contract.

Use these documents for the current project plan:

- `build_plan_v1.md`
- `current_build_status_and_next_steps.md`
- `m1_biosphere_kernel_spec.md`

## 1. Delivery Strategy

We should treat this as an experimental systems project with strict gates.

Each milestone must produce:

- code
- tests
- at least one probe script
- one short decision note describing what worked and what failed

No milestone should introduce a major mechanism without its control condition.

Inheritance-specific design reference:

```text
docs/inheritance_architecture_v0.md
```

Kernel-specific design reference:

```text
docs/m1_biosphere_kernel_spec.md
```

## 2. Milestone Sequence

## M0. Repository skeleton and reproducibility

Deliverables:

- package layout
- project config
- deterministic seeding utilities
- smoke test entrypoint
- one saved probe config

Exit criteria:

- seeded runs are reproducible
- config can be serialized and reloaded
- event logs write to disk cleanly

## M1. Biosphere kernel

Scope:

- world clock
- habitat graph
- bounded climate update
- resource regeneration
- carrying capacity pressure

Deliverables:

- `world.py`
- `habitat.py`
- `config.py`
- world invariant tests

Exit criteria:

- no negative resource values
- no unbounded climate drift
- at least one refuge remains viable under default settings

## M2. Organism lifecycle

Scope:

- genome and phenotype separation
- energy / matter / integrity / information accounting
- age and life-stage transitions
- movement, probe, harvest, repair, reproduction preparation
- death resolution

Deliverables:

- `organism.py`
- `genome.py`
- `controller.py`
- lifecycle tests

Exit criteria:

- organisms can survive, age, reproduce, and die
- death causes are logged distinctly
- resource accounting is conservation-safe under tests

## M3. Event logging and lineage

Scope:

- event schema from `world_design_v0.md`
- lineage graph
- parent-child relationships
- mutation logging
- population summary metrics

Deliverables:

- `events.py`
- `lineage.py`
- `metrics.py`
- lineage probe script

Exit criteria:

- every organism has traceable ancestry
- birth and death totals reconcile over time
- lineage depth and branch factor can be computed from saved logs

## M4. Latent protocols and somatic learning

Scope:

- habitat protocol banks
- protocol discovery through interaction
- short-term organism memory
- learning cost
- protocol usage metrics

Deliverables:

- `memory.py`
- protocol implementation inside habitats or dedicated module
- protocol probe script
- learning ablation

Exit criteria:

- learned agents outperform random action on protocol exploitation
- learning has measurable cost
- benefits remain local without inheritance

## M5. Vertical inheritance by compression

Scope:

- start from clonal vertical inheritance
- add mutation plus duplication/divergence logging
- convert successful experience into compact capsules
- transmit capsules at reproduction with bandwidth limit
- compare against no inheritance and raw-state inheritance

Deliverables:

- `inheritance.py`
- inheritance ablation script
- decision note on transfer quality

Exit criteria:

- offspring adaptation speed improves over no-inheritance control
- compressed inheritance is more robust than raw-state cloning
- inherited capsules do not trivialize all habitats

Guardrail:

```text
do not add homologous crossover until innovation ids or equivalent gene
identity markers exist
```

## M6. Cultural archive

Scope:

- population or clade archive
- costly access rules
- horizontal transfer logging
- archive freeloading pathologies

Deliverables:

- `archive.py`
- archive access probe
- archive controls

Exit criteria:

- archive improves resilience under shocks
- archive access has non-trivial cost
- exploitation events are visible in logs

## M7. Habitat coevolution

Scope:

- habitat mutation or diversification
- bounded creation of new regimes
- population-habitat feedback loop

Deliverables:

- habitat diversification logic
- shock and coevolution probe scripts
- comparison against static habitats

Exit criteria:

- new habitat regimes appear without global collapse
- migration and re-specialization are measurable
- no single trivial policy dominates all generated habitats

## 3. Testing Strategy

We need three layers of testing from the beginning.

### Unit tests

- resource accounting
- mutation bounds
- protocol resolution
- inheritance bandwidth
- event schema integrity

### Property tests

- bounded state ranges
- no impossible negative conservation states
- deterministic replay under identical seed

### Probe tests

- short seeded simulations that write metrics and summary tables
- these are not unit tests, but they are required evidence

## 4. Decision Gates

We should stop and review before moving on if any of these happens:

- default world collapses to extinction in most seeds
- one lineage dominates every habitat early
- inheritance has no measurable effect
- archive access makes learning effectively free
- metrics cannot explain observed behavior

If a gate fails, we revise the mechanism before adding complexity.

## 5. First Implementation Slice

The smallest worthwhile first slice is:

1. 7 habitats from the default template
2. 32 founders in two nursery habitats
3. 4 organism state variables
4. fixed small controller
5. no archive yet
6. latent protocols enabled
7. full event logging enabled

This slice is enough to test whether a lived episode can become a useful
parent-to-child prior.

## 6. Expected Early Outputs

Every probe run should at minimum emit:

- event log csv or parquet
- population summary csv
- lineage summary csv
- habitat occupancy summary csv
- one markdown decision note

Without this discipline, the system will quickly become impossible to reason
about.
