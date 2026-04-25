# Ant Sandbox M17 Multi-Niche Open Evolution Slice 2026-04-25

## Purpose

This slice turns the current ant-and-decomposer world into a reusable campaign
workflow.

Before this slice, the branch had:

- long-running worlds
- checkpoints
- branch comparison
- open-endedness metrics
- a first successor life layer

But these pieces still had to be orchestrated manually.

After this slice, the branch can run a forked multi-niche campaign end to end.

## What Changed

The branch now includes:

- `src/alife_biosphere/ant_sandbox/campaign.py`
- `scripts/run_ant_sandbox_multi_niche_open_evolution.py`
- tests for campaign artifact generation and manifest structure

The campaign workflow now automates:

```text
root branch
-> fork branches
-> branch observers
-> branch comparison
-> open-endedness metrics
-> campaign manifest
```

## New Output Contract

Default campaign layout:

```text
outputs/ant_sandbox_multi_niche_open_evolution/<campaign-id>/
  branches/
  observers/
  comparison/
  open_endedness/
  campaign_manifest.json
  campaign_summary.md
```

Each branch gets:

- `checkpoint_final.json`
- `status.json`
- `config.json`
- `world.json`
- `events.json`
- observer HTML and data

## Example Command

```bash
uv run python scripts/run_ant_sandbox_multi_niche_open_evolution.py \
  --campaign-id m17_smoke \
  --root-tick 40 \
  --fork-additional-ticks 20 \
  --fork-seeds 11 29
```

## Smoke Result

Current smoke campaign output:

```text
outputs/ant_sandbox_multi_niche_open_evolution_smoke/
```

The smoke run now emits:

- one root branch
- two fork branches
- campaign comparison output
- campaign open-endedness output

That means the branch now has a real campaign-level execution path rather than
only isolated scripts.

## Verification

Targeted campaign verification:

```text
uv run pytest tests/test_ant_sandbox_open_evolution_campaign.py tests/test_ant_sandbox_successor_life.py tests/test_ant_sandbox_open_endedness_metrics.py tests/test_ant_sandbox_branch_comparison.py
17 passed in 16.00s
```

Full suite after M17:

```text
uv run pytest
80 passed
```

## Why This Slice Matters

This is the first point where the project can run:

```text
ants + decomposers + branch families + metrics
```

as one integrated experimental workflow.

That is the minimum needed before asking whether multi-niche histories diverge
in a way that looks like early open evolution.

## Current Limits

This slice does not yet mean the ecosystem is rich.

It means the experimentation method is now ready for richer ecology.

Still limited:

- only one successor layer
- no fungus or plant layer yet
- no decomposer mutation
- no multi-step dependency chain beyond corpse -> decomposer -> enriched residue

## Next Step

The next move is not more orchestration.

It is:

```text
broaden successor ecology beyond one decomposer layer
while preserving branch observability and metric discipline
```
