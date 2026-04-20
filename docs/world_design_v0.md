# Artificial Life Biosphere Design v0

## Status Note

This is the baseline design note kept for design lineage.

It is still useful for seeing the first-world assumptions clearly, but
`world_design_v1.md` is the current authoritative design after later literature
and implementation planning updates.

Use these documents for the current design contract:

- `world_design_v1.md`
- `research_synthesis_v1.md`
- `m1_biosphere_kernel_spec.md`

## 1. Design Position

We are not building a game and we are not building a benchmark runner.

We are building an experimental substrate for one question:

> How can lived experience become heritable structure inside a persistent
> population?

This design deliberately separates itself from the archived `maze_novelty` and
`market_novelty` projects. Those projects remain historical references. The new
project starts from ecology, lineage, memory, and inheritance.

Companion documents:

- `docs/genetics_bibliography_v0.md`
- `docs/inheritance_architecture_v0.md`

## 2. What The Literature Forces Us To Respect

The design constraints below come directly from the major artificial-life and
open-ended-evolution results we reviewed.

### 2.1 No single global objective

- `Tierra`, `Avida`, `Novelty Search`, `MAP-Elites`, and `POET` all show that a
  single global objective collapses diversity too early.
- The biosphere must use local survival and reproduction pressure as the
  primary driver.
- Evaluation metrics are for researchers, not for organisms.

### 2.2 Experience must enter a transmissible channel

- `Avida` and later digital-evolution work show that long-run improvement comes
  from cumulative lineages, not isolated training runs.
- A learned policy that dies with the individual is not enough.
- The system needs vertical inheritance, optional horizontal transfer, and a
  persistent lineage log.

### 2.3 Resource limitation is not optional

- `Tierra`, `Polyworld`, and related systems only produce ecological structure
  when memory, energy, space, and replication all have cost.
- Free learning and free copying destroy selective meaning.

### 2.4 Diversity needs structure, not slogans

- `MAP-Elites` shows that diversity becomes useful when niches are explicitly
  maintained.
- The biosphere needs habitat diversity, carrying capacity, migration, and a
  niche archive.

### 2.5 Strange behavior is data

- Digital-evolution studies repeatedly show exploitation, parasitism, and
  unexpected shortcuts.
- The system must log pathologies and ecological anomalies rather than silently
  filtering them out.

## 3. Research Hypotheses

### H1. Heritable compressed experience beats direct weight inheritance

Offspring should adapt faster when they inherit compact behavioral priors or
skill capsules than when they inherit raw controller state alone.

### H2. Ecological archives preserve innovation better than leaderboards

Niche-preserving populations should survive regime shifts and continue
innovating longer than winner-take-all populations.

### H3. Development matters

Different juvenile environments should produce different adult capacities even
under related genomes, allowing lineage specialization.

### H4. Habitat variation must be bounded

Open-ended behavior requires variation, but numerical stability requires
bounded resources, bounded damage, and refuges from total extinction.

## 4. Core World Model

## 4.1 Main entities

```text
Biosphere
  -> HabitatGraph
  -> Organisms
  -> Species / Clades
  -> CulturalArchive
  -> LineageGraph
  -> EventLog
```

### Biosphere

The top-level simulation state. It owns global time, habitats, populations,
global event streams, and experiment configuration.

### Habitat

A local ecological region with its own:

- resource profile
- hazard profile
- carrying capacity
- latent protocol family
- climate dynamics
- migration edges
- ecological memory

### Organism

The fundamental life unit:

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
```

### Species / Clade

Not a hard-coded class label. It is inferred online from genotype distance,
behavior distance, and reproductive continuity.

### CulturalArchive

A population-level repository of reusable behavior capsules. This is not free.
Access requires time, energy, or social exposure.

### LineageGraph

A first-class record of ancestry, mutation events, inherited capsules,
developmental environments, and survival outcomes.

### EventLog

An append-only log of:

- birth
- death
- migration
- exposure
- skill acquisition
- reproduction
- mutation
- parasitism
- archive access
- habitat collapse or shock

## 4.3 Inheritance channels

Inheritance in the biosphere is explicitly multi-channel:

| Channel | Timescale | What it carries | Default v0 status |
| --- | --- | --- | --- |
| genetic | long | modular structural biases, controller priors, developmental rules | implement first |
| epigenetic | short | decaying parental stress and developmental bias | implement after clonal genetics |
| somatic | within-lifetime | learned local state and short-horizon adaptation | local only, not directly inherited |
| ecological | medium to long | habitat modifications and persistent traces | present from the start through habitat memory |
| cultural | medium | archive capsules and socially accessible skill fragments | implement after basic vertical inheritance |

This split exists to prevent one recurring mistake:

```text
treating every useful experience as if it should become genome
```

That would make the project look adaptive, but it would erase the difference
between structural inheritance, parental carryover, local learning, and shared
ecology.

## 4.2 Habitat graph

The world is not a continuous realistic planet. It is a graph of habitats:

```text
Habitat A -- Habitat B -- Habitat C
      \         |           /
        ---- Habitat D ----
