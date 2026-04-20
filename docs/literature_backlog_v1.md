# Literature Backlog v1

## Purpose

This document defines the next literature pass for `alife_biosphere`.

It is not a general bibliography.
It is a build-oriented reading backlog.

Each item is here because it should change at least one of the following:

- a core mechanism
- a state variable
- an event type
- an ablation or control
- a metric family

The project already has broad coverage in:

- digital evolution
- open-ended evolution
- niche construction
- multicellularity and individuality transitions
- cultural inheritance
- evolvability and modularity

What we need next is not more breadth.
What we need is sharper support for the next build decisions.

## Priority Summary

Recommended reading order:

1. founder effects and lineage turnover
2. resilience, collapse, and recovery
3. signaling, trust, and deception
4. dual inheritance with recombination and forgetting

That order is chosen to match the likely build order:

```text
lineage
-> habitat shock and recovery
-> communication and trust
-> archive and dual inheritance
```

## Theme 1. Founder Effects, Bottlenecks, and Lineage Turnover

## Why this theme matters

The project wants:

- migration between habitats
- lineage branching
- colonization of new habitats
- turnover rather than one permanent dominant lineage

But the current literature set does not yet give us a strong formal handle on:

- founder events
- bottleneck severity
- small-colony divergence
- recolonization dynamics

Without this, migration risks becoming just movement, not speciation pressure.

## Candidate papers

### Templeton (1980), "The theory of speciation via the founder principle"

Why read it:

- classic theoretical entry point for founder effects
- helps distinguish simple dispersal from true lineage divergence pressure

Mechanism implications:

- migration should sometimes create small founding groups
- habitat entry should impose a bottleneck cost or filter
- post-migration success should be tracked at lineage level, not only individual
  survival

Possible implementation consequences:

- `migration_bottleneck_size`
- `founder_group_id`
- `colonization_event`
- `lineage_reexpansion_rate`

Metrics it should influence:

- founder lineage survival
- time to local diversification
- occupancy persistence after colonization

### Mayr (1954), "Change of genetic environment and evolution"

Why read it:

- helps frame why a small lineage entering a new setting may not simply behave
  like a smaller copy of the old population
- useful for discussing ecological and genetic context changes together

Mechanism implications:

- lineage context matters, not only mutation count
- habitat shift should alter selective meaning of inherited structure

Possible implementation consequences:

- habitat-specific lineage performance logging
- post-migration adaptation lag
- interaction between founder size and habitat novelty

### Carson and Templeton style reviews on founder effect debates

Why read them:

- the founder principle has a large debate history
- useful for avoiding overclaiming that every bottleneck creates meaningful new
  lineages

Mechanism implications:

- founder events need controls
- some observed divergence will be drift noise rather than new ecological role

Control implications:

- compare bottleneck migration vs full-population migration
- compare novel habitat vs same-habitat recolonization

## What to add to our docs after this reading

Add to design:

- explicit `colonization_event`
- explicit founder group logging
- lineage bottleneck severity metric

Add to experiments:

- migration bottleneck ablation
- recolonization vs novel colonization control

## Theme 2. Resilience, Collapse, and Ecological Recovery

## Why this theme matters

The project wants:

- shocks
- refuges
- nontrivial extinction pressure
- long-run persistence without trivial stability

Right now we talk about collapse and recovery, but the theoretical base is still
light. We need a more formal ecological language for:

- resilience
- basin shifts
- recovery time
- reorganization after disturbance

## Candidate papers

### Holling (1973), "Resilience and Stability of Ecological Systems"

Why read it:

- foundational distinction between stability and resilience
- directly relevant to our desire for systems that survive shocks without being
  frozen

Mechanism implications:

- we should not optimize only for smooth equilibrium
- refuges and heterogeneous habitats should be treated as resilience structures

Possible implementation consequences:

- `recovery_lag`
- `shock_severity`
- `refuge_capacity`
- `post_shock_lineage_recovery`

Metrics it should influence:

- time to functional recovery
- lineage loss after shock
- habitat occupancy rebound

### Gunderson and Holling / panarchy literature

Why read it:

- useful for thinking about nested adaptive cycles rather than a single global
  stability condition
- likely relevant once habitats and lineages interact across scales

Mechanism implications:

- different habitats may recover on different timescales
- local collapse should not imply global collapse

Possible implementation consequences:

- habitat-specific recovery windows
- asynchronous climate and shock schedules

### Scheffer et al. on regime shifts and critical transitions

Why read it:

- helps define early-warning style metrics for approaching collapse
- useful if we later want to detect when archive dependence or monopoly
  dominance is destabilizing the world

Mechanism implications:

- event logs should preserve enough information to inspect pre-collapse state
- simple aggregate reward curves will not be enough

Possible implementation consequences:

- rolling variance metrics
- occupancy concentration metrics
- pre-collapse warning probes

## What to add to our docs after this reading

Add to design:

- explicit resilience metrics section
- distinction between stable world and resilient world

Add to experiments:

- shock protocol with severity ladder
- refuge ablation
- recovery-time benchmark

## Theme 3. Signaling, Trust, and Deception

## Why this theme matters

The project already expects:

- low-bandwidth communication
- archive trust gates
- kin recognition
- exploiters, mimics, and jammers

But these ideas currently rest more on intuition than on a communication
theory base. If we want signaling to matter, we need literature that explains
why:

