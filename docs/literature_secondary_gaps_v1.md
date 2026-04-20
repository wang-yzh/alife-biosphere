# Secondary Literature Gaps Review v1

## Purpose

This document continues the literature collection after:

- `literature_gap_review_v0.md`
- `literature_to_mechanism_matrix_v0.md`
- `founder_effects_and_lineage_turnover_review_v0.md`

The goal here is narrower than in the first pass.
We want evidence for the next mechanisms that will affect implementation order:

- dual inheritance with validation, forgetting, and bounded copying
- signaling under deception, ambiguity, and trust failure
- catastrophe recovery, bottlenecks, and rescue dynamics
- spatial parasite pressure and substrate-level parasite management

This note is meant to answer one practical question:

```text
What do we now know strongly enough to move into the core world design?
```

## 1. Dual Inheritance, Validation, And Forgetting

### [Rendell et al. 2010, "Why Copy Others? Insights from the Social Learning Strategies Tournament"](https://pmc.ncbi.nlm.nih.gov/articles/PMC2989663/)

Main result:

- in a changing world, strategies that leaned heavily on social learning often
  performed best
- the benefit came partly from population-level filtering, because copied
  information had already been tested by others

What we should take from it:

- social learning is useful when it is selective, not when it is blind
- an archive can work as a distributed filter rather than a magical knowledge
  dump

Design implication:

- archive access should expose only a bounded slice of visible capsules
- copied capsules should retain source and recency metadata

### [Enquist et al. 2007, "Critical Social Learning: A Solution to Rogers's Paradox of Nonadaptive Culture"](https://www.researchgate.net/publication/227723473_Critical_Social_Learning_A_Solution_to_Rogers%27s_Paradox_of_Nonadaptive_Culture)

Main result:

- a strategy that first copies socially and then falls back to individual
  learning when the copied behavior fails can outperform pure social learning
- this advantage disappears when transmission is too noisy, environments change
  too quickly, or social learning becomes too expensive

What we should take from it:

- copying needs a validation phase
- culture remains adaptive only if organisms can discard bad inherited or
  copied structure

Design implication:

- archive use should follow `copy -> test -> retain/discard`
- forgetting is not a bug; it is a required mechanism

### [Rendell et al. 2012, "Adaptive strategies for cumulative cultural learning"](https://www.sciencedirect.com/science/article/abs/pii/S0022519312000756)

Main result:

- strategies that work for simple social learning do not automatically work for
  cumulative cultural learning
- cumulative systems depend on how copying, innovation, and improvement are
  sequenced

What we should take from it:

- the archive should distinguish:
  - copied structure
  - refined structure
  - recombined structure

Design implication:

- cultural capsules should record provenance and modification status

### [Fay et al. 2019, "Increasing population size can inhibit cumulative cultural evolution"](https://pmc.ncbi.nlm.nih.gov/articles/PMC6452720/)

Main result:

- more available exemplars do not automatically improve cumulative culture
- coordination and working-memory constraints can reverse the expected benefits

What we should take from it:

- larger archive visibility can make the system worse, not better

Design implication:

- archive visibility, copying time, and evaluation budget should all be capped

## 2. Signaling Under Deception, Ambiguity, And Trust

### [Smaldino et al. 2018, "The Evolution of Covert Signaling"](https://pmc.ncbi.nlm.nih.gov/articles/PMC5861109/)

Main result:

- ambiguous signals can improve cooperation by helping similar agents assort
  without openly alienating dissimilar ones

What we should take from it:

- useful signaling is not always fully public and fully transparent

Design implication:

- signals in the biosphere should be allowed to be partially decodable and
  receiver-dependent

### [Számadó 2017, "When honesty and cheating pay off: the evolution of honest and dishonest equilibria in a conventional signalling game"](https://bmcecolevol.biomedcentral.com/articles/10.1186/s12862-017-1112-y)

Main result:

- both honest and deceptive signaling equilibria can be stable under different
  population conditions

What we should take from it:

- honesty should not be assumed
- bluffing should remain a legal strategy in the world

Design implication:

- signal trust must be dynamic
- deceptive signaling needs to be logged as a measurable event family

### [Számadó et al. 2023, "Honesty in signalling games is maintained by trade-offs rather than costs"](https://link.springer.com/article/10.1186/s12915-022-01496-9)

Main result:

- reliable signaling does not require high equilibrium signal cost
- trade-offs between sender and receiver outcomes matter more than simple cost

What we should take from it:

- "make signals expensive" is not enough

Design implication:

- we should couple signaling to verification, future trust, and partner choice
  consequences, not only energy cost

## 3. Bottlenecks, Founder History, And Rescue

### [Orr and Unckless 2014, "The Population Genetics of Evolutionary Rescue"](https://pmc.ncbi.nlm.nih.gov/articles/PMC4133041/)

Main result:

- rescue probability depends on the amount and source of adaptive variation,
  and rescued populations often show a decline followed by rebound

What we should take from it:

- rescue is not a vague success story; it has measurable geometry

Design implication:

- probes should log trough depth, rebound delay, and the inferred source of
  rescue

### [Olazcuaga et al. 2023, "Population demographic history and evolutionary rescue: Influence of a bottleneck event"](https://doi.org/10.1111/eva.13581)

Main result:

- populations with bottleneck history were more extinction-prone and adapted
  less strongly in a subsequent challenge than populations without bottleneck
  history

What we should take from it:

- demographic history before a crisis changes future rescue odds

Design implication:

- every lineage should track founder history and severe bottleneck count

### [LaBar and Adami 2017, "Evolution of drift robustness in small populations"](https://www.nature.com/articles/s41467-017-01003-7)

Main result:

- small populations can evolve reduced sensitivity to drift by occupying
  drift-robust regions of the fitness landscape

What we should take from it:

- small groups are not only fragile; they can be differently robust

Design implication:

- local deme size and founder bottleneck width should be independent variables

### [Eriksson et al. 2014, "The emergence of the rescue effect from explicit within- and between-patch dynamics in a metapopulation"](https://pmc.ncbi.nlm.nih.gov/articles/PMC4027396/)

Main result:

- rescue effects emerge from explicit patch dynamics rather than requiring a
  separate macro-level assumption

What we should take from it:

- rescue should arise from habitat structure and migration, not from a hidden
  global safeguard

Design implication:

- the world needs refuges and non-trivial migration structure

### [Draghi et al. 2024, "Demographic feedbacks during evolutionary rescue can slow or speed adaptive evolution"](https://pmc.ncbi.nlm.nih.gov/articles/PMC10865011/)

Main result:

- demographic feedback can either slow or accelerate rescue depending on how
  ecological and genetic effects couple

What we should take from it:

- disturbance response should not be reduced to a single scalar penalty

Design implication:

- post-shock dynamics should depend on occupancy, diversity, and resource state

## 4. Spatial Parasite Dynamics And Substrate Management

### [Tellier and Brown 2011, "Spatial heterogeneity, frequency-dependent selection and polymorphism in host-parasite interactions"](https://pmc.ncbi.nlm.nih.gov/articles/PMC3273489/)

Main result:

- spatial heterogeneity and limited coupling between demes help maintain
  polymorphism in host-parasite systems

What we should take from it:

- well-mixed worlds erase exactly the structure we need

Design implication:

- parasite pressure should vary across habitats and migration must stay bounded

### [Deshpande et al. 2025, "Landscape structure as a driver of eco-evolution in host-parasite systems"](https://pmc.ncbi.nlm.nih.gov/articles/PMC12137051/)

Main result:

- network topology changes virulence evolution qualitatively, and kin structure
  explains much of the difference across landscapes

What we should take from it:

- graph topology is not neutral

Design implication:

- the habitat graph itself should become an experimental treatment

### [Stepney and Hickinbotham 2021, "What is a Parasite? Defining reaction and network properties in an open ended automata chemistry"](https://pure.york.ac.uk/portal/en/publications/what-is-a-parasite-defining-reaction-and-network-properties-in-an/)

Main contribution:

- proposes operational definitions for parasitic structure in Stringmol-like
  systems

What we should take from it:

- parasitism should be defined from interaction and network properties, not
  only from narrative interpretation

Design implication:

- our interaction graph should support operational parasite detection

### [Hickinbotham et al. 2016, "Maximizing the Adjacent Possible in Automata Chemistries"](https://pubmed.ncbi.nlm.nih.gov/26649811/)

Main contribution:

- substrate-level softness and mortality affect whether chemistry-like systems
  can keep innovating in the presence of exploiters

What we should take from it:

- over-rigid rule systems make parasite pressure absolute and brittle

Design implication:

- the biosphere should keep some interaction softness and avoid hard immortal
  categories

### [Plum et al. 2025, "Spatial structure supports diversity in prebiotic autocatalytic chemical ecosystems"](https://pmc.ncbi.nlm.nih.gov/articles/PMC12226336/)

Main result:

- spatial structure supports coexistence of otherwise incompatible cycles and
  exposes more variation to selection

What we should take from it:

- space preserves diversity even below the organism level

Design implication:

- adjacency and local occupancy are non-negotiable even in the minimal world

## 5. Strong New Design Commitments

This second literature pass makes the following commitments defensible.

1. Culture must be selective:
   copying requires validation, bounded visibility, and forgetting.

2. Signaling must be fallible:
   honesty, deception, and covert coordination should all be legal states.

3. Disturbance must be historically grounded:
   founder history and bottleneck scars must affect later rescue.

4. Rescue must be spatial:
   it should emerge from refuge structure and migration, not a hidden reset.

5. Parasites must be operationalized:
   parasitism should be inferable from event and network data.

## 6. What Still Remains For Later

The next follow-up literature pass, after the next design freeze, should focus
on:

- explicit dual-inheritance models with recombination and forgetting
- signaling language evolution under stronger deception
- quantitative early-warning indicators for collapse
- more direct parasite-management mechanisms in spatial artificial chemistries

