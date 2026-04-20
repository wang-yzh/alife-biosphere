# M1 Ecology Kernel Spec v2

## 1. Purpose

This document freezes the first implementation target under the ecology-first
plan.

References:

- `ecology_north_star_v1.md`
- `world_design_v2.md`
- `build_plan_v2.md`

The question for M1 is not:

```text
Can we already model advanced inheritance?
```

The question is:

```text
Can we produce a small, watchable world where topology, pressure, movement,
death, and habitat roles visibly matter?
```

## 2. What M1 Must Prove

M1 must prove that the world can produce ecological structure worth extending.

Minimum proof:

- habitats are not used evenly
- movement depends on local conditions
- crowding and hazard matter
- deaths have interpretable causes
- reproduction readiness varies by ecological conditions

## 3. Scope Boundary

### In scope

- explicit habitat graph connectivity
- movement and migration friction
- occupancy pressure
- habitat-family differences
- bounded climate and regeneration
- hazard and crowding damage
- life-stage records
- reproduction readiness state
- explicit death reasons
- M1 ecological probe and tests

### Explicitly out of scope

- offspring creation
- mutation
- compact inheritance
- signaling
- trust
- archive systems
- parasites
- first-class groups
- inferred species or niche labels

Those can wait until the ecological kernel earns them.

## 4. Default Small World

M1 should still use a small debug-friendly graph.

Recommended habitats:

```text
nursery_a
nursery_b
refuge
frontier_a
frontier_b
wild_a
wild_b
```

Recommended edges:

```text
nursery_a  <-> refuge
nursery_b  <-> refuge
refuge     <-> frontier_a
refuge     <-> frontier_b
frontier_a <-> wild_a
frontier_b <-> wild_b
frontier_a <-> frontier_b
```

This is large enough to show:

- refuge concentration
- frontier filtering
- wild pressure
- corridor dependence

## 5. Habitat Families

Allowed M1 families:

- `nursery`
- `refuge`
- `frontier`
- `wild`

Expected ecological roles:

- `nursery`: lower hazard, lower upside, safer early life
- `refuge`: lower hazard, lower productivity, long-term survival anchor
- `frontier`: transition zone with medium risk
- `wild`: higher risk with higher upside or lower crowding

## 6. Required State Additions

### Habitat

Add or maintain:

- `habitat_family`
- `neighbors`
- `max_resource_level`
- `occupancy_pressure`
- `recent_occupancy`
- `depletion_trace`
- `refuge_score`

### Organism

Add or maintain:

- `life_stage`
- `reproduction_ready`
- `death_reason`
- `last_habitat_id`
- `movement_cooldown`

Allowed M1 life stages:

- `juvenile`
- `mature`
- `senescent`
- `dead`

## 7. Tick Priorities

Each M1 tick should preserve this ecological order:

1. habitat regeneration and climate update
2. occupancy pressure recomputation
3. organism metabolism and aging
4. movement decision and migration resolution
5. local harvesting
6. hazard and crowding damage
7. reproduction readiness update
8. death resolution
9. tick summary emission

## 8. Required Event Families

M1 must log at least:

- `move`
- `move_blocked`
- `harvest`
- `hazard_damage`
- `crowding_damage`
- `reproduction_ready`
- `reproduction_unready`
- `death`
- `tick_summary`

The logs must make later ecological interpretation possible without guessing.

## 9. Required Probe Outputs

M1 should produce at least one probe summary containing:

- occupancy by habitat
- occupancy pressure by habitat
- movement count
- death reason counts
- reproduction-ready count
- refuge occupancy

These are the minimum indicators that the world is beginning to behave like an
ecology rather than a static board.

## 10. Exit Criteria

M1 is complete when the default probe can show all of the following:

- non-trivial occupancy differences across habitats
- at least one visible refuge-like usage pattern
- ecologically interpretable movement
- ecologically interpretable deaths
- reproduction readiness that differs across habitats or life situations

M1 is not complete just because the code runs.
It is complete when the world begins to look ecologically shaped.
