# Ant Sandbox M12 Checkpoint Observer Spec v1

## Purpose

M12 makes checkpointed and forked worlds visible.

The project already has:

- replay observer from a config
- live observer from active stepping
- checkpoint, resume, and fork runtime

The missing piece is:

```text
open a saved branch and inspect it as a branch, not as a default replay
```

## Problem

The current replay observer is excellent for default showcase runs, but it does
not yet treat checkpoint branches as first-class experiment objects.

That creates a handoff risk:

- long runs can be saved
- forks can be created
- but branch state is mostly inspected through JSON

Open evolution needs direct visual inspection of branch histories.

## Scope

M12 should implement:

- final-state observer from `checkpoint_final.json`
- branch provenance panel
- optional replay continuation from checkpoint to target tick
- output under a branch-specific directory

M12 should not implement:

- full branch comparison
- timeline database
- background daemon
- complex web app state management
- new ecological mechanisms

## Proposed Script

Add:

```text
scripts/run_ant_sandbox_checkpoint_observer.py
```

Required CLI:

```bash
uv run python scripts/run_ant_sandbox_checkpoint_observer.py \
  --checkpoint outputs/ant_sandbox_infinite_experiment/root/checkpoint_final.json
```

Optional replay continuation:

```bash
uv run python scripts/run_ant_sandbox_checkpoint_observer.py \
  --checkpoint outputs/ant_sandbox_infinite_experiment/root/checkpoint_final.json \
  --target-tick 2400
```

Optional output override:

```bash
uv run python scripts/run_ant_sandbox_checkpoint_observer.py \
  --checkpoint outputs/ant_sandbox_infinite_experiment/root/checkpoint_final.json \
  --output-dir outputs/ant_sandbox_checkpoint_observer/root
```

## Output Contract

Default output:

```text
outputs/ant_sandbox_checkpoint_observer/<branch-id>/
  observer.html
  observer_data.json
  checkpoint_metadata.json
```

If branch id is missing, use:

```text
checkpoint_tick_<tick>
```

## UI Requirements

The observer must show:

- branch id
- run id
- parent branch id
- parent run id
- forked-from tick
- current tick
- target tick if replay continuation was used
- seed
- inheritance mode
- mutation rate

The main world view should remain visually similar to the current ant sandbox
observer.

The goal is continuity, not a new dashboard.

## Data Requirements

The observer payload should include:

- `source_checkpoint`
- `checkpoint_metadata`
- `loaded_tick`
- `target_tick`
- `replayed_from_checkpoint`

For final-state-only mode:

- one frame is acceptable
- frame tick equals checkpoint tick

For replay continuation mode:

- frames start at checkpoint tick or checkpoint tick + 1
- final frame equals target tick
- output metadata must make it clear that this is a continuation, not the
  original full history

## Implementation Notes

Reuse:

- `load_checkpoint`
- `step_world`
- existing observer frame serialization where practical

If current observer helpers are too private, extract a small internal helper
instead of duplicating all rendering logic.

Do not mutate the source checkpoint.

## Tests

Required tests:

- checkpoint observer payload contains provenance metadata
- final-state mode returns a frame at checkpoint tick
- continuation mode advances to target tick
- source checkpoint remains loadable after observer generation

Targeted test path:

```text
tests/test_ant_sandbox_checkpoint_observer.py
```

## Acceptance Criteria

M12 is complete when:

- a checkpoint branch can produce `observer.html`
- the observer visibly identifies the branch and parent metadata
- continuation replay works for a short target range
- tests pass
- README and docs mention the new script

## Failure Modes

Stop if:

- observer hides fork metadata
- replay output implies a full original history when it is a continuation
- branch outputs overwrite each other unexpectedly
- checkpoint loading changes the source checkpoint file

## Execution Note

This is the next implementation milestone.

Do not start branch comparison before this exists, because branch comparison
without branch visual inspection will be too easy to misread.
