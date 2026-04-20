# Adaptive Cycle And Trust Mechanisms v1

## Purpose

This note narrows the literature program to two questions that now matter for
experimental design:

1. How can the adaptive cycle be approximated cheaply enough for a small
   artificial-life world?
2. How should trust update under repeated deception when observations are
   partial, private, and noisy?

The goal is not to reproduce the source theories in full.
The goal is to extract a defensible first implementation rule set.

## 1. Adaptive Cycle: What We Can Use Without Overclaiming

### [Angeler et al. 2015, "Quantifying the Adaptive Cycle"](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0146053)

Main result:

- the adaptive cycle can be tested quantitatively rather than used purely as a
  metaphor
- in their phytoplankton case study, they found support for:
  - reorganization into distinct states
  - conservative within-cycle trajectories
  - long-run adaptation across repeated cycles

What we should take from it:

- we do not need full mechanistic physics to study cycle-like behavior
- it is enough to show:
  - distinct reorganized states
  - recurring but not identical trajectories
  - gradual structural turnover across cycles

Design implication:

- our probes should separate:
  - reorganization
  - conservatism
  - adaptation
- one number called "adaptive cycle score" would be too coarse

### [Walker et al. 2019, "The adaptive cycle: More than a metaphor"](https://www.sciencedirect.com/science/article/pii/S1476945X1830165X)

Main result:

- the review argues that adaptive cycles reflect endogenous complex-system
  dynamics rather than being only a storytelling device
- it points to thermodynamic and systems-level indicators as ways to quantify
  phases and scale interactions

What we should take from it:

- adaptive-cycle reasoning is most useful when tied to measurable internal
  structure and cross-scale interaction

Design implication:

- we should track a small set of internal structural indicators, not only
  population counts

### [zu Castell and Schrenk 2020, "Computing the adaptive cycle"](https://www.nature.com/articles/s41598-020-74888-y)

Main result:

- proposes an information-theoretic way to estimate the adaptive cycle through
  three variables:
  - potential
  - connectedness
  - resilience
- the authors report cyclic structure across multiple systems, including the
  Tangled Nature Model
- they also note that real systems do not always show the ideal textbook
  duration of phases

What we should take from it:

- adaptive-cycle phase can be estimated from interaction networks
- we should avoid assuming that release and reorganization are always short

Design implication:

- interaction-network summaries should be part of the core output
- later phase estimates can be based on information transfer and graph
  structure, not on hand-labeled states

## 2. A Cheap Adaptive-Cycle Approximation For Our World

The literature does not force us to implement full thermodynamic accounting in
the first version.

For the first useful approximation, each habitat or group can be tracked with
four proxy families:

### 2.1 Potential proxies

Interpretation:

- how much latent scope exists for further change or exploitation

Candidate proxies:

- unconsumed resource capacity
- protocol diversity not yet exploited locally
- unused archive diversity visible in that habitat
- lineage diversity inside the habitat

### 2.2 Connectedness proxies

Interpretation:

- how tightly coupled and structured the local system currently is

Candidate proxies:

- interaction density
- migration edge usage concentration
- archive dependency concentration
- signal reuse concentration

### 2.3 Resilience proxies

Interpretation:

- how much perturbation can be absorbed before the local regime shifts

Candidate proxies:

- rebound speed after disturbance
- refuge accessibility
- trust redundancy across partners
- diversity of rescue sources

### 2.4 Release / reorganization proxies

Interpretation:

- whether a local regime is breaking down or being rebuilt

Candidate proxies:

- abrupt occupancy loss
- spike in event entropy
- increased protocol experimentation
- increased founder / colonization events

## 3. Recommended Phase Estimator For Early Experiments

For a first implementation, avoid a hard four-state classifier.

Instead, compute a rolling habitat or group profile:

```text
phase_profile =
  {
    potential_proxy,
    connectedness_proxy,
    resilience_proxy,
    disruption_proxy
  }
```

Then infer tendencies:

- high potential, rising connectedness, moderate resilience:
  exploitation-like
- moderate potential, high connectedness, falling flexibility:
  conservation-like
- falling resilience, rising disruption, abrupt occupancy loss:
  release-like
- lower connectedness, rising novelty, founder / colonization spikes:
  reorganization-like

Why this is the right compromise:

- it respects the literature
- it avoids pretending we can perfectly label phases early
- it gives us quantitative traces we can compare between seeds and treatments

## 4. Trust Under Repeated Deception: What The Literature Actually Says

### [Hilbe et al. 2018, "Indirect reciprocity with private, noisy, and incomplete information"](https://pmc.ncbi.nlm.nih.gov/articles/PMC6275544/)

Main result:

- when reputation information becomes private, noisy, and incomplete, most
  classic binary reputation norms lose their ability to sustain full
  cooperation

What we should take from it:

- a simple public good/bad label is too brittle for our world

Design implication:

- trust should be private and partially local
- binary trust is a bad default for the biosphere

### [Rich and Zollman 2016, "Honesty through repeated interactions"](https://doi.org/10.1016/j.jtbi.2016.02.002)

Main result:

- repeated interactions can sustain honest signaling without obvious signal
  costs
- this can happen even when deception cannot be directly observed
- the key mechanism is that receivers condition future responses on signaling
  history

What we should take from it:

