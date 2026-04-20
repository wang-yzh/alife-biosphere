# Alife Biosphere Research Synthesis v1

## Status Note

This is an inheritance-centered synthesis of the earlier design line.

It remains useful as a mechanism background document, but it is no longer the
sole top-level project north star after the ecology-first realignment on
2026-04-21.

Use these documents for the current top-level direction:

- `ecology_north_star_v1.md`
- `world_design_v2.md`
- `build_plan_v2.md`

## Purpose

This document synthesizes the current literature program and design notes into
one integrated position.

It answers five practical questions:

1. What are we actually trying to build?
2. Which design rules are now non-negotiable?
3. Which experimental variables matter most?
4. What kinds of results would count as real progress?
5. What claims are still out of scope?

This is not a replacement for the detailed topic reviews.
It is the shortest document that tries to hold the whole argument together.

## 1. The Project In One Sentence

`alife_biosphere` is an attempt to build a persistent artificial world in which
lived experience can enter multiple inheritance channels and reshape population,
group, and habitat structure over long horizons.

That sentence has three parts that matter:

- persistent artificial world
- multiple inheritance channels
- long-horizon structural reshaping

If any one of those pieces is missing, the project collapses back into a more
ordinary optimizer or training pipeline.

## 2. What This Project Is Not

The literature collected so far allows us to rule out several wrong framings.

This project is not:

- a benchmark leaderboard
- a single-agent reinforcement-learning environment
- a transfer-learning pipeline with ecological decoration
- a game world optimized for player entertainment
- a simulation that treats culture as free copying
- a world where shocks are random punishment and recovery is hidden handholding

These exclusions are not stylistic.
They are conclusions forced by the literature.

## 3. The Core Problem Stack

The project can now be expressed as a stack of linked scientific problems.

### Problem 1. Lifetime experience

Can an organism learn, adapt, or discover useful local structure during its own
life?

### Problem 2. Vertical inheritance

Can some of that lifetime structure be compressed and transmitted across
generations without becoming brittle replay?

### Problem 3. Cultural inheritance

Can useful structure spread horizontally without turning into free omniscience
or degenerating into stale noise?

### Problem 4. Group organization

Can kin groups become persistent, asymmetrical, and ecologically meaningful
without being manually scripted as classes?

### Problem 5. Ecological memory

Can populations alter habitats in ways that descendants and competitors inherit
indirectly?

### Problem 6. Resilience and transformation

Can the world survive disturbance, reorganize, and continue producing novelty
without trivial stability or total collapse?

The project only works if these problems interact.
Solving one in isolation is not enough.

## 4. The Evidence Base Now Points To Ten Non-Negotiable Rules

## Rule 1. No single global objective

The world must not be dominated by a single researcher-defined score.

Why:

- novelty-search, quality-diversity, digital-ecology, and open-endedness
  literature all show that one scalar objective tends to collapse diversity too
  early

Consequence:

- selection pressure should be local, ecological, and multi-source

## Rule 2. Multiple inheritance channels must stay distinct

We must distinguish:

- genetic inheritance
- developmental bias
- somatic memory
- cultural inheritance
- ecological inheritance

Why:

- if we collapse these channels, we lose the ability to say what caused
  adaptation

Consequence:

- the data model and event logs must preserve channel identity

## Rule 3. Culture must be selective, validated, and forgetful

Why:

- social-learning and cumulative-culture literature shows that blind copying
  fails
- archive overload is a real failure mode

Consequence:

- archive access must include visibility limits, provenance, validation, and
  forgetting

## Rule 4. Groups matter, but should not be romanticized

Why:

- major-transitions and multicellularity literature shows that higher-level
  individuality requires more than clustering

Consequence:

- `KinGroup` must exist as a data structure
- but higher-level individuality must be measured from dependence, persistence,
  and conflict suppression

## Rule 5. Communication must be low-bandwidth, partial, and fallible

Why:

- signaling and deception literature shows that honesty is conditional, not
  automatic
- partial observability is the normal case, not a later difficulty setting

Consequence:

- signals should be local, noisy, possibly deceptive, and trust-mediated

## Rule 6. Trust must be private, graded, and channel-specific

Why:

- private-noisy information breaks many binary reputation rules
- direct interaction trust and archive/source trust are not the same thing

Consequence:

- trust should be split into:
  - direct partner trust
  - archive/source trust

## Rule 7. Habitat dynamics must be state-dependent

Why:

- niche-construction and open-ended-dynamics work shows that state-dependent
  change is stronger than purely exogenous noise for sustained innovation

Consequence:

- habitats must respond to occupancy, depletion, signaling, parasite pressure,
  and other world-produced traces

## Rule 8. Disturbance and rescue must be explicit

Why:

- resilience, metapopulation, and rescue literature all show that collapse and
  rebound are structured phenomena

Consequence:

- the world needs:
  - local and regional disturbance classes
  - refuge structure
  - rescue-source classification
  - bottleneck history

## Rule 9. Space and topology are part of the mechanism

Why:

- host-parasite, metapopulation, and connectivity literature show that graph
  structure changes virulence, rescue flow, and local diversity

Consequence:

- habitat graph design is not cosmetic
- topology becomes an eventual treatment variable

## Rule 10. Metrics must be plural, humble, and reconstructable

Why:

- open-endedness measurement work warns against one master metric
- warning-signal work shows high false positive and false negative risk

Consequence:

- keep raw events, lineage traces, and interaction networks
- derive multiple diagnostic metrics rather than one definitive score

## 5. The Minimal Causal Story Of The World

This is the simplest causal picture that still respects the literature.

```text
habitat structure
  -> local exposures and costs
  -> lifetime adaptation and coordination
  -> compressed inheritance and selective copying
  -> lineage branching and group organization
  -> niche construction and altered habitat memory
  -> future selection, collapse, rescue, and novelty
```