```

Why a graph:

- easier to keep stable than full free-space simulation
- enough structure for migration and ecological isolation
- easy to add heterogeneous habitat families
- suitable for controlled experiments

Each habitat has:

- `capacity`: soft carrying capacity
- `climate_state`: bounded evolving regime
- `resource_vector`: local abundance
- `hazard_vector`: local risk
- `protocol_bank`: discoverable behavioral regularities
- `memory_field`: environmental traces left by prior populations

## 5. Numerical Design

The world must be stable enough to run long horizons and varied enough to
support specialization. We therefore use a small number of bounded state
variables with explicit costs.

## 5.1 Organism state variables

### `energy` in `[0, 100]`

- consumed every step by metabolism and action
- replenished by successful resource extraction
- required for learning, repair, and reproduction

### `matter` in `[0, 100]`

- substrate for growth, repair, and offspring construction
- more slowly accumulated than energy
- prevents pure energy-rich habitats from dominating reproduction

### `integrity` in `[0, 1]`

- health / structural viability
- reduced by hazards, conflict, and severe scarcity
- increased by repair actions that consume `energy` and `matter`
- death occurs at `integrity <= 0`

### `information` in `[0, 50]`

- acquired from novel, structured, or informative interactions
- required to consolidate experience into skill capsules
- decays slowly if unused
- makes learning an ecological act rather than a free side effect

### `age`

- measured in world ticks
- contributes to maturity, senescence, and life-stage transitions

## 5.2 Metabolic costs

At each step:

```text
metabolic_cost =
  base_cost
  + controller_complexity_cost
  + active_memory_cost
  + habitat_stress_modifier
```

Recommended initial values:

- `base_cost = 0.6`
- `controller_complexity_cost = 0.08 * controller_size`
- `active_memory_cost = 0.05 * active_memory_slots`
- `habitat_stress_modifier = 0.0 to 0.4`

This keeps complexity meaningful without making it impossible.

## 5.3 Action costs

Actions consume resources even when they fail:

- `move`: `energy -0.4`
- `probe`: `energy -0.5`
- `harvest`: `energy -0.6`
- `repair`: `energy -1.0`, `matter -0.6`
- `consolidate`: `energy -1.2`, `information -1.0`
- `reproduce_prepare`: variable by offspring budget

This matters because exploration must be expensive enough to select for useful
priors, but cheap enough that juvenile learning remains possible.

## 5.4 Resource channels

Each habitat exposes three resource channels and one risk channel:

- `fuel`: mainly replenishes `energy`
- `substrate`: mainly replenishes `matter`
- `signal`: mainly replenishes `information`
- `hazard`: mainly threatens `integrity`

Different habitats are defined by different mixtures:

- refuge habitats: moderate fuel, moderate substrate, low signal, low hazard
- frontier habitats: high signal, high hazard, uneven fuel
- nursery habitats: low hazard, medium signal, low carrying capacity
- depleted habitats: low fuel, low substrate, unstable occupancy

This is enough to support trade-offs without overcomplicating the substrate.

## 5.5 Bounded climate dynamics

Each habitat has a bounded climate process:

```text
state_t+1 =
  clamp(
    alpha * state_t
    + seasonal_component
    + neighbor_influence
    + bounded_noise
    + shock_event,
    lower_bound,
    upper_bound
  )
