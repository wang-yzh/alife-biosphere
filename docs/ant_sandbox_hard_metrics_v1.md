# Ant Sandbox Hard Metrics v1

## Purpose

This document defines the hard gates for the project when the actual target is
an ant-sandbox world rather than an abstract ecology graph.

These gates are meant to prevent a common failure mode:

```text
the project looks increasingly sophisticated,
but it is becoming sophisticated in the wrong world type
```

If the goal is an ant sandbox, these gates matter more than the old
mechanism-first roadmap.

## Main Rule

Do not spend the main line on inheritance, archive systems, trust, or other
higher-order mechanism layers until the sandbox passes the first three hard
metrics below.

## Primary Hard Metrics

| ID | Metric | What it measures | Pass condition |
| --- | --- | --- | --- |
| `M1` | spatial realism | whether the world is actually a sandbox rather than a node graph | organisms act in real 2D space or a fine local grid; decisions are based on local sensing only; dependence on global habitat scoring is zero |
| `M2` | foraging loop | whether the colony is performing a real colony task rather than wandering | stable `find food -> carry -> return to nest -> unload` loops appear repeatedly with net food recovery |
| `M3` | pheromone effectiveness | whether coordination emerges through environmental traces | enabling pheromone trails measurably improves foraging or homing efficiency over a no-pheromone control |
| `M4` | colony persistence | whether the colony can remain alive as a bounded living system | births, deaths, and replacement all occur over long runs; the colony neither crashes immediately nor explodes without bound |
| `M5` | role differentiation | whether colony-level internal specialization appears | without hard-coded roles, behavior traces separate into at least two or three stable clusters such as scout/forager/nurse-like patterns |
| `M6` | disturbance recovery | whether the colony remains functionally alive after disruption | after food shifts, path breakage, or local losses, the colony recovers a large fraction of prior function, such as `>=70%` of food return rate |

## Secondary Metrics

These matter after the primary sandbox identity is already real.

| ID | Metric | What it measures | Pass condition |
| --- | --- | --- | --- |
| `S1` | lineage traceability | whether later artificial-life claims are even possible | every new individual has `parent_id`, `lineage_id`, and `birth_tick`; ancestry is reconstructable |
| `S2` | adaptive comparability | whether later evolutionary claims can be compared cleanly | across seeds, colony variants, or mutation settings, food efficiency, recovery speed, and role stability can be measured side by side |

## Priority Order

The correct order for an ant-sandbox project is:

1. `M1 spatial realism`
2. `M2 foraging loop`
3. `M3 pheromone effectiveness`
4. `M4 colony persistence`
5. `M5 role differentiation`
6. `M6 disturbance recovery`
7. `S1 lineage traceability`
8. `S2 adaptive comparability`

## Why This Order Exists

An ant sandbox is not just a system where agents live in a world and sometimes
reproduce.

It specifically needs:

- local space
- local interaction
- colony task structure
- environmental trace coordination
- visible collective behavior

If those are missing, the project may still be interesting, but it is not an
ant sandbox in the sense the user actually wants.

## Promotion Rule

Before claiming that the project has entered a real ant-sandbox phase, require:

- `M1` pass
- `M2` pass
- `M3` pass

Before claiming that the sandbox has become a living colony system, require:

- `M4` pass
- `M5` pass

Before claiming that the project has begun to support artificial-life or
evolutionary comparisons, require:

- `M6` pass
- `S1` pass
- `S2` pass

## What To De-Prioritize Until These Pass

Do not put the main line here yet:

- archive systems
- trust systems
- higher-level group governance
- compact inheritance research
- sophisticated cultural-transfer mechanisms

Those may be worthwhile later.
They are not the first proof that the sandbox world itself is correct.
