# Symbiosis, Mutualism, Partner Choice, And Holobiont Review v0

## Purpose

This note extends the literature program toward a major open question for
`alife_biosphere`:

```text
Can higher-order organization arise only from kin structure,
or can stable interdependence also emerge across different lineages?
```

The goal is to thicken the project's account of:

- mutualism,
- partner choice,
- host sanctions,
- long-term symbiosis,
- and holobiont-like composite organization.

In practice, this note asks:

1. Why are mutually beneficial cross-lineage relationships so hard to stabilize?
2. What mechanisms make symbiosis more durable than temporary cooperation?
3. When should a host-plus-partner system be treated as a meaningful higher
   unit, and when is that overreach?
4. How should the biosphere represent non-kin interdependence without becoming
   conceptually sloppy?

## Short Answer

The literature suggests a strong but careful position:

```text
cross-lineage cooperation can become highly stable,
but only when there are mechanisms that align interests strongly enough:
partner choice,
partner fidelity,
host sanctions,
shared dependence,
or repeated transmission coupling.
```

It also suggests an equally important caution:

```text
not every host-associated or mutually beneficial assemblage is a true unit of
selection.
```

For our project, that means:

- mutualism should be treated as structurally difficult, not naturally given;
- non-kin composite organization should be allowed, but not overclaimed;
- partner-choice and sanction mechanisms belong in the roadmap;
- holobiont-like organization should be modeled as a spectrum, not an automatic
  label.

## Core Papers

## 1. Bronstein (1994), "Our current understanding of mutualism"

Why it matters:

- this is one of the classic broad reviews of mutualism
- it is still useful because it emphasizes how diverse mutualisms are and how
  dangerous overgeneralization can be

The key lesson:

```text
mutualism is not one mechanism.
it is a family of interactions with different ecological conditions,
different vulnerabilities, and different evolutionary supports.
```

This matters directly to `alife_biosphere`.

If we later add cross-lineage beneficial relationships, they should not all be
treated as equivalent.

Design implication:

- mutualism type should be classified, not lumped together
- stability mechanisms should be logged explicitly

Useful translation into biosphere terms:

- `mutualism_mode`
- `partner_dependence`
- `stability_mechanism`

## 2. Bronstein (1994), "Conditional outcomes in mutualistic interactions"

Why it matters:

- this paper is especially important because it warns that mutualistic outcomes
  are often conditional
- it helps prevent a naive "benefits both -> permanent mutualism" story

The key lesson:

```text
the same interspecific association can shift among beneficial, neutral,
or even harmful outcomes depending on ecological context
```

This is a very useful design constraint.

For us, it means:

- a beneficial partnership in one habitat or phase may fail in another
- mutualism should be context-sensitive

Design implication:

- partnership value should depend on habitat, scarcity, and co-occupants
- the same pairing should be allowed to change outcome over time

Useful translation into biosphere terms:

- `conditional_mutualism_score`
- `context_dependence`
- `partnership_viability_window`

## 3. Sachs, Mueller, Wilcox, Bull (2004), "The evolution of cooperation"

Why it matters:

- this review is a major bridge between within-species and between-species
  cooperation
- it gives a useful framework of mechanisms such as byproduct benefits, partner
  choice, and partner-fidelity feedback

The key lesson:

```text
cross-lineage cooperation persists only under special structural conditions;
it is not a default outcome of repeated contact
```

This is exactly the tone we need.

The paper is especially useful for distinguishing mechanisms such as:

- byproduct mutualism
- partner choice
- partner fidelity feedback

Design implication:

- the biosphere should later encode why a mutualism is stable
- partner-fidelity and partner-choice mechanisms should be distinguishable

Useful translation into biosphere terms:

- `partner_choice_strength`
- `partner_fidelity_feedback`
- `byproduct_benefit_fraction`

## 4. Simms and Taylor (2002), "Partner Choice in Nitrogen-Fixation Mutualisms"

Why it matters:

- this is a clean canonical entry for partner choice
- it shows how one side of a mutualism can bias which partners are retained

The key lesson:

```text
mutualism can be stabilized not only by trust,
but by selective association with better partners
```

This is extremely useful for `alife_biosphere`.

It suggests that stable non-kin cooperation may require:

- selective admission
- selective retention
- selective investment

Design implication:

- future host-like organisms or groups should be able to sort partners
- partner-quality screening should be a real mechanism

Useful translation into biosphere terms:

- `partner_screening_threshold`
- `partner_selection_accuracy`
- `selective_association_gain`

## 5. Kiers et al. (2003), "Host sanctions and the legume-rhizobium mutualism"

Why it matters:

- this is one of the classic empirical demonstrations that sanctions can
  stabilize mutualism
- it shows that partner choice alone is not the whole story

The key lesson:

```text
ongoing cooperation can be maintained when hosts punish poorly performing
partners
```

