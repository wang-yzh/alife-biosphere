# Ant Sandbox M7 M8 Scale-Up Slice 2026-04-22

## Purpose

This slice records the first implementation pass for the scale-up phase.

It answers:

```text
Did the sandbox actually become larger and more terrain-aware,
or did we only update planning documents?
```

## Short Answer

Yes.

The branch now has a real first scale-up slice:

- larger default showcase map
- terrain layer in the simulation substrate
- terrain-aware movement constraints
- richer observer rendering for terrain and ant bodies

## What Changed

This pass added:

- default showcase map uplift from `64 x 48` to `128 x 96`
- terrain categories:
  - `open_ground`
  - `dense_grass`
  - `sand`
  - `rock`
- terrain-aware path blocking and terrain-weighted movement preference
- terrain-aware trail deposition
- observer rendering for terrain
- ant glyph rendering with heading-aware body shapes

## Food Sources

Food-source identity remains patch-based.

For this slice:

- a source is active while `remaining_amount > 0`
- the observer now only renders active food bodies
- depletion / reseed logic still exists, but the default large-map showcase is
  currently tuned to emphasize transport over rapid turnover

## Default Showcase Outcome

The current default scale-up showcase was checked at `240` ticks.

- `tick 239 alive = 32`
- `tick 240 alive = 32`
- `food_pickups = 40`
- `food_unloads = 36`

So the larger world is not just visually larger.
It still supports a real food loop.

## Validation Note

After this pass:

- full `pytest` returned `37 passed`
- the validation matrix still reports:
  - `M1 pass`
  - `M2 pass`
  - `M3 pass`
  - `M4 pass`
  - `M5 pass`
  - `M6 pass`

## What Still Needs Work

Still not finished in the scale-up phase:

- stronger larger-map route richness
- more frequent default food-source depletion events
- richer terrain visual language
- explicit nest entrance styling beyond the current simple surface marker
