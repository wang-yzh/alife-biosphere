# Collective Intelligence, Swarm Cognition, And Consensus Failure Review v0

## Purpose

This note extends the literature program toward a question that becomes
increasingly important once `alife_biosphere` contains groups, communication,
memory, and governance:

```text
Can a population or group become smarter than its members,
and if so, when does that collective intelligence work,
and when does it fail?
```

The goal is not to romanticize swarm behavior.
The goal is to understand:

- how distributed decision-making can create group-level cognition,
- what structural conditions make it adaptive,
- and why the same processes can also produce herding, lock-in, and collective
  error.

In practice, this note asks:

1. What is collective intelligence in a living system?
2. How can local interactions produce useful group-level decisions?
3. Why do quorum, diversity, and informed minorities matter?
4. Why does consensus sometimes amplify error instead of knowledge?

## Short Answer

The literature points to a sharp but balanced answer:

```text
collective intelligence is not just many individuals doing the same thing.
it emerges when distributed interactions let groups pool information,
filter noise, and coordinate action better than isolated members could.
```

But it also shows:

```text
the same social influence that enables collective intelligence
can also destroy it by collapsing diversity, locking in bad signals,
or amplifying premature consensus.
```

For our project, that means:

- collective intelligence should be treated as an empirical outcome, not an
  automatic property of groups;
- group cognition depends on information diversity, interaction structure, and
  decision rules;
- quorum, minority leadership, and local information pooling are all distinct
  mechanisms;
- consensus failure should be designed as carefully as consensus success.

## Core Papers

## 1. Sumpter (2006), "The principles of collective animal behaviour"

Why it matters:

- this is one of the foundational reviews for collective behavior in animals
- it gives the clearest general framework for self-organization in groups

The key lesson:

```text
simple local interaction rules can generate complex adaptive collective
behavior,
but only under the right balance of positive feedback, negative feedback,
response thresholds, and noise.
```

This is directly relevant to `alife_biosphere`.

It means that group-level organization should not be built as a mysterious
higher mind.
It should emerge from:

- local sensing,
- information amplification,
- information decay,
- and coordinated thresholds.

Design implication:

- collective decision systems should be decomposed into local mechanisms
- feedback loops should be explicit in the design

Useful translation into biosphere terms:

- `positive_feedback_gain`
- `negative_feedback_gain`
- `response_threshold`
- `information_decay_rate`

## 2. Conradt and Roper (2003), "Group decision-making in animals"

Why it matters:

- this is one of the clearest early papers distinguishing democratic and
  despotic group decisions
- it ties decision rule structure directly to group-level cost

The key lesson:

```text
how a group aggregates preferences matters.
despotic and democratic decisions can have very different costs for members and
for the group as a whole.
```

This is very useful for `alife_biosphere`.

It means collective decisions should not be treated as a single generic process.
We should later distinguish:

- majority-like consensus
- leadership by informed minority
- despotic rule
- quorum-based rule

Design implication:

- decision mode should be a real variable
- group decision efficiency and distributional cost should both be measurable

Useful translation into biosphere terms:

- `decision_mode`
- `consensus_cost_distribution`
- `leader_bias`
- `group_decision_efficiency`

## 3. Conradt and Roper (2005), "Consensus decision making in animals"

Why it matters:

- this is still one of the most useful syntheses for consensus as an ecological
  problem
- it emphasizes that consensus often occurs under real conflicts of interest

The key lesson:

```text
consensus is not only about information integration.
it is also about resolving conflicts while keeping the group coherent.
```

This matters because `alife_biosphere` already aims to support:

- shared movement
- group persistence
- large-group coordination
- conflict mediation

Design implication:

- consensus should be evaluated in relation to both accuracy and cohesion
- conflict-sensitive consensus rules should be possible

Useful translation into biosphere terms:

- `consensus_accuracy`
- `group_split_risk`
- `cohesion_preservation_score`

## 4. Couzin, Krause, Franks, Levin (2005),
"Effective leadership and decision-making in animal groups on the move"

Why it matters:

- this is the canonical paper on informed minorities guiding large groups
- it is one of the strongest pieces of evidence that leadership can emerge
  without explicit signaling or central authority

The key lesson:

```text
a small informed minority can guide a much larger group
if the interaction structure allows its information to propagate effectively.
```

This is extremely important for `alife_biosphere`.

It suggests that:

- collective intelligence does not always require explicit voting;
- leadership can be distributed and information-sensitive;
- group accuracy may depend on the ratio of informed to uninformed members.

Design implication:

- later worlds should support informed-minority guidance
- leadership should be a dynamic influence relation, not only a hard-coded role

Useful translation into biosphere terms:

- `informed_fraction`
- `minority_guidance_strength`
- `leadership_emergence_score`

## 5. Seeley and Buhrman (1999),
"Group decision making in swarms of honey bees"

Why it matters:

- this is one of the best concrete biological examples of distributed collective
  choice
- it shows a swarm acting as a real decision-making system without central
  control

The key lesson:

```text
distributed scout activity, recruitment, competition among alternatives,
and eventual convergence can produce high-quality collective choice.
```

This matters because it gives us a model richer than generic averaging.

The honeybee case shows:

- option discovery,
- option advertisement,
- option competition,
- and group commitment.

Design implication:

- collective decision systems should later support parallel option discovery
- competition among options should be explicit

Useful translation into biosphere terms:

- `option_advertisement_strength`
- `parallel_option_count`
- `commitment_convergence`

## 6. Seeley and Visscher (2004), "Quorum sensing during nest-site selection by honeybee swarms"

Why it matters:

- this is the strongest classic paper for quorum as a decision mechanism
- it makes the transition from exploration to commitment empirically concrete

The key lesson:

```text
groups often need a threshold rule for when to stop exploring
and commit to coordinated action.
```

This is one of the clearest design implications for `alife_biosphere`.

Without quorum or a similar threshold:

- groups may never commit,
- or they may commit too early.

Design implication:

- quorum thresholds should be explicit and tunable
- collective commitment should be distinct from mere local preference

Useful translation into biosphere terms:

- `quorum_threshold`
- `commitment_delay`
- `premature_commitment_risk`

## 7. Couzin (2009), "Collective cognition in animal groups"

Why it matters:

- this is one of the strongest conceptual syntheses for group-level cognition
- it explicitly frames collective behavior as a form of cognition, not just
  movement pattern

The key lesson:

```text
groups can integrate distributed information, amplify weak signals,
buffer noise, and effectively perform cognitive operations at the collective
level.
```

This is especially useful for us because it legitimizes a stronger claim:

- group cognition can be a real object in the biosphere

Design implication:

- the project should later support explicit collective-cognition diagnostics
- distributed sensing and distributed memory should be linked to decision
  quality

Useful translation into biosphere terms:

- `collective_cognition_score`
- `distributed_sensing_gain`
- `collective_inference_accuracy`

## 8. Lorenz, Rauhut, Schweitzer, Helbing (2011),
"How social influence can undermine the wisdom of crowd effect"

Why it matters:

- this is one of the strongest cautionary papers on consensus failure
- it shows that even mild social influence can reduce collective accuracy

The key lesson:

```text
social influence can reduce diversity without improving truth-tracking,
producing confident convergence on worse collective outcomes.
```

This is extremely important for `alife_biosphere`.

It means we should not assume:

- more communication -> better collective cognition

Sometimes the opposite is true.

Design implication:

- opinion diversity should be tracked as a resource
- collective accuracy and convergence should be measured separately

Useful translation into biosphere terms:

- `belief_diversity`
- `confidence_without_accuracy`
- `social_influence_gain`
- `collective_error`

## 9. Bikhchandani, Hirshleifer, Welch (1992),
"A Theory of Fads, Fashion, Custom, and Cultural Change as Informational Cascades"

Why it matters:

- this is the canonical cascade paper
- it shows how populations can ignore private information once social signals
  become dominant enough

The key lesson:

```text
sequential social observation can trigger cascades in which individuals stop
using their own information and simply follow the apparent majority.
```

This is a crucial failure mode for any long-lived communication or governance
system.

Design implication:

- later worlds should support informational cascades as a real risk
- the project should distinguish:
  - evidence pooling
  - from evidence suppression by conformity

Useful translation into biosphere terms:

- `cascade_risk`
- `private_signal_ignored`
- `herding_pressure`
- `cascade_break_threshold`

## 10. Couzin (2025), "Collective intelligence in animals and robots"

Why it matters:

- this is a recent synthesis by one of the central researchers in the field
- it is useful because it updates the animal-group perspective with a more
  explicit distributed-computation framing

The key lesson:

```text
collective systems can perform sensing, decision-making, and control tasks that
scale beyond the capability of isolated individuals, but only when information
flow, embodiment, and interaction structure align well.
```

This is valuable for us because it bridges:

- collective behavior
- distributed sensing
- swarm control
- and artificial systems design

Design implication:

- collective intelligence should later be evaluated partly as a distributed
  computation problem
- group performance should be compared against what isolated organisms or simple
  aggregation could achieve

## What This Means For Our Project

The literature suggests that `alife_biosphere` should not treat group
coordination as a side effect of many individuals being present.

The stronger interpretation is:

```text
groups can become information-processing systems
that discover options, pool signals, commit through thresholds,
and in some cases solve problems better than any member could alone
```

But this only holds when the system preserves enough:

- information diversity,
- useful local interaction,
- commitment discipline,
- and protection against bad cascades.

That means collective intelligence in the biosphere should be treated as:

- possible,
- measurable,
- and fragile.

## Direct Design Consequences

## 1. Collective cognition should be explicit

Later worlds should distinguish:

- individual information
- distributed information
- group decision state
- collective outcome quality

Suggested fields:

- `collective_cognition_score`
- `belief_diversity`
- `distributed_sensing_gain`
- `collective_error`

## 2. Decision rules should be typed

