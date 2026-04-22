# Ant Sandbox World Design v2

## 1. Purpose

This document updates the ant-sandbox world design for the first major scale-up
phase.

The branch has already proven the small-map core:

- local space
- foraging loop
- pheromone usefulness
- bounded persistence
- role-like differentiation
- disturbance recovery

The next question is different:

```text
Can the sandbox become a larger, richer, more watchable surface world
without losing its ant-like causal clarity?
```

## 2. New Direction

The world is still an ant sandbox.

It is not becoming:

- a culture simulator
- a colony politics simulator
- a nest-interior management game

It is becoming:

- a larger outdoor surface world
- with more route choice
- with visible terrain pressure
- with more legible food logistics

## 3. World Layers

The next world should be read as layered space:

```text
SurfaceWorld
  -> Terrain Layer
  -> Nest Entrance Region
  -> Food Sources
  -> Ant Population
  -> Trace Fields
  -> Event Log
  -> Observer View
```

## 4. Space Scale

The small map proved the core loop.
The next phase should move to a clearly larger showcase scale.

Recommended next default:

```text
128 x 96
```

This is large enough to create:

- longer outward routes
- real scouting lanes
- terrain bottlenecks
- meaningful food-source separation

without immediately forcing a full engine rewrite.

Probe worlds may still use smaller layouts when needed.

## 5. Terrain System

The next surface world needs terrain, not just empty ground.

The first terrain system should stay simple and causal.

Minimum terrain families:

- `open_ground`
  baseline movement and baseline trail behavior
- `dense_grass`
  slower travel and weaker long-range readability
- `sand`
  slower travel but strong trail persistence
- `rock`
  impassable or near-impassable barrier cells

The terrain system exists to create:

- route choice
- local congestion
- detours
- place identity

It should not yet become a giant materials simulation.

## 6. Nest

The nest should remain visually important, but still simple.

For this phase the nest means:

- nest entrance region
- stored food
- spawn anchor
- return anchor

Explicit non-goal for this phase:

```text
Do not simulate nest interior chambers yet.
```

We want stronger outdoor colony behavior first.

## 7. Food Sources

Food sources should become proper surface objects with a persistent identity.

Each food source should have:

- `source_id`
- position
- footprint / radius
- `remaining_amount`
- `initial_amount`
- active / depleted state

Important rule:

```text
A food source exists as long as its remaining total amount is not zero.
```

That means the observer should not treat a source as gone just because local
pickup is happening around it.

Only when total remaining amount reaches zero should the source become
depleted.

Later turnover is still allowed, but only after true depletion.

## 8. Ant Presentation

The ants should remain simple agents internally, but become more expressive
visually.

Desired observer feel:

- each ant reads like a tiny creature, not just a neutral dot
- carrying ants are immediately obvious
- trails read like route memory, not just debug residue
- nest entrance is visually distinct

This phase should support:

- ant glyph or segmented-body rendering
- small carry marker
- better ant contrast against terrain
- clearer movement on larger maps

## 9. Observer Direction

The observer should now become a stronger “living world window”.

The main visual priority should be:

1. terrain
2. nest entrance
3. food-source bodies
4. ants
5. trail flow
6. only then metrics

The observer should help a human notice:

- where traffic lanes form
- where scouts go far and return rarely
- where terrain forces rerouting
- which food sources are fading or exhausted

## 10. First Non-Goals For This Phase

Still not now:

- nest interior architecture
- culture
- teaching or archive systems
- combat
- multi-colony diplomacy
- realistic larval biology

## 11. Success Standard

This phase succeeds if a human can watch the sandbox and feel:

- the map is bigger
- the ground is not uniform
- food sources are real places with depletion
- ants form longer and more varied routes
- the colony looks more alive, not just more decorated