```

Rules:

- no unbounded growth
- no fully global synchronized collapse by default
- at least one refuge habitat must remain low-hazard at all times
- shocks are local or regional, not universal

This creates pressure without trivial extinction.

## 5.6 Initial world template

The first runnable world should be small and opinionated.

Recommended `v0.1` habitat set:

| Habitat | Role | Capacity | Fuel | Substrate | Signal | Hazard |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `nursery_0` | juvenile development | 12 | 0.55 | 0.45 | 0.65 | 0.10 |
| `nursery_1` | juvenile development | 12 | 0.50 | 0.50 | 0.60 | 0.12 |
| `refuge_0` | stable survival basin | 16 | 0.75 | 0.60 | 0.25 | 0.08 |
| `refuge_1` | stable survival basin | 14 | 0.68 | 0.62 | 0.30 | 0.10 |
| `frontier_0` | high-variance discovery | 10 | 0.82 | 0.40 | 0.90 | 0.60 |
| `frontier_1` | high-upside specialization | 8 | 0.65 | 0.35 | 0.95 | 0.72 |
| `volatile_0` | regime-shifting stress test | 10 | 0.45-0.85 | 0.20-0.70 | 0.40-0.90 | 0.15-0.80 |

Recommended graph:

```text
nursery_0 -- refuge_0 -- frontier_0 -- volatile_0
     |          |             |
