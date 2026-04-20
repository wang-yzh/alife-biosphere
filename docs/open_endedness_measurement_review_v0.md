# Open-Endedness Measurement Review v0

## Purpose

This note isolates a question that now deserves its own design document:

```text
How will we know whether the biosphere is becoming more open-ended,
rather than merely staying noisy, large, or long-running?
```

The project already cites open-ended evolution literature in broader review
documents. What was still missing is a measurement-oriented synthesis that can
be translated directly into metrics and probes.

In practice, this note asks:

1. Which families of open-endedness should we distinguish?
2. Why is one scalar score not enough?
3. Which measurement stack is realistic for our biosphere?
4. What should count as progress before we ever claim open-ended evolution?

## Short Answer

The literature points to a disciplined position:

```text
Open-endedness is multi-dimensional.
It is not the same as long run time, high variance, or raw diversity.
```

For our project, that means:

- do not build a single `open_endedness_score`;
- separate novelty, complexity, ecological restructuring, and cumulative
  lineage change;
- keep raw logs, because system-specific interpretation matters;
- make the first goal "credible open-endedness probes," not a headline claim.

## Core Papers

### [Bedau, Snyder, and Packard 1998, "A Classification of Long-Term Evolutionary Dynamics"](https://cseweb.ucsd.edu/~rik/alife6/papers/KI40.html)

Main contribution:

- defines long-term evolutionary dynamics in terms of:
  - diversity,
  - new evolutionary activity,
  - mean cumulative evolutionary activity;
- separates systems into classes with absent, bounded, or unbounded adaptive
  activity.

Why it matters:

- this is the clean starting point for saying "not all ongoing dynamics are
  equally life-like";
- it gives us a first warning that simple diversity is not enough.

Design implication:

- we should distinguish:
  - diversity of forms,
  - new adaptive activity,
  - cumulative persistence of adaptive structures;
- the biosphere should log enough to compute lineage persistence and novelty,
  not just instantaneous counts.

### [Bedau et al. 1998, "A Comparison of Evolutionary Activity in Artificial Evolving Systems and in the Biosphere"](https://www.santafe.edu/research/results/working-papers/a-comparison-of-evolutionary-activity-in-artificia)

Main contribution:

- compares artificial systems against fossil-record-inspired activity measures;
- argues that artificial systems can remain qualitatively different from the
  biosphere even when they are active.

Why it matters:

- it is a strong caution against congratulating ourselves too early;
- it reinforces that continual turnover is not automatically biosphere-like.

Design implication:

- later probes should compare internal controls, not only absolute values;
- our metrics should explicitly separate "activity" from "open-endedness-like
  activity."

### [Maley 1999, "Four Steps Toward Open-Ended Evolution"](https://www.researchgate.net/publication/2608823_Four_Steps_Toward_Open-Ended_Evolution)

Main contribution:

- critiques the idea that unbounded evolutionary activity alone is enough;
- argues that richer requirements are needed for credible open-ended systems.

Why it matters:

- this is one of the clearest early warnings against metric overconfidence;
- it supports using activity statistics, but not worshipping them.

Design implication:

- even if the biosphere later shows increasing evolutionary activity, we should
  still ask whether genuinely new organizational modes are appearing.

### [Taylor et al. 2016, "Open-Ended Evolution: Perspectives from the OEE Workshop in York"](https://pubmed.ncbi.nlm.nih.gov/27472417/)

Main contribution:

- argues that open-endedness is plural, not singular;
- separates hallmarks from mechanisms.

Why it matters:

- this gives us permission to build a measurement stack rather than a single
  definition;
- it also means we should not lock the project to one favorite mechanism.

Design implication:

- measure multiple hallmarks separately;
- keep mechanism claims downstream from observed dynamics.

### [Dolson et al. 2019, "The MODES Toolbox: Measurements of Open-Ended Dynamics in Evolving Systems"](https://direct.mit.edu/artl/article/25/1/50/2915/The-MODES-Toolbox-Measurements-of-Open-Ended)

Main contribution:

- proposes four measurement families:
  - change potential,
  - novelty potential,
  - complexity potential,
  - ecological potential.

Why it matters:

- this is the most directly reusable measurement framework for our project;
- it translates open-endedness into something operational without pretending to
  solve all interpretation problems.

Design implication:

- the biosphere should preserve enough raw structure to compute MODES-like
  summaries;
- our metrics stack should map naturally onto these four families.

### [Packard et al. 2019, "Open-Ended Evolution and Open-Endedness: Editorial Introduction to the Open-Ended Evolution I Special Issue"](https://pubmed.ncbi.nlm.nih.gov/30933628/)

Main contribution:

- frames open-ended evolution as diversity-producing evolutionary creativity,
  not mere survival dynamics.

Why it matters:

- it reinforces that innovation is central, not optional;
- it is useful for keeping our measurement language broad enough.

Design implication:

- do not mistake resilience alone for open-endedness;
- resilience is necessary, but innovation remains a separate axis.

### [Packard et al. 2019, "An Overview of Open-Ended Evolution: Editorial Introduction to the Open-Ended Evolution II Special Issue"](https://arxiv.org/abs/1909.04430)

Main contribution:

