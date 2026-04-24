# Ant Sandbox M13 Branch Comparison Slice 2026-04-24

## Purpose

This slice makes checkpoint branches comparable.

Before this slice, the project could:

- save a branch
- fork a branch
- open a branch in the observer

But it still lacked a structured answer to this question:

```text
what changed across alternate futures from the same parent checkpoint?
```

After this slice, branch families can be compared through machine-readable and
human-readable reports.

## What Changed

The branch now includes:

- `src/alife_biosphere/ant_sandbox/comparison.py`
- `scripts/run_ant_sandbox_branch_comparison.py`
- tests for provenance, grouping, JSON/Markdown output, and pairwise deltas

The comparison layer now reports:

- branch provenance
- family grouping by shared checkpoint ancestry
- branch outcome metrics
- first spatial signatures
- pairwise divergence deltas

## Output Contract

Default output:

```text
outputs/ant_sandbox_branch_comparison/<comparison-id>/
  comparison.json
  comparison.md
```

The JSON file is the machine-readable contract.

The Markdown file is the handoff/reporting layer for humans.

## Example Command

```bash
uv run python scripts/run_ant_sandbox_branch_comparison.py \
  --checkpoints \
  outputs/ant_sandbox_infinite_experiment/root/checkpoint_final.json \
  outputs/ant_sandbox_infinite_experiment/root_seed_11/checkpoint_final.json \
  outputs/ant_sandbox_infinite_experiment/root_seed_99/checkpoint_final.json
```

Directory scan mode is also supported:

```bash
uv run python scripts/run_ant_sandbox_branch_comparison.py \
  --input-dir outputs/ant_sandbox_infinite_experiment
```

## First Metrics

Per branch:

- alive count by colony
- births, deaths, pickups, unloads by colony
- nest food by colony
- total food remaining
- depleted and contested source counts
- combat start count
- max generation
- genome count
- mutated birth count
- unique lineage count
- total event count
- occupied cell count
- food trail and home trail cell counts
- top food source by pickup count

Per branch pair:

- alive delta
- unload delta
- nest food delta
- generation delta
- trail cell delta
- lineage count delta

## Verification

Targeted comparison tests:

```text
uv run pytest tests/test_ant_sandbox_branch_comparison.py tests/test_ant_sandbox_checkpoint.py tests/test_ant_sandbox_checkpoint_observer.py
12 passed in 10.43s
```

Full suite after M13:

```text
uv run pytest
63 passed
```

Smoke chain:

- generated root branch at `tick 30`
- generated two forks from that checkpoint
- rendered `comparison.json`
- rendered `comparison.md`

Smoke output:

```text
outputs/ant_sandbox_branch_comparison_smoke/
```

## Why This Slice Matters

This slice changes checkpointing from:

```text
storage
```

into:

```text
method
```

The branch can now ask not only "what happened in this run?" but also:

```text
which future branches diverged,
and how did they diverge?
```

## Important Caution

This slice does not prove open-ended evolution.

It only establishes the comparison layer needed before stronger ecological
claims.

The report deliberately avoids ranking branches as winners and losers.

## Next Step

The next implementation milestone is:

```text
M14 niche substrate
```

The correct next move is not more mutation or more combat.

It is:

```text
make ant activity leave behind persistent environmental material
that future organisms could exploit.
```
