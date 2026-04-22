# Ant Sandbox Instinct Pressure Slice 2026-04-22

## Purpose

This slice strengthens instinctive colony pressure without adding social or
cultural systems.

The goal is simple:

- ants should have more reason to keep the food loop alive
- empty food sites should stop being permanent fixtures
- observer playback should show these pressures directly

## Changes

This pass added two world-level pressures.

1. Nest upkeep:
- the nest now consumes a small amount of stored food over time
- this creates colony-level demand even when many ants are temporarily idle

2. Dynamic food turnover:
- default food patches are smaller
- when a patch is depleted, it waits, then respawns at a new location
- this keeps scouting relevant and prevents the world from collapsing into one
  permanent route forever

This pass also exposed the new signals to the observer and probes:

- `nest_upkeep`
- `food_patch_reseed`

## Default World Outcome

The default observer world was rechecked after this pass.

- `tick 239 alive = 32`
- `tick 240 alive = 32`
- `tick 239 carrying = 11`
- `tick 240 carrying = 13`
- `food_patch_reseed = 1`

So the default showcase still stays alive through the late playback window, but
it now shows stronger task pressure and at least one food-site turnover event.

## Notes

- Long-run persistence validation still uses a more generous food setup than
  the default observer world.
- That is intentional: the observer world is tuned to feel alive and changing,
  while the persistence checks are tuned to test bounded continuity over longer
  horizons.
