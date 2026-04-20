# Community Assembly, Invasion, And Ecological Networks Review v0

## Purpose

This note extends the literature program beyond the first four backlog themes.

The goal is to strengthen one of the most important missing ecological layers in
`alife_biosphere`:

```text
How populations actually occupy the world,
in what order they arrive,
how they exclude or enable one another,
and how those interactions accumulate into ecological structure.
```

In practice, this note asks:

1. What should "community assembly" mean in the biosphere?
2. Why do arrival order and invasion history matter?
3. Why should interaction networks be treated as outputs, not just side effects?

## Short Answer

The literature points to a fairly strong position:

```text
Who arrives first matters.
Who arrives later can still matter.
And the ecological structure that results is not just a pile of individuals,
but a network of interactions shaped by invasion order, habitat filtering,
and historical contingency.
```

For our project, that means:

- habitat occupancy should be history-dependent;
- colonization should interact with priority effects;
- invasion should be modeled as an ecological event, not just migration;
- interaction networks should be reconstructable from logs.

## Core Papers

## 1. Fukami (2015),
"Historical Contingency in Community Assembly: Integrating Niches, Species Pools, and Priority Effects"

Why it matters:

- this is the cleanest modern synthesis of priority effects and historical
  contingency in community assembly
- it gives us a framework for why arrival order matters without reducing
  everything to simple competition

The key idea we should reuse:

Priority effects require at least two ingredients:

- a regional pool capable of producing alternative outcomes
- local dynamics fast enough that early arrivals reshape later conditions

That is directly relevant to `alife_biosphere`.

It suggests that history matters most when:

- habitats differ enough to filter entrants;
- early occupants can preempt or modify local opportunity;
- later arrivals face a changed world, not a blank slot.

Design implication:

- habitat state should be changed by occupants, not only by exogenous climate
- invasion timing should be logged
- occupancy order should be part of downstream interpretation

Useful translation into biosphere terms:

- `arrival_order`
- `priority_effect_strength`
- `niche_preemption_score`
- `niche_modification_score`

## 2. Chase (2003)-style historical contingency perspective

Why it matters:

- the classic historical-contingency framing helps us avoid a purely static
  community view
- it supports the idea that multiple community outcomes can arise under similar
  broad conditions depending on assembly history

What we should take from it:

- local community structure should not always converge to the same result
- early contingent differences can echo into long-run occupancy patterns

Design implication:

- probe runs should compare repeated worlds under different arrival orders
- assembly history should be preserved in logs rather than overwritten by
  end-state summaries

## 3. Law and Morton / invasion-assembly line of work

Why it matters:

- invasion-based community assembly is useful for our world because it treats
  occupancy as a dynamic sequence rather than a fixed equilibrium

What we should take from it:

- communities can be studied through repeated invasions and persistence checks
- successful entry depends on existing occupants, not just habitat quality

Design implication:

- migration into occupied habitats should be treated as invasion, not just move
- the success of an entrant should depend on incumbent configuration

Useful translation into biosphere terms:

- `invasion_event`
- `incumbent_resistance`
- `invader_establishment_success`
- `post_invasion_turnover`

## 4. Fortuna et al. (2013), "Evolving Digital Ecological Networks"

Why it matters:

- this is directly in the digital-evolution line we care about
- it shows that ecological networks in digital systems are not decorative; they
  can be observed and analyzed as evolving structure

What we should take from it:

- competition, parasitism, predation, and mutualism can be represented as
  network edges
- ecological network structure is itself a research object

That is important for us because otherwise we might log only individual success
and miss the real system-level organization.

Design implication:

- event logs should make interaction graphs reconstructable
- network descriptors should be part of metrics from early stages

Useful translation into biosphere terms:

- `interaction_type`
- `interaction_partner_id`
- `interaction_strength`
- `network_modularity`
- `network_nestedness`

## 5. Drake / alternative stable states and transient assembly line

Why it matters:

- community assembly is not only about one final stable endpoint
- many systems remain in long transient states that still matter ecologically

This connects well to our project because we do not want to assume:

```text
world runs long enough
-> one clean equilibrium appears
```

Instead, it is often more useful to ask:

- what patterns persist for meaningful time windows?
- when do invasions trigger reorganization rather than convergence?

Design implication:

- assembly probes should track transient occupancy patterns
- not all useful ecological structure will be equilibrium structure

## What This Means For Our Project

The literature suggests that `alife_biosphere` should not model habitats as
empty containers waiting to be filled.

The more defensible interpretation is:

