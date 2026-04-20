# Literature Gap Review v0

## 1. Purpose

This document collects the literature that was missing from the first round of
world design.

The goal is not to assemble a large bibliography. The goal is to close the
argument gaps behind the following design claims:

- higher-level individuality does not arise from resource competition alone
- ecological inheritance must be modeled explicitly
- cooperation, communication, and cheating need formal treatment
- development must be separated from simple training
- evolvability requires structured variation, not only adaptation
- the simulation substrate itself constrains what kind of life can emerge
- community assembly and open-endedness need dedicated measurement
- cultural inheritance is a separate evolutionary channel

All papers listed here were selected because they change what we should build,
measure, or control in the biosphere.

## 2. Collected Directions

| Direction | Why it matters for us | Collection status |
| --- | --- | --- |
| Major transitions in individuality | justifies kin groups, division of labor, group-level traits | collected |
| Niche construction and ecological inheritance | justifies state-dependent habitats and environmental memory | collected |
| Cooperation, communication, cheating, coevolution | justifies parasites, signaling, and anti-freeloader design | collected |
| Development and phenotypic plasticity | justifies juvenile stage and genome-to-phenotype separation | collected |
| Evolvability, modularity, canalization | justifies modular protocols and structured environmental variation | collected |
| Artificial chemistry and substrate design | justifies bottom-level world rules and replication substrate choices | collected |
| Community assembly and ecological networks | justifies invasion, occupancy, and assembly metrics | collected |
| Measurement of open-endedness | justifies metric discipline and raw event preservation | collected |
| Cultural inheritance and cumulative culture | justifies archive design, access cost, and transmission constraints | collected |

## 3. Major Transitions in Individuality

### [West et al. 2015, "Major evolutionary transitions in individuality"](https://pmc.ncbi.nlm.nih.gov/articles/PMC4547252/)

Main idea:

- a major transition requires more than cooperation
- lower-level units must become mutually dependent
- within-group conflict must become negligible enough that the higher-level unit
  behaves as an individual

Result that matters:

- division of labor, communication, mutual dependence, and conflict suppression
  are not optional decorations; they are core conditions for higher-level
  individuality

Design implication:

- the biosphere needs explicit support for kin groups, group traits, and
  group-level failure modes
- we should not claim "new individuals" merely because clusters form

### [Moreno and Ofria 2019, "Toward Open-Ended Fraternal Transitions in Individuality"](https://pubmed.ncbi.nlm.nih.gov/31150287/)

Main idea:

- digital evolution can be used to study fraternal transitions where related
  units combine into higher-level entities

Result that matters:

- argues directly that transitions in individuality are one of the missing
  ingredients in digital systems that aspire to open-ended complexity

Design implication:

- our world should include conditions under which offspring groups, not only
  isolated individuals, can become the selectable unit

### [Moreno and Ofria 2022, "Exploring Evolved Multicellular Life Histories in a Open-Ended Digital Evolution System"](https://www.frontiersin.org/journals/ecology-and-evolution/articles/10.3389/fevo.2022.750837/full)

Main result:

- repeated emergence of reproductive division of labor, resource sharing within
  kin groups, resource investment in offspring groups, asymmetrical
  message-mediated behavior, morphological patterning, and adaptive apoptosis

Design implication:

- we should support:
  - kin recognition
  - local messaging
  - offspring-group investment
  - adaptive self-sacrifice
  - asymmetric roles within a lineage

### [Goldsby et al. 2014, "The Evolutionary Origin of Somatic Cells under the Dirty Work Hypothesis"](https://pmc.ncbi.nlm.nih.gov/articles/PMC4019463/)

Main result:

- when useful work carries mutagenic cost, digital multicells evolve a
  germ-soma split
- lineages often pass through a "pseudo-soma" stage before true soma

Design implication:

- useful but damaging work should exist in the world
- reproductive protection and task specialization should be modelable
- we should log transitional organization, not only final successful forms

### [Ispolatov et al. 2012, "Division of labour and the evolution of multicellularity"](https://pmc.ncbi.nlm.nih.gov/articles/PMC3297448/)