- honest communication can exist
- dishonest communication can persist
- trust should be costly and conditional

## Candidate papers

### Johnstone and Grafen (1993), "Dishonesty and the handicap principle"

Why read it:

- classic treatment of why honest and dishonest signaling can coexist
- directly relevant to any future archive trust or social signaling mechanism

Mechanism implications:

- signaling should have cost or risk
- not all cheap signals should be trusted equally
- trust likely needs context, kin weighting, or history

Possible implementation consequences:

- `signal_cost`
- `trust_threshold`
- `deception_penalty`
- `signal_reputation_trace`

Metrics it should influence:

- false-positive trust rate
- coordination success
- exploit success under signaling

### Johnstone and Grafen (1992), "Error-prone signalling"

Why read it:

- helps distinguish deception from ordinary noisy communication
- important for simulations where limited channels may fail even without
  adversaries

Mechanism implications:

- message noise and deception should be modeled separately

Possible implementation consequences:

- `message_noise`
- `message_loss`
- `mimic_success_rate`

### Skyrms style signaling-game literature

Why read it:

- good theoretical bridge from abstract signaling games to agent-world
  interactions
- useful if we later add conventions, role markers, or archive admission cues

Mechanism implications:

- simple signal-meaning conventions may emerge without language-like complexity

Possible implementation consequences:

- role marker channels
- convention formation metrics

## What to add to our docs after this reading

Add to design:

- separate noisy communication from deception
- define trust as a mechanism with cost and failure cases

Add to experiments:

- honest-only vs noisy vs deceptive signaling control
- kin gate vs reputation gate ablation

## Theme 4. Dual Inheritance, Recombination, and Forgetting

## Why this theme matters

The project wants both:

- vertical inheritance of compressed experience
- horizontal or archive-mediated transmission

We already have cultural-evolution references, but we still need a tighter
formal basis for:

- when vertical and horizontal channels conflict
- how recombination changes transmitted structure
- why forgetting and filtering are necessary

Without this, the archive may become an unlimited convenience layer rather than
an ecological inheritance channel.

## Candidate papers

### Cavalli-Sforza and Feldman (1978), "A dual inheritance model of the human evolutionary process"

Why read it:

- classic formal entry point for dual inheritance
- useful even if our organisms are not human-like because the transmission logic
  is general

Mechanism implications:

- vertical and horizontal inheritance should be distinguished in logs
- transmission probabilities should be explicit rather than implicit

Possible implementation consequences:

- `inheritance_mode`
- `vertical_capsule_count`
- `horizontal_transfer_count`
- `copy_fidelity`

### Henrich and McElreath (2007), "Dual Inheritance Theory"

Why read it:

- good synthesis of why cultural and genetic inheritance are related but not the
  same
- useful for keeping archive dynamics from collapsing into a second genome

Mechanism implications:

- archive transmission should have its own timescale and failure modes
- social learning should not be free

Possible implementation consequences:

- archive access budget
- teacher availability
- forgetting and obsolescence rate

### Henrich, Boyd, Richerson on misunderstandings of cultural evolution

Why read it:

- useful for avoiding naive assumptions that "more copying" automatically means
  cumulative improvement

Mechanism implications:

- copying burden, bias, and filtering should all matter

Possible implementation consequences:

- `archive_filter_width`
- `copy_time_budget`
- `capsule_recombination_rate`
- `archive_obsolescence_rate`

### More formal models of cultural recombination and forgetting

Why read them:

- our archive will likely need explicit recombination and pruning
- otherwise it will either explode in size or become a static library

Mechanism implications:

- archive maintenance should be active and selective

Possible implementation consequences:

- forgetting curves
- recombination constraints
- archive overload metrics

## What to add to our docs after this reading

Add to design:

- explicit dual-inheritance section with vertical, horizontal, and ecological
  channels separated
- explicit forgetting and archive pruning rules

Add to experiments:

- no archive vs bounded archive vs free archive
- with and without recombination
- with and without forgetting

## Cross-Cutting Questions This Backlog Should Answer

After this literature pass, the project should be able to answer these design
questions more cleanly:

1. When does migration create a new lineage pressure rather than simple spread?
2. How should habitat shocks be measured: by stability, resilience, or both?
3. How do we distinguish noise, mistrust, and active deception?
4. How do vertical and horizontal inheritance compete or cooperate?
5. What mechanisms prevent the archive from becoming a free omniscient memory?

## Expected Document Follow-Ups

At the time this backlog was written, the most useful follow-up work looked
like a mix of one kernel spec and several mechanism-specific design notes.

The follow-up path that was actually realized later is:

1. `docs/m1_biosphere_kernel_spec.md`
2. `docs/research_synthesis_v1.md`
3. `docs/current_build_status_and_next_steps.md`
4. `docs/unresolved_question_register_v1.md`

The earlier placeholder names:

- docs/lineage_and_colonization_design_v0.md
- docs/signaling_and_trust_design_v0.md
- docs/dual_inheritance_design_v0.md

were not created as standalone files.
Their intended scope was absorbed into later integrated design and control
documents instead.

## Short Team Summary

The project does not mainly need more "classic artificial life" reading.

It now needs targeted literature that will sharpen:

- lineage turnover
- shock and recovery
- trust and deception
- dual inheritance mechanics

Those are the next theory bottlenecks between the current design and a robust
world model.
