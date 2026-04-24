# Ant Sandbox M10B Genome v1 Slice 2026-04-24

## Purpose

This slice formalizes the first explicit inheritance contract for the active
ant-sandbox branch.

The branch already had inheritable instinct traits.
What it did not yet have was a clean answer to this question:

```text
What exactly is being inherited?
```

This slice answers that with a small, readable `Genome v1`.

## What Changed

The inherited instinct payload is now wrapped in an explicit genome structure.

Current `Genome v1` fields:

- `genome_id`
- `parent_genome_id`
- `generation`
- `range_bias`
- `trail_affinity`
- `harvest_drive`
- `mutation_count`
- `mutation_log`

Every ant now carries a genome object rather than only loose trait fields.

## What Stays The Same

This slice does not turn mutation on.

Birth still uses single-parent clonal inheritance.
The child still copies the parent instinct values exactly.

That means this slice is:

```text
genome contract first
mutation later
```

## Why This Matters

Without an explicit genome object, the branch could not cleanly distinguish:

- inherited structure
- per-ant runtime state
- lineage labels
- future mutation bookkeeping

With this slice in place, later work can add mutation without first rewriting
the whole agent model.

## Observer And Probe Impact

The observer now exposes:

- `genome_id`
- `parent_genome_id`
- `generation`
- `mutation_count`

The probe summary now also reports:

- `max_generation`
- `alive_generation_distribution`
- `mean_traits_by_colony`

## Current Signal

Latest showcase probe after `Genome v1`:

- `max_generation=2`
- `alive_generation_distribution={'1': 27, '2': 6}`

Current colony mean traits:

- `wei`: `range=0.6459`, `trail=0.6258`, `harvest=0.4531`
- `shu`: `range=0.8097`, `trail=0.2486`, `harvest=0.5588`
- `wu`: `range=0.4700`, `trail=0.3064`, `harvest=0.3393`

## Verification

Verification for this slice:

- targeted tests: `26 passed in 34.37s`
- full suite: `49 passed in 35.98s`

## Next Step

The next correct step is not recombination or heavy genome mechanics.

It is:

```text
bounded point mutation
+ ablation controls
+ generation-level comparison metrics
```
