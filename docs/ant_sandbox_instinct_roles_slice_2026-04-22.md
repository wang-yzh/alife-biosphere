# Ant Sandbox Instinct Roles Slice 2026-04-22

## Purpose

This slice strengthens role differentiation through innate bias, not through
culture or explicit caste scripting.

The question for this pass was:

```text
Can ants separate into clearer task tendencies while still behaving like one
colony?
```

## What Changed

Each ant now carries a small instinct profile:

- `range_bias`
- `trail_affinity`
- `harvest_drive`

These are continuous tendencies, not hard role labels.

They affect:

- how far an ant prefers to range from the nest
- how strongly it responds to trail fields
- how aggressively it locks onto nearby food

Births also keep weak variation, so long runs do not collapse into one totally
uniform ant type.

## Reporting Change

Role clustering still uses behavior summaries as the primary evidence.

This pass tightened the interpretation so that:

- far-travel, low-return clusters can be labeled `scout_like`
- near-nest, low-harvest clusters can be labeled `nest_like`
- strong pickup / unload clusters remain `forager_like`

## Result

The validation matrix now reports:

- `M1 spatial realism = pass`
- `M2 foraging loop = pass`
- `M3 pheromone effectiveness = pass`
- `M4 colony persistence = pass`
- `M5 role differentiation = pass`
- `M6 disturbance recovery = pass`

## Observer Note

Selected ants in the observer now also show their current instinct profile, so
the viewer can inspect how visible behavior relates to built-in tendency.
