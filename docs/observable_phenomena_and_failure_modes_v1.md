# Observable Phenomena And Failure Modes v1

## Purpose

This document answers a practical question:

```text
If the project is trying to build a real artificial ecosystem,
what should we expect to see when it starts working,
and what would count as obvious dead ends?
```

## 1. Target Phenomena

These are the first phenomena worth chasing.
They are ordered by importance.

## P1. Uneven habitat use

We should see:

- some habitats fill more than others
- some habitats act as refuges
- some habitats are risky but attractive
- movement patterns depend on ecological state

Why it matters:

- without this, the graph is decorative rather than causal

## P2. Birth, death, and turnover

We should see:

- organisms survive for different lengths of time
- deaths happen for understandable ecological reasons
- births replenish populations
- local populations change rather than remaining fixed founders forever

Why it matters:

- without turnover there is no ecology, only occupancy

## P3. Recolonization after local loss

We should see:

- some local collapses
- some failed recolonizations
- some successful recolonizations from connected habitats

Why it matters:

- this is the first visible sign that topology and disturbance are doing real
  work

## P4. Lineage branching and loss

We should see:

- some lineages spread
- some lineages go extinct
- some habitats become temporarily dominated by particular lineages

Why it matters:

- this is the bridge from ecology to evolution

## P5. Habitat history

We should see:

- prior heavy occupancy changes later conditions
- depletion and recovery are visible over time
- habitat outcomes depend partly on what happened there before

Why it matters:

- this turns the environment into part of the causal system

## P6. Partial coexistence

We should see:

- more than one viable local strategy or lineage at least some of the time
- not every run collapsing immediately to one immortal winner

Why it matters:

- coexistence is a better sign of ecological structure than raw diversity
  counts alone

## 2. What To Watch Directly

If someone watches a run and asks whether the ecology feels real yet, the
easiest visible cues are:

- crowding at some habitats and emptiness at others
- migrations after pressure rises
- refuges acting differently from frontier or wild regions
- births appearing in some places and not others
- local boom-bust cycles
- recolonization attempts after loss
- persistent traces of prior exploitation

## 3. Red Flags

These are dead-end patterns.

## R1. One strategy wins everywhere too early

Meaning:

- topology and habitat differences are too weak
- the world is collapsing to one generic optimum

## R2. Everything dies in almost every seed

Meaning:

- hazards and reproduction costs are badly balanced
- disturbance is functioning as punishment, not as ecological structure

## R3. Nothing really changes

Meaning:

- the world is numerically stable but dynamically dead
- populations only drift superficially

## R4. Interesting behavior exists only after adding advanced mechanisms

Meaning:

- the base ecology is too thin
- we are compensating with mechanism complexity instead of world structure

## R5. Metrics look rich but runs look empty

Meaning:

- instrumentation is outrunning actual ecological content
- we are narrating complexity that is not really there

## R6. Habitat history does not matter

Meaning:

- habitats are still backgrounds, not ecological memory carriers

## 4. Promotion Rule For New Mechanisms

Do not prioritize signaling, archive systems, or compact inheritance until the
world can already produce at least these three convincingly:

1. uneven habitat use
2. birth/death/turnover
3. recolonization or lineage branching

Those are the minimum signs that the world is worth enriching rather than just
repairing.

## 5. First Practical Goal

The first convincing version of the project does not need culture, trust, or
parasites.

It needs a run where a human observer can say:

```text
These populations are living in different places under different pressures,
some are dying, some are reproducing, some places recover, and the world has
started to remember what happened.
```

That is the first real milestone.
