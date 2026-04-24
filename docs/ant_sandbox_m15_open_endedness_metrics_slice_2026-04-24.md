# Ant Sandbox M15 Open-Endedness Metrics Slice 2026-04-24

## Purpose

This slice turns branch comparison into an explicit open-endedness metrics
layer.

Before this slice, the branch could:

- compare alternate futures
- inspect branch provenance
- measure branch deltas

But it still lacked a dedicated answer to this question:

```text
which branch differences look like early stepping stones,
and which are only raw divergence?
```

After this slice, the project emits a separate metrics layer organized around
five metric families.

## What Changed

The branch now includes:

- `src/alife_biosphere/ant_sandbox/open_endedness.py`
- `scripts/run_ant_sandbox_open_endedness_metrics.py`
- tests for loading comparison payloads, metric status labels, dependency
  gating, and no-single-score output

The metrics layer now groups signals into:

- branch divergence
- niche occupancy
- stepping-stone persistence
- ecological dependency
- novelty without collapse

## Important Constraint

This slice does not produce one universal score.

That is intentional.

The output is designed to resist a regression back into:

```text
one-number fitness ranking
```

## Status Labels

Each metric now carries one of these labels:

- `available`
- `proxy`
- `requires_m14`
- `requires_m16`
- `not_implemented`

This lets the project distinguish:

- what is directly measured now
- what is inferred only as a proxy
- what cannot exist until successor life is implemented

## New Output Contract

Default output:

```text
outputs/ant_sandbox_open_endedness/<comparison-id>/
  metrics.json
  metrics.md
```

Example:

```bash
uv run python scripts/run_ant_sandbox_open_endedness_metrics.py \
  --comparison outputs/ant_sandbox_branch_comparison_smoke/comparison.json
```

The script can also build from checkpoints by reusing the comparison layer
first.

## Current Signal

The first implementation currently provides:

- available branch signature distances
- proxy resource patch occupancy
- proxy trail and residue persistence
- explicit `requires_m16` dependency metrics
- available non-collapse and observability checks

Current interpretation:

```text
the project can now say which branch differences look structurally distinct,
which substrate signals persist,
and which dependency claims must wait for M16
```

That is the right scope for this stage.

## Verification

Targeted metrics verification:

```text
uv run pytest tests/test_ant_sandbox_open_endedness_metrics.py tests/test_ant_sandbox_branch_comparison.py
10 passed in 11.24s
```

Smoke output:

```text
outputs/ant_sandbox_open_endedness_smoke/
```

Generated files:

- `metrics.json`
- `metrics.md`

## Why This Slice Matters

M15 is the first place where the project explicitly separates:

- divergence
- occupancy
- persistence
- dependency
- collapse

Without that separation, later open-evolution claims would be too easy to
overstate.

## Current Limits

This slice still marks dependency metrics as `requires_m16`.

That is correct.

The project now has:

- ant-created substrate
- branch comparison
- open-endedness framing

But it still does not have:

- a second organism layer that consumes or depends on that substrate

## Next Step

The next implementation milestone is:

```text
M16 successor life layer
```

The correct next move is not more metrics detail.

It is:

```text
introduce one simple non-ant life layer
that depends on corpse or residue substrate.
```
