# Ant Sandbox M12 Checkpoint Observer Slice 2026-04-24

## Purpose

This slice turns the new checkpoint runtime into a directly watchable branch
workflow.

Before this slice, the project could:

- save a branch
- resume a branch
- fork a branch

But saved branches were still mostly JSON artifacts.

After this slice, a saved branch can be opened as a first-class observer world.

## What Changed

The branch now includes:

- `build_ant_checkpoint_observer_payload(...)`
- `scripts/run_ant_sandbox_checkpoint_observer.py`
- branch provenance rendering in the ant sandbox observer UI

The new observer can:

- load `checkpoint_final.json`
- render a final-state snapshot at the checkpoint tick
- optionally continue replay from the checkpoint to a later target tick
- show provenance such as branch id, parent branch id, fork tick, seed,
  inheritance mode, and mutation rate

## New Output Path

Default output:

```text
outputs/ant_sandbox_checkpoint_observer/<branch-id>/
  observer.html
  observer_data.json
  checkpoint_metadata.json
```

## Example Command

Snapshot view:

```bash
uv run python scripts/run_ant_sandbox_checkpoint_observer.py \
  --checkpoint outputs/ant_sandbox_infinite_experiment/root/checkpoint_final.json
```

Continuation replay:

```bash
uv run python scripts/run_ant_sandbox_checkpoint_observer.py \
  --checkpoint outputs/ant_sandbox_infinite_experiment/root/checkpoint_final.json \
  --target-tick 2400
```

## Verification

Targeted observer and checkpoint tests:

```text
uv run pytest tests/test_ant_sandbox_checkpoint_observer.py tests/test_ant_sandbox_observer.py tests/test_ant_sandbox_checkpoint.py
11 passed in 12.84s
```

Full suite:

```text
uv run pytest
58 passed in 40.39s
```

Smoke run:

- generated checkpoint branch at `tick 40`
- rendered continuation observer to `tick 50`
- wrote `outputs/ant_sandbox_checkpoint_observer_smoke/observer.html`

## Why This Slice Matters

Open evolution in this branch is branch-relative.

That means:

```text
if forked futures cannot be watched,
they cannot be interpreted safely
```

This slice makes branch history visible before the project starts branch
comparison or successor ecology work.

## Next Step

The next implementation milestone is:

```text
M13 branch comparison ledger
```

The correct next question is not:

```text
how do we add more organisms right now?
```

It is:

```text
how do we compare alternate futures from the same checkpoint family?
```