Main result:

- aggregates can gain new fitness peaks when incompatible tasks are distributed
  across cells

Design implication:

- the world should contain task incompatibilities that make specialization
  valuable
- one unit doing everything well should be structurally disfavored

## 4. Niche Construction and Ecological Inheritance

### [Laland et al. 2016, "An introduction to niche construction theory"](https://pmc.ncbi.nlm.nih.gov/articles/PMC4922671/)

Main idea:

- organisms do not only adapt to environments; they also systematically modify
  them
- those modifications can persist across generations as ecological inheritance

Design implication:

- `ecological_memory` is not optional terminology; it is a real inheritance
  channel
- habitats should retain lineage-caused changes that influence descendants

### [Laland et al. 2017, "Niche construction, sources of selection and trait coevolution"](https://pmc.ncbi.nlm.nih.gov/articles/PMC5566808/)

Main result:

- niche construction modifies selection in directed and sustained ways, for the
  constructor and for other species

Design implication:

- habitat dynamics should depend partly on occupant behavior
- environmental feedback should affect both self-lineages and competitors

### [Adams et al. 2017, "Formal Definitions of Unbounded Evolution and Innovation Reveal Universal Mechanisms for Open-Ended Evolution in Dynamical Systems"](https://pmc.ncbi.nlm.nih.gov/articles/PMC5430523/)

Main result:

- among the tested mechanisms, state-dependent dynamics outperformed purely
  random or externally imposed rule changes and was the only scalable route to
  open-ended evolution in their cellular-automata study

Design implication:

- habitat change should not be only exogenous noise
- part of world dynamics must depend on current population state, usage history,
  or interaction structure

## 5. Cooperation, Communication, Cheating, and Coevolution

### [Vostinar et al. 2019, "Suicidal selection: Programmed cell death can evolve in unicellular organisms due solely to kin selection"](https://pmc.ncbi.nlm.nih.gov/articles/PMC6706235/)

Main result:

- kin selection alone can evolve programmed death in digital unicells
- direct benefits to nearby kin and indirect benefits through harming nonkin
  behave differently

Design implication:

- altruistic self-sacrifice should be possible
- kin thresholding matters and should be a tunable mechanism
- direct and indirect kin benefit channels should be separated in experiments

### [Knoester and McKinley 2011, "Evolution of synchronization and desynchronization in digital organisms"](https://pubmed.ncbi.nlm.nih.gov/21087147/)

Main result:

- digital organisms evolved robust synchronization and desynchronization through
  limited signaling

Design implication:

- minimal communication channels can generate useful temporal coordination
- we should allow very small message primitives before adding rich languages

### [Fortuna et al. 2013, "Evolving Digital Ecological Networks"](https://pmc.ncbi.nlm.nih.gov/articles/PMC3605903/)

Main result:

- digital organisms can generate evolving interaction networks including
  competition, parasitism, predation, and mutualism, with directly observable
  network structure

Design implication:

- we should treat interaction graphs as first-class outputs
- our event logs should make ecological networks reconstructable

### [Zaman et al. 2014, "Coevolution Drives the Emergence of Complex Traits and Promotes Evolvability"](https://journals.plos.org/plosbiology/article?id=10.1371%2Fjournal.pbio.1002023)

Main result:

- host-parasite coevolution increased trait complexity and made hosts more
  evolvable than controls without parasites

Design implication:

- antagonists are not just stressors; they can be engines of complexity
- parasite / exploiter classes should be part of the roadmap, not a late add-on

### [Acosta and Zaman 2022, "Ecological Opportunity and Necessity: Biotic and Abiotic Drivers Interact During Diversification of Digital Host-Parasite Communities"](https://www.frontiersin.org/articles/10.3389/fevo.2021.750772/full)

Main result:

- abiotic complexity and parasitism both affect diversification, but they do so
  differently
- host abundance, diversity, and complexity cannot be collapsed into a single
  measurement

Design implication:

- our metrics must separate abundance, diversity, and complexity
- biotic antagonism and abiotic variation should be manipulated independently

## 6. Development and Phenotypic Plasticity