- extends the first editorial into a broader survey of mechanisms and research
  strategies.

Why it matters:

- helpful for separating:
  - novelty generation,
  - complexity growth,
  - domain expansion,
  - ecological restructuring.

Design implication:

- our probes should not reduce open-endedness to novelty alone.

### [Adams et al. 2017, "Formal Definitions of Unbounded Evolution and Innovation Reveal Universal Mechanisms for Open-Ended Evolution in Dynamical Systems"](https://pmc.ncbi.nlm.nih.gov/articles/PMC5430523/)

Main contribution:

- defines two hallmarks:
  - unbounded evolution,
  - innovation;
- shows state-dependent dynamics as especially effective.

Why it matters:

- this is one of the best formal bridges between dynamical systems and
  artificial life;
- it supports our emphasis on state-dependent habitats and ecological feedback.

Design implication:

- we should measure:
  - whether trajectories keep producing novel structured states,
  - whether those states require population-world coupling rather than mere
    external noise.

### [Hintze 2019, "Open-Endedness for the Sake of Open-Endedness"](https://direct.mit.edu/artl/article/25/2/198/2923/Open-Endedness-for-the-Sake-of-Open-Endedness)

Main contribution:

- sharpens the distinction between open-ended systems and systems that simply
  run for a long time or oscillate.

Why it matters:

- very relevant to our world, because a dynamic equilibrium with recurring
  disturbances could still be non-open-ended.

Design implication:

- repeated cycles alone are not enough;
- we need evidence of continuing production of new organizational structure.

### [Borg et al. 2024, "Evolved Open-Endedness in Cultural Evolution"](https://pubmed.ncbi.nlm.nih.gov/37253238/)

Main contribution:

- brings cultural evolution directly into open-endedness research.

Why it matters:

- especially important for us because the biosphere intends to include a costly
  cultural archive;
- it warns that open-endedness can appear through multiple inheritance
  channels, not just genetic lineages.

Design implication:

- measure cultural open-endedness separately from genetic or lineage
  open-endedness;
- archive novelty and cumulative transformation need their own metrics.

## What This Means For Our Project

The measurement literature suggests we should stop asking:

```text
Is the biosphere open-ended?
```

and instead ask:

```text
Along which axes is the biosphere becoming more open-ended,
and what evidence would be strong enough for each axis?
```

That leads to a much better measurement plan.

## Recommended Measurement Stack

### 1. Change potential

Questions:

- does the system keep changing in a nontrivial way?
- are habitats, lineages, and interaction networks still restructuring?

Candidate metrics:

- event entropy over time
- turnover rate in habitat occupancy
- lineage turnover rate
- interaction-network change rate

### 2. Novelty potential

Questions:

- are genuinely new configurations appearing?
- are new niches, protocol bundles, or role combinations emerging?

Candidate metrics:

- new lineage-behavior clusters
- new habitat-role occupation patterns
- protocol novelty rate
- new interaction motifs

### 3. Complexity potential

Questions:

- are organizational structures becoming richer without simply bloating?

Candidate metrics:

- lineage branching depth
- group-role differentiation
- interaction-network modularity
- developmental state diversity

### 4. Ecological potential

Questions:

- does the system keep creating new ecological relations and opportunities?

Candidate metrics:

- invasion success into previously resistant habitats
- rescue-source diversity
- antagonist/host diversification
- habitat-assembly path diversity

### 5. Cultural potential

Questions:

- does the archive create cumulative change rather than only repeated copying?

Candidate metrics:

- capsule modification depth
- cumulative archive improvement
- archive-origin novelty rate
- retention vs discard after validation

## What We Should Not Do

Do not define:

```text
open_endedness_score = weighted_sum(...)
```

Reasons:

- different axes can move in different directions;
- a single score hides whether the system is:
  - merely turbulent,
  - resilient but stagnant,
  - novel but not cumulative,
  - complex but ecologically flat.

## Minimal Claim Ladder

The biosphere should use a graded claim structure.

### Level 0

```text
bounded and non-collapsing
```

### Level 1

```text
continual ecological change under bounded state
```

### Level 2

```text
continuing novelty in niches, roles, or interaction motifs
```

### Level 3

```text
cumulative lineage or archive structure that is not reducible to noise
```

### Level 4

```text
multi-channel open-endedness:
genetic + ecological + cultural
```

We should not jump levels in writing or interpretation.

## Direct Design Consequences

1. Raw logs stay mandatory.
2. Habitat, lineage, interaction, and archive metrics must remain separate.
3. Probes should report multiple axes, not one summary score.
4. Recovery after shock should not be mistaken for open-ended innovation.
5. Cycles and oscillations should be treated as candidate structure, not proof.

## Recommended New Output Families

Later, the project should emit:

- `open_ended_change_summary.csv`
- `open_ended_novelty_summary.csv`
- `open_ended_complexity_summary.csv`
- `open_ended_ecology_summary.csv`
- `open_ended_culture_summary.csv`

These names are provisional, but the separation is important.

## Bottom Line

The strongest lesson from this literature is simple:

```text
Open-endedness is not one thing.
So it should not be measured with one thing.
```

If we respect that now, we will save ourselves from a lot of future
self-deception.
