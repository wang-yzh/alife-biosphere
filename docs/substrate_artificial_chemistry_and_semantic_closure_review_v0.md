# Substrate, Artificial Chemistry, Semantic Closure, And Development Review v0

## Purpose

This note extends the literature program toward a deeper artificial-life
question:

```text
Which parts of the system are allowed to evolve,
and which parts are permanently fixed by the simulator?
```

The goal is not to turn `alife_biosphere` into a full artificial chemistry
immediately.

The goal is to clarify how far the project wants to go beyond:

- fixed controller interpretation
- fixed capsule semantics
- fixed inheritance meaning

In practice, this note asks:

1. What should the substrate guarantee?
2. What should remain evolvable above the substrate?
3. Why does semantic closure matter if we care about open-ended life-like
   systems?
4. What should stand between genome and realized phenotype?

## Short Answer

The literature suggests a deep but usable distinction:

```text
Some layer must remain fixed enough to provide a world.
But if too much of the representation, interpretation, and inheritance meaning
is fixed from the outside, then the system may remain optimization-like rather
than life-like.
```

The most important lesson is:

```text
open-ended artificial life becomes stronger when the meaning of inherited
structure depends on internal evolved interpreters and constructors,
not only on an external fixed decoder.
```

For our project, that does not mean we must build a chemistry first.
It does mean we should eventually ask whether:

- capsules are just external tokens with simulator-defined meaning;
- or whether some part of their interpretation can itself be lineage-evolved.
- and whether development is treated as a real inherited interpretive process
  rather than a thin convenience layer.

## Core Papers

## 1. von Neumann, "Theory of Self-Reproducing Automata"

Why it matters:

- this is the foundational source for the universal-constructor idea
- it gives the deepest early framing of self-reproduction as more than copying

The key idea we should reuse:

Self-reproduction in rich systems is not just:

```text
copy structure
```

It is:

```text
copy description
+ interpret description
+ construct a functioning descendant
```

This distinction matters enormously for us.

Right now, in a typical simulator design, the meaning of inherited data is often
completely outside the evolving system.

von Neumann's perspective pushes us to ask:

```text
is inherited structure merely copied,
or is it also part of a system that internally interprets and reconstructs
itself?
```

Design implication:

- we should distinguish inherited description from inherited machinery
- group, archive, and capsule systems may later need separate copier and
  interpreter roles

## 2. Hickinbotham et al. (2016),
"Maximizing the Adjacent Possible in Automata Chemistries"

Why it matters:

- this paper is especially useful because it is about substrate design
- it asks how to design low-level rules so open-ended possibilities are not
  killed by the substrate itself

What we should take from it:

- the substrate has to balance fixed and evolvable aspects
- some boundaries belong to "physics" and some to "biology"
- if too many useful operations are impossible, the adjacent possible stays too
  small
- if too much is unconstrained, the system may become meaningless or unstable

This is highly relevant to `alife_biosphere`, even if we are not building a
chemistry.

We still need to choose:

- what counts as immutable world law
- what counts as evolvable protocol
- what counts as lineage-dependent interpretation

Design implication:

- the project should explicitly separate:
  - fixed substrate rules
  - evolvable organism-level structure
  - optional later evolvable interpretation layers

Useful translation into biosphere terms:

- `fixed_world_rules`
- `evolvable_protocol_bank`
- `interpreter_mutability`
- `constructor_cost`

## 3. Clark, Hickinbotham, Stepney (2017),
"Semantic closure demonstrated by the evolution of a universal constructor architecture in an artificial chemistry"

Why it matters:

- this is the most direct paper for the question we now face
- it shows an in silico system where genomic meaning is not merely declared by
  the simulator once and for all

The key idea:

```text
semantic closure
```

means, roughly, that the system's symbols mean what they mean because the system
contains the machinery that interprets them, and that machinery is itself part
of what is inherited.

This is a much stronger form of heredity than:

```text
the simulator decodes token X as behavior Y forever
```

What we should take from it:

- evolving systems become richer when copier, constructor, and genomic material
  can co-evolve
- meaning can shift through lineage change rather than being fixed externally

This matters because our current biosphere plans still assume many things like:

- capsule categories
- archive semantics
- controller interpretation

will be externally defined.

That is a reasonable starting point.
But this paper tells us where the deeper artificial-life horizon lies.

Design implication:

- we may eventually want a distinction between:
  - inherited content
  - inherited interpreter
  - inherited constructor
- the semantics of some behavioral structures may later need to be lineage-local
  rather than globally fixed