```text
each habitat is assembled over time through arrival, occupation, resistance,
modification, turnover, and interaction.
```

That means:

- occupancy is path-dependent;
- migration may become invasion;
- founder effects and priority effects should connect;
- the resulting ecology should be inspectable as a network.

## Direct Design Consequences

## 1. Assembly history should be explicit

We should not only store current occupants.

We should also store:

- who arrived when
- who established successfully
- who failed to establish
- which occupants were displaced

Suggested fields:

- `arrival_order`
- `establishment_tick`
- `displacement_count`
- `incumbent_blocking_score`

## 2. Invasion should be a distinct event from migration

Movement into an empty habitat is not the same as entry into an occupied
habitat.

Suggested event types:

- `migration_event`
- `invasion_event`
- `establishment_success`
- `establishment_failure`
- `displacement_event`

## 3. Priority effects should be measurable

The project should eventually distinguish at least two broad mechanisms:

- niche preemption
- niche modification

For us, that could mean:

- early occupants consume or reserve resources that later arrivals needed
- early occupants alter hazard, signals, archive trust, or ecological memory

Suggested fields:

- `priority_effect_strength`
- `resource_preemption`
- `environment_modification_score`

## 4. Interaction graphs should be reconstructable

This is one of the strongest implications from Fortuna et al.

Logs should allow us to build graphs of:

- competition
- mutual aid
- signaling dependence
- parasitic exploitation
- archive-mediated influence

Suggested event payload additions:

- `partner_id`
- `interaction_type`
- `interaction_outcome`
- `interaction_weight`

## 5. Community metrics should go beyond abundance

The project should not rely only on:

- population size
- survival rate
- habitat occupancy count

We also need:

- richness
- evenness
- turnover
- persistence
- network structure

Suggested metrics:

- occupancy stability
- invasion success rate
- turnover rate
- richness
- evenness
- network modularity
- parasitic edge fraction

## Proposed Additions To The Existing Design

### New fields

- `arrival_order`
- `priority_effect_strength`
- `incumbent_resistance`
- `establishment_score`
- `interaction_type`
- `interaction_weight`

### New event types

- `invasion_event`
- `establishment_success`
- `establishment_failure`
- `displacement_event`
- `interaction_event`

### New metrics

- invasion success rate
- occupancy turnover
- community richness
- community evenness
- interaction network modularity
- priority-effect persistence

## Proposed Probe Design

The first community-assembly probe can stay small.

A reasonable first probe is:

```text
three habitats
-> repeated arrival of organisms or lineages in different orders
-> compare empty-habitat entry with occupied-habitat invasion
-> measure establishment, displacement, and persistence
```

The first useful question is:

```text
Does arrival order create different long-lived occupancy and interaction
patterns under the same broad world settings?
```

That is enough to justify explicit assembly logic.

## Build Recommendations

This literature review suggests three near-term build tasks.

### 1. Separate migration from invasion

Reason:

- entry into occupied habitats is ecologically different from simple movement

### 2. Preserve assembly history in logs

Reason:

- end-state occupancy alone cannot recover priority effects

### 3. Make interaction graphs reconstructable

Reason:

- ecological structure is likely to be network-shaped before it is clearly
  species-shaped

## Bottom Line

The community-assembly literature tells us that the world should not be treated
as a neutral board where agents simply spread.

A better target is:

```text
a historically assembled ecology
where arrival order, invasion success, incumbent resistance,
and interaction structure shape long-run occupancy
```

That would make `alife_biosphere` feel much more like a living system and much
less like a repeated placement experiment.

## Sources

- Fukami, T. (2015).
  "Historical Contingency in Community Assembly: Integrating Niches,
  Species Pools, and Priority Effects."
  [Annual Reviews](https://www.annualreviews.org/doi/pdf/10.1146/annurev-ecolsys-110411-160340)
- Fortuna, M. A., Zaman, L., Wagner, A. P., Ofria, C. (2013).
  "Evolving Digital Ecological Networks."
  [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC3605903/)
- Law, R., Morton, R. D. (1996).
  "Permanence and the assembly of ecological communities."
  [Ecology](https://esajournals.onlinelibrary.wiley.com/doi/10.2307/2265731)
- Chase, J. M. (2003).
  "Community assembly: when should history matter?"
  [Oecologia](https://link.springer.com/article/10.1007/s00442-003-1311-7)
- Fukami, T., Nakajima, M. (2011).
  "Community assembly: alternative stable states or alternative transient states?"
  [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC3187870/)
