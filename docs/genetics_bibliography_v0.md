# Genetics Bibliography v0

## Purpose

This note collects the genetics and inheritance papers that matter most for the
first real design of `alife_biosphere`.

The goal is not to maximize paper count. The goal is to answer five engineering
questions:

```text
1. What should count as the heritable unit?
2. How should genomes be recombined without nonsense crossover?
3. What should stay genetic, what should stay somatic, and what should be
   short-lived epigenetic memory?
4. Which mutation operators are likely to create useful structure instead of
   mostly breakage?
5. How should we stage inheritance so that v0 is useful without pretending to
   solve all of biology?
```

## Short Answer

The literature points toward a layered approach:

```text
genome
+ epigenome
+ somatic learning
+ ecological inheritance
+ cultural inheritance
```

And it strongly argues against starting with:

```text
"take everything learned in a lifetime and write it directly into the genome"
```

## A. Directly Actionable Papers

These are the papers I would treat as first-pass design anchors.

### [Stanley and Miikkulainen 2002, "Evolving Neural Networks through Augmenting Topologies"](https://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf)

Why it matters:

- gives a practical answer to homologous crossover through `historical
  markings` / innovation ids;
- shows why structural innovation needs temporary protection;
- supports incremental complexification from a simple founder genome.

Build implication:

- every structural gene in our system should carry an `innovation_id`;
- v0 crossover, if present at all, should align genes by innovation id instead
  of position;
- speciation or clade protection should exist before sexual recombination is
  turned on.

### [Hinton and Nowlan 1987, "How Learning Can Guide Evolution"](https://www.cs.toronto.edu/~hinton/absps/evolution.htm)

Why it matters:

- the classic Baldwin-effect argument;
- learning changes selection pressure without directly becoming genome.

Build implication:

- keep lifetime learning and inherited structure separate;
- let learning affect reproductive success first;
- do not assume Lamarckian write-back is the right default.

### [Fernando et al. 2018, "Meta-Learning by the Baldwin Effect"](https://arxiv.org/abs/1806.07917)

Why it matters:

- shows a modern version of Baldwin-style adaptation;
- the inherited object is often a learning bias, initialization, or
  hyperparameter, not a final solved behavior.

Build implication:

- genome should encode biases and capacities, not whole solved policies;
- inherited material should often be "how easy it is to learn X" rather than
  "X itself".

### [Danchin et al. 2011, "Beyond DNA: integrating inclusive inheritance into an extended theory of evolution"](https://www.nature.com/articles/nrg3028)

Why it matters:

- clean statement that inheritance is broader than sequence transmission;
- useful for separating genetic, epigenetic, ecological, and cultural channels.

Build implication:

- inheritance should be logged by channel;
- experiments should distinguish:
  - genetic inheritance
  - epigenetic carryover
  - ecological inheritance
  - cultural inheritance

### [Perez and Lehner 2019, "Intergenerational and transgenerational epigenetic inheritance in animals"](https://www.nature.com/articles/s41556-018-0242-9)

Why it matters:

- useful conceptual distinction between short-timescale parental effects and
  longer-timescale transgenerational effects;
- emphasizes molecules and signals beyond DNA.

Build implication:

- epigenetic marks in the biosphere should be:
  - low bandwidth
  - explicitly decaying
  - inherited for a limited number of generations

### [Cussat-Blanc, Harrington, and Banzhaf 2018, "Artificial Gene Regulatory Networks: A Review"](https://pubmed.ncbi.nlm.nih.gov/30681915/)

Why it matters:

- the best compact review for genome-to-phenotype systems that are more
  life-like than flat parameter tables;
- useful bridge from genotype to development.

Build implication:

- v0 does not need a full AGRN;
- but the genome should be shaped so it can later grow into a regulatory system
  rather than needing a rewrite.

### [Parter, Kashtan, and Alon 2008, "Facilitated Variation: How Evolution Learns from Past Environments To Generalize to New Environments"](https://pmc.ncbi.nlm.nih.gov/articles/PMC2563028/)

