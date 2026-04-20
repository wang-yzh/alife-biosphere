# Artificial-Life Positioning From Classic Papers

## Why This Note Exists

This note is for discussion with multiple readers.

Status note:

- this is a historical transition note written before `alife_biosphere` was
  initialized
- it is useful for project lineage, not as a current control document
- references to maze-project results below point to archived workspace
  materials, not to files inside this repository

The goal is not to defend the old maze-transfer pipeline as the final answer.
The goal is to place the project in a clearer research lineage and say, in
plain terms, what kind of system we should build next if the real aim is
artificial life.

Current repository status matters:

```text
maze_novelty is now archived as a historical project.
It remains useful as a source of components, diagnostics, and lessons.
It should not continue unchanged as the main research line.
```

That conclusion is already recorded in:

```text
the archived maze closure note in the workspace archive
```

## Short Version

If we summarize the classic literature honestly, the next project should not be
"a stronger maze-solving algorithm."

It should be:

```text
a persistent artificial-life training ecology
where populations accumulate experience,
compress part of that experience into inheritable structure,
and continue changing across generations and habitats
```

In that framing:

- maze tasks are habitats, not the final goal;
- behavior priors are candidate inherited material, not the whole organism;
- transfer tests are migration events, not the whole research question;
- novelty is an ecological pressure, not just a scalar bonus.

## What The Current Repo Actually Achieved

Before the papers, it helps to place the current repo clearly.

This project did succeed at several real things:

- it built a disciplined MiniGrid experimentation stack;
- it showed that training history changes later target-side behavior;
- it extracted and executed behavior priors from target probing;
- it developed negative-control discipline and transfer calibration.

It did not validate the stronger claim:

```text
pretraining reliably improves adaptation on the target task
```

Recent documents make that clear:

- the archived multiseed pretraining-benefit result note
- the archived transfer-ladder sweep result note
- the archived maze closure note

So the right move is not to pretend the repo already became artificial life.
The right move is to treat it as a bridge:

```text
cyclic novelty / transfer experiments
-> behavior structure vocabulary
-> next artificial-life architecture
```

## Five Classic Paper Lenses

## 1. Options: behavior should exist above single actions

Reference:

- Sutton, Precup, Singh (1999), "Between MDPs and Semi-MDPs"

Core contribution:

```text
An agent should not only choose primitive actions.
It should also have temporally extended behavior units.
```

Why it matters here:

The repo's `motif`, `prior`, and `option-like` vocabulary is not random. It
touches a serious and durable idea: useful behavior often lives at an
intermediate time scale.

What this paper supports in our direction:

- inherited structure should not be stored only as raw episodes;
- behavior chunks are a reasonable unit of memory;
- a lineage may pass down reusable behavior patterns.

What it does not give us:

- a population model;
- an ecology;
- open-ended novelty;
- inheritance and lineage as first-class entities.

So this paper supports one layer of the future project, but not the whole
architecture.

## 2. Novelty Search: direct objective maximization is often the wrong driver

Reference:

- Lehman, Stanley (2011), "Abandoning Objectives: Evolution Through the Search
  for Novelty Alone"

Core contribution:

```text
Complex behavior may emerge more reliably when search rewards behavioral
difference instead of immediate task success.
```

Why it matters here:

This explains why the project's original cyclic novelty instinct was not
crazy. If the search space is deceptive, directly optimizing "solve the maze"
can kill useful exploration too early.

What this paper supports in our direction:

- open exploration phases are legitimate;
- diversity pressure is not just decoration;
- a system may need room to become interesting before it becomes competent.

What it does not give us:

- long-lived populations;
- inherited memory;
- ecological succession;
- persistent world history.

This is important: novelty search explains why we wanted "open novelty," but it
still lives inside an optimization mindset unless we embed it inside a real
population ecology.

## 3. Avida and digital life: the subject is the population, not the score

Reference:

- Ofria, Wilke (2004), "Avida: A Software Platform for Research in
  Computational Evolutionary Biology"

Core contribution:

```text
Digital organisms can be studied as evolving populations with inheritance,
mutation, competition, adaptation, and lineage history.
```

Why it matters here:

This is much closer to the project's original dream than the current
pretraining-transfer framing.

What this paper supports in our direction:

- the main object should be a persistent population;
- individuals should reproduce, vary, and leave descendants;
- lineage history should be recorded and analyzed;
- environments should shape what survives.

This is the biggest missing piece in the archived repo.

The repo mostly tracked:

```text
method
-> artifact
-> target evaluation
```

But an artificial-life system should track:

```text
world
-> habitat
-> population
-> organism
-> lifetime
-> inheritance
-> lineage
-> extinction and diversification
```

That is the architectural gap.

## 4. Open-ended evolution: novelty is not enough without ongoing innovation

Reference:

- Taylor et al. (2016), "Open-Ended Evolution: Perspectives from the OEE
  Workshop in York"

Core contribution:

```text
Open-endedness is not just producing variety once.
It is sustaining the conditions for continuing innovation and new organization.
```

Why it matters here:

This paper helps us avoid fooling ourselves.

The archived repo can produce many diagnostics:

- more transitions;
- more prior executions;
- more structural movement;
- more motifs.

But open-ended evolution asks a harder question:

```text
Does the system keep generating genuinely new organization,
new behavioral niches,
or new inherited structures over time?
```

Under that standard, the repo is still pre-open-ended.

It has mechanisms and proxies, but not yet an enduring evolutionary process.