This is especially important for us because many future biosphere structures
will involve:

- archive access
- shared resources
- partner-provided functions

and these will all be vulnerable to freeloading.

Design implication:

- sanction systems should not be reserved only for within-group policing
- cross-lineage partnerships may also require sanctions

Useful translation into biosphere terms:

- `host_sanction_strength`
- `partner_defection_penalty`
- `symbiosis_monitoring_accuracy`

## 6. Sagan/Margulis (1967), "On the origin of mitosing cells"

Why it matters:

- this is the classic symbiogenesis landmark
- it is the strongest reminder that some of the biggest evolutionary
  reorganizations may begin as long-run symbiotic integration

The key lesson:

```text
some major innovations may arise not from one lineage inventing everything,
but from formerly independent lineages becoming deeply integrated
```

This matters for the project because it opens a much bigger possibility:

- stable cross-lineage composites
- eventually inherited or developmentally repeated partnerships
- role-specialized consortia

Design implication:

- the biosphere should leave room for long-term cross-lineage binding, not only
  temporary trade
- symbiotic integration may become a source of novelty, not only a side
  interaction

Useful translation into biosphere terms:

- `symbiotic_binding_strength`
- `integration_depth`
- `composite_reproduction_dependence`

## 7. Bordenstein and Theis (2015), "Host Biology in Light of the Microbiome"

Why it matters:

- this is one of the clearest modern affirmative statements of holobiont-style
  thinking
- it argues that host-associated multispecies organization can be biologically
  central, not peripheral

What we should take from it:

- host-plus-microbiota systems can behave as meaningful biological entities
- development, physiology, and fitness can depend on composite organization

This is useful for our project because it legitimizes a stronger design horizon:

- a host-like lineage may depend on persistent associated partners
- development itself may be composite

Design implication:

- later worlds may support composite organism records
- phenotypes may depend partly on retained partner communities

Useful translation into biosphere terms:

- `composite_organism_score`
- `partner_set_stability`
- `developmental_symbiont_dependence`

## 8. Theis et al. (2016), "Getting the hologenome concept right"

Why it matters:

- this is useful because it is more careful and ecologically framed than a
  simple sloganized holobiont story
- it distinguishes the holobiont as an entity from stronger claims about unit
  selection

The key lesson:

```text
host-associated collectives are real ecological entities,
but different claims about evolutionary individuality should be kept separate
```

This is exactly the nuance we need.

Design implication:

- the biosphere can represent composite host-partner assemblages without
  assuming every such assemblage is a full unit of selection
- composite organization should be measured in degrees

Useful translation into biosphere terms:

- `holobiont_like_entity_score`
- `partner_transmission_mode`
- `selection_level_claim_strength`

## 9. Moran and Sloan (2015), Douglas and Werren (2016)

Why they matter:

- these are the most important cautionary counterweights
- they prevent us from treating all host-microbe or host-partner systems as
  holobionts in the strong sense

The key lesson:

```text
shared association is not enough.
without sufficient partner fidelity, aligned transmission,
and coherent selective interests,
the composite may not evolve as a unit.
```

This matters a lot for `alife_biosphere`.

Otherwise, once we add persistent partnerships, we may overclaim that we have
created a higher-level unit when we may only have created:

- repeated association
- loose dependence
- or ecological co-occurrence

Design implication:

- we should later measure:
  - partner fidelity
  - transmission coupling
  - alignment of survival and reproduction
  - conflict within composites

Useful translation into biosphere terms:

- `partner_fidelity`
- `transmission_coupling`
- `composite_conflict_score`
- `selection_alignment_score`

## What This Means For Our Project

The literature suggests that `alife_biosphere` should expand beyond
kin-structured cooperation while staying conceptually disciplined.

The strongest interpretation is:

```text
the world should support cross-lineage partnerships that range from
conditional mutualism,
to screened and sanctioned cooperation,
to long-term interdependence,
and in rare cases to composite organization approaching a higher-level entity
```

That is much more useful than either of these extremes:

- "all cooperation is basically kin selection"
- "every persistent host-partner system is a holobiont"

## Direct Design Consequences

## 1. Mutualism should have explicit stability mechanisms

Later worlds should distinguish at least:

- byproduct mutualism
- partner-choice mutualism
- partner-fidelity mutualism
- sanction-stabilized mutualism
- obligate interdependence

Suggested fields:

- `mutualism_mode`
- `partner_choice_strength`
- `partner_fidelity`
- `host_sanction_strength`

## 2. Partner quality should be screenable

This is one of the strongest practical implications.

Suggested fields:

- `partner_screening_threshold`
- `partner_quality_estimate`
- `association_acceptance_rule`

Suggested event types:

- `partner_screened`
- `partner_accepted`
- `partner_rejected`

## 3. Sanctions should extend beyond within-lineage policing