Why it matters:

- environments with reusable substructure promote modular variation and
  generalization;
- this connects world design to genome design.

Build implication:

- habitats should vary in structured combinations, not random soup;
- genome modules should be reusable across habitat families.

### [Kirschner and Gerhart 1998, "Evolvability"](https://pmc.ncbi.nlm.nih.gov/articles/PMC33871/)

Why it matters:

- argues that evolvability depends on weak linkage, compartmentation,
  exploratory mechanisms, and robust reuse.

Build implication:

- do not make every mutation globally coupled;
- prefer modular genomes and partially decoupled regulatory links.

### [Whitacre 2010, "Degeneracy: a link between evolvability, robustness and complexity in biological systems"](https://pmc.ncbi.nlm.nih.gov/articles/PMC2830971/)

Why it matters:

- partial overlap in function is often better than one-function-per-module;
- a strong clue for how to avoid brittle specialization.

Build implication:

- different modules may overlap in what they can do;
- the phenotype should not collapse if one module mutates or disappears.

### [Jouffrey, Leonard, and Ahnert 2021, "Gene duplication and subsequent diversification strongly affect phenotypic evolvability and robustness"](https://pmc.ncbi.nlm.nih.gov/articles/PMC8220273/)

Why it matters:

- duplication is not just redundancy; it can improve both robustness and future
  innovation.

Build implication:

- duplication-divergence should be a first-class mutation operator;
- duplication should happen at the module level, not just scalar parameter
  level.

### [Wagner and Altenberg 1996, "Complex Adaptations and the Evolution of Evolvability"](https://dynamics.org/Altenberg/PAPERS/CAEE/)

Why it matters:

- one of the clearest statements that random variation alone is not enough;
- complex adaptation depends on representation that makes useful variation
  reachable.

Build implication:

- genome design is not a detail; it is the main lever of evolvability;
- we should treat representation quality as a first-class design variable, not
  a later optimization.

## B. Strong Supporting Papers

These are not necessarily first reads, but they sharpen specific mechanisms.

### [Soucy, Huang, and Gogarten 2015, "Horizontal gene transfer: building the web of life"](https://www.nature.com/articles/nrg3962)

Use:

- high-level intuition for horizontal gene transfer;
- especially useful later when we add non-reproductive exchange.

Build implication:

- horizontal transfer should be conditional, local, and ecologically grounded;
- it should probably begin as rare module transfer, not whole-genome mixing.

### [Atkinson, Plump, and Stepney 2020, "Horizontal gene transfer for recombining graphs"](https://link.springer.com/article/10.1007/s10710-020-09378-1)

Use:

- a computational model of neutral HGT on structured graph-like genotypes.

Build implication:

- if genome becomes graph-structured, HGT can copy inactive or latent
  subgraphs;
- suggests a later-stage mechanism after clonal inheritance is stable.

### [Nasvall et al. 2012, "Real-Time Evolution of New Genes by Innovation, Amplification, and Divergence"](https://pmc.ncbi.nlm.nih.gov/articles/PMC4392837/)

Use:

- argues for the `innovation-amplification-divergence` path.

Build implication:

- v1 mutation operators should include:
  - latent weak function
  - amplification
  - divergence under continued pressure

### [Copley 2020, "Evolution of new enzymes by gene duplication and divergence"](https://pmc.ncbi.nlm.nih.gov/articles/PMC9306413/)

Use:

- helps distinguish naive duplication from useful duplication under selection.

Build implication:

- duplicated modules should pay a cost until they earn their keep;
- otherwise duplication becomes free clutter.

### [Melo, Porto, and Cheverud 2016, "Modularity: genes, development and evolution"](https://pmc.ncbi.nlm.nih.gov/articles/PMC5617135/)

Use:

- clarifies that modularity is genetic, developmental, and phenotypic.

Build implication:

- we should log modularity at multiple levels:
  - genome modularity
  - behavior modularity
  - habitat-protocol modularity

