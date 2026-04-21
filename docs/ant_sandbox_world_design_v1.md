# Ant Sandbox World Design v1

## 1. Status

This document is the current design contract for the ant-sandbox branch.

It supersedes the ecology-graph world as the main branch goal.
The older ecology-graph line remains useful as a reference for disturbance,
reporting, and environment-history ideas.

## 2. Core Shift

The key shift is:

```text
The world is no longer a small habitat graph.
The world is now a local substrate with many visible agents.
```

## 3. Core Entities

```text
AntSandboxWorld
  -> Grid or Local 2D Space
  -> Nest
  -> FoodPatches
  -> Obstacles
  -> Ants
  -> TraceField
  -> EventLog
```

## 3.1 Space

The first substrate should use a fine local grid rather than a coarse graph.

Why:

- easy deterministic stepping
- easy local sensing
- easy local trace deposition
- easy rendering

This can later evolve toward more continuous motion if needed.

## 3.2 Nest

The nest must be a real region in space.

It needs at least:

- nest coordinates / region
- stored food count
- spawn location

The nest is not just metadata.
It is the colony anchor.

## 3.3 Food Patches

Food should exist as local patches with quantity.

Required first properties:

- position
- amount
- radius or local footprint

The first sandbox must support actual foraging loops, not abstract harvesting.

## 3.4 Ants

The ant should be a local-space agent with a small state:

```text
Ant =
  ant_id
  x
  y
  heading
  carrying_food
  energy
  age
  alive
  parent_id
  lineage_id
```

Possible later additions:

- role tendency
- internal memory
- pheromone sensitivity
- task persistence

## 3.5 Trace Field

The first trace field can be intentionally simple.

Minimum useful version:

- food-trail strength by cell
- home-trail strength by cell
- decay over time
- optional diffusion or blur

This is the smallest meaningful bridge to ant-like coordination.

## 4. Required Behaviors

The first meaningful sandbox should support:

- wandering / exploration
- food detection
- pick-up
- return-to-nest behavior
- unload at nest
- trace deposition

No sophisticated cognition is required at first.
The key is local causal behavior.

## 5. First Non-Goals

Not first:

- mutation-heavy evolution
- colony warfare
- multiple species
- rich reproduction rules
- realistic ant biology
- large neural controllers

## 6. The First Real Test

The first real test is not:

```text
Can this world produce elegant metrics?
```

It is:

```text
Can a human watch the sandbox and see ants find food, return home,
and begin to organize local traffic?
```

If that is not yet true, the branch is not ready for more abstract layers.
