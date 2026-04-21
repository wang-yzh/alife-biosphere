# Ant Sandbox Status v1

## Purpose

This document is the branch-level status page for the current ant-sandbox
branch.

It does not replace the detailed slice notes.
It compresses them into one answer:

```text
Which sandbox milestones are now actually passing,
and which are still provisional?
```

## Current Validation Basis

The current status is based on:

- `M1` foraging probe
- `M2` pheromone comparison
- `M3` persistence probe
- `M4` role clustering summary
- `M5` disturbance recovery probe

and a multi-seed validation matrix over:

```text
7, 11, 13
```

## Current Status

| Metric | Status | Reason |
| --- | --- | --- |
| `M1 spatial realism` | `pass` | the branch now runs on a local grid with local movement and local sensing rather than a habitat graph |
| `M2 foraging loop` | `pass` | the branch now repeatedly produces `food_pickup` and `food_unload` with net nest food return |
| `M3 pheromone effectiveness` | `pass` | in the current default sandbox, pheromone-on outperforms pheromone-off on food return across the current validation seeds |
| `M4 colony persistence` | `pass` | the branch now shows births, deaths, and bounded alive counts in longer runs without total collapse under the current persistence configuration |
| `M5 role differentiation` | `pass` | the branch now produces multiple role-like behavior clusters from trace summaries |
| `M6 disturbance recovery` | `pass` | the branch now recovers a substantial fraction of prior function after local-space disturbance in the current probe setup |

## Important Caution

These are current branch-level passes, not final claims of robustness.

The current status should be read as:

```text
the sandbox now passes these gates in its present default and probe settings,
not yet under broad adversarial validation
```

## What Is Still Provisional

Still provisional:

- wider multi-seed robustness
- wider food layout robustness
- stronger role interpretation
- disturbance recovery under harder settings
- observer integration of role and disturbance overlays

## Current Working Interpretation

The branch is no longer just a substrate experiment.
It is now a real early ant sandbox with:

- local space
- foraging loops
- trace-mediated improvement
- bounded persistence
- behavior clustering
- local-space recovery

That is enough to treat it as the real project world, not just a sketch.
