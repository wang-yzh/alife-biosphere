# Warning Metrics And Uncertainty Design v1

## Purpose

This document freezes a first design position for warning metrics in
`alife_biosphere`.

It answers four practical questions:

1. What kinds of bad or good transitions are we trying to warn about?
2. Which metric families are justified by the literature already collected?
3. How should uncertainty, false alarms, and misses be handled?
4. What can warning metrics support, and what can they not prove?

This note exists because the current literature already gives us two strong
warnings:

- warning signals are useful enough to be part of the project
- warning signals are too fragile to be treated as truth labels

## 1. Warning Is Not One Problem

The biosphere should not have one generic `warning_score`.

We need to distinguish at least four situations:

### 1.1 Collapse risk

The local system may be approaching a loss of viability.

Examples:

- occupancy crash
- resource collapse
- signal poisoning
- parasite bloom
- lineage bottleneck cascade

### 1.2 Resilience loss

The system may still be alive, but its ability to absorb disturbance is
shrinking.

Examples:

- recovery after perturbation gets slower
- rescue paths become narrower
- connectedness becomes brittle

### 1.3 Regime shift candidate

A local habitat, group, or lineage may be moving into a qualitatively different
organization mode.

Examples:

- frontier habitat becomes permanently predator-dominated
- refuge becomes chronically saturated and ceases to function as refuge
- signaling conventions reorganize after widespread deception

### 1.4 Recovery opportunity

The system may be approaching rebound, not collapse.

Examples:

- post-crash recolonization windows
- rising rescue-source diversity
- declining parasite pressure after peak
- renewed protocol experimentation after release

These must stay distinct.
Otherwise we will confuse abrupt change, regime change, collapse, and recovery.

## 2. What The Literature Lets Us Say

### [Scheffer et al. 2009, "Early-warning signals for critical transitions"](https://www.nature.com/articles/nature08227)

Useful take:

- rising variance
- rising autocorrelation
- slower recovery

These are valid candidate diagnostics for systems near some critical
transitions.

### [Boettiger and Hastings 2012, "Quantifying limits to detection of early warning for critical transitions"](https://pmc.ncbi.nlm.nih.gov/articles/PMC3427498/)

Useful take:

- warning indicators can fail badly
- uncertainty and error accounting are central
- model-aware approaches can outperform purely generic summary statistics

### [Lade and Gross 2012, "Early Warning Signals for Critical Transitions: A Generalized Modeling Approach"](https://pmc.ncbi.nlm.nih.gov/articles/PMC3271022/)

Useful take:

- warning can combine structural knowledge with observed time series

### [O'Brien et al. 2023, "Early warning signals have limited applicability to empirical lake data"](https://www.nature.com/articles/s41467-023-43744-8)

Useful take:

- abrupt change is not always a critical transition
- many indicator families perform weakly in real settings

### [Clements et al. 2019, "Early warning signals of recovery in complex systems"](https://www.nature.com/articles/s41467-019-09684-y)

Useful take:

- warning-style analysis can detect recovery onset, not only decline

### [Holling 1973, "Resilience and Stability of Ecological Systems"](https://doi.org/10.1146/annurev.es.04.110173.000245)

Useful take:

- loss of resilience is not identical to immediate collapse

These papers together imply a disciplined position:

```text
warning metrics should be probabilistic diagnostics for specific transition
families, not universal truth labels.
```

## 3. Design Decision

The biosphere warning layer should be:

- plural
- rolling
- uncertainty-aware
- transition-specific
- reconstructable from saved raw traces

It should not be:

- a single master warning score
- a binary tipping-point classifier
- the only evidence used to interpret runs

## 4. The Warning Metric Stack

For the first implementation-grade design, warning diagnostics should be built
from five stacked metric families.

## 4.1 Abundance and occupancy family

Candidate rolling signals:

- habitat occupancy mean
- occupancy variance
- occupancy autocorrelation
- local extinction count
- recolonization count

Use:

- collapse risk
- recovery onset

Limit:

- abundance alone cannot distinguish regime shift from ordinary cycling

## 4.2 Resource and habitat family

Candidate rolling signals:

- fuel availability trend
- substrate availability trend
- hazard persistence
- refuge_score trend
- depletion_trace accumulation

Use:

- resilience loss
- habitat regime change

Limit:

- environmental changes can lag population changes

## 4.3 Structural network family

Candidate rolling signals:

- weighted interaction density
- corridor concentration
- module separation
- path redundancy
- strength inequality

Use:

- rescue brittleness
- connectedness collapse
- shifting adaptive-cycle phase

Limit:

- structure can change without immediate viability loss

## 4.4 Behavioral and cultural family

Candidate rolling signals:

- signal reliability
- deception rate
- verification success
- archive validation success
- stale-capsule reuse rate

Use:

- social-regime shifts
- archive poisoning risk
- cooperation erosion

Limit:

- social instability may be local even when total population stays large

## 4.5 Lineage and rescue family

Candidate rolling signals:

- lineage depth change
- bottleneck frequency
- founder success rate
- rescue-source diversity
- rebound delay

Use:

- persistence quality
- post-shock resilience
- collapse versus rescue interpretation

