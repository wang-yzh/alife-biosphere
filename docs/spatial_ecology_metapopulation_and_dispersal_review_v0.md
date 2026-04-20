# Spatial Ecology, Metapopulation, And Dispersal Review v0

## Purpose

This note extends the literature program toward a major missing layer in
`alife_biosphere`:

```text
How should space matter,
not just as geometry,
but as a driver of extinction, recolonization, persistence, and ecological
organization?
```

The goal is to thicken the current habitat-graph idea into something closer to
real spatial ecology.

In practice, this note asks:

1. Why should local extinction and recolonization matter?
2. What makes a habitat patch a source, a sink, or a corridor?
3. Why does fragmentation change more than map shape?
4. How should dispersal be treated as ecology rather than movement alone?

## Short Answer

The literature points to a very strong spatial-ecology view:

```text
space does not just distribute organisms.
space shapes whether lineages persist at all.
```

A world becomes ecologically spatial when:

- local populations can disappear without the whole lineage ending;
- recolonization depends on patch size, isolation, and connectivity;
- some habitats export surplus while others depend on immigration;
- corridors, barriers, and fragmentation change long-run persistence, not just
  travel convenience.

For our project, that means:

- habitat graph edges should eventually matter demographically, not only as move
  permissions;
- local extinction should be normal, not exceptional;
- recolonization and rescue effects should be first-class;
- source-sink structure should shape lineage and community organization.

## Core Papers

## 1. Levins (1969),
"Some demographic and genetic consequences of environmental heterogeneity for biological control"

Why it matters:

- this is the classic metapopulation starting point
- it introduces the core colonization-extinction perspective that still underlies
  most later spatial ecology thinking

The key lesson:

```text
a species can persist regionally even when local populations frequently go
extinct,
as long as colonization and recolonization keep the regional network alive
```

This is a very important conceptual upgrade for `alife_biosphere`.

Without it, a habitat graph risks becoming:

- a set of locations with travelers

instead of:

- a persistence system with turnover

Design implication:

- local extinction should be allowed and expected
- regional persistence should be a separate concept from local success
- colonization rate and extinction rate should be explicit variables

Useful translation into biosphere terms:

- `local_extinction_rate`
- `colonization_rate`
- `patch_occupancy`
- `regional_persistence`

## 2. Hanski (1998), "Metapopulation dynamics"

Why it matters:

- this is the best broad review for connecting classic metapopulation ideas to
  real fragmented landscapes
- it brings patch size, isolation, migration, and extinction together

The key lesson:

```text
metapopopulation persistence depends on patch area, patch isolation,
colonization, extinction, and migration among local populations
```

For us, this is directly actionable.

It means habitat nodes should not differ only in resource profile.
They should also differ in:

- area or effective capacity
- connectivity
- immigration sensitivity
- extinction sensitivity

Design implication:

- habitat graph should carry patch-level spatial meaning
- rescue effects should later be measurable
- occupancy should be treated as dynamic and stochastic

Useful translation into biosphere terms:

- `patch_capacity`
- `patch_isolation`
- `rescue_effect_strength`
- `occupancy_turnover`

## 3. Pulliam (1988), "Sources, sinks, and population regulation"

Why it matters:

- this is the canonical source-sink paper
- it is one of the most important corrections to naive local-performance
  thinking

The key lesson:

```text
some habitats can maintain populations through local surplus,
while others remain occupied only because immigrants keep arriving
```

This is enormously relevant for `alife_biosphere`.

It means:

- local occupancy does not imply local viability
- a lineage may look successful in a patch while actually depending on another
  patch
- habitat role should not be inferred only from who is present

Design implication:

- each habitat should later have source/sink diagnostics
- we should distinguish self-sustaining occupancy from immigration-dependent
  occupancy

Useful translation into biosphere terms:

- `source_surplus`
- `sink_dependence`
- `immigration_dependence`
- `self_sustaining_occupancy`

