# Ant Sandbox M0 Substrate Spec v1

## Purpose

This document freezes the first implementation target for the ant-sandbox
branch.

The question is:

```text
Can we stand up a deterministic local-space world with nest, food,
and visible ants before adding any higher-order behavior?
```

## Scope

In scope:

- fixed-size local grid
- empty / obstacle / nest / food cell types
- ant spawn at nest
- deterministic initialization
- one tick shell that can later host local decisions

Out of scope:

- pheromone logic
- food return logic
- reproduction
- mutation
- colony roles
- disturbance

## Required Data Structures

### World

```text
AntSandboxWorld =
  width
  height
  nest
  food_patches
  ants
  occupied_cells
  tick
```

### Nest

```text
Nest =
  x
  y
  radius
  stored_food
```

### FoodPatch

```text
FoodPatch =
  patch_id
  x
  y
  radius
  amount
```

### Ant

```text
Ant =
  ant_id
  x
  y
  heading
  carrying_food
  age
  alive
  parent_id
  lineage_id
```

## Default World

Suggested default:

- width: `64`
- height: `48`
- one nest near center-left
- two or three food patches at medium and long range
- `32` ants

This is big enough to watch spatial structure but still small enough to debug.

## Exit Condition

M0 is done when:

- the world initializes deterministically under seed
- ants occupy valid local cells
- food patches occupy valid local cells
- the observer can render the local world layout

Nothing more is required for M0.
