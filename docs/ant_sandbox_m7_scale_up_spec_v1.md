# Ant Sandbox M7 Scale-Up Spec v1

## Purpose

This is the next implementation freeze for the ant-sandbox branch.

It defines what must be true before new scale-up development starts.

## Scope

This phase must deliver:

- larger default showcase map
- terrain layer
- persistent food-source semantics
- richer world-first observer

This phase must not deliver:

- nest interior simulation
- culture
- archive-like systems
- explicit caste scripting

## Frozen Decisions

### 1. Default Showcase Size

The next default showcase should move from:

```text
64 x 48
```

to:

```text
128 x 96
```

This should become the main observer world unless performance proves clearly
too poor.

### 2. Nest Representation

The nest remains an entrance region only.

It must support:

- spawn
- unload
- feeding
- visual identity

It must not yet support:

- tunnels
- chambers
- internal worker routing

### 3. Terrain Families

The first scale-up terrain system should support exactly these families:

- `open_ground`
- `dense_grass`
- `sand`
- `rock`

Expected first semantics:

- `open_ground`: baseline
- `dense_grass`: slower, softer visibility
- `sand`: slower but trail-friendly
- `rock`: blocked path or strong barrier

### 4. Food Source Contract

Each food source should expose:

- total remaining amount
- active / depleted state
- visible footprint
- persistent `source_id`

Required rule:

```text
remaining_amount > 0  => source still exists
remaining_amount == 0 => source is depleted
```

Only after depletion may a turnover rule create a new source.

### 5. Observer Contract

The next observer must clearly show:

- larger map extent
- terrain regions
- nest entrance
- food-source bodies
- ant glyphs
- carrying state
- trace flow

Metrics remain secondary.

## Acceptance Signals

The phase is acceptable when all of the following are visibly true:

1. The map feels materially larger than the current showcase.
2. Terrain changes where ants move.
3. At least one route detour is visible because of terrain.
4. Food sources remain visible while they still have non-zero total amount.
5. The observer feels richer and more alive, not just zoomed out.

## First Development Order

Build in this order:

1. map-size uplift
2. terrain data model
3. terrain-aware movement and trace behavior
4. persistent food-source lifecycle
5. observer rendering upgrade
6. larger-map validation and replay pass