### [Fortuna 2022, "The phenotypic plasticity of an evolving digital organism"](https://pmc.ncbi.nlm.nih.gov/articles/PMC9470259/)

Main result:

- the environment can alter execution flow so that the same genome yields
  distinct phenotypes
- this plasticity comes with viability and generation-time cost

Design implication:

- development should not be treated as free adaptation
- the system needs explicit plasticity cost
- genotype and phenotype must remain analytically separate

## 7. Evolvability, Modularity, and Canalization

### [Kashtan and Alon 2005, "Spontaneous evolution of modularity and network motifs"](https://pmc.ncbi.nlm.nih.gov/articles/PMC1236541/)

Main result:

- modularly varying goals produced modular structure and motifs
- fixed-goal or randomly varying settings did not do so in the same way

Design implication:

- environmental variation should be structured and recombinable, not arbitrary
- latent protocols should share substructure across related habitats

### [Huizinga, Stanley, and Clune 2018, "The Emergence of Canalization and Evolvability in an Open-Ended, Interactive Evolutionary System"](https://direct.mit.edu/artl/article/24/3/157/2904/The-Emergence-of-Canalization-and-Evolvability-in)

Main result:

- in Picbreeder, goalless interactive evolution produced canalization,
  modularity, hierarchy, and better offspring generation potential

Design implication:

- divergent, open-ended exploration should remain in the system
- we should monitor whether lineages are becoming easier to adapt, not just more
  fit in current habitats

## 8. Artificial Chemistry and Substrate Design

### [Hickinbotham et al. 2016, "Maximizing the Adjacent Possible in Automata Chemistries"](https://pubmed.ncbi.nlm.nih.gov/26649811/)

Main contribution:

- proposes substrate design principles for open-ended chemistry-like systems:
  `Everything Evolves`, `Everything's Soft`, and `Everything Dies`

Design implication:

- our lowest simulation layer should avoid hard-coded immortal categories
- fixed and evolvable parts of the substrate must be distinguished explicitly

### [Clark, Hickinbotham, and Stepney 2017, "Semantic closure demonstrated by the evolution of a universal constructor architecture in an artificial chemistry"](https://pmc.ncbi.nlm.nih.gov/articles/PMC5454285/)

Main result:

- simultaneous evolution of genomic material, copier, and constructor can arise
  in silico within a universal-constructor architecture

Design implication:

- if we ever want deeper heredity than parameter inheritance, we need a more
  explicit description/interpreter split
- `Genome` and `Phenotype` should remain distinct from the start

## 9. Community Assembly and Ecological Networks

### [Hraber, Jones, and Forrest 1997, "The ecology of echo"](https://pubmed.ncbi.nlm.nih.gov/9385733/)

Main result:

- Echo produced species-abundance patterns and ecological structure under local
  interaction and resource limitation

Design implication:

- local interaction rules and limited resources are enough to justify our graph
  habitat approach
- ecology should be allowed to emerge from agent interaction rather than only
  from top-down scoring

### [Hraber and Milne 1997, "Community assembly in a model ecosystem"](https://www.sciencedirect.com/science/article/pii/S0304380097001117)

Main result:

- invasion rate and interaction type jointly shape population size, richness,
  and evenness
- selective interactions and random interactions produce different assembly
  regimes

Design implication:

- we need explicit invasion, migration, and assembly metrics
- turnover pressure should be a tunable world variable

### [Smith and Bedau 2000, "Is Echo a Complex Adaptive System?"](https://direct.mit.edu/evco/article/8/4/419/875/Is-Echo-a-Complex-Adaptive-System)

Main result:

- Echo lacked the hierarchically organized aggregates expected of complex
  adaptive systems

Design implication:

- simple ecosystem competition is not enough
- we must actively look for whether higher-level aggregates arise, not assume
  they will

## 10. Measuring Open-Endedness

### [Taylor et al. 2016, "Open-Ended Evolution: Perspectives from the OEE Workshop in York"](https://research.monash.edu/en/publications/open-ended-evolution-perspectives-from-the-oee-workshop-in-york/)

