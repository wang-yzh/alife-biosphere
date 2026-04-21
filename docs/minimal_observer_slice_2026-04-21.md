# Minimal Observer Slice 2026-04-21

## Purpose

This note records the first visual observer slice for the current small-world
ecosystem.

It answers:

```text
How can we start watching the sandbox directly instead of only reading JSON
summaries?
```

## What Changed

This slice adds a self-contained HTML observer export.

The observer was later upgraded away from a dashboard-first style toward a
world-first style:

- habitat regions instead of abstract node circles
- visible organism dots inside habitats
- births, deaths, moves, and disturbance as direct visual events
- statistics moved to a secondary panel

Added in this pass:

- `src/alife_biosphere/observer.py`
- `scripts/run_observer_export.py`
- `outputs/observer/observer.html`
- `outputs/observer/observer_data.json`
- observer tests in `tests/test_observer.py`

## What The Observer Shows

The observer currently visualizes:

- habitat graph topology
- habitat family coloring
- occupancy by habitat over time
- lineage presence by habitat over time
- disturbance pulses
- visible organism dots
- births, moves, deaths, and alive counts per tick

## What To Run

```text
/Users/qlqwpy/Documents/游乐园/.venv/bin/python -m pytest
/Users/qlqwpy/Documents/游乐园/.venv/bin/python scripts/run_observer_export.py
```

Then open:

```text
outputs/observer/observer.html
```

## Why This Matters

This is the first slice that turns the current ecosystem into something that
can be watched directly.

It is still minimal.
It is not yet a rich interactive sandbox.
But it is now possible to see:

- habitats fill and empty
- disturbances hit the map
- lineage labels shift across places
- births and movement appear in time rather than only in ledgers

## What It Does Not Do Yet

Not yet:

- live simulation
- editing parameters in the browser
- multi-run comparison
- source/sink overlays inside the map
- long-run playback across many seeds

## Next Practical Step

The most useful next observer upgrades are:

- source/sink overlays on the map
- disturbance and recovery annotations in the timeline
- side-by-side seed comparison