nursery_1 -- refuge_1 -- frontier_1
```

World rules for the first build:

- reproduction is allowed in all habitats, but most efficient in refuges
- juvenile spawn is restricted to nursery habitats
- frontier habitats expose richer protocols but harsher damage
- `volatile_0` changes regime every `40` to `80` ticks with bounded noise

## 5.7 Default starting population

Recommended defaults:

- `founder_genomes = 8`
- `copies_per_founder = 4`
- `initial_population = 32`
- `initial_age = juvenile`
- `initial_energy = 55`
- `initial_matter = 35`
- `initial_integrity = 1.0`
- `initial_information = 5`

Initialization policy:

- founders are distributed only across nurseries
- each founder genome starts with no learned capsules
- genome diversity is seeded manually to avoid immediate collapse into clones

## 6. Where Experience Lives

This project only makes sense if we distinguish memory layers clearly.

## 6.1 Somatic memory

Private to the individual:

- short replay traces
- local model updates
- temporary beliefs about habitat protocols
- recent interaction summaries

Dies with the organism unless compressed.

## 6.2 Heritable memory

Passed from parent to child:

- behavior priors
- action-sequence templates
- habitat-response biases
- controller initialization hints
- compression rules

This is not a full checkpoint clone. It is a compact bias on development.

## 6.3 Cultural memory

Shared at the population or clade level:

- reusable skill capsules
- discovered protocol fragments
- anti-parasite countermeasures
- migration heuristics

Acquisition must be costly or gated by exposure, otherwise culture becomes a
free cheat code.

## 6.4 Ecological memory

Stored in the world itself:

- depleted zones
- trail signals
- altered resource schedules
- predator / parasite pressure left by prior populations

This lets populations inherit history indirectly through the environment.

## 7. Latent Protocols: The Key Mechanism

We need a mechanism that makes lived experience valuable without requiring a
human-designed task list.

Each habitat therefore contains a bank of latent protocols.

A latent protocol is a structured regularity such as:

- a sequence of actions that unlocks better harvest
- a context-conditioned response that avoids hazard
- a repeated migration pattern that exploits climate phase changes
- a social interaction pattern that enables safe archive transfer

Protocols are not revealed directly. Organisms must discover them through
interaction.

### Why protocols are central

- they make experience useful
- they allow pretraining to become development rather than checkpoint storage
- they let inheritance pass structure instead of exact solutions
- they create room for specialization across habitats

### Initial protocol format

For the first implementation, keep protocols simple:

- finite-state motifs
- short horizon sequence dependencies
- partial observability
- stochastic but bounded payoffs

Do not start with large symbolic grammars or complex physics.

### Initial protocol defaults

For `v0.1`:

- `protocols_per_habitat = 3`
- `protocol_length = 2 to 5`
- `protocol_overlap_between_related_habitats = 0.3 to 0.6`
- `protocol_reward_bonus = 4 to 12` resource units
- `protocol_discovery_noise = low but non-zero`

Protocol interpretation:

- short motifs should be learnable during one lifetime
- partial overlap should make transfer helpful without becoming exact replay
- protocol rewards should matter, but should never dominate plain survival

## 8. Organism Design

## 8.1 Genome

The genome is the heritable description, not the learned state.

Initial genome fields:

- controller architecture seed
- learning rate parameters
- memory capacity
- consolidation threshold
- reproduction threshold
- exploration bias
- migration bias
- repair bias
- protocol-attention weights

Genome mutation types:

- scalar perturbation
- threshold shift
- slot count expansion or contraction
- structural controller mutation at low frequency
- capsule transmission mutation

## 8.2 Phenotype

The phenotype is the expressed life form in the current world:

- instantiated controller
- active sensor mapping
- current behavior biases
- material and energetic state
- currently loaded skill capsules

Phenotype depends on both genome and developmental experience.

## 8.3 Controller

The first controller should be intentionally small:

- recurrent or stateful controller
- low-dimensional observations
- discrete action set
- optional internal memory state

We are not trying to win through model size. We are trying to observe ecology.

## 8.4 Life stages

Each organism has four stages:

1. `juvenile`
2. `mature`
3. `reproductive`
4. `senescent`

Stage transitions depend on:

- age
- integrity
- resource reserves
- prior developmental success

The juvenile stage is where pretraining becomes biologically meaningful.

## 9. Lifecycle

Each world tick runs a fixed phase order:

1. habitat update
2. local interactions and perception
3. organism action
4. resource and damage resolution
5. learning updates
6. consolidation opportunities
7. reproduction and mutation
8. death resolution
9. archive and lineage logging

## 9.1 Birth

Birth creates a new organism with:

- mutated genome
- inherited skill priors
- initial resource allocation from parent
- lineage metadata
- assigned nursery habitat

## 9.2 Development

The juvenile period serves as controlled early exposure:

- reduced hazard
- limited resource abundance
- high opportunity to sample protocols
- no guarantee of adulthood

This makes developmental history measurable.

## 9.3 Active ecological life

Adults must:

- maintain energy and integrity
- choose where to live or migrate
- exploit or discover protocols
- avoid overspecializing to one fragile niche

## 9.4 Reproduction

Reproduction requires all of:

- `energy >= 70`
- `matter >= 45`
- `integrity >= 0.7`
- age above maturity threshold

Parent invests:

- offspring construction budget
- inherited capsules
- optional cultural references

Reproduction is local and capacity-constrained. Overcrowding reduces success.

## 9.5 Death

Death conditions:

- starvation
- integrity collapse
- senescence
- failure during reproduction
- habitat catastrophe

Death is not a failure of the experiment. It is the core selection mechanism.

## 10. Diversity And Ecological Structure

We want diversity to persist because the world makes it useful, not because a
researcher force-balances every species manually.

## 10.1 Niche support

Niches emerge from differences in:

- habitat preference
- protocol family specialization
- reproduction timing
- learning style
- archive usage
- migration strategy

## 10.2 Anti-collapse mechanisms

The first version should include:

- soft carrying capacity per habitat
- local competition for resources
- at least one low-risk refuge
- frontier habitats with better upside and higher risk
- migration friction
- limited reproduction bandwidth

These are enough to prevent instant monoculture in many settings.

## 10.3 Parasitism and exploitation

We should allow, not forbid, behaviors such as:

- resource theft
- archive freeloading
- following others' trails
- low-investment reproduction strategies

But they must be observable and logged as explicit event types.

## 11. Stability Guardrails

To keep the system experimentally useful:

- all core resources are bounded
- every action has cost
- every habitat has bounded climate updates
- the world always contains some refuge capacity
- mutation rates are bounded and configurable
- archive access is never free
- inheritance bandwidth is capped
- protocol rewards saturate

Hard constraints are good here. We need reproducible science, not mystical
complexity.

## 12. Metrics

Metrics are for researchers. Organisms never optimize them directly.

## 12.1 Population metrics

- population size over time
- extinction count
- species count
- occupancy per habitat
- migration rate

## 12.2 Lineage metrics

- lineage depth
- branch factor
- lineage survival time
- ancestry concentration
- inherited capsule retention rate

## 12.3 Diversity metrics

- genotype diversity
- behavior diversity
- protocol diversity
- niche count
- archive diversity

## 12.4 Adaptation metrics

- juvenile-to-adult maturation rate
- adaptation lag after climate shock
- offspring time-to-stability
- survival after migration
- survival after habitat change

## 12.5 Memory and inheritance metrics

- consolidation success rate
- cost per consolidated capsule
- vertical transfer gain
- horizontal transfer gain
- ecological-memory reuse rate

## 12.6 Open-endedness proxies

We should be careful not to overclaim open-ended evolution. For now we only
track proxies:

- sustained novelty rate
- niche creation rate
- long-horizon non-collapse
- complexity trend under bounded cost
- repeated emergence of new protocol usage

## 12.7 Required event schema

The first implementation should log events in a normalized row format:

| Field | Meaning |
| --- | --- |
| `tick` | global simulation step |
| `event_type` | birth, death, move, harvest, consolidate, reproduce, mutate, etc. |
| `organism_id` | actor identifier |
| `parent_id` | parent for birth / inheritance events |
| `lineage_id` | persistent ancestry id |
| `species_id` | inferred species / clade id |
| `habitat_id` | local habitat |
| `protocol_id` | protocol touched, if any |
| `delta_energy` | state change |
| `delta_matter` | state change |
| `delta_integrity` | state change |
| `delta_information` | state change |
| `cause` | free-form short reason code |
| `payload` | structured json-like metadata |

If this schema is missing, later analysis will become guesswork.

## 13. Minimal Viable Experiment Ladder

We should not build everything at once. The right path is staged.

## Phase 0. Deterministic substrate sanity

Goal:

- validate world updates and conservation bounds

Pass criteria:

- no numerical explosions
- no unavoidable global extinction
- reproducible seeded runs

## Phase 1. Ecology without learning

Goal:

- show that simple inherited strategies can occupy multiple habitats

Pass criteria:

- at least two stable niches over long runs
- migration and local extinction both occur

## Phase 2. Add somatic learning

Goal:

- show that individuals can exploit latent protocols during life

Pass criteria:

- learned protocol usage beats random baseline
- learned benefits remain local without inheritance

## Phase 3. Add heritable compression

Goal:

- convert successful lifetime experience into inheritable priors

Pass criteria:

- offspring adapt faster than non-inheriting controls
- inherited priors help but do not fully solve all habitats

## Phase 4. Add cultural archive

Goal:

- enable costly horizontal transfer without removing selection pressure

Pass criteria:

- archive helps population resilience
- freeloading and unequal access become visible and measurable

## Phase 5. Add habitat coevolution

Goal:

- let the environment diversify in response to population history

Pass criteria:

- new habitat regimes appear
- populations split, migrate, and re-specialize
- no immediate collapse to one trivial meta-strategy

## 14. Implementation Plan

Recommended initial package layout:

```text
alife_biosphere/
  README.md
  docs/
    world_design_v0.md
  src/
    biosphere/
      config.py
      world.py
      habitat.py
      organism.py
      genome.py
      controller.py
      memory.py
      inheritance.py
      archive.py
      lineage.py
      events.py
      metrics.py
  scripts/
    run_probe.py
    run_shock_probe.py
    run_inheritance_ablation.py
  tests/
