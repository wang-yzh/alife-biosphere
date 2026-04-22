# Ant Sandbox Long-Horizon Construction Route v1

## Purpose

This document turns the user-facing long-horizon vision into a practical build
route for the ant-sandbox branch.

It does not replace the current scale-up plan.
It answers a different question:

```text
After the larger terrain-aware sandbox is stable,
what should be built next, and in what order?
```

## Core Rule

The branch is still building instinctive colony life.

Not a target:

- culture
- archive systems
- abstract society mechanics

Current long-horizon target:

- food competition
- multi-colony conflict
- stronger death consequences
- heritable variation
- longer-run adaptive divergence

## Ordering Principle

These future features are not independent.

They should be built in dependency order:

1. competition
2. conflict
3. stronger death ecology
4. inheritance and mutation
5. evolutionary comparison

If we reverse the order, later systems become decorative rather than causal.

## Phase R1. Resource Competition

Goal:

- make food pressure genuinely competitive

Minimum requirements:

- multiple food sources with meaningful scarcity
- overlapping foraging territories
- measurable source depletion and contest timing
- colony-level difference in food access

Why this comes first:

- war without competition is theatre
- mutation without pressure is drift without meaning

Success signal:

- two groups can visibly interfere with each other’s access to food

## Phase R2. Multi-Nest World

Goal:

- move from one colony to multiple colonies in the same outdoor map

Minimum requirements:

- multiple nest entrances
- colony identity per ant
- separate food ledgers by colony
- colony-specific trails or at least colony-specific routing data

Why this comes second:

- “tribal war” only makes sense once there are real colonies
- competition must become spatially and organizationally legible

Success signal:

- a human can watch the map and tell which ants belong to which colony

## Phase R3. Conflict Layer

Goal:

- introduce direct antagonism between colonies

Minimum first conflict mechanics:

- contested overlap zones
- collision / blocking / repulsion
- simple combat or damage exchange
- retreat, loss, and territorial consequence

Important constraint:

```text
Do not begin with elaborate combat classes.
Start with small, readable conflict mechanics.
```

Success signal:

- the map can show local territory tension and visible colony losses

## Phase R4. Stronger Death Ecology

Goal:

- make death more than a counter increment

Possible first upgrades:

- explicit death causes in the surface world
- bodies or corpse traces for a short time
- zone danger memory after conflict
- local loss of route continuity after deaths

Why this sits after conflict:

- stronger death becomes much more meaningful once loss comes from competition,
  starvation, and combat rather than only age or disturbance

Success signal:

- a human can watch deaths alter route structure or territorial use

## Phase R5. Heritable Variation

Goal:

- make some instinctive differences transmissible and mutable

First inheritance target:

- inherit weak tendency parameters such as:
  - range bias
  - trail affinity
  - harvest drive
- allow bounded mutation
- compare colony outcomes under different inherited mixes

Important constraint:

```text
Do not jump straight to heavy genomes.
Start by inheriting the instinct parameters the sandbox already uses.
```

Success signal:

- different lineages or colonies show reproducible behavioral differences over generations

## Phase R6. Evolutionary Runs

Goal:

- move from “interesting colony sandbox” to “adaptive ant life experiment”

Required prerequisites:

- competition exists
- conflict exists
- death has consequence
- inheritance exists

Only then should we ask:

- which instincts win under which terrain
- which colonies stabilize or collapse
- whether food strategy and territorial strategy diverge over long runs

Success signal:

- runs produce persistent colony differences that can be compared rather than merely watched

## Concrete Route Summary

The intended route is:

```text
larger terrain world
-> food competition
-> multi-nest coexistence
-> conflict
-> stronger death consequences
-> inherited instinct variation
-> long-run evolution
```

## What To Avoid

Avoid these dead ends:

- war before multiple colonies exist
- mutation before traits matter
- heavy genomes before inherited instincts are proven useful
- ornate faction lore before food pressure and conflict are observable

## Current Working Interpretation

The branch is not heading toward a vague “ant civilization sim”.

It is heading toward:

```text
an instinct-first evolving ant world,
where competition, conflict, death, and inherited behavioral differences
emerge from a readable surface ecology.
```
