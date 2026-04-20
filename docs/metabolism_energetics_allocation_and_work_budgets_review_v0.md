# Metabolism, Energetics, Allocation, And Work Budgets Review v0

## Purpose

This note extends the literature program toward a question that becomes more
important the more ambitious `alife_biosphere` becomes:

```text
What does it actually cost to stay alive,
to grow,
to explore,
to repair,
to reproduce,
and to build more complex organization?
```

The goal is to thicken the project's treatment of metabolism and energetics so
that energy, material, and work budgets become real organizing constraints
rather than abstract bookkeeping.

In practice, this note asks:

1. Why should metabolism matter beyond a single energy meter?
2. Why do allocation trade-offs structure almost every life-history decision?
3. Why are energy and material constraints not always the same thing?
4. Why should the biosphere treat "work budgets" as causal rather than cosmetic?

## Short Answer

The literature supports a strong combined view:

```text
metabolism is not just fuel consumption.
it is the organized conversion of matter and energy into maintenance, growth,
repair, development, reproduction, and work.
```

It also suggests:

```text
ecological and evolutionary dynamics often depend less on how much total energy
exists than on how it can be acquired, converted, allocated, buffered, and
wasted under real constraints.
```

And importantly:

```text
metabolic constraints are not reducible to one universal scalar law.
size, temperature, architecture, resource quality, elemental balance,
and ecological context can all change what metabolism means in practice.
```

For our project, this means:

- energy budgets should be directional and allocated, not just stored;
- maintenance, growth, exploration, reproduction, defense, and signaling should
  compete for common budgets;
- matter and elemental quality should matter as well as raw energy;
- and some of the world's most important trade-offs should be explicitly
  metabolic.

## Core Papers

## 1. West, Brown, Enquist (1997),
"A General Model for the Origin of Allometric Scaling Laws in Biology"

Why it matters:

- this is one of the foundational scaling papers behind later metabolic theory
- it gives a classic network-constraint explanation for why body size and
  resource transport matter together

The key lesson:

```text
metabolic organization is constrained by how resources are physically
distributed through organisms.
```

This matters for `alife_biosphere` even if we never model literal blood vessels.

It suggests that:

- transport and distribution costs are part of why size and form matter;
- energy is not equally available everywhere inside a system;
- architecture can constrain scaling.

Design implication:

- future body-plan and metabolism layers should be linked
- larger or more complex organisms may pay rising distribution and maintenance
  costs

Useful translation into biosphere terms:

- `transport_cost`
- `distribution_efficiency`
- `body_size_metabolic_scaling`
- `architecture_burden`

## 2. Brown, Gillooly, Allen, Savage, West (2004),
"Toward a Metabolic Theory of Ecology"

Why it matters:

- this is the canonical metabolic theory of ecology paper
- it is one of the strongest arguments that metabolic rate links individual
  physiology to population, community, and ecosystem dynamics

The key lesson:

```text
metabolic rate sets many basic biological tempos:
resource uptake,
development,
growth,
mortality,
population turnover,
and trophic process rates.
```

This is very important for the biosphere.

It suggests that energy throughput can help organize:

- life-history pace
- ecological interaction rates
- and world-level production/consumption structure

Design implication:

- metabolic rate should later affect development rate, repair rate, aging load,
  reproduction timing, and ecological throughput
- the world should support tempo differences among lineages and roles

Useful translation into biosphere terms:

- `metabolic_rate`
- `life_history_pace`
- `throughput_rate`
- `interaction_tempo`

## 3. Kooijman (2010) and Sousa et al. (2010),
Dynamic Energy Budget theory

Why they matter:

- DEB theory is probably the most useful framework for this project at the
  individual level
- it explicitly separates acquisition, reserves, maintenance, growth,
  maturation, and reproduction

The key lesson:

```text
organisms should be modeled as budget systems:
energy and matter are acquired, stored, mobilized,
and then partitioned into competing uses across the life cycle.
```

This is almost exactly what `alife_biosphere` needs.

Unlike a single energy bar, DEB-style thinking naturally supports:

- reserves,
- maintenance costs,
- growth,
- maturation,
- reproduction,
- and aging links.

Design implication:

- budgets should later have at least:
  - acquisition
  - reserve
  - maintenance
  - growth/maturation
  - reproduction
- life stages should interact through budget partitioning

Useful translation into biosphere terms:

- `reserve_pool`
- `maintenance_draw`
- `growth_allocation`
- `maturation_budget`
- `reproduction_budget`

## 4. Zera and Harshman (2001),
"The Physiology of Life History Trade-Offs in Animals"

Why it matters:

- this is one of the strongest reviews linking physiology to life-history
  trade-offs
- it is highly relevant because it turns abstract trade-offs into allocation
  mechanisms

The key lesson:

