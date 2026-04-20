# Founder Effects And Lineage Turnover Review v0

## Purpose

This note is the first targeted literature follow-up from
`docs/literature_backlog_v1.md`.

The goal is not to import biological speciation theory literally into the
biosphere.
The goal is to clarify what founder effects should and should not mean for our
world design.

In practice, this note is meant to answer:

1. When should migration count as a genuine lineage bottleneck?
2. When can a small founding group plausibly create new long-run structure?
3. What controls do we need so we do not label ordinary spread as innovation?

## Short Answer

The literature suggests a balanced position:

```text
Founder events matter,
but bottlenecks alone are not enough.

A small colonizing group becomes interesting only when:
- it enters a meaningfully different habitat,
- selection changes after entry,
- inherited structure is reweighted rather than merely copied,
- and the descendant lineage persists or differentiates.
```

This is good news for `alife_biosphere`.

It means we do not need to simulate textbook biological speciation.
We do need to make colonization a distinct ecological event with:

- a bottleneck,
- a new local selection regime,
- lineage-level tracking,
- and controls against drift-only storytelling.

## Core Papers

## 1. Mayr (1954), "Change of Genetic Environment and Evolution"

Why it matters:

- this is one of the classic foundations for peripheral isolates and founder
  thinking
- it emphasizes that evolutionary change is not only about mutation count; the
  surrounding genetic and ecological context also changes

What we should take from it:

- a lineage entering a new habitat should not be treated as a smaller copy of
  the old population
- inherited structure may change meaning after migration
- context shift is part of the event, not just sample size reduction

What we should not over-import:

- we should not claim that every small isolate becomes a new lineage type
- our system is digital and ecological, not a direct model of biological
  reproductive isolation

Design implication:

```text
migration event
-> founder bottleneck
-> new habitat context
-> altered selective meaning of inherited structure
```

## 2. Templeton (1980), "The Theory of Speciation via the Founder Principle"

Why it matters:

- this is the strongest formal founder-effect entry point for our purposes
- it upgrades the vague founder principle into a more explicit account of when
  a founder event may produce a rapid shift

The key idea we should reuse:

Templeton's account is not "small population -> magic innovation."

It is closer to:

```text
founder event
-> altered population structure
-> altered selection on interacting traits
-> possible shift to a different adaptive region
```

For us, the important part is the middle:

```text
selection changes because structure and context changed
```

Design implication:

- colonization should be followed by a period of altered local pressure
- the event should affect interacting behavior bundles, not only one parameter
- founder success should be judged by later lineage persistence, not immediate
  survival alone

Useful translation into biosphere terms:

- bottleneck severity
- habitat novelty
- post-colonization adaptation lag
- lineage reexpansion success
- inherited capsule retention after habitat shift

## 3. Dodd and Powell (1985), "Founder-Flush Speciation: An Update of Experimental Results with Drosophila"

Why it matters:

- this gives an experimental angle rather than only theory
- useful for separating "founder event happened" from "founder event caused a
  durable shift"

What we should take from it:

- founder events need explicit observation after the bottleneck
- temporary spread and durable divergence are different outcomes

Design implication:

- colonization experiments should not stop at initial survival
- we need follow-up windows:
  - immediate survival
  - reexpansion
  - persistence
  - divergence from source lineage

## 4. Barton and Charlesworth (1984), "Genetic Revolutions, Founder Effects, and Speciation"

Why it matters:

- this is the important skeptical counterweight
- it prevents us from turning founder effects into a storytelling machine

What we should take from it:

- founder-effect speciation claims need strong evidence
- many apparent founder narratives can be explained by ordinary selection,
  drift, or later divergence
- bottlenecks do not automatically generate new adaptive organization

This paper is useful for us precisely because it is cautionary.

It tells us our digital system should not treat:

```text
small migrant group
```

as equal to:

```text
new lineage mechanism
```

Design implication:

We need controls.

At minimum:

- bottleneck migration vs no-bottleneck migration
- novel habitat colonization vs same-habitat recolonization
- lineage persistence vs short-lived occupancy

## 5. Moya, Galiana, Ayala (1995), "Founder-effect speciation theory: failure of experimental corroboration"

Why it matters:

- this is another strong caution signal
- it argues that empirical support for founder-effect speciation was weaker than
  many narratives suggested

What we should take from it:

- do not claim founder dynamics just because small-group colonization looks
  dramatic
- make negative controls part of the design from the start

Design implication:

- every founder experiment should include null comparisons
- lineage novelty must be measured, not inferred from drama

## What This Means For Our Project

The literature does support founder events as a meaningful source of lineage
turnover.
It does not support a naive version where bottlenecks alone create innovation.

For `alife_biosphere`, the defensible interpretation is:

```text
Founder effects are a structured colonization mechanism.
They become scientifically interesting only when bottlenecked migration enters
a changed habitat and leads to measurable lineage persistence, altered behavior,
or new ecological role occupancy.
```

