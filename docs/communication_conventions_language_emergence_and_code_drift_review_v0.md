# Communication Conventions, Language Emergence, And Code Drift Review v0

## Purpose

This note extends the literature program beyond basic signaling into a more
system-level question:

```text
How does a population move from isolated signals
to something that behaves like a communication system?
```

The goal is not to build human language in `alife_biosphere`.
The goal is to understand when a population-level signaling ecology can produce:

- shared conventions,
- code drift,
- increasingly structured message systems,
- and new failure modes such as covert signaling, ambiguity, and semantic
  divergence.

In practice, this note asks:

1. How do signaling conventions emerge at population scale?
2. Why does transmission across generations change communication structure?
3. Why do codes drift even without obvious selection?
4. Why can ambiguity or covert signaling be adaptive rather than defective?

## Short Answer

The literature suggests a strong common theme:

```text
communication systems do not need to be designed from above.
they can self-organize through repeated coordination, transmission bottlenecks,
population drift, and selective pressure on usefulness and learnability.
```

It also suggests:

```text
once a communication system exists,
it does not stay still.
it can drift, split, compress, become compositional,
or be strategically made ambiguous.
```

For our project, that means:

- signals should not be treated only as one-step actions;
- population-level code formation is a legitimate target;
- archives and lineages may eventually transmit conventions, not just behaviors;
- code drift and semantic divergence should be expected, not treated as bugs.

## Core Papers

## 1. Steels (1995), "A Self-Organizing Spatial Vocabulary"

Why it matters:

- this is one of the cleanest classic artificial-life style demonstrations of
  convention formation
- it shows that a population of agents can self-organize a usable vocabulary
  from repeated interactions without a central designer

The key lesson:

```text
shared communicative structure can emerge from local interaction,
feedback, and adaptation,
even when agents begin without a fixed common vocabulary.
```

This is highly relevant to `alife_biosphere`.

It suggests that later communication should not have to start as:

- fixed global tokens with fixed universal meaning

It could instead begin as:

- local conventions that stabilize through repeated use

Design implication:

- signal systems can be allowed to form from scratch inside the world
- convention success should be measured at the population level
- communication can be self-organizing before it is evolutionarily inherited

Useful translation into biosphere terms:

- `convention_id`
- `local_vocabulary_size`
- `communicative_success`
- `population_consensus_level`

## 2. Skyrms (2009), "Evolution of signalling systems with multiple senders and receivers"

Why it matters:

- this generalizes simple sender-receiver games to a network setting
- it is one of the strongest bridges from isolated signals to communication
  systems

The key lesson:

```text
meaning can emerge in populations through repeated coordination across multiple
agents, not only in idealized one-to-one games
```

This matters because `alife_biosphere` is explicitly multi-agent and ecological.

Design implication:

- communication should be modeled as a population network process
- convention success may depend on network position and repeated local
  interaction
- group or habitat-local codes may emerge without world-level consensus

Useful translation into biosphere terms:

- `sender_receiver_network_density`
- `local_code_coherence`
- `cross_group_signal_alignment`

## 3. Nowak, Plotkin, Krakauer (1999), "The evolutionary language game"

Why it matters:

- this is a foundational mathematical treatment of communication code formation
- it shows how signaling systems can be analyzed as population dynamics over
  signal-object associations

The key lesson:

```text
communication systems can be studied as evolving mappings between signals and
meanings,
with population-level competition among alternative codes
```

This is useful for us because it gives a rigorous way to think about:

- signal repertoire size
- ambiguity
- convention competition
- code replacement

Design implication:

- a code should be treated as a population-level structure that can compete with
  alternative codes
- communication can drift or stabilize through differential success

Useful translation into biosphere terms:

- `signal_meaning_map`
- `code_competition_score`
- `ambiguity_rate`
- `convention_replacement_rate`

## 4. Nowak, Plotkin, Jansen (2000), "The evolution of syntactic communication"

Why it matters:

- this paper pushes beyond simple symbol-object mappings
- it gives a route for thinking about how more structured communication can
  emerge from simpler signaling

We do not need human syntax.
But the paper is still useful because it raises a key design question:

```text
when does a communication system become compositional,
so that a small vocabulary can support more expressive combinations?
```

This matters to us because later biosphere lineages may need:

- role markers
- context markers
- archive access cues
- warning-plus-target combinations

Design implication:

- later signal systems may evolve from atomic tokens toward small compositional
  codes
- message structure could itself become an evolvable object

Useful translation into biosphere terms:

- `compositional_signal_score`
- `message_factorization`
- `expressive_efficiency`

## 5. Kirby, Griffiths, Smith (2014), "Iterated learning and the evolution of language"

Why it matters:

- this is the clearest modern summary of iterated learning as a mechanism for
  population-level structure formation
- it is especially relevant because our project already cares about transmission
  across generations

The key lesson:

```text
transmission bottlenecks and repeated learning can reshape communication systems
toward patterns that are easier to learn and use
```

This is extremely relevant to `alife_biosphere`.

It suggests that communication conventions may evolve not only through immediate
utility, but through:

- learnability
- compressibility
- cultural transmission bias

Design implication:

- the project should later distinguish direct communicative usefulness from
  transmission fitness
- archive or lineage transmission may simplify or regularize codes

Useful translation into biosphere terms:

- `transmission_bottleneck`
- `learnability_score`
- `code_compressibility`
- `iterated_transfer_fidelity`

## 6. Crutchfield and Whalen (2012), "Structural Drift"

Why it matters:

- this is one of the strongest formal entries for drift in sequential learning
  systems
- it is very useful for us because it makes code drift a population process,
  not merely a mistake

The key lesson:

```text
communication systems can drift structurally through repeated transmission,
even without a simple adaptive story for each local change
```

This matters because later biosphere worlds may have:

- lineage-local communication
- archive-mediated communication
- group codes
- cross-habitat transmission

and those codes may diverge simply through sequential transmission and memory.

Design implication:

- code drift should be expected under long communication chains
- fidelity and innovation can trade off
- different habitats or lineages may develop semantically separated dialects

Useful translation into biosphere terms:

- `code_drift_rate`
- `communication_fidelity`
- `dialect_divergence`
- `sequential_transmission_loss`

## 7. Smaldino, Flamson, McElreath (2018), "The Evolution of Covert Signaling"

Why it matters:

- this paper is especially valuable because it shows ambiguity can be adaptive
- it is a perfect bridge between communication systems and social ecology

The key lesson:

```text
signals do not always evolve to maximize clarity.
sometimes deliberately ambiguous or covert signals are favored
because they coordinate allies without alienating outsiders.
```

This matters a lot for `alife_biosphere`.

Once the world contains:

- group identity
- trust gates
- coalition formation
- archive access
- cheaters and mimics

then some communication may be selected to remain partially hidden.

Design implication:

- ambiguity should not always count as communication failure
- later communication systems may have public and covert channels
- coalition-friendly signaling may coexist with general signaling

Useful translation into biosphere terms:

- `covert_signal_rate`
- `public_signal_rate`
- `coalition_selectivity`
- `outsider_detection_rate`

## 8. "Communication breakdown": the evolution of signal unreliability and deception (2014)

Why it matters:

- this review is valuable because it distinguishes multiple kinds of
  unreliability
- it helps avoid using "deception" as a catch-all label

What we should take from it:

- unreliability can come from noise, misalignment, strategic deception, or other
  causes
- communication systems may remain functional even when they are imperfect

This is a strong complement to the earlier signaling review.

Design implication:

- code drift, ambiguity, noise, and deception should be logged separately
- communication failure analysis should become more granular once systems get
  richer

## What This Means For Our Project

The literature suggests that `alife_biosphere` should treat communication as a
population-level evolving system, not only as local signaling acts.

The stronger interpretation is:

```text
lineages and groups may develop local conventions,
those conventions may drift or regularize through transmission,
and communication systems may become clearer, more compositional,
or strategically more ambiguous depending on ecological pressure
```

That is a much richer target than:

- one signal token
- one trust gate
- one fixed meaning map

## Direct Design Consequences

## 1. Communication should support convention formation

Later worlds should allow:

- local code emergence
- convention competition
- partial consensus
- group-local vocabularies

Suggested fields:

- `convention_id`
- `local_code_coherence`
- `signal_meaning_map`
- `consensus_strength`

## 2. Transmission should shape communication

This is one of the strongest practical lessons from iterated learning.

Later communication systems should be influenced by:

- who teaches whom
- what the transmission bottleneck is
- how much code must be compressed or generalized

Suggested fields:

- `transmission_bottleneck`
- `teaching_exposure`
- `code_compressibility`
- `iterated_transfer_fidelity`

## 3. Code drift should be expected and measured

Not every change in signal usage is a useful adaptation.

Some will be:

- drift
- local divergence
- sequential distortion
- semantic split

Suggested fields:

- `code_drift_rate`
- `dialect_divergence`
- `cross_group_alignment`

Suggested event types:

- `convention_shift_event`
- `dialect_split_event`
- `semantic_drift_event`

## 4. Communication systems may become compositional

We should reserve the idea that richer codes can emerge from simpler tokens.

This does not require full language.
It may only mean:

- role token + target token
- warning token + location token
- archive request token + trust marker

Suggested fields:

- `compositional_signal_score`
- `message_part_count`
- `factorized_meaning_count`

## 5. Ambiguity and covert signaling may be adaptive

This is especially important once group structure deepens.

Later worlds should allow:

- public signals
- covert coalition signals
- ambiguous identity markers
- selective comprehensibility

Suggested fields:

- `covert_signal_rate`
- `audience_specific_readability`
- `ambiguity_gain`

## Proposed Additions To The Existing Design

### New fields

- `convention_id`
- `signal_meaning_map`
- `local_code_coherence`
- `transmission_bottleneck`
- `code_drift_rate`
- `compositional_signal_score`
- `covert_signal_rate`

### New event types

- `convention_formed`
- `convention_shift_event`
- `dialect_split_event`
- `semantic_drift_event`
- `covert_signal_used`

### New metrics

- consensus strength
- cross-group code alignment
- learnability of code
- code drift rate
- compositional expressivity
- covert coordination success

## Proposed Probe Design

The first communication-system probe can stay focused.

A reasonable first probe is:

```text
population with repeated local coordination problems
-> allow signals to emerge and stabilize
-> compare fixed code, self-organized code, and transmitted code
-> then introduce group separation and partial coalition structure
-> measure convention formation, drift, and covert communication
```

The first useful question is:

```text
Do repeated local interactions plus transmission produce stable but drift-prone
communication conventions that later differentiate across groups?
```

That is enough to justify a full communication-systems layer.

## Build Recommendations

This literature review suggests three near-term design tasks.

### 1. Distinguish signal acts from communication systems

Reason:

- local signaling is not yet a population-level convention ecology

### 2. Reserve a place for transmission-shaped code evolution

Reason:

- learnability and compression may be as important as immediate utility

### 3. Treat semantic drift as a normal long-run outcome

Reason:

- long-lived lineages and archives will almost certainly drift unless codes are
  artificially pinned down

## Bottom Line

The communication-systems literature tells us that the real question is not only:

```text
can agents signal?
```

It is:

```text
can a population grow, stabilize, transmit, drift, and strategically reshape a
shared communication system over time?
```

For `alife_biosphere`, that is the stronger and more interesting target.

## Sources

- Steels, L. (1995).
  "A Self-Organizing Spatial Vocabulary."
  [PDF](https://ai.vub.ac.be/sites/default/files/Steels%20-%201995%20-%20A%20Self-Organizing%20Spatial%20Vocabulary.pdf)
- Skyrms, B. (2009).
  "Evolution of signalling systems with multiple senders and receivers."
  [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC2689717/)
- Nowak, M. A., Plotkin, J. B., Krakauer, D. C. (1999).
  "The evolutionary language game."
  [PubMed](https://pubmed.ncbi.nlm.nih.gov/10504282/)
- Nowak, M. A., Plotkin, J. B., Jansen, V. A. A. (2000).
  "The evolution of syntactic communication."
  [Nature](https://www.nature.com/articles/35006635)
- Kirby, S., Griffiths, T., Smith, K. (2014).
  "Iterated learning and the evolution of language."
  [PubMed](https://pubmed.ncbi.nlm.nih.gov/25062470/)
- Crutchfield, J. P., Whalen, S. (2012).
  "Structural Drift: The Population Dynamics of Sequential Learning."
  [PLOS Computational Biology](https://journals.plos.org/ploscompbiol/article?id=10.1371%2Fjournal.pcbi.1002510)
- Smaldino, P. E., Flamson, T. J., McElreath, R. (2018).
  "The Evolution of Covert Signaling."
  [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC5861109/)
- "Communication breakdown": the evolution of signal unreliability and deception
  (2014).
  [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0003347213004843)
