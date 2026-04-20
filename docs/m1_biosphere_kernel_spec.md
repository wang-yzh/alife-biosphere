# M1 Biosphere Kernel Spec

## Status Note

This is the predecessor M1 spec from the earlier mechanism-heavy planning line.

It remains useful as a reference, but `m1_ecology_kernel_spec_v2.md` is now the
current M1 implementation spec under the ecology-first plan.

## 1. Purpose

`world_design_v1.md` is the current scientific design.
`build_plan_v1.md` is the current milestone order.

This document freezes the first mechanism-heavy implementation target:

```text
M1 = graph-aware biosphere kernel
```

The M0 scaffold proved that we can run a deterministic bounded world.
M1 must prove that the world has enough ecological structure for later lineage,
inheritance, and archive mechanisms to mean something.

## 2. What M1 Must Add

Compared with M0, M1 must add:

1. explicit habitat graph connectivity
2. movement and migration friction
3. carrying-capacity pressure
4. refuge-aware habitat roles
5. disturbance scheduling hooks
6. explicit death reasons
7. reproduction readiness state
8. richer event logging for ecological interpretation

If we do not freeze these now, later inheritance work will attach to a world
that is still too thin to support real ecological history.

## 3. Scope Boundary

### In scope

- habitat graph
- movement and migration
- occupancy pressure
- refuge/frontier differentiation
- bounded local disturbance hooks
- death cause classification
- reproduction readiness interface
- M1 event schema
- M1 tests and one kernel probe

### Explicitly out of scope

- actual offspring creation
- mutation
- lineage graph implementation
- archive access
- protocol learning
- signaling
- parasites
- trust
- group-level organization

Those all depend on a trustworthy kernel.

## 4. Default Topology

M1 should use **7 habitats** by default.

Recommended IDs:

```text
nursery_a
nursery_b
refuge
frontier_a
frontier_b
wild_a
wild_b
```

Recommended undirected edges:

```text
nursery_a  <-> refuge
nursery_b  <-> refuge
refuge     <-> frontier_a
refuge     <-> frontier_b
frontier_a <-> wild_a
frontier_b <-> wild_b
frontier_a <-> frontier_b
```

This graph is small enough to debug but large enough to produce:

- unequal occupancy
- corridor dependence
- refuge concentration
- frontier filtering
- wild recolonization paths

## 5. Habitat Roles

Every habitat must have a `habitat_family`.

Allowed M1 families:

```text
nursery
refuge
frontier
wild
```

Intended behavior:

- `nursery`: low hazard, lower upside, developmental bias
- `refuge`: low hazard, lower resources, long-term survival anchor
- `frontier`: medium hazard, medium resources, corridor role
- `wild`: high hazard, potentially high upside, specialization pressure

The main reason to freeze these now is that later archive and inheritance
metrics will need habitat-family context.

## 6. Required Config Additions

### 6.1 `HabitatConfig`

Add:

```text
habitat_family: str
max_resource_level: float
climate_drift: float
climate_push: float
refuge_score: float
```

Rules:

- `max_resource_level > 0`
- `climate_drift >= 0`
- `climate_push` stays small enough to keep climate bounded
- `refuge_score` in `[0, 1]`

### 6.2 `WorldConfig`

Add:

```text
habitat_edges: tuple[tuple[str, str], ...]
movement_cost: float
migration_integrity_risk: float
occupancy_stress_scale: float
crowding_energy_penalty: float
senescence_age: int
max_age: int
reproduction_energy_threshold: float
reproduction_matter_threshold: float
reproduction_integrity_threshold: float
disturbance_seed_offset: int
```

### 6.3 `OrganismConfig`

Add:

```text
hazard_damage_scale: float
crowding_integrity_penalty: float
movement_cooldown_ticks: int
```

## 7. State Model Additions

### 7.1 Habitat

Add fields:

```text
habitat_family: str
max_resource_level: float
neighbors: tuple[str, ...]
occupancy_pressure: float
recent_occupancy: float
refuge_score: float
```

### 7.2 Organism

Add fields:

```text
life_stage: str
reproduction_ready: bool
death_reason: str
last_habitat_id: str | None
movement_cooldown: int
```

