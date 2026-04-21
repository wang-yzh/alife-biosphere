# M3 Disturbance And Recovery Slice 2026-04-21

## Purpose

This note records the first M3-oriented implementation slice.

It answers:

```text
What disturbance and recovery analysis can the project now do,
and how should someone inspect it?
```

## What Changed

This slice did not add a new ecological mechanism family.
It made current disturbance behavior interpretable.

Added in this pass:

- `src/alife_biosphere/reporting.py`
- disturbance / collapse / recolonization summary derivation
- lineage-aware habitat occupancy in `tick_summary`
- lineage-sensitive recolonization classification
- disturbance status classification:
  - `collapsed_and_recovered`
  - `collapsed_delayed_recovery`
  - `collapsed_unrecovered`
  - `occupied_after_disturbance`
  - `already_empty`
- lineage recovery mode classification:
  - `same_lineage_return`
  - `replacement_recovery`
  - `mixed_recovery`
- `outputs/ecology_probe/disturbance_recovery_summary.json`
- reporting tests in `tests/test_reporting.py`

## What To Run

```text
/Users/qlqwpy/Documents/游乐园/.venv/bin/python -m pytest
/Users/qlqwpy/Documents/游乐园/.venv/bin/python scripts/run_ecology_probe.py
```

## Current Observed Recovery Summary

At the time of writing, the ecology probe reports:

```text
disturbance_count=5
collapse_count=25
recolonization_count=21
successful_recovery_count=2
delayed_recovery_count=1
failed_recovery_count=0
```

Current disturbance status counts:

```text
collapsed_and_recovered=2
collapsed_delayed_recovery=1
already_empty=2
```

Current lineage recovery mode counts:

```text
replacement_recovery=3
```

## What This Supports

This slice supports the narrower claim that:

- the event log is now rich enough to derive simple disturbance outcomes
- local collapse and recolonization can be detected from current runs
- some disturbances are followed by local recovery within a short window
- recovery can now be classified by whether the returning occupants belong to
  the same lineage or a replacement lineage

## What It Does Not Support

This slice does not yet support claims about:

- rescue-source classification
- robust recolonization under many seeds
- stable long-run ecosystem persistence
- habitat-memory-driven recovery

## Next Practical Step

The next useful extension is:

- habitat-specific recovery lag metrics
- rescue-source and lineage-source summaries
- better distinction between transient vacancy and true local crash
