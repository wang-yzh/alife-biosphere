# Ecology North Star v1

## Purpose

This document states the current project north star in the simplest possible
form.

It exists because the library had grown rich enough that the project risked
confusing mechanism ambition with actual destination.

## The Project In One Sentence

`alife_biosphere` is trying to build a long-running artificial ecosystem that
remains interesting because organisms compete, reproduce, die, spread, recover,
and leave lasting traces in the habitats they occupy.

## What We Actually Want To See

The desired end state is not "a smart agent."
It is not "a large list of mechanisms."
It is a world where:

- local behavior is watchable rather than scripted
- different habitats push populations toward different outcomes
- lineages persist, split, disappear, and sometimes return
- disturbance causes real loss without forcing global reset
- habitats remember occupancy, depletion, and recovery history
- the system stays alive long enough for novelty to matter

## Success Hierarchy

The order matters.

### Level 1. Watchable sandbox

The world should already feel alive enough to watch:

- movement is uneven
- habitats are used differently
- deaths happen for understandable reasons
- refuge and frontier roles are visible

### Level 2. Real ecology

The world should produce ecological structure:

- local crowding and scarcity matter
- reproduction and turnover occur
- recolonization is possible but not guaranteed
- multiple local strategies can coexist for non-trivial periods

### Level 3. Sustained ecological history

The world should accumulate history rather than only noise:

- lineage branching becomes traceable
- disturbance and recovery leave measurable consequences
- habitat traces influence later population outcomes
- novelty and stability can coexist without hidden handholding

### Level 4. Optional higher-order mechanisms

Only after the earlier levels are real should we decide whether to add:

- compact inheritance
- signaling
- archive systems
- antagonists
- richer group structure

These are possible amplifiers, not the first proof of life.

## What This Project Is Not Optimizing For First

Not first:

- benchmark scores
- large learned controllers
- cultural archive complexity
- trust systems for their own sake
- pre-scripted social classes
- full biological realism

## The Core Research Question

The current main question is:

```text
What conditions let an artificial ecosystem remain alive, differentiated,
historical, and capable of further change?
```

Only after that question has a positive answer should the project push hard on:

```text
How does experience become inheritable structure?
```

That second question still matters.
It is no longer allowed to outrun the first one.

## Design Rule

When choosing between two next steps:

- prefer the one that makes the world more ecological
- defer the one that only makes the mechanism stack more elaborate

If a feature does not help the world stay alive, diversify, recover, or leave
history, it is not yet on the critical path.
