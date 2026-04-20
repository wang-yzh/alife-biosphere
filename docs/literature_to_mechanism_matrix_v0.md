# Literature to Mechanism Matrix v0

## 1. Purpose

This matrix turns literature into build decisions.

Each row answers:

- what the paper argues or demonstrates
- what mechanism the biosphere should contain
- what variable should be tunable in experiments
- what metric should tell us whether the mechanism matters

## 2. Matrix

| Direction | Paper | Mechanism requirement | Experimental variables | Key metrics |
| --- | --- | --- | --- | --- |
| higher-level individuality | [West et al. 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4547252/) | kin groups, conflict suppression, mutual dependence, division of labor | kin threshold, group resource sharing, group reproduction probability | group persistence, within-group conflict, division-of-labor index |
| fraternal transitions | [Moreno and Ofria 2019](https://pubmed.ncbi.nlm.nih.gov/31150287/) | selectable higher-level units | offspring group formation, group inheritance bandwidth | group lineage depth, higher-level reproduction success |
| multicellular life histories | [Moreno and Ofria 2022](https://www.frontiersin.org/journals/ecology-and-evolution/articles/10.3389/fevo.2022.750837/full) | messaging, offspring investment, adaptive apoptosis | messaging cost, kin recognition strictness, offspring-group budget | asymmetry score, apoptosis frequency, offspring survival |
| dirty work specialization | [Goldsby et al. 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC4019463/) | useful but damaging work channel | work reward, work damage rate, bottleneck size | germ/soma split, damage concentration, reproductive fidelity |
| niche construction | [Laland et al. 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4922671/) | ecological memory | memory persistence, world feedback strength | descendant environment similarity, ecological inheritance reuse |
| state-dependent OEE | [Adams et al. 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5430523/) | population-dependent habitat dynamics | occupancy feedback, depletion feedback, interaction feedback | novelty rate, non-collapse duration, post-shock adaptation lag |
| kin-selected sacrifice | [Vostinar et al. 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6706235/) | self-sacrifice behaviors with kin targeting | kin inclusivity, direct benefit radius, indirect harm radius | sacrifice frequency, kin benefit, lineage retention |
| minimal communication | [Knoester and McKinley 2011](https://pubmed.ncbi.nlm.nih.gov/21087147/) | low-bandwidth messages | message loss, message cost, timing noise | coordination score, robustness under loss |
| antagonistic coevolution | [Zaman et al. 2014](https://journals.plos.org/plosbiology/article?id=10.1371%2Fjournal.pbio.1002023) | parasites / exploiters / defenders | parasite virulence, mutation rate, host defense bandwidth | complexity trend, host evolvability, parasite extinction rate |
| biotic vs abiotic diversification | [Acosta and Zaman 2022](https://www.frontiersin.org/articles/10.3389/fevo.2021.750772/full) | separate antagonistic and habitat-complexity controls | abiotic complexity, phenotypic space size, parasite presence | abundance, diversity, complexity as separate outputs |
| phenotypic plasticity | [Fortuna 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9470259/) | plastic development with cost | developmental noise, plasticity bandwidth, plasticity cost | same-genome phenotype spread, maturation rate, plasticity cost |
| modular adaptation | [Kashtan and Alon 2005](https://pmc.ncbi.nlm.nih.gov/articles/PMC1236541/) | related habitats sharing subgoals | protocol overlap, environment switching structure | modularity score, transfer speed, adaptation after switch |
| canalization / evolvability | [Huizinga et al. 2018](https://direct.mit.edu/artl/article/24/3/157/2904/The-Emergence-of-Canalization-and-Evolvability-in) | divergent search pressure and phenotype axes | novelty pressure, archive branching, phenotype descriptors | offspring quality, canalized variation, hierarchy score |
| substrate principles | [Hickinbotham et al. 2016](https://pubmed.ncbi.nlm.nih.gov/26649811/) | soft substrate with death and mutation everywhere possible | fixed-vs-evolvable boundary, immortality exemptions, hard resets | innovation rate, substrate brittleness, exploit collapse frequency |
| semantic closure | [Clark et al. 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5454285/) | explicit genome/interpreter split | interpreter mutability, copy fidelity, constructor cost | heritable meaning shifts, viable offspring rate |
| ecological networks | [Fortuna et al. 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC3605903/) | reconstructable interaction graph | encounter radius, interaction type mix | network modularity, nestedness, trophic or parasitic diversity |
| community assembly | [Hraber and Milne 1997](https://www.sciencedirect.com/science/article/pii/S0304380097001117) | invasion and turnover mechanisms | invasion rate, migration friction, interaction selection mode | richness, evenness, turnover, occupancy stability |
| open-ended measurement | [Dolson et al. 2019](https://direct.mit.edu/artl/article/25/1/50/2915/The-MODES-Toolbox-Measurements-of-Open-Ended) | change, novelty, complexity, ecology metrics from day one | metric sampling interval, lineage window size | MODES-compatible summaries |
| metric humility | [Stepney and Hickinbotham 2024](https://www-users.york.ac.uk/~ss44/bib/ss/nonstd/artl23.htm) | retain raw logs beyond summary metrics | event granularity, snapshot cadence | ability to perform system-specific post hoc analysis |
| cumulative culture | [Caldwell and Millen 2008](https://pmc.ncbi.nlm.nih.gov/articles/PMC2607341/) | archive and social transmission channel | archive visibility, copy fidelity, teacher availability | cumulative improvement, convergence, archive reuse |
| archive overload | [Fay et al. 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6452720/) | bounded archive access and filtering | archive size, visible exemplars, copy time budget | transfer gain, copying fidelity, archive overload failure |
| cultural OEE | [Borg et al. 2024](https://direct.mit.edu/artl/article/30/3/417/116175/Evolved-Open-Endedness-in-Cultural-Evolution-A-New) | dual inheritance and recombination | vertical vs horizontal balance, recombination chance | cultural novelty, cumulative depth, bounded-to-unbounded transitions |

## 3. Immediate Design Additions Suggested By The Matrix

These items are not yet fully explicit in `world_design_v0.md`, but the
literature suggests they should be added soon.

### 3.1 Higher-level organization

Needed fields:

- `group_id`
- `group_role`
- `group_birth_event`
- `group_resource_pool`

### 3.2 State-dependent habitat memory

Needed fields:

- `recent_occupancy`
- `resource_depletion_trace`
- `signal_trace`
- `parasite_pressure`

### 3.3 Antagonist support

Needed roles:

- parasite
- thief
- mimic
- jammer
- mutualist

### 3.4 Development variables

Needed per-organism records:

- developmental habitat sequence
- phenotype divergence from founder genome
- plasticity cost paid
- consolidation success during juvenile stage

### 3.5 Archive controls

Needed variables:

- archive access fee
- archive visibility limit
- archive trust / kin gate
- capsule recombination rate

## 4. Next Literature Pass After Implementation Begins

Once `M1-M3` are implemented, the most useful next literature pass will be:

1. bottleneck and founder-effect theory for lineage turnover
2. signaling language evolution under deception
3. catastrophe recovery in ecological systems
4. dual-inheritance models with recombination and forgetting