### [Uller et al. 2018, "Developmental Bias and Evolution: A Regulatory Network Perspective"](https://pmc.ncbi.nlm.nih.gov/articles/PMC6063245/)

Use:

- developmental bias is not noise; some phenotypes are easier to produce than
  others for structural reasons.

Build implication:

- the project should not try to make all phenotypes equally reachable;
- the design should intentionally produce bias in what variation is easy.

### [Elena and Sanjuan 2008, "The effect of genetic robustness on evolvability in digital organisms"](https://link.springer.com/article/10.1186/1471-2148-8-284)

Use:

- explicit digital-evolution evidence that robustness can promote evolvability.

Build implication:

- we should monitor:
  - mutational survivability
  - offspring viability under perturbation
  - post-mutation adaptation speed

### [Mesoudi and Thornton 2018, "What is cumulative cultural evolution?"](https://pmc.ncbi.nlm.nih.gov/articles/PMC6015846/)

Use:

- helps define when shared archive behavior is merely transmission versus true
  cumulative culture.

Build implication:

- archive metrics should distinguish:
  - copying
  - retention
  - additive improvement
  - lineage-independent reuse

### [Lala 2025, "A developmentalist's view of inheritance"](https://link.springer.com/article/10.1007/s10211-025-00464-0)

Use:

- a recent open-access review emphasizing that inheritance should be understood
  as transmission of developmental means, not DNA sequence alone.

Build implication:

- reinforces the decision to separate:
  - genome
  - developmental bias
  - epigenetic carryover
  - ecological context
- supports treating development as part of inheritance architecture rather than
  a post hoc training stage

### [Jablonka-style epigenetic review via Nilsson et al. 2018, "Environmentally induced epigenetic transgenerational inheritance of disease"](https://pmc.ncbi.nlm.nih.gov/articles/PMC6051467/)

Use:

- not because disease is our target, but because it clarifies germline-like
  persistence and the difference between direct exposure and true
  transgenerational effects.

Build implication:

- if we simulate epigenetic marks, we should distinguish:
  - direct parental carryover
  - true multi-generation persistence

## C. Design Conclusions

If we only keep the strongest engineering consequences, the literature says:

### C1. Start clonal

The first useful inheritance system should be:

```text
vertical clonal inheritance
+ mutation
+ duplication/divergence
+ lineage logging
```

Reason:

- it is much easier to attribute success or collapse to inherited structure;
- it supports clean lineage analysis;
- it matches the earliest stable route to higher-level individuality.

### C2. Add epigenetic carryover before sexual crossover

Reason:

- low-bandwidth parental bias is cheaper and more interpretable than early
  multi-parent recombination;
- it lets us test whether short-lived inherited stress memory matters.

### C3. Only add crossover after homologous gene identity exists

Reason:

- otherwise crossover is mostly destructive;
- innovation ids or equivalent homology markers should exist first.

### C4. Use duplication/divergence as a primary innovation operator

Reason:

- it is biologically grounded;
- it scales better than only point mutation;
- it gives a clean path from redundancy to specialization.

### C5. Keep cultural inheritance separate from genome

Reason:

- genome should remain the slow structural channel;
- cultural archive should remain an explicit, costly, inspectable second
  inheritance channel.

## D. Proposed v0-v2 Inheritance Staging

### v0

```text
genome
+ clonal reproduction
+ point mutation
+ module duplication
+ lineage logging
```

### v1

```text
v0
+ decaying epigenetic tags
+ inheritance bandwidth
+ juvenile development effects
```

### v2

```text
v1
+ homologous crossover
+ optional horizontal transfer
+ cultural archive with access cost
```

## E. Next Reading Order

If time is limited, read in this order:

1. Stanley and Miikkulainen 2002
2. Hinton and Nowlan 1987
3. Danchin et al. 2011
4. Cussat-Blanc et al. 2018
5. Parter et al. 2008
6. Kirschner and Gerhart 1998
7. Whitacre 2010
8. Jouffrey et al. 2021

That set is enough to design the first usable genetics layer without pretending
we already understand all inheritance channels.
