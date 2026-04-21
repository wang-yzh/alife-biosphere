# Ant Sandbox Observer Slice 2026-04-22

## Purpose

This note records the first dedicated visualization layer for the
`ant-sandbox` branch.

It answers:

```text
Can we watch the ant world directly as a colony sandbox,
instead of reusing the old ecology dashboard?
```

## Short Answer

Yes.

The branch now has:

- an offline replay observer
- a live self-refreshing observer window

both built specifically for:

- nest
- food patches
- ants
- trails
- births and deaths

## What Changed

Added in this pass:

- `src/alife_biosphere/ant_sandbox/observer.py`
- `scripts/run_ant_sandbox_observer.py`
- `scripts/run_ant_sandbox_live_observer.py`
- `tests/test_ant_sandbox_observer.py`

## Launch Commands

Offline replay:

```text
/Users/qlqwpy/Documents/游乐园/.venv/bin/python scripts/run_ant_sandbox_observer.py
```

Open:

```text
outputs/ant_sandbox_observer/observer.html
```

Live window:

```text
/Users/qlqwpy/Documents/游乐园/.venv/bin/python scripts/run_ant_sandbox_live_observer.py
```

Open:

```text
outputs/ant_sandbox_live_observer/live_observer.html
```

## Visual Direction

This observer deliberately avoids the old dashboard-first style.

The main view now prioritizes:

- colony space
- nest region
- food patches
- ant motion
- trail glow
- direct birth / death / carrying cues

Metrics remain present, but secondary.

## What It Does Not Do Yet

Not yet:

- role-color overlays
- disturbance overlays in ant space
- multi-run comparison inside the viewer
- editable parameters from the UI

## Next Practical Step

The most useful next observer upgrades are:

- render role clusters directly on ants
- show pheromone effectiveness visually over time
- add disturbance overlays for the colony branch