Later group decisions should not all look the same.

Suggested decision modes:

- `majority_consensus`
- `quorum_commitment`
- `informed_minority_guidance`
- `despotic_leadership`
- `weighted_reputation_consensus`

Suggested field:

- `decision_mode`

## 3. Quorum and commitment thresholds should be explicit

This is one of the strongest practical lessons from the bee literature.

Suggested fields:

- `quorum_threshold`
- `commitment_delay`
- `premature_commitment_risk`

Suggested event types:

- `quorum_reached`
- `collective_commitment_made`
- `premature_commitment_detected`

## 4. Consensus failure should be modeled directly

Following Lorenz and cascade theory:

- the system should support good consensus and bad consensus

Suggested fields:

- `cascade_risk`
- `herding_pressure`
- `private_signal_retention`
- `confidence_without_accuracy`

Suggested event types:

- `cascade_started`
- `cascade_broken`
- `collective_misfire`
- `minority_signal_suppressed`

## 5. Group intelligence should be compared against member intelligence

A strong claim of collective intelligence requires more than coordination.

It should later be possible to ask:

- did the group outperform typical individuals?
- did the group outperform simple averaging?
- did the group preserve useful heterogeneity?

Suggested metrics:

- group-over-individual accuracy lift
- group-over-average performance lift
- diversity-preserving decision quality
- consensus speed vs error tradeoff

## Proposed Additions To The Existing Design

### New fields

- `decision_mode`
- `belief_diversity`
- `quorum_threshold`
- `minority_guidance_strength`
- `cascade_risk`
- `collective_cognition_score`
- `confidence_without_accuracy`

### New event types

- `quorum_reached`
- `collective_commitment_made`
- `cascade_started`
- `cascade_broken`
- `collective_misfire`
- `minority_guidance_success`

### New metrics

- group-over-individual accuracy lift
- consensus speed
- belief-diversity retention
- cascade frequency
- premature commitment rate
- collective error under influence

## Proposed Probe Design

The first collective-intelligence probe can stay focused.

A reasonable first probe is:

```text
group with distributed partial information
-> compare isolated decisions, simple averaging,
   informed-minority guidance, and quorum-based consensus
-> then add stronger social influence and reduced diversity
-> measure group accuracy, convergence, and failure modes
```

The first useful question is:

```text
Under what conditions does the group genuinely outperform its members,
and under what conditions does social influence collapse useful diversity into
bad consensus?
```

That is enough to justify a collective-cognition layer.

## Build Recommendations

This literature review suggests three near-term design tasks.

### 1. Add collective-cognition diagnostics to the long-run roadmap

Reason:

- group intelligence should be a measurable property, not a narrative claim

### 2. Reserve quorum and informed-minority mechanisms early

Reason:

- they are among the clearest routes to adaptive distributed decisions

### 3. Treat consensus failure as a core phenomenon, not a bug

Reason:

- long-lived collective systems will almost certainly face herding and cascade
  problems

## Bottom Line

The collective-intelligence literature tells us that group-level cognition is
real, but conditional.

For `alife_biosphere`, the stronger target is:

```text
a world where groups can become distributed cognitive systems,
yet remain vulnerable to bad cascades, overconfidence, and premature consensus
```

That is the version of collective intelligence worth building toward.

## Sources

- Sumpter, D. J. T. (2006).
  "The principles of collective animal behaviour."
  [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC1626537/)
- Conradt, L., Roper, T. J. (2003).
  "Group decision-making in animals."
  [Nature](https://www.nature.com/articles/nature01294)
- Conradt, L., Roper, T. J. (2005).
  "Consensus decision making in animals."
  [PubMed](https://pubmed.ncbi.nlm.nih.gov/16701416/)
- Couzin, I. D., Krause, J., Franks, N. R., Levin, S. A. (2005).
  "Effective leadership and decision-making in animal groups on the move."
  [Nature](https://www.nature.com/articles/nature03236)
- Seeley, T. D., Buhrman, S. C. (1999).
  "Group decision making in swarms of honey bees."
  [DOI metadata / PDF mirrors](https://doi.org/10.1007/s002650050536)
- Seeley, T. D., Visscher, P. K. (2004).
  "Quorum sensing during nest-site selection by honeybee swarms."
  [DOI metadata / PDF mirrors](https://doi.org/10.1007/s00265-004-0814-5)
- Couzin, I. D. (2009).
  "Collective cognition in animal groups."
  [PubMed](https://pubmed.ncbi.nlm.nih.gov/19058992/)
- Lorenz, J., Rauhut, H., Schweitzer, F., Helbing, D. (2011).
  "How social influence can undermine the wisdom of crowd effect."
  [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC3107299/)
- Bikhchandani, S., Hirshleifer, D., Welch, I. (1992).
  "A Theory of Fads, Fashion, Custom, and Cultural Change as Informational Cascades."
  [SSRN entry](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1286306)
- Couzin, I. D. (2025).
  "Collective intelligence in animals and robots."
  [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12575731/)
