# Resilience, Regime Shifts, And Signaling Review v1

## Purpose

This note continues the literature program for `alife_biosphere` with a tighter
focus on three coupled topics:

- resilience, regime shifts, and adaptive cycles
- early warning signals for collapse and recovery
- communication under deception, ambiguity, and partial observability

The point of this review is practical.
We want to decide how the world should be stressed, how warning signs should be
measured, and how signaling should behave under realistic evolutionary pressure.

## 1. Resilience Is Not The Same As Stability

### [Holling 1973, "Resilience and Stability of Ecological Systems"](https://doi.org/10.1146/annurev.es.04.110173.000245)

Main result:

- resilience and stability are not interchangeable
- stability concerns return to a local equilibrium
- resilience concerns how much disturbance can be absorbed before the system
  shifts into a different behavioral regime

What matters for us:

- our world should not be optimized for smooth stationarity
- the goal is not to prevent all change
- the goal is to maintain a system that can absorb shocks without losing its
  capacity for future adaptation

Design implication:

- we need refuge structure, asynchronous shocks, and recovery metrics
- a system can be healthy even if it fluctuates

### [Folke et al. 2010, "Resilience thinking: integrating resilience, adaptability and transformability"](https://research.fs.usda.gov/treesearch/42598)

Main result:

- resilience, adaptability, and transformability are related but distinct
- adaptability means adjusting within the current stability domain
- transformability means crossing into a new development trajectory
- smaller scales can generate novelty during crisis that supports resilience at
  larger scales

What matters for us:

- we should not collapse all improvement into one axis
- some changes should count as adaptation within the same regime
- other changes should count as genuine transition to a new regime

Design implication:

- the biosphere should track:
  - resilience
  - adaptability
  - transformability
- smaller habitat or group scales should be allowed to experiment during crisis

### [Resilience Alliance, "Panarchy"](https://www.resalliance.org/index.php/panarchy)

Main contribution:

- panarchy links adaptive cycles across nested scales
- small fast scales "revolt"
- large slow scales "remember"

What matters for us:

- the world should not only have one timescale
- fast-changing local groups and slower habitat memory should interact

Design implication:

- smaller local groups can be the source of novelty
- larger habitat or lineage structures should preserve memory and constraints

### [zu Castell and Schrenk 2020, "Computing the adaptive cycle"](https://www.nature.com/articles/s41598-020-74888-y)

Main result:

- the adaptive cycle can be made quantitative rather than left as metaphor
- the authors estimate system position using information-transfer networks and
  the variables potential, connectedness, and resilience
- one case study is the Tangled Nature Model, which is directly relevant for
  artificial evolutionary systems

What matters for us:

- adaptive-cycle language can be operationalized
- phase tracking does not have to remain narrative only

Design implication:

- we should consider tracking per-habitat or per-group proxies for:
  - potential
  - connectedness
  - resilience
- later probes can estimate whether a habitat is in exploitation,
  conservation, release, or reorganization

## 2. Early Warning Signals Are Useful But Fragile

### [Scheffer et al. 2009, "Early-warning signals for critical transitions"](https://www.nature.com/articles/nature08227)

Main result:

- many systems approaching tipping points may show generic warning signals
- classic examples include rising variance and autocorrelation due to critical
  slowing down

What matters for us:

- the world should record enough time-series structure to estimate warning
  signals before collapse

Design implication:

- retain rolling measures of:
  - variance
  - autocorrelation
  - recovery time
- treat them as diagnostics, not as direct world-control rules

### [Boettiger and Hastings 2012, "Quantifying limits to detection of early warning for critical transitions"](https://pmc.ncbi.nlm.nih.gov/articles/PMC3427498/)

Main result:

- common warning indicators can have severe error rates even under favorable
  assumptions
- uncertainty quantification should be central, not an afterthought
- model-based indicators can outperform naive summary statistics

What matters for us:

- our probes cannot treat rising variance as truth
- warning systems need false-positive and false-negative accounting

Design implication:

- every warning metric should be accompanied by:
  - confidence or uncertainty estimate
  - control runs
  - known error characterization where possible

### [Lade and Gross 2012, "Early Warning Signals for Critical Transitions: A Generalized Modeling Approach"](https://pmc.ncbi.nlm.nih.gov/articles/PMC3271022/)

Main result:

- integrating structural knowledge with time series can improve warning quality
- early warning does not need to be purely model-free

What matters for us:

- our warning layer can combine generic indicators with knowledge of habitat and
  interaction structure

Design implication:

- warning models should use both:
  - generic rolling statistics
  - structural information such as occupancy pressure, parasite load, and graph
    connectivity

### [O'Brien et al. 2023, "Early warning signals have limited applicability to empirical lake data"](https://www.nature.com/articles/s41467-023-43744-8)

Main result:

- in real lake data, few cases looked like genuine critical transitions
- different trophic levels often showed different forms of abrupt change
- most indicators did not perform better than chance
- multivariate methods were only weakly better than univariate

What matters for us:

- regime shift and critical transition are not synonyms
- many abrupt changes will not fit bifurcation-style warning theory