Allowed `life_stage` values in M1:

```text
juvenile
mature
senescent
dead
```

M1 does not yet need full reproductive stages; readiness is enough.

## 8. Tick Order

Each M1 tick should run in this order:

1. habitat climate and regeneration update
2. occupancy pressure recomputation
3. organism metabolism and aging
4. movement decision and migration resolution
5. local harvesting
6. hazard and crowding damage
7. reproduction readiness update
8. death resolution
9. tick summary emission

This order makes migration depend on current ecological state while keeping the
loop simple enough to test.

## 9. Habitat Update Rules

### 9.1 Regeneration

For each habitat:

```text
resource_level =
  clamp(
    resource_level
    + regeneration_rate
    - occupancy_pressure * 0.25,
    0,
    max_resource_level,
  )
```

### 9.2 Climate

M1 climate should stay bounded and deterministic-under-seed:

```text
climate_state =
  clamp(
    climate_state + climate_push + bounded_noise(climate_drift),
    -1.0,
    1.0,
  )
```

### 9.3 Occupancy pressure

Compute:

```text
occupancy_ratio = occupant_count / capacity
occupancy_pressure = max(0, occupancy_ratio - 1.0)
```

And update:

```text
recent_occupancy = 0.8 * recent_occupancy + 0.2 * occupant_count
```

`recent_occupancy` is a bridge to later state-dependent habitat memory.

## 10. Movement And Migration

### 10.1 Allowed moves

An organism may:

- stay in place
- move to one connected neighbor

No multi-hop moves in a single tick.

### 10.2 M1 movement heuristic

Prefer movement when:

- current occupancy pressure is high
- current hazard is high
- a neighbor has lower pressure or better resources
- movement cooldown is zero

Prefer staying when:

- the organism is juvenile in a nursery
- current habitat is a refuge with low stress
- integrity is too low for a safe move

### 10.3 Movement cost

On successful move:

```text
energy -= movement_cost
integrity -= migration_integrity_risk * max(0, destination_hazard - source_hazard)
```

### 10.4 Cooldown

After moving:

```text
movement_cooldown = movement_cooldown_ticks
```

Cooldown decrements every tick.

This prevents meaningless oscillation between two habitats.

## 11. Harvesting

M1 harvesting should now depend on crowding.

Use:

```text
effective_harvest =
  min(
    harvest_gain * (1.0 - min(0.6, occupancy_pressure * 0.5)),
    resource_level,
  )
```

This gives overcrowding a real ecological effect before direct conflict exists.

## 12. Damage And Death

### 12.1 Hazard damage

After harvesting:

```text
integrity -= hazard_level * hazard_damage_scale
```

### 12.2 Crowding damage

If `occupancy_pressure > 0`:

```text
energy -= crowding_energy_penalty * occupancy_pressure
integrity -= crowding_integrity_penalty * occupancy_pressure
```

### 12.3 Senescence

If `age >= senescence_age`, apply a small per-tick integrity penalty.

If `age >= max_age`, death may occur with:

```text
death_reason = "senescence"
```

### 12.4 Death reasons

Allowed M1 values:

```text
starvation
hazard
crowding
senescence
movement_failure
integrity_collapse
```

The goal is clean observability, not perfect biological realism.

## 13. Reproduction Readiness

M1 does not yet create offspring.
It does need a state meaning:

```text
this organism would qualify to reproduce if reproduction were enabled
```

Set:

```text
reproduction_ready = (
  energy >= reproduction_energy_threshold
  and matter >= reproduction_matter_threshold
  and integrity >= reproduction_integrity_threshold
  and life_stage == "mature"
)
```

Emit:

- `reproduction_ready` when an organism first becomes ready
- `reproduction_unready` when it loses readiness

This makes later birth logic attach to an existing kernel signal.

## 14. Disturbance Hooks

M1 should not yet implement full disturbance ecology, but it should include
hooks for it.

Required structure:

```text
scheduled_disturbance: bool
disturbance_kind: str | None
disturbance_intensity: float
```

for habitats or a world-level disturbance queue.

