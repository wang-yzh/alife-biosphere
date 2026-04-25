# Ant Sandbox M18 Economic Stabilization Slice 2026-04-25

## Purpose

This slice is the first implementation step under
`ant_sandbox_open_evolution_engineering_plan_v2.md`.

Its goal is not to remove ecological pressure.

Its goal is:

```text
reduce late-stage colony collapse pressure enough that upper ecological layers
are not built on a brittle baseline
```

## What Changed

The default showcase economy was tuned conservatively:

- `initial_stored_food`: `10 -> 12`
- `colony_upkeep_per_ant_tick`: `0.0035 -> 0.0032`
- `metabolism_cost`: `0.05 -> 0.047`
- `hunger_return_threshold`: `6.5 -> 7.2`
- `nest_feed_amount`: `4.0 -> 4.4`

No changes were made to:

- mutation logic
- successor ecology logic
- campaign structure
- branch comparison structure

This is a substrate-stability pass, not a mechanism-expansion pass.

## Current Signal

Current showcase probe after the stabilization pass:

```text
alive=36
births=50
deaths=46
death_reasons={'old_age': 20, 'starvation': 26}
food_remaining=98
decomposer_patch_count=4
enriched_residue_cell_count=18
```

Most important change:

```text
starvation deaths dropped from 42 to 26
```

This does not mean the world is now safe.

It means the economy is less brittle while still clearly resource-limited.

## Window Signal

The probe now emits `window_summaries`, which makes late-horizon behavior
explicit.

Current `300`-tick windows:

- `1-300`: `births=11`, `deaths=0`
- `301-600`: `births=4`, `deaths=0`
- `601-900`: `births=6`, `deaths=5`
- `901-1200`: `births=10`, `deaths=9`
- `1201-1500`: `births=12`, `deaths=7`
- `1501-1800`: `births=7`, `deaths=25`

Interpretation:

```text
the late horizon is still pressured,
but the system now reaches that horizon with more living structure intact
and with much lower starvation-driven failure
```

That is a stabilization result, not a solved economy.

## Why This Slice Matters

Without this pass, later ecological layers would have been judged on top of a
colony economy that was too close to starvation churn.

This pass gives:

- more breathing room for successor ecology
- stronger late-horizon continuity
- lower risk that every upper-layer signal is really just colony collapse noise

## Current Limits

This slice does not claim:

- perfect demographic balance
- no late decline
- no starvation
- a finished stable ecosystem

The final `300` ticks still show real pressure.

That is acceptable for now.

The goal was not comfort.

The goal was:

```text
pressure with continuity
```

## Verification

Current probe outputs:

- `outputs/ant_sandbox_probe/summary.json`
- `outputs/ant_sandbox_probe/derived_summary.json`

Full test suite after M18 tuning:

```text
uv run pytest
80 passed
```

## Next Step

The next milestone is:

```text
M19 fungus layer
```

The correct next move is now to extend the dependency chain from:

```text
corpse -> decomposer -> enriched residue
```

to:

```text
corpse -> decomposer -> enriched residue -> fungus
```