```

Build order:

1. `config.py`, `world.py`, `habitat.py`
2. `organism.py`, `genome.py`, `controller.py`
3. `events.py`, `lineage.py`, `metrics.py`
4. `memory.py`, `inheritance.py`
5. `archive.py`
6. probe scripts and ablations

## 15. Initial Experimental Controls

Every major mechanism must ship with a control.

### Inheritance controls

- no inheritance
- raw parameter inheritance
- compressed prior inheritance

### Archive controls

- no archive
- free archive access
- costly archive access

### Habitat controls

- static habitats
- bounded dynamic habitats
- coevolving habitats

### Population controls

- winner-take-all
- local ecological selection
- niche-preserving selection

Without these controls we will not know what actually caused improvement.

## 16. The Main Failure Modes We Must Watch

### Failure mode 1. Leaderboard disguised as ecology

If one scalar score determines almost all reproduction, the biosphere collapses
back into ordinary optimization.

### Failure mode 2. Free learning

If learning or archive access is too cheap, inheritance stops mattering.

### Failure mode 3. Dead inheritance

If inherited capsules are too specific, they overfit and become noise in new
habitats.

### Failure mode 4. Permanent monoculture

If refuge/frontier trade-offs are weak, one lineage will dominate everything.

### Failure mode 5. Chaos mistaken for richness

If climate shocks are too large or too global, diversity measurements become
meaningless because nothing persists long enough to evolve.

## 17. Immediate Next Step

The first implementation target should be:

> a small biosphere kernel with 4 to 8 habitats, bounded climate dynamics,
> organisms with energy/matter/integrity/information, and latent protocols but
> no cultural archive yet

This is the smallest substrate that can already test:

- survival
- specialization
- juvenile learning
- compressed vertical inheritance
- lineage accumulation

That is enough to tell us whether the new direction is real.
