# Formal Dual Inheritance And Recombination Models Review v0

## Purpose

This note narrows the inheritance literature to the most formal question we had
left open:

```text
If the biosphere eventually supports both vertical and cultural inheritance,
what do the more formal transmission models suggest about recombination,
selection, and forgetting?
```

We already have broad design notes on:

- multi-channel inheritance,
- archive validation,
- forgetting,
- provenance,
- and overload.

What was still missing is a more model-oriented view:

- what formal dual-inheritance models actually separate,
- how transmission and selection interact,
- where recombination enters,
- and what kind of simplifications are still defensible for our project.

## Short Answer

The formal literature supports a fairly clear position:

```text
Dual inheritance should be modeled as distinct transmission channels with
different timescales, different biases, and different coupling to selection.
```

It also suggests:

```text
Recombination is not a decorative extra.
It changes what combinations of inherited structure can be explored,
but only makes sense when the inherited pieces have meaningful identity.
```

For the biosphere, that means:

- keep vertical and horizontal inheritance explicitly separate;
- log transmission route and transmission bias;
- delay recombination until inherited units have stable boundaries;
- treat forgetting as a structural necessity, not as cleanup.

## 1. What Formal Dual-Inheritance Models Actually Buy Us

### [Cavalli-Sforza and Feldman 1978, "A dual inheritance model of the human evolutionary process I"](https://www.sciencedirect.com/science/article/abs/pii/0140175078900037)

Why it matters:

- this is the classic formal starting point;
- it treats biological and cultural transmission as distinct channels shaping
  phenogenotypes.

What we should take from it:

- dual inheritance is not just "genes plus some learning";
- the full state is a coupled phenotype/genotype object whose transmission
  depends on multiple rules.

Design implication:

- our biosphere should keep at least three explicit transmission labels:
  - vertical
  - horizontal
  - ecological
- and later allow them to interact rather than compressing everything into one
  inheritance update.

### [Feldman and Zhivotovsky 1992, "Gene-culture coevolution: toward a general theory of vertical transmission"](https://pmc.ncbi.nlm.nih.gov/articles/PMC50672/)

Main result:

- gives a general formulation of cultural transmission under vertical
  inheritance with multi-locus genetics;
- focuses on phenogenotype frequencies rather than only one transmission path.

What we should take from it:

- even "vertical" inheritance can be more complicated than parent copies
  offspring;
- the inherited state should be treated as structured, not atomic.

Design implication:

- offspring state should later allow:
  - inherited genome,
  - inherited developmental bias,
  - inherited cultural traces,
  each with separate fields.

### [Feldman, Cavalli-Sforza, and Peck 1985, "Gene-culture coevolution: models for the evolution of altruism with cultural transmission"](https://pmc.ncbi.nlm.nih.gov/articles/PMC390643/)

Main result:

- demonstrates that cultural transmission can qualitatively alter the evolution
  of traits such as altruism.

What we should take from it:

- cultural and genetic transmission do not only add linearly;
- transmission mode can change which social traits persist.

Design implication:

- if we later evolve cooperation, kin conflict, or sacrifice, we should not
  assume those traits can be understood from genetic inheritance alone;
- culture and direct interaction history may be decisive.

## 2. Selection And Dual Inheritance

### [Aoki 2001, "Theoretical and empirical aspects of gene-culture coevolution"](https://pubmed.ncbi.nlm.nih.gov/11560446/)

Why it matters:

- a compact synthesis of how cultural transmission interacts with selection.

What we should take from it:

- dual inheritance changes both equilibrium structure and transient dynamics;
- transmission bias matters alongside viability or fitness effects.

Design implication:

- biosphere experiments should always distinguish:
  - transmission bias
  - viability pressure
  - ecological feedback

### [Burger and Feldman 2018, "Gene-culture coevolution under selection"](https://www.sciencedirect.com/science/article/abs/pii/S0040580917301946)

Main result:

- formal analysis of genotype-dependent phenotypes under selection and cultural
  transmission;
- shows how polymorphism and equilibrium structure depend jointly on selection
  and transmission rules.

What we should take from it:

- transmission is not a passive wrapper around fitness;
- selection and transmission logic co-define the resulting population.

Design implication:

- our later probes should avoid saying "selection caused X" if transmission
  rules changed at the same time;
- transmission parameters must be exposed as first-class treatment variables.

### [Houkes 2012, "Population thinking and natural selection in dual-inheritance theory"](https://link.springer.com/article/10.1007/s10539-012-9307-5)

