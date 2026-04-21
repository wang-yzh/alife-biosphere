# Live Observer Window Slice 2026-04-21

## Purpose

This note records the first real-time window slice for the current sandbox.

It answers:

```text
Can the project now show a window that plays the current situation forward
tick by tick instead of only exporting finished summaries?
```

## Short Answer

Yes.

The project now has a live observer export that rewrites one self-refreshing
HTML file as the simulation advances.

## What Changed

Added in this pass:

- `scripts/run_live_observer.py`
- self-refreshing `outputs/live_observer/live_observer.html`
- companion `outputs/live_observer/state.json`
- reuse of `step_world(...)` for tick-by-tick execution

## How To Use It

Run:

```text
/Users/qlqwpy/Documents/游乐园/.venv/bin/python scripts/run_live_observer.py
```

Open:

```text
outputs/live_observer/live_observer.html
```

The page will refresh itself while the script advances the simulation.

## What The Window Shows

- habitat graph layout
- habitat family colors
- current occupancy by habitat
- current lineage presence by habitat
- current disturbance pulses
- current alive count, births, moves, and lineage count

## Why This Matters

This is the first slice that behaves like a real sandbox window instead of only
an offline report.

It is still minimal.
It is not yet a full interactive simulator.
But it now gives the project something you can actually watch while it runs.

## What It Does Not Do Yet

Not yet:

- user-adjustable parameters while running
- pause / rewind in the live window
- source/sink overlays in the live map
- side-by-side seed comparison
- true continuous simulation beyond one scripted run

## Next Practical Step

The most valuable next observer upgrades are:

- source/sink overlays on top of the live map
- disturbance and recovery annotations in the window
- seed presets or side-by-side run comparison