## 5. Evolutionary innovation types: what kind of novelty are we trying to make

Reference:

- Tim Taylor (2019), "Evolutionary Innovations and Where to Find Them"

Core contribution:

The paper distinguishes among:

- exploratory novelty: new combinations within a known space;
- expansive novelty: entering previously unreachable parts of the space;
- transformational novelty: changing the effective space itself.

Why it matters here:

This gives us a much better language for the future project.

Most current maze experiments are still near the exploratory level:

```text
new traces
new motifs
new transfer guards
new combinations of existing local behavior
```

A stronger artificial-life system should aim for expansive novelty:

```text
new stable strategies,
new ecological roles,
new inherited behavior packages,
new migration success patterns across habitats
```

Transformational novelty would be even bigger:

```text
the population changes what counts as an effective unit of behavior,
memory, cooperation, or inheritance
```

That is likely too ambitious for version one, but it is the right horizon.

## What These Papers Suggest We Are Actually Building

Putting the papers together, the most defensible description is:

```text
We are trying to build a digital population in maze-like habitats
where behavior is not relearned from zero every generation.
Individuals should accumulate life experience,
part of that experience should become inheritable structure,
and lineages should diversify under changing ecological pressure.
```

That means the next system is not just:

```text
agent + replay + transfer benchmark
```

It is closer to:

```text
World
  -> Habitats
  -> Population
  -> Organisms
  -> Lifetimes
  -> Experience archives
  -> Inheritance packets
  -> Variation operators
  -> Selection events
  -> Lineage records
  -> Ecological memory
```

## What We Likely Missed In The Old Framing

The archived project was strongest when it treated behavior as structure.
It drifted when it treated benchmark transfer as the main proof of value.

What seems to have been missing:

### 1. A first-class lineage model

The system needs explicit answers to:

- who is the parent of whom;
- what was inherited;
- what mutated;
- which lineages died out;
- which lineages expanded into new habitats.

### 2. A real inheritance mechanism

Experience cannot remain only:

- a log;
- a motif list;
- a diagnostic prior bank.

It needs a rule for becoming heritable material.

The key research question becomes:

```text
Which parts of lived experience become stable inherited structure?
```

### 3. Habitats instead of benchmark levels

MiniGrid tasks should become an ecology of habitats:

- some easy and resource-rich;
- some sparse and punishing;
- some dynamic;
- some migration gateways;
- some extinction traps.

A habitat should shape survival, not only serve as a test item.

### 4. Lifecycle and turnover

Each organism should have a lifecycle:

- birth;
- development;
- exploration;
- stress;
- reproduction;
- death;
- legacy.

Without this, we still have training runs, not lives.

### 5. Population-level evaluation

The main questions should shift from:

```text
Did method A beat method B on final score?
```

to:

```text
Did the population diversify?
Did inherited structure persist?
Did lineages adapt to new habitats?
Did ecological pressure create new stable behavior roles?
Did innovation survive selection?
```

## How To Reuse This Repo Without Repeating Its Limits

This repo still has valuable pieces to carry forward:

- MiniGrid adaptation layer;
- state-signature encoding ideas;
- motif / behavior-prior vocabulary;
- transfer-ladder and negative-control discipline;
- documentation habits and versioned experiment reporting.

But these pieces should be demoted into components of a larger organism-world
system.

Recommended reuse stance:

```text
Keep the implementation pieces.
Do not keep the benchmark-first worldview.
```

## Candidate Thesis For The Next Project

Here is a discussion-ready wording that is more aligned with the literature:

```text
We aim to build an artificial-life system in maze-like worlds where a
persistent population of digital organisms accumulates experience across
generations. The system should convert part of each organism's lifetime
experience into inheritable behavioral structure, allowing lineages to
differentiate, migrate across habitats, and adapt under changing ecological
pressure. The scientific goal is not only task performance, but the emergence
and persistence of open-ended behavioral innovation.
```

Shorter version:

```text
We are building a maze-based artificial-life ecology,
not just a maze solver.
```

## Questions For Multi-Person Review

If this note is circulated, the most useful disagreements will probably be
about these points:

1. What should count as heritable material in version one:
   behavior priors, motifs, subgoal memory, or something more genome-like?
2. Is the first persistent world still based on MiniGrid, or should MiniGrid be
   only a prototype habitat?
3. What is the minimum viable lineage record?
4. What ecological pressures should alternate over time:
   abundance, scarcity, migration, hazard, or competition?
5. What would count as genuine expansive novelty in the first publishable
   version?

## Suggested Next Architectural Objects

If the next repo starts fresh, these look like the right top-level concepts:

```text
World
Habitat
Population
Organism
Genome
Lifetime
Experience
InheritancePacket
LineageRecord
SelectionPolicy
EcologicalMemory
MigrationEvent
```

That would put the implementation much closer to the literature we say we are
following.

## References

- Sutton, R. S., Precup, D., Singh, S. (1999). Between MDPs and Semi-MDPs:
  A Framework for Temporal Abstraction in Reinforcement Learning.
- Lehman, J., Stanley, K. O. (2011). Abandoning Objectives: Evolution Through
  the Search for Novelty Alone.
- Ofria, C., Wilke, C. O. (2004). Avida: A Software Platform for Research in
  Computational Evolutionary Biology.
- Taylor, T., et al. (2016). Open-Ended Evolution: Perspectives from the OEE
  Workshop in York.
- Taylor, T. (2019). Evolutionary Innovations and Where to Find Them.