```text
life-history trade-offs are not only statistical patterns;
they are built out of concrete differences in acquisition, allocation,
endocrine regulation, and physiological routing.
```

This is a very important correction for the biosphere.

It means trade-offs should later be represented as:

- resource routing conflicts
- hormonal or state-dependent shifts
- opportunity costs across tasks

Design implication:

- the world should later support dynamic reallocation:
  - more repair -> less reproduction
  - more exploration -> less storage
  - more defense -> less growth

Useful translation into biosphere terms:

- `allocation_policy`
- `routing_bias`
- `maintenance_vs_reproduction_tradeoff`
- `exploration_vs_storage_tradeoff`

## 5. Sterner and Elser (2002) and Elser et al. (2000),
Ecological stoichiometry

Why they matter:

- these are the strongest classic sources for why energy alone is not enough
- they show that the balance of multiple elements and materials constrains
  ecological interaction in deep ways

The key lesson:

```text
organisms do not live on energy alone.
the quality and ratio of required materials can strongly constrain growth,
reproduction, trophic transfer, and interaction outcomes.
```

This is extremely important for the biosphere because your world already uses:

- energy
- matter
- information

Stoichiometric thinking suggests that "matter" should not be a generic bulk
mass forever.
Quality, composition, and mismatch can matter.

Design implication:

- later worlds should distinguish energy-rich from material-suitable inputs
- resource mismatch should matter for growth and reproduction
- trophic transfer should include inefficiency and quality constraints

Useful translation into biosphere terms:

- `resource_quality`
- `material_balance`
- `stoichiometric_mismatch`
- `growth_limitation_mode`

## 6. Glazier (2014, 2015, 2022),
metabolic scaling as context-dependent rather than one universal law

Why these matter:

- these reviews and syntheses are important cautionary correctives
- they warn against overinterpreting one universal metabolic scaling rule

The key lesson:

```text
metabolic scaling is often variable and context-dependent.
ecology, activity, architecture, and life history can all reshape it.
```

This is healthy for `alife_biosphere`.

It means we should use metabolic theory as a guide, not a straightjacket.

Design implication:

- metabolic scaling in the biosphere should later be allowed to vary by:
  - body plan
  - trophic role
  - activity level
  - developmental stage
  - habitat condition

Useful translation into biosphere terms:

- `context_dependent_scaling`
- `activity_metabolism_multiplier`
- `role_specific_cost_curve`
- `stage_specific_metabolic_profile`

## What This Means For Our Project

The literature suggests that `alife_biosphere` should treat metabolism as a
multi-layer constraint system, not a single resource counter.

The most useful layered picture is:

### 1. Acquisition

- how much usable energy and material can be obtained?

### 2. Reserve

- what can be buffered or stored for later?

### 3. Maintenance

- what must be spent to remain viable?

### 4. Growth and maturation

- what can be converted into developmental change?

### 5. Reproduction

- what is diverted into descendants rather than the current body?

### 6. Work

- what can be spent on movement, sensing, defense, engineering, signaling,
  governance, and exploration?

This is a much better fit than:

- one energy meter
- one action cost column

## Direct Design Consequences

## 1. Budgets should be directional, not flat

Later worlds should distinguish:

- intake
- reserve
- maintenance outflow
- work expenditure
- reproductive diversion

Suggested fields:

- `energy_intake_rate`
- `material_intake_rate`
- `reserve_pool`
- `maintenance_draw`
- `work_budget`
- `reproductive_diversion`

## 2. Work classes should be explicit

The biosphere already has many candidate kinds of work:

- movement
- active sensing
- repair
- signaling
- defense
- engineering
- archive access
- governance / policing

Later worlds should make these work types metabolically legible.

Suggested fields:

- `movement_cost`
- `sensing_cost`
- `repair_cost`
- `defense_cost`
- `signaling_cost`
- `engineering_cost`

## 3. Matter quality should matter alongside energy

Following stoichiometry, later worlds should not treat all inputs as
interchangeable.

Suggested fields:

- `resource_quality`
- `material_balance`
- `construction_suitability`
- `growth_limitation_mode`

## 4. Allocation policy should become evolvable

This is one of the strongest practical conclusions.

Later lineages may differ not only in how much they acquire,
but in how they allocate.

Suggested fields:

- `allocation_policy`
- `maintenance_priority`
- `reproduction_priority`
- `exploration_priority`
- `defense_priority`

Suggested event types:

- `allocation_shift_event`
- `reserve_reallocated`
- `maintenance_shortfall_detected`

## 5. Metabolic architecture should interact with ecology

Following Brown/Kooijman/Glazier:

- the same budget logic may play out differently by role and habitat

Suggested fields:

- `role_specific_cost_curve`
- `stage_specific_metabolic_profile`
- `habitat_metabolic_modifier`
- `activity_metabolism_multiplier`