Main contribution:

- distinguishes behavioral hallmarks of open-ended evolution from hypothesized
  mechanisms
- argues for pluralism: there is more than one kind of open-endedness

Design implication:

- our design documents should keep hallmarks and mechanisms separate
- we should avoid a single scalar "open-endedness score"

### [Dolson et al. 2019, "The MODES Toolbox: Measurements of Open-Ended Dynamics in Evolving Systems"](https://direct.mit.edu/artl/article/25/1/50/2915/The-MODES-Toolbox-Measurements-of-Open-Ended)

Main contribution:

- provides metrics for change potential, novelty potential, complexity
  potential, and ecological potential

Design implication:

- the biosphere should emit the data needed for these classes of metrics from
  the first implementation

### [Stepney and Hickinbotham 2024, "On the Open-Endedness of Detecting Open-Endedness"](https://www-users.york.ac.uk/~ss44/bib/ss/nonstd/artl23.htm)

Main contribution:

- argues that generic metrics alone will eventually fail because open-ended
  systems escape current models of behavior

Design implication:

- save raw event logs and lineage data
- expect to combine generic metrics with system-specific analyses

### [Packard and McCaskill 2024, "Open-Endedness in Genelife"](https://direct.mit.edu/artl/article/30/3/356/119274/Open-Endedness-in-Genelife)

Main result:

- genetic and spatial patterns can both exhibit ongoing innovation in a
  Game-of-Life extension, but this still falls short of biological-style
  functional innovation

Design implication:

- novelty in patterns is not enough
- we should distinguish structural novelty from functional novelty in our probes

## 11. Cultural Inheritance and Cumulative Culture

### [Caldwell and Millen 2008, "Studying cumulative cultural evolution in the laboratory"](https://pmc.ncbi.nlm.nih.gov/articles/PMC2607341/)

Main result:

- cumulative cultural evolution can produce adaptive complexity and behavioral
  convergence through transmission chains

Design implication:

- a population archive can genuinely change long-run population behavior
- horizontal transmission deserves its own controls

### [Fay et al. 2019, "Increasing population size can inhibit cumulative cultural evolution"](https://pmc.ncbi.nlm.nih.gov/articles/PMC6452720/)

Main result:

- larger populations increased variation and access to better artifacts, but did
  not necessarily improve cumulative culture
- coordination and working-memory constraints can reverse the expected effect

Design implication:

- bigger archive access is not automatically better
- archive bandwidth, filtering, and copying burden should be modeled explicitly

### [Borg et al. 2024, "Evolved Open-Endedness in Cultural Evolution"](https://direct.mit.edu/artl/article/30/3/417/116175/Evolved-Open-Endedness-in-Cultural-Evolution-A-New)

Main contribution:

- cultural evolution provides a second route to evolved open-endedness
- emphasizes cumulative culture, recombination, and transitions from bounded to
  unbounded innovation

Design implication:

- the future `CulturalArchive` should not be an optional convenience layer
- dual inheritance is central to the long-term agenda

## 12. What This Collection Changes In The Design

The literature above strengthens six concrete design decisions.

1. Add higher-level units, not only organisms:
   kin groups, clades, and possible group-level reproduction.

2. Make habitat dynamics state-dependent:
   occupation, depletion, signaling, and antagonistic pressure should feed back
   into future conditions.

3. Reserve space for antagonists and parasites:
   they are candidate engines of complexity, not only failure cases.

4. Separate development from adult adaptation:
   juvenile exposure and plasticity should have measurable and costly effects.

5. Preserve raw history:
   event logs, lineage graphs, and ecological networks must be kept even when
   summary metrics are available.

6. Treat culture as a second inheritance channel:
   with cost, access limits, copying bottlenecks, and failure modes.

## 13. Still Under-Collected

The immediate evidence base is now strong enough to proceed, but four secondary
areas still deserve follow-up collection later:

- formal models of dual inheritance with explicit recombination costs
- evolvable signaling languages beyond minimal coordination
- quantitative theories of catastrophe recovery and bottleneck design
- artificial chemistry work on parasite management in spatial substrates

