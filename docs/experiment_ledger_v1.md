# Experiment Ledger v1

## Purpose

This file is the first centralized experiment ledger for `alife_biosphere`.

It is intentionally modest.
The project has not yet run a real experiment suite.
Therefore this ledger records what actually exists now:

- one scaffold-level smoke run
- the question it addresses
- the files that capture its evidence
- the limits on what it allows us to claim

The point is not to look busier than we are.
The point is to give the project one honest place where runs are registered.

## Ledger

| ID | Kind | Status | Question | Configuration / Scope | Evidence files | Observed result | What it supports | What it does not support |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `EXP-000` | smoke baseline | completed | Can the M0 scaffold run deterministically, emit events, and write outputs? | default `SimulationConfig`, seed `7`, `20` ticks, `3` habitats, `8` founders | `outputs/smoke/config.json`, `outputs/smoke/events.json`, `outputs/smoke/summary.json`, `tests/test_simulation_smoke.py` | summary reports `ticks=20`, `alive=8`, `dead=0`, `events=127`; repeated runs under the same seed are checked for deterministic equality in tests | supports the claim that the executable scaffold runs, emits events, and is deterministic under the default smoke setting | does not support claims about lineage, inheritance, archive use, rescue, group organization, or open-ended dynamics |

## Current Scope Limitation

At the time of writing, the ledger contains only scaffold-level evidence.

That means the project currently has:

- a run registry
- but not yet an experimental program

The distinction matters.

