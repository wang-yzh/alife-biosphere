# Ant Sandbox Build Plan v1

## Purpose

This is the milestone plan for the ant-sandbox branch.

The goal is not to migrate every old ecology-graph mechanism into the new
branch immediately.
The goal is to build the correct world type first.

## M0. Local substrate scaffold

Scope:

- local grid world
- nest placement
- food patch placement
- ant population initialization
- deterministic stepping shell

Required result:

- a deterministic local-space world exists and can be rendered

## M1. Foraging loop

Scope:

- random exploration
- local food pickup
- return to nest
- unload behavior
- basic food accounting

Required result:

- stable `find -> carry -> return -> unload` loops

## M2. Trace field

Scope:

- trail deposition
- trail decay
- trail following
- pheromone-on / pheromone-off comparison

Required result:

- measurable improvement when traces are enabled

## M3. Colony persistence

Scope:

- bounded births / deaths or bounded replenishment
- long-run population stability
- basic disturbance

Required result:

- the colony persists with fluctuations instead of trivial crash or explosion

## M4. Role differentiation

Scope:

- behavior logging by ant
- clustering or classification of role-like patterns
- repeated role emergence checks

Required result:

- at least two or three stable behavior clusters

## M5. Disturbance recovery

Scope:

- food source shift
- path breakage
- local mortality
- recovery measurement

Required result:

- the colony restores a large fraction of prior function after disruption

## M6. Later layers

Only after the above:

- lineage comparison
- adaptive comparison
- mutation / variation
- longer-term artificial-life questions

## Rule

If the branch cannot pass `M1`, `M2`, and `M3`, do not spend the main line on
inheritance, archive systems, or abstract ecology research.
