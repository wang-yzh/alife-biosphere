# Resilience, Collapse, And Recovery Review v0

## Purpose

This note is the second targeted literature follow-up from
`docs/literature_backlog_v1.md`.

The goal is to make the project's future shock and recovery design more
disciplined.

In practice, this note asks:

1. What does it mean for the biosphere to be resilient?
2. How is resilience different from stability?
3. What should count as collapse, recovery, and transformation in our world?

## Short Answer

The literature strongly suggests this:

```text
A good world is not one that never changes.
A good world is one that can absorb disturbance,
reorganize, and continue producing ecological structure
without either freezing into stasis or collapsing into trivial extinction.
```

For our project, that means:

- we should not optimize only for smooth equilibrium;
- shocks should be a designed part of the world, not a late add-on;
- recovery should be measured over time, not guessed from one summary value;
- some collapses should count as failure, while some transformations should
  count as healthy reorganization.

## Core Papers

## 1. Holling (1973), "Resilience and Stability of Ecological Systems"

Why it matters:

- this is the foundational distinction we need most
- it separates:
  - `stability`: return speed and local constancy
  - `resilience`: capacity to absorb disturbance and remain within the same
    broad regime

What we should take from it:

- a system can be very stable and still be brittle
- a system can fluctuate a lot and still be resilient
- constancy is not the same thing as long-run viability

This matters directly because a naive simulation will often drift toward one of
two bad attractors:

- frozen world with little novelty
- unstable world that crashes all the time

Holling gives us the right target:

```text
bounded but disturbance-tolerant dynamics
```

Design implication:

- shock resistance and recovery should be explicit metrics
- habitat refuges are not optional decoration
- variance alone should not be treated as failure

## 2. Scheffer et al. (2001), "Catastrophic shifts in ecosystems"

Why it matters:

- this paper sharpens the idea that gradual change can produce abrupt regime
  shifts
- it helps us think about thresholds, not only noise

What we should take from it:

- systems can look healthy while losing resilience
- collapse may arrive suddenly after a long gradual drift
- maintaining resilience is often more important than optimizing an immediate
  performance target

For our project this is extremely useful.

It means:

```text
we should log pre-collapse state,
not just post-collapse outcomes
```

Design implication:

- event history before shock must be preserved
- concentration of occupancy or archive dependence may be early warning signs
- habitat stress variables should accumulate, not only spike

## 3. Walker, Holling, Carpenter, Kinzig (2004),
"Resilience, Adaptability and Transformability in Social-Ecological Systems"

Why it matters:

- this paper helps separate three ideas we would otherwise blur together

Key distinction:

- `resilience`: absorb disturbance and still retain core identity
- `adaptability`: actors can influence resilience from within the regime
- `transformability`: create a new regime when the old one is no longer viable

This is exactly the distinction our biosphere needs.

Without it, any big change is easy to mislabel:

- sometimes a change is just recovery;
- sometimes it is adaptation within the same ecology;
- sometimes it is a real system transition.

Design implication:

We should not treat every post-shock change as either:

- "failure", or
- "success".

Some changes should count as:

```text
healthy transformation
```

That will matter later when habitats, archives, and lineages coevolve.

## 4. Panarchy-related work

Why it matters:

- panarchy gives a useful multi-scale intuition
- local collapse and global collapse are not the same
- different subsystems can recover on different timescales

What we should take from it:

- habitats should not all shock or recover identically
- asynchronous disturbance is probably healthier than synchronized global reset
- refuge habitats should sometimes stay stable while frontier habitats churn

Design implication:

- shock scheduling should be heterogeneous
- habitat-specific recovery windows should be built in
- global collapse should be rare by design

## What This Means For Our Project

The literature gives us a more precise target than "make the world robust."

For `alife_biosphere`, the defensible target is:

```text
build a world that can experience local collapse, pressure, and reorganization
without losing all lineage continuity, all habitat diversity, or all meaningful
future adaptation capacity
```

That is stronger than numerical stability.
It is also more realistic than permanent equilibrium.

## Direct Design Consequences

## 1. We need to distinguish stability from resilience

Right now it is easy to imagine a world being called "good" because:

- no values explode
- population stays nonzero
- outputs look smooth

That is not enough.

A stable but monopolized world may be less useful than a noisier world that
keeps multiple lineages alive through shocks.

We should therefore track both:

- numerical boundedness
- post-disturbance recovery

## 2. Shock should be a first-class world mechanism

Shock should not be just ad hoc random bad luck.

We should define explicit disturbance types such as:

