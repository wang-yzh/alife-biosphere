# M4 Habitat Memory Slice 2026-04-21

## Purpose

This note records the first M4-oriented implementation slice.

It answers:

```text
Has habitat history become a real part of the world dynamics yet,
or is it still only being recorded as metadata?
```

## Short Answer

Yes, in an initial bounded form.

Habitats now accumulate a small ecological memory signal and feed that signal
back into current hazard, regeneration, and recolonization difficulty.

## What Changed

Added in this pass:

- `memory_field` per habitat
- `recovery_lag` per habitat
- `empty_ticks` per habitat
- state-dependent hazard updates
- state-dependent regeneration updates
- recolonization pressure for empty habitats
- `recolonization` and `recolonization_failed` events
- memory and recovery fields in `tick_summary`
- `summarize_habitat_memory(...)` in `src/alife_biosphere/reporting.py`
- `outputs/ecology_probe/habitat_memory_summary.json`

## What The Mechanism Now Does

Each habitat now updates a bounded memory signal using:

- recent occupancy
- depletion trace
- disturbance trace
- time spent empty

That memory then affects:

- current `hazard_level`
- current `regeneration_rate`
- tracked `recovery_lag`
- recolonization success pressure for empty habitats

This means habitat history is no longer only a passive record.
It now changes current ecological conditions.

## What To Run

```text
/Users/qlqwpy/Documents/游乐园/.venv/bin/python -m pytest
/Users/qlqwpy/Documents/游乐园/.venv/bin/python scripts/run_ecology_probe.py
```

## Current Observed Signs

At the time of writing, the ecology probe shows non-zero habitat memory and
non-zero recovery lag.

Examples from the current probe:

- `frontier_a` reaches `max_recovery_lag=12`
- `wild_b` reaches `max_recovery_lag=10`
- `nursery_b` reaches `peak_memory_field=0.3422`
- `frontier_a` reaches `peak_memory_field=0.3227`
- the current ecology probe emits non-zero `recolonization` events with
  attached `colonization_pressure`

This is enough to say that habitats are beginning to carry history in a
mechanistically relevant way.

## What This Supports

This slice supports the narrower claim that:

- habitat history is now affecting ongoing dynamics
- past pressure and disturbance can change later hazard and regeneration
- recovery lag is now a world property rather than only a retrospective phrase
- recolonization difficulty now depends partly on habitat memory and recovery
  state

## What It Does Not Support

This slice does not yet support claims about:

- strong ecological inheritance
- long-run habitat diversification
- robust memory-driven coexistence
- irreversible regime shifts
- stable memory effects across many seeds and parameter sweeps

## Next Practical Step

The next useful extensions are:

- add longer-run probes to see whether memory stabilizes or compounds
- test whether memory changes source/sink role patterns across seeds
- test whether memory shifts coexistence and persistence over many runs
