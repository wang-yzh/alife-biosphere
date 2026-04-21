# Experiment Ledger v1

## Purpose

This file is the centralized experiment ledger for `alife_biosphere`.

The project still does not have a broad experiment suite, but it now has more
than a single scaffold run.

This ledger records what actually exists now:

- one default ecology smoke run
- one harsher ecology probe with disturbance
- the question each run addresses
- the files that capture their evidence
- the limits on what each run allows us to claim

The point is not to look busier than we are.
The point is to give the project one honest place where runs are registered.

## Ledger

| ID | Kind | Status | Question | Configuration / Scope | Evidence files | Observed result | What it supports | What it does not support |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `EXP-000` | default ecology smoke | completed | Can the current ecology kernel run deterministically and produce movement, turnover precursors, and structured outputs under the default seed? | default `SimulationConfig`, seed `7`, `20` ticks, `7` habitats, `8` founders | `outputs/smoke/config.json`, `outputs/smoke/events.json`, `outputs/smoke/summary.json`, `tests/test_simulation_smoke.py` | summary reports `ticks=20`, `alive=13`, `dead=0`, `events=737`; repeated runs under the same seed are checked for deterministic equality in tests | supports the claim that the ecology kernel runs deterministically and emits richer ecological events under the default setting | does not support strong claims about sustained coexistence, robust recovery, or long-run ecological memory |
| `EXP-001` | ecology probe | completed | Can the harsher probe produce births, deaths, disturbances, and simple recovery summaries without total immediate collapse? | `ticks=40`, `founder_count=10`, `disturbance_interval=8`, `disturbance_resource_shock=2.0`, `disturbance_hazard_pulse=0.12`, `senescence_age=24`, `max_age=50` | `outputs/ecology_probe/config.json`, `outputs/ecology_probe/events.json`, `outputs/ecology_probe/summary.json`, `outputs/ecology_probe/derived_summary.json`, `outputs/ecology_probe/disturbance_recovery_summary.json`, `scripts/run_ecology_probe.py`, `tests/test_reporting.py` | summary reports `ticks=40`, `alive=5`, `dead=9`, `events=1239`; derived outputs report `birth_events=4`, `death_events=9`, `disturbance_events=5`, `move_events=100`, `successful_recovery_count=2`, `delayed_recovery_count=1`, `lineage_count=4` | supports the claim that the current world can produce disturbance, local collapse, recolonization, and simple recovery classifications in a deterministic small-world probe | does not yet support claims about robust rescue, stable coexistence, or strong ecological persistence across many seeds |

## Current Scope Limitation

At the time of writing, the ledger contains only small-world ecology evidence.

That means the project currently has:

- a real run registry
- but not yet a broad experimental program

The distinction matters.