- resource shock
- hazard spike
- migration blockage
- archive corruption or archive inaccessibility
- parasite bloom
- habitat regime shift

Suggested event type:

```text
shock_event
```

Suggested payload fields:

- `shock_type`
- `shock_severity`
- `shock_duration`
- `target_habitat_ids`
- `global_or_local`

## 3. Recovery needs time-window metrics

Recovery is not a single number.

We should track at least:

- immediate loss
- short-term rebound
- medium-term reorganization
- long-term persistence

Suggested metrics:

- `recovery_lag`
- `post_shock_survival_fraction`
- `lineage_rebound_rate`
- `habitat_reoccupation_time`
- `post_shock_diversity_delta`

## 4. Refuges should be designed, not accidental

The resilience literature strongly supports the value of heterogeneity and
partially protected zones.

In our system this suggests:

- some habitats should be frontier habitats
- some should be nursery habitats
- some should be refuge habitats

Refuges are useful because they:

- preserve lineage continuity
- prevent every disturbance from becoming total extinction
- allow recolonization after local collapse

Suggested habitat field:

```text
refuge_strength
```

## 5. Pre-collapse signals should be inspectable

Scheffer-style regime-shift thinking suggests that collapse is often preceded
by loss of resilience.

That means we should save enough structure to inspect:

- occupancy concentration
- falling diversity
- archive dependence concentration
- habitat depletion persistence
- declining recovery after repeated smaller shocks

Suggested probe outputs:

- rolling habitat occupancy variance
- lineage concentration index
- repeated-shock response curve

## 6. Not every large change is failure

Walker et al. are especially useful here.

If the world reorganizes after a shock but still supports:

- living lineages
- multiple habitats
- renewed colonization
- continued innovation

then this may be:

```text
transformability
```

not simple failure.

So we should define three distinct outcomes:

- brittle collapse
- resilient recovery
- transformable reorganization

## Proposed Additions To The Existing Design

### New fields

- `shock_severity`
- `shock_duration`
- `recovery_window`
- `refuge_strength`
- `collapse_state`
- `last_major_shock_tick`

### New event types

- `shock_event`
- `habitat_collapse`
- `recovery_start`
- `recovery_complete`
- `transformation_event`

### New metrics

- recovery lag
- post-shock lineage survival
- habitat reoccupation time
- diversity rebound
- occupancy concentration before shock
- repeated-shock resilience decay

## Proposed Probe Design

The first resilience probe does not need to simulate full ecological realism.

A reasonable first probe is:

```text
baseline run
-> introduce local shock to one frontier habitat
-> compare worlds with and without refuges
-> compare mild and severe shock
-> measure lineage survival, recolonization, and recovery lag
```

The first useful question is:

```text
Can the world absorb local disturbance without either
global extinction or total frozen recovery?
```

That is enough to validate the first resilience layer.

## Build Recommendations

This literature review suggests three near-term build tasks.

### 1. Add explicit shock scheduling

Reason:

- otherwise disturbances will remain too informal for serious analysis

### 2. Add refuge-aware habitat roles

Reason:

- without refuges, "resilience" risks collapsing into raw survival probability

### 3. Add recovery-window metrics from the beginning

Reason:

- post-shock interpretations become weak if we only inspect final state

## Bottom Line

The resilience literature tells us to avoid two mistakes:

```text
mistake 1: calling smooth equilibrium success
mistake 2: calling every large disruption failure
```

The better target is:

```text
a biosphere that can absorb shocks,
reorganize unevenly across habitats,
preserve enough continuity for lineage history to matter,
and still remain open to future change
```

That is the version of resilience we should build toward.

## Sources

- Holling, C. S. (1973). "Resilience and Stability of Ecological Systems."
  [Annual Reviews](https://doi.org/10.1146/annurev.es.04.110173.000245)
- Scheffer, M., Carpenter, S., Foley, J. A., Folke, C., Walker, B. (2001).
  "Catastrophic Shifts in Ecosystems."
  [Nature](https://www.nature.com/articles/35098000)
- Walker, B., Holling, C. S., Carpenter, S. R., Kinzig, A. (2004).
  "Resilience, Adaptability and Transformability in Social-Ecological Systems."
  [DOAJ](https://doaj.org/article/5e2033ca6a834752aae27aa6a0f29895)
- Gunderson, L. H., Holling, C. S. (eds.) (2002).
  "Panarchy: Understanding Transformations in Human and Natural Systems."
  [Penn State Libraries](https://catalog.libraries.psu.edu/catalog/2284846)
