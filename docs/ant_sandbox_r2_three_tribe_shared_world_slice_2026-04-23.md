# Ant Sandbox R2 Three Tribe Shared World Slice 2026-04-23

## Purpose

This slice begins the first real multi-origin competition step for the
ant-sandbox branch.

The project is no longer only asking:

```text
Which food source does one colony prefer?
```

It is now asking:

```text
What happens when three different ant origins share one world?
```

## What Changed

The branch now supports a shared surface world with three tribes:

- `wei`
- `shu`
- `wu`

Each tribe has:

- its own nest
- its own stored food ledger
- its own ant population
- its own home and food trails
- its own colony color in the observer

## What Is Shared

All three tribes currently share:

- the same terrain map
- the same food sources
- the same outdoor surface

This means the current slice is already a real shared-world competition layer,
even before direct combat mechanics exist.

## What Is Not Added Yet

Not yet in this slice:

- combat
- damage exchange between tribes
- blocking or pushing rules
- explicit territorial ownership

This is intentional.
The branch first needs shared-world coexistence and competition visibility.

## Observer Result

The observer now renders:

- three separate nests
- tribe-colored ants
- tribe-specific trail layers

So the user can watch “different sources of ants” in the same world rather
than only one colony mirrored across a map.

## Current Probe Signal

Current shared-world probe now shows:

- all three tribes active on one map
- shared food-source contention
- per-tribe unload activity

This is the correct foundation for later:

- food conflict
- route conflict
- territorial pressure
- war-like mechanics