## 4. Hanski (2001), "Spatially realistic theory of metapopulation ecology"

Why it matters:

- this is useful because it pushes beyond spatially implicit theory
- it connects metapopulation thinking to explicit real-world patch geometry and
  movement structure

What we should take from it:

- explicit spatial configuration matters
- simple occupancy fraction alone is often not enough
- patch arrangement and movement pathways shape persistence

Design implication:

- habitat graph topology matters in its own right
- corridor placement and edge weight should affect recolonization dynamics

Useful translation into biosphere terms:

- `edge_distance`
- `corridor_quality`
- `spatial_recolonization_probability`

## 5. Fahrig (2003), "Effects of Habitat Fragmentation on Biodiversity"

Why it matters:

- this is the major review that prevents sloppy fragmentation claims
- it emphasizes how easy it is to confuse habitat loss with fragmentation per se

This matters directly to our project.

If we later change the graph, we should not casually treat:

- fewer patches
- smaller patches
- more isolation
- more broken connectivity

as if they were all one variable.

Design implication:

- fragmentation should be decomposed into distinct controls
- habitat amount and patch breakup should be separable in experiments

Useful translation into biosphere terms:

- `habitat_amount`
- `fragmentation_degree`
- `patch_breakup_score`
- `connectivity_loss`

## 6. Beier and Noss (1998), "Do Habitat Corridors Provide Connectivity?"

Why it matters:

- this is a classic corridor review
- it helps move corridor thinking out of pure intuition and into demographic
  consequences

What we should take from it:

- corridors are not just map decorations
- they matter when they improve movement, occupancy, or viability
- corridor value should be evaluated empirically, not assumed

Design implication:

- corridor edges should affect more than travel cost
- corridor benefit should be measurable at the population level

Useful translation into biosphere terms:

- `corridor_quality`
- `corridor_use_rate`
- `corridor_viability_gain`

## 7. MacArthur and Wilson (1967), island biogeography line

Why it matters:

- although older and simpler than modern metapopulation ecology, this is still a
  foundational way of thinking about colonization, extinction, and patch
  isolation

The key lesson:

```text
patch occupancy can reflect a dynamic balance between colonization and
extinction, shaped by size and isolation
```

This is still useful for us because it helps frame:

- patch size
- isolation
- immigration pressure

as first-order spatial variables.

Design implication:

- patch size and isolation should remain explicit in the world model even if the
  later ecology becomes richer than island theory

## What This Means For Our Project

The literature suggests that `alife_biosphere` should not treat the habitat
graph as a neutral navigation scaffold.

The stronger spatial-ecology interpretation is:

```text
the habitat graph is a persistence structure,
where local extinction, recolonization, rescue, corridor effects,
and source-sink asymmetries shape long-run lineage and community outcomes
```

That is a much richer target.

It also connects naturally to things we already care about:

- founder effects
- community assembly
- refuge habitats
- trophic asymmetries
- habitat engineering

## Direct Design Consequences

## 1. Local extinction should be normal

We should later assume that local occupancy is temporary in at least part of the
world.

Suggested fields:

- `local_extinction_risk`
- `patch_occupancy_state`
- `time_since_last_occupancy`

Suggested event types:

- `local_extinction_event`
- `recolonization_event`

## 2. Recolonization and rescue effects should be measurable

This is one of the strongest practical implications from metapopulation theory.

Suggested fields:

- `recolonization_probability`
- `rescue_effect_strength`
- `immigration_buffer`

Suggested metrics:

- rescue frequency
- recolonization lag
- occupancy recovery after local loss

## 3. Source and sink habitats should be diagnosed, not assumed

We should later distinguish:

- habitats that export surplus
- habitats that require immigration

Suggested fields:

- `source_surplus`
- `sink_dependence`
- `net_export_rate`
- `net_import_rate`

Suggested metrics:

- source-sink classification stability
- immigration dependence
- sink occupancy persistence

## 4. Fragmentation should be decomposed

Following Fahrig, later experiments should not bundle together:

- total habitat amount
- patch number
- patch isolation
- corridor loss

Suggested fields:

- `habitat_amount`
- `fragmentation_degree`
- `isolation_score`
- `corridor_quality`

## 5. Corridors should have demographic meaning

Corridors should not be just shortest-path helpers.

They should later affect:

- movement probability
- recolonization probability
- survival during dispersal
- recovery after local extinction

Suggested event types:

- `corridor_crossing`
- `corridor_failure`
- `corridor_supported_recolonization`

## Proposed Additions To The Existing Design

### New fields

- `patch_capacity`
- `patch_isolation`
- `local_extinction_risk`
- `recolonization_probability`
- `rescue_effect_strength`
- `source_surplus`
- `sink_dependence`
- `corridor_quality`
- `fragmentation_degree`

### New event types

- `local_extinction_event`
- `recolonization_event`
- `rescue_event`
- `corridor_crossing`
- `corridor_supported_recolonization`

### New metrics

- patch occupancy turnover
- recolonization lag
- rescue frequency
- source-sink stability
- corridor viability gain
- fragmentation sensitivity

## Proposed Probe Design

The first spatial-ecology probe can stay modest.

A reasonable first probe is:

```text
same lineage set
-> habitat graph with variable patch capacity and isolation
-> compare no-corridor, weak-corridor, and strong-corridor settings
-> allow local extinctions and recolonization
-> measure regional persistence and source-sink dependence
```

The first useful question is:

```text
Does the graph support regional persistence through turnover and recolonization,
or does it behave like a set of independent local worlds?
```

That is enough to justify a true spatial-ecology layer.

## Build Recommendations

This literature review suggests three near-term design tasks.

### 1. Give habitat nodes spatial-demographic meaning

Reason:

- otherwise the graph remains mostly geometric

### 2. Add local extinction and recolonization to the roadmap

Reason:

- spatial ecology is hard to justify without turnover

### 3. Separate habitat loss, fragmentation, and corridor quality in future experiments

Reason:

- they are related but not interchangeable

## Bottom Line

The spatial-ecology literature tells us that space becomes biologically
interesting when it changes persistence, not just position.

For `alife_biosphere`, the stronger target is:

```text
a habitat graph where extinction, recolonization, rescue, source-sink flow,
and fragmentation jointly shape long-run lineage and community structure
```

That is the version of space worth building.

## Sources

- Levins, R. (1969).
  "Some demographic and genetic consequences of environmental heterogeneity for
  biological control."
  [Oxford Academic](https://academic.oup.com/ae/article/15/3/237/255899)
- Hanski, I. (1998).
  "Metapopulation dynamics."
  [Nature](https://www.nature.com/articles/23876)
- Pulliam, H. R. (1988).
  "Sources, sinks, and population regulation."
  [ResearchGate PDF entry](https://www.researchgate.net/publication/230692996_Sources_Sinks_and_Population_Regulation)
- Hanski, I. (2001).
  "Spatially realistic theory of metapopulation ecology."
  [PubMed](https://pubmed.ncbi.nlm.nih.gov/11688412/)
- Fahrig, L. (2003).
  "Effects of Habitat Fragmentation on Biodiversity."
  [Annual Reviews](https://www.annualreviews.org/doi/10.1146/annurev.ecolsys.34.011802.132419)
- Beier, P., Noss, R. F. (1998).
  "Do Habitat Corridors Provide Connectivity?"
  [DOI metadata / public mirror](https://experts.nau.edu/en/publications/do-habitat-corridors-provide-connectivity)
- MacArthur, R. H., Wilson, E. O. (1967).
  "The Theory of Island Biogeography."
  [JSTOR book page](https://www.jstor.org/stable/j.ctt19cc1t2)