Why it matters:

- useful philosophical clarification of what dual-inheritance theory does and
  does not claim.

What we should take from it:

- not every cultural dynamics result should be called natural selection;
- population thinking can be useful without flattening all inheritance channels
  into one Darwinian story.

Design implication:

- our project should stay explicit about which dynamics are:
  - transmission effects,
  - ecological effects,
  - and which are genuinely selection-like.

## 3. Recombination And Combination

### [Ghirlanda, Enquist, and Perc 2010, "Modelling the evolution and diversity of cumulative culture"](https://pmc.ncbi.nlm.nih.gov/articles/PMC3013467/)

Main result:

- cumulative culture can be modeled through dependencies between cultural
  elements;
- combinations and stepwise constructions matter;
- path dependence can generate divergence between independently evolving
  cultures.

What we should take from it:

- recombination is not only sexual mixing;
- cultural combinations themselves can generate branching structure and
  historical contingency.

Design implication:

- archive recombination should later operate on capsules that have meaningful
  internal dependencies, not just unordered bag-of-skills merging;
- later cultural novelty can be measured partly through new combinations of
  existing capsules.

### [Evolution with recombination as Gibbs sampling (2023)](https://www.sciencedirect.com/science/article/pii/S0040580923000229)

Main result:

- gives a formal population-genetic model where recombination changes the
  distribution over offspring states in a precise way.

What we should take from it:

- recombination is a distribution-shaping operator, not just "mixing for
  diversity";
- the way parent contributions are sampled matters.

Design implication:

- once recombination exists in the biosphere, it should be logged with:
  - parent count,
  - inherited unit identities,
  - recombination success/failure,
  - downstream viability.

### [NEAT crossover grounding via Stanley and Miikkulainen 2002](https://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf)

Why it matters here:

- not a dual-inheritance paper, but still the most practical lesson for
  recombination in evolving structured systems:
  meaningful crossover requires homologous identities.

What we should take from it:

- recombination only makes sense after inherited units have stable markers such
  as innovation ids or capsule identities.

Design implication:

- do not add archive or genome recombination before unit identity is explicit;
- otherwise recombination will mostly be noise.

## 4. Forgetting In Formal Context

### [Enquist et al. 2007, "Critical Social Learning"](https://www.researchgate.net/publication/227723473_Critical_Social_Learning_A_Solution_to_Rogers%27s_Paradox_of_Nonadaptive_Culture)

Main result:

- socially copied information only remains adaptive when organisms validate and
  discard bad information.

What we should take from it:

- forgetting and rejection are part of adaptive transmission, not signs of
  failure.

Design implication:

- later archive models should include explicit discard logic;
- copied items should not move automatically into long-term structure.

### [Memory, Forgetting, And Distributed Memory Review v0](./memory_forgetting_and_distributed_memory_review_v0.md)

Why it matters here:

- our own existing review already established that forgetting must be active and
  selective.

What we should take from it:

- dual-inheritance models need an explicit forgetting channel if they are to
  remain ecologically meaningful at scale.

Design implication:

- later formal archive probes should vary:
  - forgetting pressure
  - retention thresholds
  - validation window length

## 5. What This Means For The Biosphere

The formal literature supports four strong rules.

### Rule 1. Treat transmission mode as a first-class variable

At minimum:

- vertical
- horizontal
- ecological

must remain distinguishable.

### Rule 2. Recombination requires unit identity

No stable inherited unit identity:

```text
=> recombination is mostly arbitrary mixing
```

Stable unit identity:

```text
=> recombination becomes a meaningful search operator
```

### Rule 3. Selection and transmission should never be narratively conflated

If a result changes when:

- validation changes,
- visibility changes,
- trust changes,
- or forgetting changes,

then it is not enough to say "selection favored it."

### Rule 4. Forgetting is part of the model, not just a storage cap

Without forgetting:

- archives saturate,
- low-value items persist too long,
- provenance becomes less useful,
- cultural overload becomes harder to interpret.

## 6. Best Remaining Use For This Literature

This formal line is most useful for later stages when we add:

- archive recombination,
- cross-lineage transfer,
- explicit parent-count choices,
- and dual-inheritance ablations.

It is less useful for M1 kernel mechanics, which is why it was left late.

## 7. Bottom Line

The cleanest lesson is:

```text
Dual inheritance is not only "more channels."
It is different transmission logic.
And once recombination is added, inherited unit identity becomes non-negotiable.
```

That is the main formal constraint this literature adds to the biosphere.
