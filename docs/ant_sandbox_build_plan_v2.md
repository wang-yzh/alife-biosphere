# Ant Sandbox Build Plan v2

## Purpose

This plan begins after the current branch has already passed:

- `M1` spatial realism
- `M2` foraging loop
- `M3` pheromone effectiveness
- `M4` colony persistence
- `M5` role differentiation
- `M6` disturbance recovery

The next phase is not about adding abstract systems.
It is about scaling the sandbox world itself.

## M7. Surface Scale-Up

Scope:

- increase default showcase map size
- keep deterministic stepping
- keep observer replay practical
- preserve readable ant motion on a bigger map

Required result:

- the sandbox still feels alive on a clearly larger map

## M8. Terrain Layer

Scope:

- add terrain map generation or fixed terrain layouts
- introduce movement constraints and route pressure
- keep terrain semantics small and legible

Required result:

- ants visibly route around barriers and through terrain-weighted paths

## M9. Food Source Lifecycle

Scope:

- persistent food-source identity
- source existence tied to remaining total amount
- true depletion state
- optional delayed turnover only after depletion

Required result:

- the observer shows food sources as meaningful places, not just local pickup spots

## M10. Observer Upgrade

Scope:

- larger-map presentation
- terrain rendering
- stronger ant visual identity
- clearer food-source bodies and depletion cues
- nest entrance emphasis

Required result:

- the viewer looks like a richer sandbox world, not just a scaled debug board

## M11. Map-Scale Colony Pressure

Scope:

- confirm that larger space still supports useful logistics
- confirm that more ants participate in long-route activity
- measure whether scouting and transport remain legible

Required result:

- larger maps produce richer colony traffic instead of route collapse or idle drift

## M12. Later Outdoor Extensions

Only after the above:

- weather-like disturbances
- multi-source seasonal pressure
- multiple nests or colonies
- stronger adaptive variation

For the longer route beyond this phase, see:

- `ant_sandbox_long_horizon_construction_route_v1.md`

## Rule

If bigger maps and terrain make the sandbox less readable or less alive,
stop and repair the world before adding new thematic systems.
