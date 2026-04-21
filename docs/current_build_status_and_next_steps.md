# Current Build Status And Next Steps

## Purpose

This document is the current working summary for `alife_biosphere`.

It is meant to answer three practical questions:

1. What is this project trying to become?
2. What has already been built?
3. What should be built next, in order?

This is not the full theory note and not the full design spec.
It is the shortest document that should let a collaborator re-enter the
project without guessing.

## Project Position

`alife_biosphere` is the new main research line.

It starts after archiving:

- `maze_novelty`
- `market_novelty`

The project goal is:

```text
build a persistent artificial-life biosphere
where populations compete, reproduce, disperse, die, recover,
and reshape habitats over long runs
```

This project is not trying to become:

- another benchmark optimizer
- another one-agent maze solver
- another transfer-only pipeline

## Current Direction

As of 2026-04-21, the controlling direction is now ecology-first.

That means the project must first prove:

- persistent ecological structure
- turnover and recolonization
- lineage and habitat history
- disturbance and recovery

before treating inheritance, signaling, trust, or archive systems as
main-line requirements.

## Core Documents

The `docs/` directory is now a large library built across multiple passes.

That is too much for a handoff path, so the active re-entry set is now:

1. `docs/README.md`
2. `../README.md`
3. `docs/current_build_status_and_next_steps.md`
4. `docs/ecology_north_star_v1.md`
5. `docs/world_design_v2.md`
6. `docs/observable_phenomena_and_failure_modes_v1.md`
7. `docs/build_plan_v2.md`
8. `docs/m1_ecology_kernel_spec_v2.md`
9. `docs/document_catalog_v1.md`
10. `docs/claim_to_evidence_table_v1.md`
11. `docs/experiment_ledger_v1.md`
12. `docs/negative_results_ledger_v1.md`
13. `docs/ablation_history_v1.md`

Everything else in `docs/` should be treated as background support rather than
first-pass entry material.

These active documents play different roles:

- `docs/README.md`: entry map for current, supporting, and historical docs
- `../README.md`: high-level project intent
- `current_build_status_and_next_steps.md`: shortest working summary for
  re-entry without full-library reading
- `ecology_north_star_v1.md`: current project destination in one page
- `world_design_v2.md`: current ecology-first world design
- `observable_phenomena_and_failure_modes_v1.md`: what we actually want to see
  in runs and what counts as dead ends
- `build_plan_v2.md`: current ecology-first milestone order
- `m1_ecology_kernel_spec_v2.md`: current first implementation spec
- `document_catalog_v1.md`: full library catalog when the short entry path is
  not enough
- `claim_to_evidence_table_v1.md`: mapping from current claims to what is
  supported, partially supported, or unsupported
- `experiment_ledger_v1.md`: centralized register of actual runs that have
  been executed so far
- `negative_results_ledger_v1.md`: current limitation and non-result record
- `ablation_history_v1.md`: current history of planned and completed
  ablations, preventing proposed controls from disappearing

Background support remains available in the rest of `docs/` for deeper topic
dives and citation backup.

## What Exists Right Now

The repository now has:

- an M1 ecology kernel
- a first M2 reproduction and lineage slice
- a first M3 disturbance / recovery summary slice

Current implemented files:

```text
pyproject.toml
src/alife_biosphere/__init__.py
src/alife_biosphere/config.py
src/alife_biosphere/rng.py
src/alife_biosphere/habitat.py
src/alife_biosphere/organism.py
src/alife_biosphere/events.py
src/alife_biosphere/world.py
src/alife_biosphere/simulation.py
src/alife_biosphere/reporting.py
src/alife_biosphere/io.py
scripts/run_smoke.py
scripts/run_ecology_probe.py
tests/
```

## What The Current Kernel Already Does

The current implementation is still small, but it is no longer only a bare
scaffold.

It can already:

- define typed simulation and world config
- create a deterministic 7-habitat graph world
- create founder organisms and offspring
- update habitats with bounded regeneration and climate noise
- compute occupancy pressure and depletion traces
- apply movement costs, hazard damage, and crowding damage
- record life stages, reproduction readiness, births, and deaths
- apply deterministic disturbance hooks
- derive disturbance / collapse / recolonization summaries
- emit append-only events
- run a smoke simulation
- run an ecology probe
- write config, summary, and event outputs to disk
- run basic tests