- repeated exposure creates endogenous cost for deception
- we do not need to force honesty through large static message cost

Design implication:

- trust should depend on interaction history
- receivers should update on downstream outcomes, not only on message form

### [Schmid et al. 2023, "Quantitative assessment can stabilize indirect reciprocity under imperfect information"](https://www.nature.com/articles/s41467-023-37817-x)

Main result:

- nuanced reputation scores can be error-correcting under private and
  unreliable information
- the paper identifies robust norm families under these conditions

What we should take from it:

- graded trust scores are more robust than brittle binary categories

Design implication:

- trust should use bounded scalar scores or short vectors
- small disagreements should not instantly collapse cooperation

### [Michel-Mata et al. 2024, "The evolution of private reputations in information-abundant landscapes"](https://www.nature.com/articles/s41586-024-07977-x)

Main result:

- aggregating several observations and using some tolerance for bad actions can
  sustain high cooperation even when information is abundant and private
- selection does not favor using all available information; a moderate number of
  observations is enough

What we should take from it:

- more memory is not always better
- simple tolerant aggregation can outperform both naive strictness and naive
  forgiveness

Design implication:

- trust should aggregate a short rolling window of observations
- we should explicitly test observation window size and tolerance threshold

### [Sarkadi et al. 2021, "The evolution of deception"](https://pmc.ncbi.nlm.nih.gov/articles/PMC8424346/)

Main contribution:

- deception emerges under competitive pressures in social information systems
- the paper emphasizes that deception should be understood as strategic false
  cooperation under social conditions

What we should take from it:

- deception is not noise; it is a selectable strategy

Design implication:

- deceptive signaling should be a normal event family in our logs

## 5. A Minimal Trust Update Rule We Can Defend

The literature does not justify a giant reputation engine for `v0.1`.
It does justify a compact private trust rule.

Recommended first rule:

```text
trust_score(source_class, source_id) in [-3, +3]
```

Each organism maintains private trust for:

- kin
- in-group non-kin
- out-group
- archive source
- optional individual counterpart for recent repeated interaction

## 5.1 Update inputs

Trust should update from outcomes, not just messages.

Inputs:

- signaled claim
- actual observed consequence
- delay between signal and consequence
- kin or familiarity relation
- whether the receiver verified before acting

## 5.2 Update logic

Suggested first rule:

- successful helpful signal: `+1`
- verified false or harmful signal: `-2`
- ambiguous / unresolved interaction: `0`
- old evidence decays toward `0`

This asymmetry is important.
Deception should damage trust faster than honesty accumulates it.

## 5.3 Observation aggregation

Do not use all available history.

Use a short rolling window:

- `M = 2 to 5` recent observations

Decision policy:

- cooperate / follow if aggregated trust exceeds threshold
- verify if near threshold
- ignore otherwise

This is the simplest defensible approximation of the recent literature.

## 5.4 Tolerance

The literature supports tolerance, not infinite forgiveness.

Recommended first implementation:

- one bad interaction does not instantly make a source unusable
- repeated bad interactions drive fast trust collapse

Equivalent interpretation:

- "look twice, forgive once" is closer to the literature than
  "one strike and permanently bad"

## 6. Minimal Experiments We Should Run Later

These are not implementation tasks for now.
They are the next paper-backed ablations we should be prepared to run.

### 6.1 Binary versus graded trust

Compare:

- binary good/bad trust
- bounded scalar trust

Expected outcome:

- graded trust should be more robust under private noisy information

### 6.2 One-observation versus aggregated trust

Compare:

- `M = 1`
- `M = 2`
- `M = 4`

Expected outcome:

- very short aggregation should beat single-observation trust
- very long aggregation may add drag and stale information

### 6.3 No-verification versus verification

Compare:

- immediate acceptance
- verify-when-uncertain
- always verify

Expected outcome:

- conditional verification should outperform both extremes

### 6.4 Cheap signals versus history-based honesty

Compare:

- no trust memory
- signal cost only
- repeated-interaction trust update

Expected outcome:

- repeated interaction should sustain more reliable signaling than cost-only
  designs

## 7. Metrics We Now Have Strong Justification For

### Adaptive-cycle metrics

- `potential_proxy`
- `connectedness_proxy`
- `resilience_proxy`
- `disruption_proxy`
- `phase_estimate`

### Trust metrics

- `signal_reliability`
- `verification_success`
- `false_trust_rate`
- `false_suspicion_rate`
- `trust_recovery_lag`
- `convention_lock_in`
- `private_reputation_divergence`

## 8. What This Changes In Our Design Thinking

This literature pass makes five design choices much clearer.

1. Adaptive cycle should enter the project as a proxy profile, not as a rigid
   classifier.

2. Trust should be private, graded, and short-memory-based.

3. Verification should sit between blind trust and blind refusal.

4. Repeated interactions should be treated as an endogenous honesty mechanism.

5. More information is not automatically better; bounded aggregation is a
   feature, not a compromise.

## 9. Remaining Open Questions

The next unresolved questions are now narrow enough to guide the next reading
pass:

- which cheap interaction-network summary best approximates connectedness in our
  small biosphere?
- how should trust update differ between direct counterpart experience and
  archive-source experience?
- when should a local phase change count as a regime shift rather than an
  ordinary release/reorganization cycle?