Limit:

- lineage summaries often react more slowly than local habitat signals

## 5. Warning Objects To Emit

The analysis layer should emit transition-specific warning objects rather than a
single scalar.

Recommended structure:

```text
WarningCandidate =
  {
    warning_type,
    target_scope,
    tick,
    horizon,
    supporting_metrics,
    uncertainty_band,
    confidence_tier,
    null_comparison,
    retrospective_label
  }
```

### Fields

- `warning_type`
  collapse_risk, resilience_loss, regime_shift_candidate, recovery_opportunity

- `target_scope`
  habitat, kin_group, lineage, or global biosphere

- `horizon`
  short, medium, or long warning horizon

- `supporting_metrics`
  the specific metrics that drove the candidate

- `uncertainty_band`
  estimated uncertainty or spread of the warning evidence

- `confidence_tier`
  low, medium, high

- `null_comparison`
  control or baseline used to contextualize the score

- `retrospective_label`
  filled in after the future is observed:
  true positive, false positive, late signal, miss, or ambiguous

## 6. Uncertainty Design

This is the most important section of the document.

The project should assume that warning diagnostics are noisy from day one.

## 6.1 Three uncertainty sources

### A. Finite-window uncertainty

Short rolling windows produce unstable estimates.

### B. Structural ambiguity

The same signal pattern can come from:

- critical slowing down
- ordinary cyclic release
- external disturbance
- temporary resource spike or drop

### C. Transition-definition uncertainty

Even after the fact, not every abrupt change should be called a regime shift.

## 6.2 Required uncertainty outputs

Every warning analysis should try to provide:

- window size used
- number of observations
- null or baseline comparison
- confidence tier
- retrospective outcome when available

## 6.3 Confidence tiers

For the first implementation:

- `low`: driven by one metric family or weak sample size
- `medium`: supported by multiple metric families with plausible agreement
- `high`: supported by multiple metric families and retrospectively consistent

These are not Bayesian truths.
They are disciplined qualitative labels.

## 6.4 False alarms and misses

The warning system must explicitly track:

- `false_alarm_rate`
- `miss_rate`
- `late_signal_rate`
- `ambiguous_transition_rate`

If we do not keep these, warning metrics will become storytelling devices.

## 7. Warning Targets And Minimum Metric Bundles

Different targets need different minimum bundles.

### 7.1 Habitat warning bundle

Minimum:

- occupancy trend
- resource trend
- refuge_score trend
- disruption proxy

### 7.2 Kin-group warning bundle

Minimum:

- group persistence
- within-group conflict
- role asymmetry stability
- direct-trust deterioration

### 7.3 Lineage warning bundle

Minimum:

- bottleneck frequency
- founder success rate
- vertical transfer gain
- rescue-source diversity

### 7.4 Archive warning bundle

Minimum:

- validation success trend
- stale-capsule reuse rate
- domain mismatch rate
- source-trust drift

## 8. What Should Count As A Regime Shift Candidate

The project should use a high bar here.

A regime shift candidate should require:

1. abrupt or sustained change in at least one viability-relevant variable
2. support from more than one metric family
3. persistence beyond a short transient window
4. evidence that the new state changes future selection or coordination

This helps us avoid labeling every release/reorganization cycle as a regime
shift.

## 9. What Should Count As Recovery Opportunity

A recovery-opportunity candidate should require:

1. prior decline or stress
2. evidence of rising rescue capacity, not just random rebound noise
3. support from at least one structural or lineage metric in addition to raw
   abundance

This follows the literature that recovery can also have advance signals.

## 10. Minimum Event And Summary Data Required

Warning metrics should only be built if the data needed to justify them exists.

Minimum retained data:

- tick-level occupancy summaries
- habitat resource summaries
- disturbance logs
- migration logs
- interaction-network snapshots or summaries
- trust and signal summaries
- lineage and founder summaries
- archive validation summaries

Without these, the warning layer will become guesswork.

## 11. Recommended First Warning Probes

These are design targets for later implementation, not immediate coding tasks.

### 11.1 Collapse-warning probe

Compare:

- no disturbance
- asynchronous disturbance
- synchronous disturbance

Outputs:

- false alarms
- misses
- rebound delay

### 11.2 Recovery-warning probe

Compare:

- isolated habitats
- refuge-connected habitats

Outputs:

- early warning of recovery
- rescue-source diversity

### 11.3 Archive-poisoning warning probe

Compare:

- validated archive
- unvalidated archive

Outputs:

- stale-capsule buildup
- source-trust deterioration
- social-regime destabilization

### 11.4 Signal-collapse warning probe

Compare:

- honest-only signaling
- deception enabled

Outputs:

- signal reliability decline
- trust collapse timing
- cooperation erosion timing

## 12. Design Decision

This document supports three concrete decisions.

1. Warning metrics should be stored and interpreted as typed candidates, not as
   one scalar score.

2. Every warning family must carry uncertainty and retrospective evaluation.

3. The project should treat collapse warning and recovery warning as separate
   but related analyses.

These choices keep the warning layer scientifically useful without pretending
that it can provide certainty.