This causal loop is the heart of the project.

If the world only does:

```text
environment -> reward -> policy update
```

then the project has failed its own premise.

## 6. The Main Mechanism Families

The current evidence base now supports seven mechanism families.

## 6.1 Habitat family

Needed features:

- resource heterogeneity
- refuge/frontier trade-offs
- state-dependent memory traces
- bounded shocks
- graph adjacency

## 6.2 Organism family

Needed features:

- bounded resource state
- life stages
- partial observability
- compact trust profile
- limited signaling

## 6.3 Inheritance family

Needed features:

- compact vertical inheritance
- provisional cultural copying
- validation and forgetting
- domain-tagged source trust

## 6.4 Group family

Needed features:

- kin groups
- shared resource pool
- role asymmetry
- founder width and bottleneck history

## 6.5 Disturbance family

Needed features:

- asynchronous crashes
- bottlenecks
- recolonization windows
- rescue classification

## 6.6 Antagonist family

Needed features:

- parasite / thief / mimic / jammer pressure
- graph-dependent spread
- operational detection from events and networks

## 6.7 Measurement family

Needed features:

- population summaries
- lineage summaries
- interaction-network summaries
- warning and recovery diagnostics
- adaptive-cycle proxy profiles

## 7. The Most Important Variable Axes

Among all possible parameters, a smaller set now stands out as the real
scientific levers.

### Ecological structure

- refuge fraction
- habitat complexity
- graph topology
- migration friction
- carrying-capacity pressure

### Inheritance

- capsule bandwidth
- developmental plasticity
- archive visibility
- forgetting rate
- validation budget

### Social dynamics

- signal cost
- verification cost
- trust decay
- domain specificity
- kin threshold

### Disturbance

- local disturbance rate
- regional disturbance rate
- bottleneck width
- recolonization friction
- rescue-source mix

### Antagonism

- parasite pressure
- mimic frequency
- deception tolerance
- defense bandwidth

These are more central than endless controller hyperparameters.

## 8. What Counts As Real Progress

The literature and design work now imply a stricter standard for success.

Progress is not:

- a single good seed
- a higher short-run reward
- a visually complex but analytically empty trace

Progress is evidence that one of the core causal loops is real.

Examples:

### Genuine progress example 1

Offspring adapt faster because inherited structure is compact and transferable,
not because they start as exact clones.

### Genuine progress example 2

Local disturbances cause decline, but rescue occurs through refuge migration or
retained diversity in a way that can be classified from the logs.

### Genuine progress example 3

Group role asymmetry emerges and improves persistence under damaging work or
signaling load.

### Genuine progress example 4

Validated archive use outperforms unconditional copying, and the failure mode
of stale culture is directly observable.

### Genuine progress example 5

Interaction-network structure shifts in ways that align with adaptive-cycle
proxy changes during collapse and reorganization.

## 9. What Would Not Count As Strong Evidence

The synthesis also clarifies some weak-evidence traps.

Weak evidence includes:

- claiming founder effects from any small migration event
- claiming group individuality from simple clustering
- claiming open-endedness from novelty alone
- claiming signal honesty because messages have energy cost
- claiming resilience because extinction did not happen in one short run
- claiming cultural inheritance because copies existed, without validation and
  reuse evidence

## 10. The Core Metric Families

The project now needs at least seven metric families.

### Population metrics

- abundance
- occupancy
- turnover
- extinction and recolonization

### Lineage metrics

- lineage depth
- branch factor
- bottleneck history
- founder persistence

### Group metrics

- group persistence
- role asymmetry
- within-group conflict
- group reproduction success

### Inheritance metrics

- vertical transfer gain
- cultural transfer gain
- forgetting rate
- cross-domain failure rate

### Communication metrics

- signal reliability
- deception rate
- verification success
- trust recovery lag

### Resilience metrics

- recovery lag
- rescue probability
- rescue-source composition
- early-warning confidence

### Structural metrics

- connectedness profile
- adaptive-cycle proxy profile
- network modularity / separation
- corridor concentration

No single metric family can stand in for the others.

## 11. The Immediate Research Program

The literature now points to a staged research program that is narrower than
"build artificial life" and stronger than "keep adding features."

### Stage A. Stable ecological kernel

Show:

- bounded habitat dynamics
- refuge structure
- nontrivial occupancy differences

### Stage B. Structured history

Show:

- lineage traces
- founder and bottleneck logging
- interaction-network reconstruction

### Stage C. Costly local learning

Show:

- protocol discovery
- limited signaling
- trust-mediated response

### Stage D. Selective inheritance

Show:

- compact vertical transfer
- validated cultural copying
- forgetting and overload

### Stage E. Ecological resilience and antagonism

Show:

- classified rescue
- topology-sensitive disturbances
- measurable antagonist effects

This is the most defensible near-term research ladder.

## 12. The Strongest Open Questions

The literature now narrows the open questions rather than eliminating them.

The hardest unresolved questions are:

1. Which cheap interaction-network summaries best approximate connectedness in
   our small worlds?
2. How should archive/source trust update differ from direct partner trust?
3. When should a local release/reorganization cycle count as a true regime shift?
4. How much cultural visibility is enough before archive overload dominates?
5. What level of group asymmetry should count as evidence for meaningful
   higher-level organization?

These are good open questions.
They are narrow enough to be attacked experimentally.

## 13. Current Working Position

Given the literature gathered so far, the current working position is:

```text
The most promising path is a small but persistent graph world
with bounded resources, partial observability, low-bandwidth signaling,
multiple inheritance channels, explicit disturbance and rescue,
and enough social and ecological structure that experience can become
lineage-level and habitat-level history.
```

This is now the clearest integrated statement of the project.
