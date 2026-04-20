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

The repository now has an initial M0 scaffold.

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
src/alife_biosphere/io.py
scripts/run_smoke.py
tests/
```

## What The M0 Scaffold Already Does

The current scaffold is intentionally small.

It can already:

- define typed simulation and world config
- create a deterministic small world
- create founder organisms
- update habitats with bounded regeneration
- apply simple organism metabolism
- perform simple harvesting
- emit append-only events
- run a smoke simulation
- write config, summary, and event outputs to disk
- run basic tests

This means the repo now has a real executable kernel instead of only design
documents.

## What The M0 Scaffold Does Not Do Yet

The current scaffold does not yet implement the actual research mechanisms.

Still missing:

- habitat graph edges and migration
- reproduction
- lineage graph
- mutation
- life stages
- protocol discovery
- somatic learning
- inheritance packets
- cultural archive
- species or niche inference
- coevolving habitats

This is expected.
The current code should be treated as foundation, not as a scientific result.

## Verified Current Status

Current local verification:

```text
/Users/qlqwpy/Documents/游乐园/.venv/bin/python -m pytest
```

Result at the time of writing:

```text
7 passed
```

Smoke script:

```text
/Users/qlqwpy/Documents/游乐园/.venv/bin/python scripts/run_smoke.py
```

Observed summary:

```text
{'ticks': 20, 'alive': 8, 'dead': 0, 'events': 127}
```

This verifies that:

- the package layout works
- the basic simulation loop runs
- tests import correctly under the shared environment

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

The next work should be narrow and disciplined.

### Step 1. Build the ecology kernel

Add:

- habitat graph connectivity
- occupancy pressure
- bounded movement between habitats
- habitat-level stress effects

Exit condition:

```text
organisms can distribute unevenly across habitats
without numerical instability
```

### Step 2. Add reproduction and lineage

Add:

- offspring creation
- parent-child recording
- lineage tracking
- founder and bottleneck summaries

Exit condition:

```text
birth and death produce real turnover instead of fixed founders
```

### Step 3. Add disturbance and recovery

Add:

- local crashes
- regional stress
- recolonization windows
- recovery summaries

Exit condition:

```text
some runs can lose local populations and recover without hidden resets
```

Only after these three steps should we move on to:

- habitat memory
- longer-run niche diagnostics
- optional higher-order mechanisms such as inheritance, signaling, or archive

That ordering matters because otherwise we would build memory systems before
the world has a stable life cycle to attach them to.

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
The project now has a clean design base and a minimal executable scaffold. It
does not yet have a sustained ecology, but it now has enough structure to
start building one in a controlled way.
```