This means the repo now has a real executable ecology kernel instead of only
design documents.

## What The Current Code Still Does Not Do Yet

The current code still does not yet implement several later-stage mechanisms or
prove the stronger ecosystem claims.

Still missing:

- mutation
- robust rescue after deeper local collapse
- stable long-run coexistence
- niche or species inference
- habitat-driven diversification over long horizons
- protocol discovery
- somatic learning
- inheritance packets
- cultural archive
- antagonists
- richer group structure
- coevolving habitats in the strong sense

This is expected.
The current code should be treated as a growing experimental world, not as a
finished ecological result.

## Verified Current Status

Current local verification:

```text
/Users/qlqwpy/Documents/游乐园/.venv/bin/python -m pytest
```

Result at the time of writing:

```text
15 passed
```

Smoke script:

```text
/Users/qlqwpy/Documents/游乐园/.venv/bin/python scripts/run_smoke.py
```

Observed summary:

```text
{'ticks': 20, 'alive': 13, 'dead': 0, 'events': 737}
```

This verifies that:

- the package layout works
- the ecology kernel runs deterministically
- tests import correctly under the shared environment

Ecology probe:

```text
/Users/qlqwpy/Documents/游乐园/.venv/bin/python scripts/run_ecology_probe.py
```

Observed summary:

```text
{'ticks': 40, 'alive': 5, 'dead': 9, 'events': 1239}
```

Observed derived highlights:

```text
birth_events=4
death_events=9
disturbance_events=5
move_events=100
successful_recovery_count=2
delayed_recovery_count=1
lineage_count=4
```

## Current Module Intent

### `config.py`

Owns typed configuration objects and validation.

### `rng.py`

Owns deterministic seed derivation.

### `habitat.py`

Owns local habitat state and bounded regeneration.

### `organism.py`

Owns organism resource state, aging, metabolism, and simple harvesting effects.

### `events.py`

Owns append-only typed event records.

### `world.py`

Owns top-level state: habitats, organisms, tick count, and event storage.

### `simulation.py`

Owns deterministic stepping and run summary logic.

### `reporting.py`

Owns derived disturbance / collapse / recolonization summaries.

### `io.py`

Owns config, summary, and event serialization.

## What Is Missing In The Documentation Set

The project now has:

- research framing
- world design
- milestone plan
- repository architecture
- executable M0 scaffold

The current first implementation spec is now:

```text
docs/m1_ecology_kernel_spec_v2.md
```

That document freezes:

- habitat graph structure
- movement and migration rules
- carrying-capacity pressure mechanics
- death causes
- reproduction readiness interface
- the first event schema expansion

## Recommended Next Build Order

The next work should stay narrow and disciplined.

### Step 1. Strengthen M3 recovery interpretation

Add:

- clearer rescue and failure summaries
- habitat-specific recovery lag reporting
- lineage-sensitive recolonization summaries

Exit condition:

```text
disturbance outcomes can be explained without reading raw events by hand
```

### Step 2. Build habitat history into real ecological memory

Add:

- occupancy-dependent habitat modification
- recovery lag accumulation
- stronger link between prior depletion and later viability

Exit condition:

```text
later habitat outcomes depend materially on what happened there before
```

### Step 3. Push longer-run ecology probes

Add:

- longer runs
- coexistence summaries
- lineage spread and local dominance summaries

Exit condition:

```text
the world can show partial persistence and differentiation without immediately
collapsing to one generic state
```

Only after those steps should the main line move hard on:

- compact inheritance
- signaling
- archive systems
- other optional higher-order mechanisms

## Current Engineering Rule

For the next few iterations, every new mechanism should come with:

- a test
- a smoke or probe path
- an event record
- one short note saying what changed and how to inspect it

Without that discipline, the project will become concept-heavy again before the
ecology is trustworthy.

## Short Team Summary

If someone asks what state the project is in right now, the honest short answer
is:

```text
The project now has a clean design base and an executable ecology kernel with
early reproduction, lineage continuity, disturbance hooks, and recovery
summaries. It does not yet have a robust long-run ecosystem, but it now has
enough structure to study how one might form.
```