Future worlds should allow:

- withholding investment from poor partners
- breaking costly associations
- reducing partner benefit when cooperation fails

Suggested event types:

- `partner_sanctioned`
- `mutualism_broken`
- `benefit_withheld`

## 4. Composite organization should be a spectrum

The world should later distinguish:

- transient cooperation
- stable partnership
- developmentally important symbiosis
- strongly integrated composite

Suggested fields:

- `integration_depth`
- `developmental_symbiont_dependence`
- `composite_reproduction_dependence`
- `selection_alignment_score`

## 5. Holobiont-like claims should require evidence

We should later evaluate:

- partner fidelity
- shared transmission
- dependence of phenotype on partner set
- conflict within the composite
- persistence of composite identity

Suggested metrics:

- composite persistence
- partner turnover within composite
- selection alignment
- composite dependence score
- conflict within partnership

## Proposed Additions To The Existing Design

### New fields

- `mutualism_mode`
- `partner_choice_strength`
- `partner_fidelity`
- `host_sanction_strength`
- `integration_depth`
- `developmental_symbiont_dependence`
- `selection_alignment_score`

### New event types

- `partner_screened`
- `partner_accepted`
- `partner_rejected`
- `partner_sanctioned`
- `mutualism_broken`
- `symbiotic_binding_event`
- `composite_formation_event`

### New metrics

- mutualism persistence
- partner turnover
- sanction success rate
- screening accuracy
- composite dependence score
- partner-fidelity stability

## Proposed Probe Design

The first symbiosis-focused probe can stay moderate.

A reasonable first probe is:

```text
two lineage classes with complementary capabilities
-> allow optional partnership formation
-> compare no screening, screening-only, and screening-plus-sanctions
-> track persistence, cheating, and dependence over time
-> then test whether some stable partnerships become developmentally important
```

The first useful question is:

```text
Under what combinations of partner choice, sanctions, and transmission coupling
do cross-lineage partnerships remain conditional exchanges,
and under what conditions do they begin to look like stable composite units?
```

That is enough to justify a symbiosis layer.

## Build Recommendations

This literature review suggests three near-term design tasks.

### 1. Add cross-lineage partnership as a distinct ecological relation

Reason:

- otherwise every durable cooperation will be forced into kin or group language

### 2. Reserve space for partner screening and sanctions

Reason:

- these are among the strongest known stabilizers of mutualism

### 3. Treat composite organization as graded, not binary

Reason:

- the holobiont literature strongly warns against all-or-nothing categories

## Bottom Line

The symbiosis literature tells us that higher-order biological organization can
arise not only from kin groups, but also from stable, selected interdependence
across lineages.

But it also tells us to stay disciplined:

```text
interdependence is easy to claim,
true composite organization is harder,
and unit-of-selection language should be earned.
```

That is the version of symbiosis worth building toward in `alife_biosphere`.

## Sources

- Bronstein, J. L. (1994).
  "Our current understanding of mutualism."
  [University of Arizona record](https://experts.arizona.edu/en/publications/our-current-understanding-of-mutualism/)
- Bronstein, J. L. (1994).
  "Conditional outcomes in mutualistic interactions."
  [PubMed](https://pubmed.ncbi.nlm.nih.gov/21236825/)
- Sachs, J. L., Mueller, U. G., Wilcox, T. P., Bull, J. J. (2004).
  "The evolution of cooperation."
  [PubMed](https://pubmed.ncbi.nlm.nih.gov/15232949/)
- Simms, E. L., Taylor, D. L. (2002).
  "Partner Choice in Nitrogen-Fixation Mutualisms of Legumes and Rhizobia."
  [Oxford PDF](https://academic.oup.com/icb/article-pdf/42/2/369/1841794/i1540-7063-042-02-0369.pdf)
- Kiers, E. T., Rousseau, R. A., West, S. A., Denison, R. F. (2003).
  "Host sanctions and the legume-rhizobium mutualism."
  [Nature](https://www.nature.com/articles/nature01931)
- Sagan, L. (1967).
  "On the origin of mitosing cells."
  [ScienceDirect abstract page](https://www.sciencedirect.com/science/article/pii/0022519367900793)
- Bordenstein, S. R., Theis, K. R. (2015).
  "Host Biology in Light of the Microbiome: Ten Principles of Holobionts and Hologenomes."
  [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC4540581/)
- Theis, K. R. et al. (2016).
  "Getting the hologenome concept right: an eco-evolutionary framework for hosts and their microbiomes."
  [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC5069740/)
- Moran, N. A., Sloan, D. B. (2015).
  "The Hologenome Concept: Helpful or Hollow?"
  [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC4670207/)
- Douglas, A. E., Werren, J. H. (2016).
  "Holes in the Hologenome: Why Host-Microbe Symbioses Are Not Holobionts."
  [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC4817262/)
