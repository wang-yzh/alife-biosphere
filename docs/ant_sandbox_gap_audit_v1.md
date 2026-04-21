# Ant Sandbox Gap Audit v1

## Purpose

This document audits the current `working copy` against the ant-sandbox hard
metrics.

It is not judging whether the current code is useless.
It is judging whether the current code is building the right type of world.

## Executive Verdict

The current implementation is:

- a reasonable early ecology-graph world
- but not an ant sandbox

That means the project is not just "a bit incomplete."
It is incomplete in the wrong direction for the sandbox target.

## Current World Type

Right now the executable world is best described as:

- a small graph of seven habitats
- occupied by mostly homogeneous organisms
- driven by resource, hazard, crowding, disturbance, and recolonization rules
- summarized through ecology and recovery analysis

That world can support graph ecology questions.
It does not yet support the ant-sandbox questions directly.

## Metric Audit

| Metric | Current status | Why it fails or only partially passes |
| --- | --- | --- |
| `M1 spatial realism` | `fail` | the world is still a fixed habitat graph, not a real local space; movement is graph neighbor selection, not local ant motion |
| `M2 foraging loop` | `fail` | there is harvesting, but not a visible nest-food-return loop with task closure |
| `M3 pheromone effectiveness` | `fail` | there is no pheromone field or trace-based coordination mechanism |
| `M4 colony persistence` | `partial` | the world can stay alive for a while and avoid trivial extinction under some settings, but it is not yet a colony-organized long-run system |
| `M5 role differentiation` | `fail` | there are no stable emergent internal colony roles; current lineages are not the same thing as worker-role clustering |
| `M6 disturbance recovery` | `partial` | the system does show collapse and recolonization summaries, but these are graph-ecology recovery signals, not yet colony functional recovery signals |
| `S1 lineage traceability` | `pass` | parent-child lineage identity and birth tracking now exist |
| `S2 adaptive comparability` | `partial` | some comparative probes are possible, but not yet on the ant-sandbox metrics that matter most |

## Main Gaps By Metric

## `M1` Spatial Realism

Missing:

- local 2D world or fine local grid
- position-based perception
- local collision / contact rules
- movement based on nearby stimuli rather than habitat score

Current blocking files:

- `src/alife_biosphere/config.py`
- `src/alife_biosphere/world.py`
- `src/alife_biosphere/simulation.py`

## `M2` Foraging Loop

Missing:

- nest as a real place
- food entities or patches in local space
- carrying state
- unload-at-nest logic
- food-return metrics

Current blocking files:

- `src/alife_biosphere/organism.py`
- `src/alife_biosphere/simulation.py`

## `M3` Pheromone Effectiveness

Missing:

- local trace field
- deposition rules
- decay rules
- trace sensing
- pheromone-on versus pheromone-off comparison

Current blocking files:

- not yet present in the codebase as a first-class substrate

## `M4` Colony Persistence

Partially present:

- births and deaths exist
- resource pressure exists
- bounded persistence exists in some settings

Still missing for a colony sandbox:

- colony-level food accounting
- colony-level survival signal
- stable bounded colony population over longer runs

## `M5` Role Differentiation

Missing:

- per-agent behavior features suitable for clustering
- long-run trace summaries by individual
- role discovery from traces

Current blockers:

- observer and reporting still summarize mostly at habitat level, not role level

## `M6` Disturbance Recovery

Partially present:

- disturbance exists
- collapse and recolonization exist
- habitat-memory effects now exist

Still missing for the ant-sandbox target:

- colony task recovery after path breakage
- food-return recovery after disturbance
- nest-function recovery metrics

## Immediate Conclusion

The current world can be kept as:

- a reference ecology-graph line
- a source of reusable infrastructure

But it should not be mistaken for the main ant-sandbox world.

## Reusable Pieces

Keep and reuse:

- deterministic config and RNG
- event logging
- test discipline
- reporting discipline
- observer export machinery

Do not keep as the main world abstraction:

- seven-habitat graph as the world itself
- graph-scored movement as the primary behavior layer
- habitat-level aggregation as the first visual truth of the sandbox

## Recommended Next Move

If the real target is the ant sandbox, the next main-line build should be a new
substrate with:

1. local 2D or local grid space
2. nest
3. food patches
4. visible ants as local agents
5. carrying and return behavior
6. simple pheromone field

Only after that should the current ecology-graph line be mined for ideas about:

- disturbance
- recovery
- environmental memory
- long-run diagnostics