That is a much stronger and more useful standard than:

```text
a few agents moved and later behaved differently
```

## Direct Design Consequences

## 1. Colonization must be a first-class event

We should add an explicit event type:

```text
colonization_event
```

Suggested payload fields:

- `source_habitat_id`
- `target_habitat_id`
- `founder_group_id`
- `founder_group_size`
- `lineage_id`
- `bottleneck_severity`
- `target_habitat_novelty`

## 2. Migration should sometimes be group-level, not always individual

The founder literature is more meaningful when a small set of related units
enters a new habitat together.

That suggests adding:

- `founder_group_id`
- optional group migration mode
- group persistence tracking

This also connects naturally to later work on higher-level individuality.

## 3. Habitat novelty must be logged explicitly

If target habitat is not meaningfully different, then founder language becomes
weak.

We should therefore log a simple novelty score at entry:

- protocol difference
- hazard difference
- resource profile difference
- occupancy regime difference

Suggested field:

```text
target_habitat_novelty
```

## 4. Post-colonization windows should be built into probes

We should not evaluate founder events at one time point only.

Recommended windows:

- immediate survival window
- short recovery window
- medium reexpansion window
- long persistence window

Suggested derived metrics:

- founder survival after `N` ticks
- descendant count after `N` ticks
- occupancy persistence
- lineage branching after colonization
- phenotype divergence from source lineage

## 5. We need founder-specific controls

Minimum control set:

### Control A. No bottleneck migration

Move a larger sample into the same target habitat.

Question:

```text
Was the observed effect due to small-group founding pressure,
or would any migration have produced it?
```

### Control B. Same-habitat recolonization

Apply the same bottleneck into a habitat that is not meaningfully novel.

Question:

```text
Was the effect due to habitat change,
or only due to temporary demographic compression?
```

### Control C. Drift-only interpretation check

Compare apparent founder divergence against persistence and ecological role
occupancy.

Question:

```text
Did a durable new role emerge,
or did a small group merely fluctuate before disappearing?
```

## Proposed Additions To The Existing Design

These are the cleanest immediate additions to `world_design_v0.md` and future
kernel specs.

### New fields

- `founder_group_id`
- `founder_group_size`
- `bottleneck_severity`
- `target_habitat_novelty`
- `colonization_tick`
- `source_lineage_id`

### New event types

- `colonization_event`
- `founder_group_failure`
- `founder_reexpansion`
- `founder_lineage_branch`

### New metrics

- founder survival rate
- founder reexpansion rate
- colonization persistence
- lineage turnover after migration
- founder-derived niche occupancy duration

## Proposed Experiment Slice

The first founder-effect probe does not need speciation-level ambition.

A reasonable first probe is:

```text
two source habitats
-> one harder frontier habitat
-> periodic small-group migration
-> compare small-group vs large-group entry
-> compare novel frontier vs familiar habitat
```

Success criterion for the probe:

```text
small-group colonization changes lineage outcomes
in a way that is not explained by simple spread alone
```

This is enough to justify founder-aware lineage mechanics without pretending we
have demonstrated biological speciation.

## Build Recommendations

This literature review suggests three near-term build tasks.

### 1. Add colonization-specific event logging

Reason:

- without this, founder dynamics will be invisible in the logs

### 2. Add habitat novelty scoring at migration time

Reason:

- without habitat difference, founder interpretation stays weak

### 3. Add founder controls before storytelling

Reason:

- the critical literature is clear that founder narratives are easy to
  overstate

## Bottom Line

The founder-effect literature gives us something useful but narrow.

It does not justify:

```text
bottleneck = innovation
```

It does justify:

```text
bottlenecked colonization as a special ecological mechanism
that can reshape lineage history when combined with new local selection pressure
and durable persistence
```

That is the version we should carry into `alife_biosphere`.

## Sources

- Mayr, E. (1954). "Change of Genetic Environment and Evolution."
  [Classic Texts page](https://www.blackwellpublishing.com/ridley/classictexts/mayr.asp)
- Templeton, A. R. (1980). "The Theory of Speciation via the Founder Principle."
  [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC1214177/)
- Dodd, D. M. B., Powell, J. R. (1985). "Founder-Flush Speciation: An Update of
  Experimental Results with Drosophila."
  [Oxford Academic](https://academic.oup.com/evolut/article/39/6/1388/6872523)
- Barton, N. H., Charlesworth, B. (1984). "Genetic Revolutions, Founder
  Effects, and Speciation."
  [Annual Reviews](https://www.annualreviews.org/content/journals/10.1146/annurev.es.15.110184.001025)
- Moya, A., Galiana, A., Ayala, F. J. (1995). "Founder-effect speciation theory:
  failure of experimental corroboration."
  [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC42086/)