Useful translation into biosphere terms:

- `capsule_interpreter_id`
- `interpreter_fidelity`
- `constructor_budget`
- `semantic_shift_event`

## 4. Pattee, matter-symbol and semantic-closure line

Why it matters:

- Pattee gives the philosophical and theoretical core behind semantic closure
- this is the strongest answer to why symbols are not just labels pasted onto
  matter

What we should take from it:

- open-ended evolution requires some relation between material dynamics and
  symbolic description
- a living system is not only matter and not only code; it is the coupling
  between them

For our project, this means:

```text
if inherited structure is always interpreted by an untouched simulator-side
decoder,
then part of the life-like loop remains outside the evolving world
```

That is not always bad.
But it marks a limit.

Design implication:

- we should know which meanings are simulator-fixed and which are potentially
  lineage-shaped
- later versions should consider whether some archive/capsule semantics can be
  interpreter-relative

## 5. Rocha (2001), "Evolution with material symbol systems"

Why it matters:

- this is useful as a bridge between abstract semantic closure and agent-based
  evolving systems
- it helps us think about when symbols help open-endedness

What we should take from it:

- symbolic representation can increase evolvability,
  but only when tied back to material constructive processes
- pure symbolic inheritance without material grounding risks becoming too
  detached

Design implication:

- the archive should not become a pure floating symbolic library
- inherited capsules should stay tied to embodiment, cost, and construction

## Development And Genotype-To-Phenotype Mapping

## Why This Theme Matters

Even with a good substrate, the project can still become shallow if it assumes:

```text
genome -> direct parameter readout -> behavior
```

That shortcut is convenient, but it throws away one of the main biological
advantages we want to keep:

```text
development
```

Development is where inherited structure is interpreted under local conditions.
Without it, we lose:

- developmental bias
- plasticity
- phenotype divergence under shared genomes
- inherited means beyond copied outcomes

## Development Papers

### [Uller et al. 2018, "Developmental Bias and Evolution: A Regulatory Network Perspective"](https://pmc.ncbi.nlm.nih.gov/articles/PMC6063245/)

Why it matters:

- developmental systems make some phenotypes easier to produce than others;
- that bias is part of evolution, not a nuisance around it.

Design implication:

- phenotype space should be structured, not flat;
- later development should intentionally preserve asymmetry in what variation is
  easy to realize.

### [Cussat-Blanc, Harrington, and Banzhaf 2018, "Artificial Gene Regulatory Networks: A Review"](https://pubmed.ncbi.nlm.nih.gov/30681915/)

Why it matters:

- gives the strongest bridge from simple inherited parameters to a richer
  genome-to-phenotype system.

Design implication:

- keep the genome modular and regulation-ready;
- avoid locking the project into a flat parameter table that later needs a full
  rewrite.

### [Lala 2025, "A developmentalist's view of inheritance"](https://link.springer.com/article/10.1007/s10211-025-00464-0)

Why it matters:

- inheritance is not only copying successful end states;
- it is transmission of the means to rebuild useful phenotypes under
  developmental conditions.

Design implication:

- developmental context belongs inside inheritance architecture;
- offspring construction should later include nursery bias, epigenetic carryover,
  and inherited priors, not only copied parameters.

### [Shea 2011, "Developmental Systems Theory Formulated as a Claim about Inherited Representations"](https://pmc.ncbi.nlm.nih.gov/articles/PMC3210733/)

Why it matters:

- inherited representations include developmental resources and interpretive
  context, not only DNA-like sequence.

Design implication:

- the multi-channel inheritance split in `inheritance_architecture_v0.md` is
  theoretically grounded, not just convenient engineering.

## What This Means For Our Project

The literature suggests a layered answer.

In the short term:

```text
it is acceptable to start with simulator-defined capsule types,
fixed habitat laws,
and externally interpreted inheritance channels
```

In the longer term:

```text
if we want a deeper artificial-life system,
we should move some representation, interpretation, and constructive meaning
inside the evolving world
```

That does not mean "full chemistry or bust."
It means we should avoid accidentally freezing too much of what counts as
meaningful heredity.

It also means:

```text
world design
genome design
development design
```

are one coupled design problem, not three later cleanups.

## Direct Design Consequences

## 1. We should explicitly separate substrate law from evolvable protocol

Right now that distinction is still mostly implicit.

We should make it explicit:

- substrate law:
  - conservation bounds
  - habitat update constraints
  - event timing
  - damage and death rules
- evolvable protocol:
  - how agents exploit resources
  - how capsules are used
  - how groups coordinate
  - how archive material is recombined

