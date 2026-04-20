# M1 Ecology And M2 Lineage Slice 2026-04-21

## Purpose

This short note records the first implementation slice after the ecology-first
realignment.

It is not a new design document.
It is a practical answer to:

```text
What was actually built, and how should someone inspect it?
```

## What Changed

The codebase moved from a minimal M0 scaffold toward:

- an M1 ecology kernel
- the first M2 reproduction and lineage slice

Implemented in this pass:

- 7-habitat graph-aware default world
- habitat families: nursery, refuge, frontier, wild
- occupancy pressure and depletion traces
- movement with cooldown, cost, and blocked-move events
- hazard damage and crowding damage
- life stages and explicit death reasons
- reproduction readiness events
- simple resource-driven repair
- minimal disturbance hook with deterministic scheduling
- offspring creation
- parent-child lineage links
- ecology probe script and derived summary output

## Main Files Touched

- `src/alife_biosphere/config.py`
- `src/alife_biosphere/habitat.py`
- `src/alife_biosphere/organism.py`
- `src/alife_biosphere/world.py`
- `src/alife_biosphere/simulation.py`
- `scripts/run_smoke.py`
- `scripts/run_ecology_probe.py`
- `tests/test_config.py`
- `tests/test_world_invariants.py`
- `tests/test_simulation_smoke.py`

## What To Inspect

### Fast verification

Run:

```text
/Users/qlqwpy/Documents/游乐园/.venv/bin/python -m pytest
```

Expected result at the time of writing:

```text
13 passed
```

### Default smoke run

Run:

```text
/Users/qlqwpy/Documents/游乐园/.venv/bin/python scripts/run_smoke.py
```

Current observed summary:

```text
{'ticks': 20, 'alive': 13, 'dead': 0, 'events': 737}
```

Outputs:

- `outputs/smoke/config.json`
- `outputs/smoke/summary.json`
- `outputs/smoke/events.json`

### Ecology probe

Run:

```text
/Users/qlqwpy/Documents/游乐园/.venv/bin/python scripts/run_ecology_probe.py
```

Current observed summary:

```text
{'ticks': 40, 'alive': 5, 'dead': 9, 'events': 1239}
```

Current derived summary:

```text
birth_events=4
death_events=9
disturbance_events=5
move_events=100
lineage_count=4
```

Outputs:

- `outputs/ecology_probe/config.json`
- `outputs/ecology_probe/summary.json`
- `outputs/ecology_probe/events.json`
- `outputs/ecology_probe/derived_summary.json`

## What This Means

The project is no longer only a static scaffold.

It now has early evidence of:

- uneven habitat use
- repeated movement
- birth and death
- disturbance under seed control
- parent-child lineage continuity
- partial persistence under a harsher probe

## What It Does Not Mean Yet

This does not yet demonstrate:

- sustained long-run coexistence
- robust recolonization after deep local collapse
- niche inference
- compact inheritance
- signaling
- archive systems
- antagonist ecology

Those remain future work.

## Immediate Next Step

The next practical target is:

- strengthen M2 lineage and turnover analysis
- make disturbance/recovery more interpretable
- push toward M3-style rescue and recolonization summaries