## Proposed Additions To The Existing Design

### New fields

- `metabolic_rate`
- `reserve_pool`
- `maintenance_draw`
- `growth_allocation`
- `reproduction_budget`
- `work_budget`
- `resource_quality`
- `stoichiometric_mismatch`

### New event types

- `reserve_filled`
- `reserve_depleted`
- `maintenance_shortfall_detected`
- `allocation_shift_event`
- `work_budget_exceeded`
- `resource_mismatch_detected`

### New metrics

- maintenance burden
- reserve half-life
- work-budget utilization
- growth vs reproduction allocation ratio
- stoichiometric mismatch cost
- metabolic flexibility

## Proposed Probe Design

The first metabolism-focused probe can stay focused.

A reasonable first probe is:

```text
same lineage base
-> compare flat energy accounting against reserve-plus-allocation accounting
-> vary resource quality as well as quantity
-> measure development, repair, reproduction, exploration, and survival
-> then compare fixed allocation policy against evolvable allocation policy
```

The first useful question is:

```text
Does a budgeted metabolism model produce more realistic life-history and
ecological trade-offs than a single pooled-energy model?
```

That is enough to justify a true metabolic layer.

## Build Recommendations

This literature review suggests three near-term design tasks.

### 1. Add a metabolism-and-allocation section to the core design

Reason:

- many existing trade-offs are currently named, but not yet budget-grounded

### 2. Separate reserve, maintenance, and work

Reason:

- these are among the most useful distinctions from DEB-style thinking

### 3. Treat material mismatch as a first-class ecological constraint

Reason:

- energy-rich but composition-poor resources should later behave differently

## Bottom Line

The metabolism literature tells us that a serious biosphere is not organized
only by what organisms want to do.

It is organized by:

```text
what they can afford to do,
what they can store,
what they must maintain,
and how they divide limited throughput among competing life functions
```

That is the version of metabolism worth building toward in `alife_biosphere`.

## Sources

- West, G. B., Brown, J. H., Enquist, B. J. (1997).
  "A General Model for the Origin of Allometric Scaling Laws in Biology."
  [Science DOI / Santa Fe Institute](https://doi.org/10.1126/science.276.5309.122)
  and [SFI page](https://www.santafe.edu/research/results/working-papers/a-general-model-for-the-origin-of-allometric-scali)
- Brown, J. H., Gillooly, J. F., Allen, A. P., Savage, V. M., West, G. B. (2004).
  "Toward a Metabolic Theory of Ecology."
  [Ecology DOI / Macquarie page](https://doi.org/10.1890/03-9000)
  and [Macquarie page](https://researchers.mq.edu.au/en/publications/toward-a-metabolic-theory-of-ecology/)
- Kooijman, S. A. L. M. (2010).
  "Dynamic Energy Budget Theory for Metabolic Organisation."
  [Cambridge page](https://doi.org/10.1017/CBO9780511805400)
  and [VU page](https://research.vu.nl/en/publications/dynamic-energy-budget-theory-for-metabolic-organisation/)
- Sousa, T., Domingos, T., Poggiale, J.-C., Kooijman, S. A. L. M. (2010).
  "Dynamic energy budget theory restores coherence in biology."
  [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC2981977/)
- Zera, A. J., Harshman, L. G. (2001).
  "The Physiology of Life History Trade-Offs in Animals."
  [Annual Reviews DOI](https://doi.org/10.1146/annurev.ecolsys.32.081501.114006)
  and [University of Nebraska copy](https://digitalcommons.unl.edu/bioscizera/15/)
- Sterner, R. W., Elser, J. J. (2002).
  "Ecological Stoichiometry: The Biology of Elements from Molecules to the Biosphere."
  [Open Library](https://openlibrary.org/books/OL29342523M/Ecological_Stoichiometry)
- Elser, J. J. et al. (2000).
  "Biological Stoichiometry from Genes to Ecosystems."
  [ResearchGate metadata / PDF access](https://www.researchgate.net/publication/216811040_Biological_Stoichiometry_from_Genes_to_Ecosystems)
- Glazier, D. S. (2014).
  "Metabolic Scaling in Complex Living Systems."
  [MDPI](https://www.mdpi.com/2079-8954/2/4/451)
- Glazier, D. S. (2015).
  "Is metabolic rate a universal 'pacemaker' for biological processes?"
  [PubMed](https://pubmed.ncbi.nlm.nih.gov/24863680/)
- Glazier, D. S. (2022).
  "Variable metabolic scaling breaks the law: from 'Newtonian' to 'Darwinian' approaches."
  [Royal Society / ResearchGate entry](https://www.researchgate.net/publication/364432558_Variable_metabolic_scaling_breaks_the_law_from_%27Newtonian%27_to_%27Darwinian%27_approaches)