Design implication:

- we should distinguish:
  - abrupt change
  - critical transition
  - resilience loss
- our analysis layer should move beyond a single "tipping point detector"

### [Clements et al. 2019, "Early warning signals of recovery in complex systems"](https://www.nature.com/articles/s41467-019-09684-y)

Main result:

- warning-style signals can appear before recovery, not just before collapse
- abundance-based and trait-based signals were both detectable in their
  fisheries study
- combining the two improved prediction

What matters for us:

- we should monitor recoverability, not only collapse risk

Design implication:

- probes should track:
  - early warning of collapse
  - early warning of recovery
- trait-like structural variables should be logged alongside abundance-like
  counts

## 3. Partial Observability Should Be Built In, Not Added Later

### [Williams and Brown 2022, "Partial observability and management of ecological systems"](https://pmc.ncbi.nlm.nih.gov/articles/PMC9468910/)

Main result:

- ecological systems are almost never fully observed
- decision-making should be based on belief states, not on assumed perfect
  system state
- partial observability changes transitions, valuation, and optimal control

What matters for us:

- our organisms should not get omniscient state access
- our researcher-facing analysis should also distinguish observed state from
  latent world state

Design implication:

- agents should act on local observations, traces, and signals
- the engine can keep latent full state internally, but organisms should only
  see partial observations
- later diagnostics may use belief-state style summaries for lineages or groups

## 4. Communication Evolves Under Specific Selection Conditions

### [Floreano et al. 2007, "Evolutionary conditions for the emergence of communication in robots"](https://pubmed.ncbi.nlm.nih.gov/17320390/)

Main result:

- communication evolved readily when colonies were genetically similar and
  selection acted at the colony level
- under individual selection in unrelated colonies, visual signaling produced
  deceptive communication strategies and reduced colony performance
- once a communication system was established, it constrained the evolution of
  more efficient alternatives

What matters for us:

- group selection and kin structure materially change signaling outcomes
- signaling lock-in is real; early conventions can become path dependent

Design implication:

- signaling experiments should vary:
  - kin relatedness
  - group-level versus individual-level selection
  - convention plasticity
- we should log communication lock-in and convention drift

### [Smaldino et al. 2018, "The Evolution of Covert Signaling"](https://pmc.ncbi.nlm.nih.gov/articles/PMC5861109/)

Main result:

- partially ambiguous signaling can be adaptive because it helps assort similar
  agents without provoking unnecessary hostility from others

What matters for us:

- useful signals are not always transparent public broadcasts

Design implication:

- signal decoding should depend on familiarity, kinship, or context
- covert and semi-private cues should be legal

### [Számadó 2017, "When honesty and cheating pay off"](https://bmcecolevol.biomedcentral.com/articles/10.1186/s12862-017-1112-y)

Main result:

- both honest and cheating signaling equilibria can evolve
- parameter regime and starting composition matter

What matters for us:

- communication outcomes are path dependent and frequency dependent

Design implication:

- signaling controls should vary initial population composition and trust regime

### [Számadó et al. 2023, "Honesty in signalling games is maintained by trade-offs rather than costs"](https://link.springer.com/article/10.1186/s12915-022-01496-9)

Main result:

- signal honesty does not require high equilibrium costs
- reliability is better understood as coming from trade-offs between sender and
  receiver outcomes

What matters for us:

- charging a small energy fee for messaging is not enough to make a good signal
  system

Design implication:

- trust, verification, and downstream consequences matter more than message cost
  alone

## 5. Strong Design Conclusions From This Pass

This literature pass strengthens six design commitments.

1. The biosphere should distinguish:
   stability, resilience, adaptability, and transformability.

2. Adaptive-cycle language should become measurable later:
   exploitation, conservation, release, and reorganization are not just
   narrative labels.

3. Early warning metrics should be probabilistic diagnostics:
   with uncertainty and controls, not binary truth labels.

4. Recovery is as important as collapse:
   the world should emit warning signals for both directions.

5. Partial observability is essential:
   organisms should operate on local signals and traces, not full world state.

6. Communication requires selection context:
   kin structure and group-level incentives strongly affect whether signaling is
   cooperative or deceptive.

## 6. Immediate Experimental Consequences

The next experimental design layer should include:

- collapse-warning probes
- recovery-warning probes
- signal deception probes
- kin-structure communication probes
- topology-sensitive refuge and rescue probes

At the metric level, the next additions should be:

- `recovery_lag`
- `warning_confidence`
- `false_alarm_rate`
- `miss_rate`
- `signal_reliability`
- `convention_lock_in`
- `group_selection_advantage`
- `phase_estimate` for adaptive-cycle state

## 7. What Still Remains Open

The literature is now strong enough to justify the design direction, but four
questions still need deeper collection later:

- how to quantify adaptive-cycle phase cheaply in a small simulation
- how to detect regime shifts that are not bifurcation-driven
- how to model trust update under repeated deception without overengineering
- how to combine partial observability with lineage-level learning in a simple
  first implementation