Suggested future document section:

```text
fixed laws vs evolvable meanings
```

## 2. Interpreter-like components should be reserved conceptually

Even if we do not implement them yet, it is worth reserving the idea that some
future inherited structures may depend on inherited interpreters.

That suggests later fields such as:

- `interpreter_id`
- `interpreter_mutability`
- `capsule_interpreter_binding`

## 3. Copying and construction should not be collapsed forever

The von Neumann / semantic-closure line suggests that there is a deep difference
between:

- copying inherited description
- constructing a working descendant from that description

Even if the first biosphere versions hide most of this inside reproduction
logic, later versions may benefit from separating:

- copied capsule data
- developmental interpretation
- phenotype construction

Suggested event types:

- `description_copied`
- `interpreter_applied`
- `construction_failure`
- `semantic_shift_event`

## 4. Archive semantics may eventually need to become local, not universal

Today it is tempting to assume:

```text
capsule type A means the same thing for everyone
```

But the semantic-closure literature suggests a richer horizon:

```text
the effect of inherited structure may depend on lineage-specific interpretation
```

This is not required for version one.
But it is important as a roadmap constraint.

## 5. We should mark the current project depth honestly

This literature also helps with humility.

`alife_biosphere` should probably begin at:

```text
fixed substrate
+ fixed interpreter
+ evolvable inherited content
```

That is already useful.

But it is not yet:

```text
semantic closure in the strong artificial-chemistry sense
```

That distinction is worth documenting so later claims stay honest.

## Proposed Additions To The Existing Design

### New conceptual fields

- `interpreter_id`
- `interpreter_mutability`
- `constructor_budget`
- `capsule_interpreter_binding`
- `semantic_shift_score`

### New event types

- `description_copied`
- `interpreter_applied`
- `construction_failure`
- `semantic_shift_event`

### New metrics

- interpreter diversity
- semantic locality
- construction success rate
- inherited-content vs inherited-interpreter contribution

## Proposed Probe Design

The first substrate-oriented probe does not need chemistry.

A reasonable first probe is:

```text
same inherited capsule set
-> compare globally fixed interpretation vs lineage-local interpretation
-> measure adaptation, divergence, and failure rate
```

The first useful question is:

```text
Does allowing limited interpreter variation increase evolvability
without destroying coherence?
```

That would be enough to test whether this deeper direction is worth pursuing.

## Build Recommendations

This literature review suggests three near-term design tasks.

### 1. Add an explicit "fixed vs evolvable" section to the core design

Reason:

- otherwise substrate assumptions will remain hidden and hard to revisit

### 2. Keep capsule semantics simple now, but document them as provisional

Reason:

- we should not accidentally mistake version-one fixed meanings for the final
  artificial-life architecture

### 3. Reserve space for later interpreter evolution

Reason:

- this is one of the clearest long-run directions if the project wants to move
  beyond externally authored inheritance semantics

## Bottom Line

The substrate and semantic-closure literature tells us that a serious
artificial-life system must eventually confront a deep question:

```text
who decides what inherited structure means?
```

If the answer is always:

```text
the simulator, from outside the world
```

then the system may remain useful, but it stays shallower.

If more of that answer moves inside the evolving world,
the project gets closer to genuinely life-like heredity.

That is the main lesson this literature adds to `alife_biosphere`.

## Sources

- von Neumann, J. (1966).
  "Theory of Self-Reproducing Automata."
  [Open Library](https://openlibrary.org/books/OL23820816M/Theory_of_self-reproducing_automata)
  and [University of Michigan archive](https://hdl.handle.net/2027.42/3954)
- Hickinbotham, S. J. et al. (2016).
  "Maximizing the Adjacent Possible in Automata Chemistries."
  [PubMed](https://pubmed.ncbi.nlm.nih.gov/26649811/)
- Clark, E. B., Hickinbotham, S. J., Stepney, S. (2017).
  "Semantic closure demonstrated by the evolution of a universal constructor
  architecture in an artificial chemistry."
  [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC5454285/)
- Pattee, H. H. (2001).
  "Evolving Self-Reference: Matter, Symbols, And Semantic Closure."
  [ResearchGate metadata](https://www.researchgate.net/publication/2515094_Evolving_Self-Reference_Matter_Symbols_And_Semantic_Closure)
- Rocha, L. M. (2001).
  "Evolution with material symbol systems."
  [ScienceDirect abstract page](https://www.sciencedirect.com/science/article/abs/pii/S0303264701001101)