Allowed M1 placeholder disturbance kinds:

```text
none
resource_shock
hazard_spike
```

M1 only needs deterministic scheduling and event emission, not rich rescue
analysis yet.

## 15. Event Schema Expansion

Keep the normalized event model, but standardize payloads.

### Required M1 event types

```text
birth
move
move_blocked
harvest
hazard_damage
crowding_damage
reproduction_ready
reproduction_unready
death
tick_summary
disturbance
```

### Payload expectations

#### `move`

```text
{
  "from_habitat": str,
  "to_habitat": str,
  "energy_cost": float,
  "integrity_cost": float
}
```

#### `move_blocked`

```text
{
  "from_habitat": str,
  "attempted_to": str,
  "reason": "cooldown" | "no_edge" | "dead" | "insufficient_energy"
}
```

#### `hazard_damage`

```text
{
  "amount": float,
  "hazard_level": float
}
```

#### `crowding_damage`

```text
{
  "amount_energy": float,
  "amount_integrity": float,
  "occupancy_pressure": float
}
```

#### `reproduction_ready`

```text
{
  "energy": float,
  "matter": float,
  "integrity": float
}
```

#### `death`

```text
{
  "reason": str,
  "age": int,
  "energy": float,
  "matter": float,
  "integrity": float
}
```

#### `disturbance`

```text
{
  "kind": str,
  "intensity": float
}
```

#### `tick_summary`

```text
{
  "alive": int,
  "dead": int,
  "ready_to_reproduce": int,
  "moved": int
}
```

## 16. M1 Invariants

M1 must preserve:

```text
0 <= resource_level <= max_resource_level
-1 <= climate_state <= 1
0 <= integrity <= 1
0 <= occupancy_pressure
dead organisms remain dead
organism habitat ids always exist
occupant sets match living occupants
graph edges only point to valid habitats
```

## 17. Required Tests

### `test_habitat_graph.py`

- all edges reference valid habitats
- default graph is symmetric

### `test_movement.py`

- moves only happen across edges
- cooldown blocks immediate repeated movement
- occupancy sets update after movement

### `test_carrying_capacity.py`

- pressure is zero below capacity
- pressure rises above capacity
- pressure affects organism state monotonically

### `test_death_reasons.py`

- starvation path yields `starvation`
- senescence path yields `senescence`
- hazard path yields `hazard`

### `test_reproduction_ready.py`

- organisms below thresholds are not ready
- crossing thresholds emits readiness event
- damage can remove readiness

### `test_m1_kernel_probe.py`

- default 7-habitat probe completes
- alive count remains bounded
- at least one habitat other than nurseries is occupied
- event log contains movement or readiness events

## 18. Required Probe

Add:

```text
scripts/run_m1_kernel_probe.py
```

Suggested defaults:

- 7 habitats
- 32 founders
- 60 ticks
- deterministic seed
- event logging enabled

Probe questions:

1. do organisms redistribute across the graph?
2. does refuge occupancy rise when frontiers are crowded?
3. do some organisms reach reproduction readiness?
4. do multiple death causes appear?

## 19. Module Worklist

### `config.py`

Add:

- habitat family
- max resource
- edges
- movement cost
- capacity stress
- senescence thresholds
- reproduction thresholds

### `habitat.py`

Add:

- family
- max resource
- neighbors
- occupancy pressure
- recent occupancy
- refuge score

### `organism.py`

Add:

- life stage
- readiness state
- death reason
- last habitat id
- movement cooldown

### `world.py`

Add:

- edge validation
- occupancy reconciliation helper
- movement application helper
- disturbance hook scaffolding

### `simulation.py`

Replace the current simple loop with the M1 phase order.

## 20. Guardrails

Do not add these during M1:

- mutation
- actual births
- archive access
- signaling
- parasites
- group logic

If they enter now, we will not know whether the kernel itself is stable.

## 21. Exit Condition

M1 is done when:

- the 7-habitat world runs deterministically under seed
- movement, crowding, death, and readiness are visible in logs
- default probe seeds show non-trivial occupancy differences
- no invariant tests fail
- the codebase can move into M2 without another world-state rewrite
